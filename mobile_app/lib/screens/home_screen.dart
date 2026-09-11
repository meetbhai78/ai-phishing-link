import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _urlController = TextEditingController();
  bool _isLoading = false;
  PredictionResult? _result;
  String? _errorMessage;

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _performScan([String? urlToScan]) async {
    final targetUrl = (urlToScan ?? _urlController.text).trim();
    if (targetUrl.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter or scan a valid URL")),
      );
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _result = null;
    });

    try {
      final res = await ApiService.scanUrl(targetUrl);
      setState(() {
        _result = res;
      });
    } catch (e) {
      setState(() {
        _errorMessage = "Connection Failed. Make sure FastAPI server is running.\nHost: ${ApiService.baseUrl}";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showApiSettingsDialog() {
    final controller = TextEditingController(text: ApiService.baseUrl);
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        title: const Text("Backend API Settings", style: TextStyle(color: Colors.cyan)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Set FastAPI Endpoint:\n- Android Emulator: http://10.0.2.2:8000/predict\n- Physical Phone: http://192.168.X.X:8000/predict",
              style: TextStyle(color: Colors.white70, fontSize: 12),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: controller,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                labelText: "API Endpoint",
                labelStyle: TextStyle(color: Colors.cyan),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () {
              setState(() {
                ApiService.baseUrl = controller.text.trim();
              });
              Navigator.pop(context);
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text("API Endpoint updated to: ${ApiService.baseUrl}")),
              );
            },
            child: const Text("Save"),
          ),
        ],
      ),
    );
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
            Icon(Icons.shield_outlined, color: Colors.cyan),
            SizedBox(width: 8),
            Text(
              "CyberShield AI",
              style: TextStyle(color: Colors.cyan, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings, color: Colors.white70),
            onPressed: _showApiSettingsDialog,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // URL Input Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.05),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.white.withOpacity(0.1)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Enter Website URL to Scan:",
                    style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w500),
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: _urlController,
                    style: const TextStyle(color: Colors.cyanAccent, fontFamily: 'monospace'),
                    decoration: InputDecoration(
                      hintText: "https://example.com",
                      hintStyle: TextStyle(color: Colors.white.withOpacity(0.3)),
                      filled: true,
                      fillColor: Colors.black26,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide.none,
                      ),
                      prefixIcon: const Icon(Icons.link, color: Colors.cyan),
                    ),
                  ),
                  const SizedBox(height: 12),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton.icon(
                      onPressed: _isLoading ? null : () => _performScan(),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.cyan,
                        foregroundColor: Colors.black,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.radar, color: Colors.black),
                      label: const Text(
                        "SCAN WITH AI & WEB ROBOT",
                        style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 0.5),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Loading Indicator
            if (_isLoading)
              const Center(
                child: Padding(
                  padding: EdgeInsets.all(32.0),
                  child: Column(
                    children: [
                      SpinKitCubeGrid(color: Colors.cyan, size: 50.0),
                      SizedBox(height: 16),
                      Text(
                        "Robot & AI Analyzing Webpage...",
                        style: TextStyle(color: Colors.white70, fontSize: 14),
                      ),
                    ],
                  ),
                ),
              ),

            // Error Card
            if (_errorMessage != null)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.withOpacity(0.15),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.red.withOpacity(0.4)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.error_outline, color: Colors.redAccent, size: 28),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        _errorMessage!,
                        style: const TextStyle(color: Colors.redAccent, fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),

            // Result Display
            if (_result != null) ...[
              _buildResultCard(_result!),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard(PredictionResult res) {
    final isDanger = res.isPhishing;
    final cardColor = isDanger ? Colors.red : Colors.green;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: cardColor.withOpacity(0.12),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: cardColor.withOpacity(0.4)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                isDanger ? Icons.warning_amber_rounded : Icons.verified_user_outlined,
                color: cardColor,
                size: 36,
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      isDanger ? "PHISHING DANGER DETECTED!" : "WEBSITE IS SAFE",
                      style: TextStyle(
                        color: cardColor,
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    Text(
                      "Confidence: ${res.confidence}% | ${res.riskLevel}",
                      style: const TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.08),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.cyan.withOpacity(0.3)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.label_outline, color: Colors.cyanAccent, size: 14),
                const SizedBox(width: 6),
                Text(
                  "Category: ${res.threatCategory}",
                  style: const TextStyle(color: Colors.cyanAccent, fontSize: 12, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
          const Divider(color: Colors.white24, height: 24),

          // SSL Certificate Inspection
          const Text(
            "🔒 SSL Certificate Security:",
            style: TextStyle(color: Colors.cyan, fontWeight: FontWeight.bold, fontSize: 13),
          ),
          const SizedBox(height: 8),
          _buildInfoRow(
            "Certificate Status",
            res.sslInfo['valid'] == true ? "Valid & Trusted" : (res.sslInfo['has_ssl'] == true ? "Invalid / Handshake Error" : "No HTTPS"),
            res.sslInfo['valid'] == true ? Colors.greenAccent : Colors.redAccent,
          ),
          _buildInfoRow(
            "Certificate Issuer",
            res.sslInfo['issuer'] ?? "None",
            Colors.white70,
          ),
          _buildInfoRow(
            "Days Remaining",
            res.sslInfo['valid'] == true ? "${res.sslInfo['days_remaining']} days" : "-",
            Colors.white70,
          ),
          const SizedBox(height: 12),

          // Robot Scraper Details
          const Text(
            "🤖 Robot Webpage Analysis:",
            style: TextStyle(color: Colors.cyan, fontWeight: FontWeight.bold, fontSize: 13),
          ),
          const SizedBox(height: 8),
          _buildInfoRow(
            "Password Input Field",
            res.contentAnalysis['has_password_field'] == true ? "DETECTED (High Risk)" : "None",
            res.contentAnalysis['has_password_field'] == true ? Colors.redAccent : Colors.white70,
          ),
          _buildInfoRow(
            "External Form Submission",
            res.contentAnalysis['external_form_action'] == true ? "UNAUTHORIZED POST" : "Safe / Internal",
            res.contentAnalysis['external_form_action'] == true ? Colors.redAccent : Colors.white70,
          ),
          _buildInfoRow(
            "Brand Impersonation",
            res.contentAnalysis['brand_mismatch'] ?? "Verified Clean",
            res.contentAnalysis['brand_mismatch'] != null ? Colors.redAccent : Colors.greenAccent,
          ),
          _buildInfoRow(
            "Robot Content Score",
            "${res.contentAnalysis['content_risk_score'] ?? 0}%",
            Colors.cyanAccent,
          ),

          // Risk signals list
          if (res.contentAnalysis['risk_signals'] != null &&
              (res.contentAnalysis['risk_signals'] as List).isNotEmpty) ...[
            const SizedBox(height: 12),
            const Text(
              "Detected Threat Signals:",
              style: TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.w600, fontSize: 12),
            ),
            const SizedBox(height: 6),
            ...((res.contentAnalysis['risk_signals'] as List).map(
              (sig) => Padding(
                padding: const EdgeInsets.only(bottom: 4.0),
                child: Row(
                  children: [
                    const Icon(Icons.warning, color: Colors.amberAccent, size: 14),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        sig.toString(),
                        style: const TextStyle(color: Colors.white70, fontSize: 11),
                      ),
                    ),
                  ],
                ),
              ),
            )),
          ],
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value, Color valColor) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.white60, fontSize: 12)),
          Flexible(
            child: Text(
              value,
              style: TextStyle(color: valColor, fontWeight: FontWeight.w600, fontSize: 12),
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}
