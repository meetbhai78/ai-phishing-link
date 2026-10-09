import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import '../services/api_service.dart';
import '../widgets/api_settings_dialog.dart';

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

  // Active Connection State
  bool _isCheckingConnection = false;
  bool _isServerOnline = false;
  String _databaseStatus = "Checking...";

  // Recent scans local history cache
  final List<PredictionResult> _recentScans = [];

  // Quick preset test URLs for instant 1-tap testing
  final List<Map<String, String>> _presetUrls = [
    {
      "label": "Safe: Google",
      "url": "https://google.com",
      "type": "safe",
    },
    {
      "label": "Threat: PayPal Fake",
      "url": "http://paypal-security-login.xyz/signin.html",
      "type": "phishing",
    },
    {
      "label": "Threat: SBI KYC Spoof",
      "url": "http://sbi-card-kyc-verify-alert.top/login.php",
      "type": "phishing",
    },
    {
      "label": "Safe: CHARUSAT",
      "url": "https://charusat.ac.in",
      "type": "safe",
    },
    {
      "label": "Threat: IP Scam",
      "url": "http://192.168.1.1/banking/login",
      "type": "phishing",
    },
  ];

  @override
  void initState() {
    super.initState();
    _checkServerConnection();
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  Future<void> _checkServerConnection() async {
    setState(() {
      _isCheckingConnection = true;
    });

    final status = await ApiService.testConnection();

    if (mounted) {
      setState(() {
        _isCheckingConnection = false;
        _isServerOnline = status['success'] == true;
        _databaseStatus = status['message'] ?? (_isServerOnline ? "MongoDB Atlas Online" : "Offline Engine");
      });
    }
  }

  Future<void> _performScan([String? urlToScan]) async {
    final targetUrl = (urlToScan ?? _urlController.text).trim();
    if (targetUrl.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter or scan a valid URL")),
      );
      return;
    }

    _urlController.text = targetUrl;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _result = null;
    });

    try {
      final res = await ApiService.scanUrl(targetUrl);
      setState(() {
        _result = res;
        // Keep unique in recent scans (up to 10)
        _recentScans.removeWhere((item) => item.url == res.url);
        _recentScans.insert(0, res);
        if (_recentScans.length > 10) {
          _recentScans.removeLast();
        }
      });
    } catch (e) {
      setState(() {
        _errorMessage =
            "Connection Failed. Make sure FastAPI server is running.\nEndpoint: ${ApiService.baseUrl}";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _showApiSettingsDialog() {
    ApiSettingsDialog.show(context, onSettingsSaved: _checkServerConnection);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F0C29),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.cyan.withAlpha(40),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.cyanAccent.withAlpha(80)),
              ),
              child: const Icon(Icons.shield, color: Colors.cyanAccent, size: 20),
            ),
            const SizedBox(width: 10),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "CyberShield AI",
                  style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 17),
                ),
                Text(
                  "Real-Time Phishing Telemetry",
                  style: TextStyle(color: Colors.white38, fontSize: 10),
                ),
              ],
            ),
          ],
        ),
        actions: [
          // Live Status Pill (Tappable to test/reconfigure)
          Tooltip(
            message: _databaseStatus,
            child: InkWell(
              onTap: _showApiSettingsDialog,
              borderRadius: BorderRadius.circular(20),
              child: Container(
                margin: const EdgeInsets.symmetric(vertical: 12, horizontal: 4),
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: _isServerOnline ? Colors.green.withAlpha(30) : Colors.amber.withAlpha(30),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: _isServerOnline ? Colors.greenAccent.withAlpha(80) : Colors.amberAccent.withAlpha(80),
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      _isCheckingConnection
                          ? Icons.sync
                          : (_isServerOnline ? Icons.circle : Icons.offline_bolt),
                      color: _isServerOnline ? Colors.greenAccent : Colors.amberAccent,
                      size: 10,
                    ),
                    const SizedBox(width: 5),
                    Text(
                      _isCheckingConnection
                          ? "Testing..."
                          : (_isServerOnline ? "Atlas Online" : "Offline Mode"),
                      style: TextStyle(
                        color: _isServerOnline ? Colors.greenAccent : Colors.amberAccent,
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.tune, color: Colors.white70),
            onPressed: _showApiSettingsDialog,
            tooltip: "API & MongoDB Settings",
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Quick 1-Tap Test Presets
            const Text(
              "⚡ Quick-Test Presets (1-Tap):",
              style: TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 38,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                itemCount: _presetUrls.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (context, index) {
                  final preset = _presetUrls[index];
                  final isThreat = preset["type"] == "phishing";
                  return InkWell(
                    onTap: () => _performScan(preset["url"]!),
                    borderRadius: BorderRadius.circular(10),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(
                        color: isThreat ? Colors.red.withAlpha(35) : Colors.cyan.withAlpha(35),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(
                          color: isThreat ? Colors.redAccent.withAlpha(90) : Colors.cyanAccent.withAlpha(90),
                        ),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            isThreat ? Icons.warning_amber_rounded : Icons.check_circle_outline,
                            size: 14,
                            color: isThreat ? Colors.redAccent : Colors.cyanAccent,
                          ),
                          const SizedBox(width: 6),
                          Text(
                            preset["label"]!,
                            style: TextStyle(
                              color: isThreat ? Colors.redAccent : Colors.cyanAccent,
                              fontSize: 12,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 16),

            // URL Input Card
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white.withAlpha(15),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.white.withAlpha(25)),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withAlpha(70),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Enter Target URL to Inspect:",
                    style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w500),
                  ),
                  const SizedBox(height: 10),
                  TextField(
                    controller: _urlController,
                    style: const TextStyle(color: Colors.cyanAccent, fontFamily: 'monospace', fontSize: 13),
                    decoration: InputDecoration(
                      hintText: "https://secure-login.xyz or google.com",
                      hintStyle: TextStyle(color: Colors.white.withAlpha(60), fontSize: 12),
                      filled: true,
                      fillColor: Colors.black.withAlpha(60),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: BorderSide(color: Colors.white.withAlpha(20)),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(12),
                        borderSide: const BorderSide(color: Colors.cyanAccent),
                      ),
                      prefixIcon: const Icon(Icons.link, color: Colors.cyanAccent),
                      suffixIcon: _urlController.text.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear, color: Colors.white38, size: 18),
                              onPressed: () {
                                _urlController.clear();
                                setState(() {});
                              },
                            )
                          : null,
                    ),
                    onChanged: (_) => setState(() {}),
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton.icon(
                      onPressed: _isLoading ? null : () => _performScan(),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.cyanAccent,
                        foregroundColor: Colors.black,
                        elevation: 4,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.radar, color: Colors.black, size: 20),
                      label: const Text(
                        "INSPECT URL WITH HYBRID AI",
                        style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 0.6, fontSize: 13),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Loading State
            if (_isLoading)
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(32.0),
                  child: Column(
                    children: [
                      const SpinKitCubeGrid(color: Colors.cyanAccent, size: 50.0),
                      const SizedBox(height: 18),
                      const Text(
                        "AI Feature Extraction & Deep Robot Analysis...",
                        style: TextStyle(color: Colors.cyanAccent, fontSize: 14, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        "Evaluating 30 Lexical Vectors, SSL Handshake & DOM Forms",
                        style: TextStyle(color: Colors.white.withAlpha(120), fontSize: 11),
                      ),
                    ],
                  ),
                ),
              ),

            // Error Display
            if (_errorMessage != null)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.red.withAlpha(35),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: Colors.redAccent.withAlpha(90)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.error_outline, color: Colors.redAccent, size: 30),
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

            // Scan Result Card
            if (_result != null) ...[
              _buildResultCard(_result!),
              const SizedBox(height: 20),
            ],

            // Recent Mobile Scans History
            if (_recentScans.isNotEmpty) ...[
              _buildRecentScansSection(),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard(PredictionResult res) {
    final isDanger = res.isPhishing;
    final cardColor = isDanger ? Colors.redAccent : Colors.greenAccent;
    final riskPercent = (res.confidence).clamp(0, 100);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: cardColor.withAlpha(25),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: cardColor.withAlpha(90), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: cardColor.withAlpha(30),
            blurRadius: 16,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Verdict
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: cardColor.withAlpha(40),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  isDanger ? Icons.gpp_bad_rounded : Icons.verified_user_rounded,
                  color: cardColor,
                  size: 32,
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      isDanger ? "THREAT DETECTED: PHISHING" : "VERIFIED SAFE WEBSITE",
                      style: TextStyle(
                        color: cardColor,
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                        letterSpacing: 0.5,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      res.url,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(color: Colors.white70, fontSize: 11, fontFamily: 'monospace'),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Cyber Threat Meter (Progress Bar)
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text("AI Risk Severity Score:", style: TextStyle(color: Colors.white70, fontSize: 12)),
                  Text(
                    "${riskPercent.toStringAsFixed(1)}% (${res.riskLevel})",
                    style: TextStyle(color: cardColor, fontWeight: FontWeight.bold, fontSize: 12),
                  ),
                ],
              ),
              const SizedBox(height: 6),
              ClipRRect(
                borderRadius: BorderRadius.circular(6),
                child: LinearProgressIndicator(
                  value: riskPercent / 100.0,
                  minHeight: 8,
                  backgroundColor: Colors.black.withAlpha(90),
                  valueColor: AlwaysStoppedAnimation<Color>(cardColor),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),

          // Threat Category Pill
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
            decoration: BoxDecoration(
              color: Colors.white.withAlpha(20),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: Colors.cyanAccent.withAlpha(80)),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.fingerprint, color: Colors.cyanAccent, size: 16),
                const SizedBox(width: 6),
                Text(
                  "Threat Class: ${res.threatCategory}",
                  style: const TextStyle(color: Colors.cyanAccent, fontSize: 12, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
          const Divider(color: Colors.white12, height: 24),

          // SSL Certificate Inspection
          const Row(
            children: [
              Icon(Icons.lock_outline, color: Colors.cyanAccent, size: 16),
              SizedBox(width: 6),
              Text(
                "SSL / TLS Certificate Telemetry:",
                style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 13),
              ),
            ],
          ),
          const SizedBox(height: 8),
          _buildInfoRow(
            "Certificate Status",
            res.sslInfo['valid'] == true
                ? "Valid & Authenticated"
                : (res.sslInfo['has_ssl'] == true ? "Handshake Error / Self-Signed" : "No HTTPS Encrypted"),
            res.sslInfo['valid'] == true ? Colors.greenAccent : Colors.redAccent,
          ),
          _buildInfoRow("Certificate Issuer", res.sslInfo['issuer'] ?? "None", Colors.white70),
          _buildInfoRow(
            "Days to Expiry",
            res.sslInfo['valid'] == true ? "${res.sslInfo['days_remaining']} days" : "-",
            Colors.white70,
          ),
          const SizedBox(height: 12),

          // Robot Content Inspection
          const Row(
            children: [
              Icon(Icons.smart_toy_outlined, color: Colors.cyanAccent, size: 16),
              SizedBox(width: 6),
              Text(
                "Webpage Content Robot Analysis:",
                style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 13),
              ),
            ],
          ),
          const SizedBox(height: 8),
          _buildInfoRow(
            "Password Credential Field",
            res.contentAnalysis['has_password_field'] == true ? "DETECTED (High Risk)" : "Safe / None",
            res.contentAnalysis['has_password_field'] == true ? Colors.redAccent : Colors.white70,
          ),
          _buildInfoRow(
            "Cross-Domain Form POST",
            res.contentAnalysis['external_form_action'] == true ? "MALICIOUS (External Action)" : "Safe / Verified",
            res.contentAnalysis['external_form_action'] == true ? Colors.redAccent : Colors.white70,
          ),
          _buildInfoRow(
            "Brand Impersonation Target",
            res.contentAnalysis['brand_mismatch'] ?? "No Brand Spoofing",
            res.contentAnalysis['brand_mismatch'] != null ? Colors.redAccent : Colors.greenAccent,
          ),
          _buildInfoRow(
            "Content Robot Risk Weight",
            "${res.contentAnalysis['content_risk_score'] ?? 0}%",
            Colors.cyanAccent,
          ),

          // Threat signals list
          if (res.contentAnalysis['risk_signals'] != null &&
              (res.contentAnalysis['risk_signals'] as List).isNotEmpty) ...[
            const SizedBox(height: 12),
            const Text(
              "Active Risk Signal Telemetry:",
              style: TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold, fontSize: 12),
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

  Widget _buildRecentScansSection() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withAlpha(12),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withAlpha(20)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Row(
                children: [
                  Icon(Icons.history, color: Colors.cyanAccent, size: 18),
                  SizedBox(width: 8),
                  Text(
                    "Recent App Scans",
                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                ],
              ),
              Text(
                "${_recentScans.length} Scans",
                style: const TextStyle(color: Colors.white38, fontSize: 12),
              ),
            ],
          ),
          const SizedBox(height: 12),
          ListView.separated(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            itemCount: _recentScans.length,
            separatorBuilder: (_, __) => const Divider(color: Colors.white10, height: 16),
            itemBuilder: (context, index) {
              final scan = _recentScans[index];
              final isPhish = scan.isPhishing;
              return InkWell(
                onTap: () {
                  _urlController.text = scan.url;
                  setState(() {
                    _result = scan;
                  });
                },
                child: Row(
                  children: [
                    Icon(
                      isPhish ? Icons.dangerous : Icons.check_circle,
                      color: isPhish ? Colors.redAccent : Colors.greenAccent,
                      size: 20,
                    ),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            scan.url,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(color: Colors.white, fontSize: 12, fontFamily: 'monospace'),
                          ),
                          Text(
                            "${scan.threatCategory} • ${scan.confidence}% Confidence",
                            style: TextStyle(
                              color: isPhish ? Colors.redAccent.withAlpha(180) : Colors.greenAccent.withAlpha(180),
                              fontSize: 10,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Icon(Icons.arrow_forward_ios, color: Colors.white24, size: 12),
                  ],
                ),
              );
            },
          ),
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
