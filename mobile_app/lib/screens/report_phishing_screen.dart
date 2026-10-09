import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ReportPhishingScreen extends StatefulWidget {
  const ReportPhishingScreen({super.key});

  @override
  State<ReportPhishingScreen> createState() => _ReportPhishingScreenState();
}

class _ReportPhishingScreenState extends State<ReportPhishingScreen>
    with TickerProviderStateMixin {
  final TextEditingController _urlController = TextEditingController();
  String _selectedLabel = '';
  bool _isSubmitting = false;
  bool _isLoadingQuestions = true;
  bool _submitted = false;
  List<CommunityQuestion> _questions = [];
  final Map<String, String> _answers = {};
  Map<String, dynamic>? _autoScanResult;
  late AnimationController _successController;

  @override
  void initState() {
    super.initState();
    _successController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    _loadQuestions();
  }

  @override
  void dispose() {
    _urlController.dispose();
    _successController.dispose();
    super.dispose();
  }

  Future<void> _loadQuestions() async {
    try {
      final questions = await ApiService.getCommunityQuestions();
      setState(() {
        _questions = questions;
        _isLoadingQuestions = false;
      });
    } catch (e) {
      setState(() {
        _isLoadingQuestions = false;
      });
    }
  }

  Future<void> _submitReport() async {
    if (_urlController.text.trim().isEmpty || _selectedLabel.isEmpty) return;

    setState(() => _isSubmitting = true);

    try {
      // Filter out skipped answers
      final cleanAnswers = Map<String, String>.from(_answers);
      cleanAnswers.removeWhere((key, value) => value == 'skipped');

      final result = await ApiService.submitCommunityReport(
        url: _urlController.text.trim(),
        userReportedLabel: _selectedLabel,
        questionsAnswers: cleanAnswers,
        source: 'app',
      );

      if (result['success'] == true) {
        _autoScanResult = result['auto_scan'];
        _successController.forward();
        setState(() {
          _submitted = true;
          _isSubmitting = false;
        });
      }
    } catch (e) {
      setState(() => _isSubmitting = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text("Failed to submit: $e"),
            backgroundColor: Colors.redAccent,
          ),
        );
      }
    }
  }

  void _resetForm() {
    setState(() {
      _urlController.clear();
      _selectedLabel = '';
      _answers.clear();
      _submitted = false;
      _autoScanResult = null;
      _successController.reset();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F0C29),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Row(
          children: [
            Icon(Icons.report_problem_outlined, color: Colors.deepOrangeAccent),
            SizedBox(width: 8),
            Text(
              "Report Phishing",
              style: TextStyle(
                color: Colors.deepOrangeAccent,
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
          ],
        ),
      ),
      body: _submitted ? _buildSuccessView() : _buildReportForm(),
    );
  }

  Widget _buildSuccessView() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: AnimatedBuilder(
          animation: _successController,
          builder: (context, child) {
            return Transform.scale(
              scale: 0.8 + (_successController.value * 0.2),
              child: Opacity(
                opacity: _successController.value.clamp(0.0, 1.0),
                child: child,
              ),
            );
          },
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.green.withAlpha(30),
                  border: Border.all(color: Colors.greenAccent.withAlpha(80)),
                ),
                child: const Icon(
                  Icons.check_circle_outline,
                  color: Colors.greenAccent,
                  size: 64,
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                "Report Submitted!",
                style: TextStyle(
                  color: Colors.greenAccent,
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),
              const Text(
                "Thank you for helping train our AI model.\nYour report will be reviewed and used to improve phishing detection.",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white54, fontSize: 13),
              ),
              if (_autoScanResult != null) ...[
                const SizedBox(height: 20),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white.withAlpha(8),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.cyan.withAlpha(50)),
                  ),
                  child: Column(
                    children: [
                      const Text(
                        "🤖 AI Auto-Scan Result",
                        style: TextStyle(
                          color: Colors.cyanAccent,
                          fontWeight: FontWeight.bold,
                          fontSize: 13,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        _autoScanResult!['auto_scan_phishing'] == true
                            ? "⚠️ AI also flagged this as PHISHING"
                            : "✅ AI classified this as SAFE",
                        style: TextStyle(
                          color: _autoScanResult!['auto_scan_phishing'] == true
                              ? Colors.redAccent
                              : Colors.greenAccent,
                          fontWeight: FontWeight.w600,
                          fontSize: 14,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        "Confidence: ${_autoScanResult!['auto_scan_confidence']}%",
                        style: const TextStyle(color: Colors.white54, fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: _resetForm,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepOrangeAccent,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  icon: const Icon(Icons.add_circle_outline),
                  label: const Text(
                    "Report Another Link",
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildReportForm() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Info card
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: [
                  Colors.deepOrangeAccent.withAlpha(20),
                  Colors.red.withAlpha(10),
                ],
              ),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: Colors.deepOrangeAccent.withAlpha(60)),
            ),
            child: const Row(
              children: [
                Icon(Icons.info_outline, color: Colors.deepOrangeAccent, size: 20),
                SizedBox(width: 10),
                Expanded(
                  child: Text(
                    "Paste a suspicious link below. Our AI will auto-scan it and your answers will help train our model.",
                    style: TextStyle(color: Colors.white60, fontSize: 12),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),

          // URL Input
          const Text(
            "Suspicious URL:",
            style: TextStyle(
              color: Colors.white70,
              fontSize: 13,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          TextField(
            controller: _urlController,
            style: const TextStyle(
              color: Colors.cyanAccent,
              fontFamily: 'monospace',
              fontSize: 13,
            ),
            decoration: InputDecoration(
              hintText: "https://suspicious-link.com...",
              hintStyle: TextStyle(color: Colors.white.withAlpha(50)),
              filled: true,
              fillColor: Colors.black26,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide.none,
              ),
              prefixIcon: const Icon(Icons.link, color: Colors.deepOrangeAccent),
            ),
          ),
          const SizedBox(height: 18),

          // Label Selection
          const Text(
            "What do you think about this link?",
            style: TextStyle(
              color: Colors.white70,
              fontSize: 13,
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              _buildLabelChip("phishing", "🚫 Phishing", Colors.redAccent),
              const SizedBox(width: 8),
              _buildLabelChip("safe", "✅ Safe", Colors.greenAccent),
              const SizedBox(width: 8),
              _buildLabelChip("unsure", "🤔 Unsure", Colors.amberAccent),
            ],
          ),
          const SizedBox(height: 20),

          // AI Training Questions
          const Text(
            "Help Train Our AI (Optional):",
            style: TextStyle(
              color: Color(0xFFA78BFA),
              fontSize: 13,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          const Text(
            "Answer these questions or skip any you don't want to answer.",
            style: TextStyle(color: Colors.white38, fontSize: 11),
          ),
          const SizedBox(height: 10),

          if (_isLoadingQuestions)
            const Center(
              child: Padding(
                padding: EdgeInsets.all(20),
                child: CircularProgressIndicator(color: Color(0xFFA78BFA)),
              ),
            )
          else
            ..._questions.asMap().entries.map((entry) {
              final idx = entry.key;
              final q = entry.value;
              return _buildQuestionCard(q, idx);
            }),

          const SizedBox(height: 20),

          // Submit Button
          SizedBox(
            width: double.infinity,
            height: 50,
            child: ElevatedButton.icon(
              onPressed: (_selectedLabel.isNotEmpty &&
                      _urlController.text.trim().isNotEmpty &&
                      !_isSubmitting)
                  ? _submitReport
                  : null,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepOrangeAccent,
                foregroundColor: Colors.white,
                disabledBackgroundColor: Colors.white.withAlpha(10),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(14),
                ),
              ),
              icon: _isSubmitting
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(
                        color: Colors.white,
                        strokeWidth: 2,
                      ),
                    )
                  : const Icon(Icons.send_rounded),
              label: Text(
                _isSubmitting ? "Submitting..." : "Submit Report",
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 15,
                ),
              ),
            ),
          ),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildLabelChip(String value, String text, Color color) {
    final isSelected = _selectedLabel == value;
    return Expanded(
      child: GestureDetector(
        onTap: () {
          setState(() => _selectedLabel = value);
        },
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: isSelected ? color.withAlpha(40) : Colors.white.withAlpha(5),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isSelected ? color.withAlpha(120) : Colors.white.withAlpha(20),
              width: isSelected ? 2 : 1,
            ),
          ),
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: isSelected ? color : Colors.white54,
              fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
              fontSize: 13,
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildQuestionCard(CommunityQuestion q, int index) {
    final currentAnswer = _answers[q.id];
    final isSkipped = currentAnswer == 'skipped';

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white.withAlpha(5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isSkipped
              ? Colors.amber.withAlpha(40)
              : const Color(0xFF7C3AED).withAlpha(30),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: const Color(0xFF7C3AED).withAlpha(40),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  "Q${index + 1}",
                  style: const TextStyle(
                    color: Color(0xFFC4B5FD),
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  q.question,
                  style: const TextStyle(
                    color: Color(0xFFA78BFA),
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 6,
            runSpacing: 6,
            children: [
              ...q.options.map((opt) {
                final isOptionSelected = currentAnswer == opt;
                return GestureDetector(
                  onTap: () {
                    setState(() => _answers[q.id] = opt);
                  },
                  child: AnimatedContainer(
                    duration: const Duration(milliseconds: 150),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: isOptionSelected
                          ? Colors.cyan.withAlpha(40)
                          : Colors.white.withAlpha(5),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(
                        color: isOptionSelected
                            ? Colors.cyanAccent.withAlpha(100)
                            : Colors.white.withAlpha(15),
                      ),
                    ),
                    child: Text(
                      opt,
                      style: TextStyle(
                        color: isOptionSelected
                            ? Colors.cyanAccent
                            : Colors.white54,
                        fontSize: 11,
                        fontWeight:
                            isOptionSelected ? FontWeight.w600 : FontWeight.w400,
                      ),
                    ),
                  ),
                );
              }),
              // Skip button
              GestureDetector(
                onTap: () {
                  setState(() => _answers[q.id] = 'skipped');
                },
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: isSkipped
                          ? Colors.amber.withAlpha(80)
                          : Colors.white.withAlpha(10),
                      style: BorderStyle.solid,
                    ),
                  ),
                  child: Text(
                    "Skip",
                    style: TextStyle(
                      color: isSkipped ? Colors.amber : Colors.white30,
                      fontSize: 11,
                      fontWeight: isSkipped ? FontWeight.w600 : FontWeight.w400,
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
