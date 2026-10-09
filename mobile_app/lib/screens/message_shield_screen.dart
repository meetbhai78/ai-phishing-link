import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';
import 'package:url_launcher/url_launcher.dart';
import '../services/api_service.dart';
import '../widgets/api_settings_dialog.dart';

class MessageShieldScreen extends StatefulWidget {
  const MessageShieldScreen({super.key});

  @override
  State<MessageShieldScreen> createState() => _MessageShieldScreenState();
}

class _MessageShieldScreenState extends State<MessageShieldScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  // Auto-Protection Toggles
  bool _whatsappGuardEnabled = true;
  bool _smsGuardEnabled = true;

  // Manual Analyzer Controllers
  final TextEditingController _senderController = TextEditingController();
  final TextEditingController _messageController = TextEditingController();
  String _selectedSource = 'whatsapp';
  bool _isAnalyzing = false;
  MessageAnalysisResult? _analysisResult;
  String? _errorMessage;

  // Simulated Heads-up Notification State
  bool _showSimulatedNotification = false;
  Map<String, dynamic>? _activeSimulatedNotification;
  MessageAnalysisResult? _simulatedScanResult;
  bool _isScanningSimulation = false;

  // Scan History
  final List<Map<String, dynamic>> _scanHistory = [];

  // Preset Realistic Scams & Safe Messages for instant 1-tap testing
  final List<Map<String, String>> _presetTemplates = [
    {
      "title": "🏦 SBI Bank KYC Suspension",
      "source": "sms",
      "sender": "+91 98765 43210",
      "text":
          "Dear SBI Customer, your YONO banking account has been suspended today. Please update your PAN Card immediately to avoid permanent deactivation: http://sbi-card-kyc-verify-alert.top/login.php",
      "type": "scam"
    },
    {
      "title": "⚡ Electricity Power Cut Urgent",
      "source": "sms",
      "sender": "+91 91234 56789",
      "text":
          "Urgent Notice: Your electricity power will be disconnected tonight at 9:30 PM from electricity office because your previous month bill was not updated. Please immediately pay your bill: http://bit.ly/power-pay-bill",
      "type": "scam"
    },
    {
      "title": "🎉 Amazon ₹50,000 Gift Voucher",
      "source": "whatsapp",
      "sender": "+92 301 2345678",
      "text":
          "Congratulations! You have been selected as the lucky winner of ₹50,000 Amazon Festive Shopping Voucher. Claim within 24 hours: https://amazon-claim-gift2024.xyz/claim.html",
      "type": "scam"
    },
    {
      "title": "💬 WhatsApp Pink New Features APK",
      "source": "whatsapp",
      "sender": "Unknown Group Forward",
      "text":
          "Update your WhatsApp to official WhatsApp Pink with secret themes and call recorder! Download and install now: http://whatsapp-pink-download.apk-safe.com/app.apk",
      "type": "scam"
    },
    {
      "title": "📦 SpeedPost Held Parcel Update",
      "source": "sms",
      "sender": "+91 99887 76655",
      "text":
          "IndiaPost Alert: Your parcel #IN88921 cannot be delivered due to incomplete street address. Please update address within 12h: http://indiapost-parcel-reschedule.info/address",
      "type": "scam"
    },
    {
      "title": "✅ Official Google Security Alert",
      "source": "sms",
      "sender": "AD-GOOGLE",
      "text":
          "G-492019 is your Google verification code. Do not share your code with anyone. Check security activity at https://myaccount.google.com/security",
      "type": "safe"
    },
  ];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _senderController.dispose();
    _messageController.dispose();
    super.dispose();
  }

  Future<void> _performAnalysis({
    String? messageToScan,
    String? sourceToUse,
    String? senderToUse,
  }) async {
    final msg = (messageToScan ?? _messageController.text).trim();
    if (msg.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter or paste a message to analyze")),
      );
      return;
    }

    final src = sourceToUse ?? _selectedSource;
    final snd = (senderToUse ?? _senderController.text).trim();

    setState(() {
      _isAnalyzing = true;
      _errorMessage = null;
      _analysisResult = null;
    });

    try {
      final res = await ApiService.analyzeMessage(
        message: msg,
        source: src,
        sender: snd,
      );

      setState(() {
        _analysisResult = res;
        _scanHistory.insert(0, {
          "source": src,
          "sender": snd.isEmpty ? (src == 'whatsapp' ? 'WhatsApp Contact' : 'SMS') : snd,
          "message": msg,
          "trustScore": res.trustScore,
          "verdict": res.verdict,
          "category": res.scamCategory,
          "timestamp": DateTime.now(),
        });
      });
    } catch (e) {
      setState(() {
        _errorMessage =
            "Analysis Failed. Make sure FastAPI server is running.\n${e.toString()}";
      });
    } finally {
      setState(() {
        _isAnalyzing = false;
      });
    }
  }

  void _triggerSimulatedNotification(Map<String, String> template) async {
    setState(() {
      _showSimulatedNotification = true;
      _activeSimulatedNotification = template;
      _simulatedScanResult = null;
      _isScanningSimulation = true;
    });

    try {
      final res = await ApiService.analyzeMessage(
        message: template['text']!,
        source: template['source']!,
        sender: template['sender']!,
      );

      if (mounted) {
        setState(() {
          _simulatedScanResult = res;
          _isScanningSimulation = false;
          _scanHistory.insert(0, {
            "source": template['source'],
            "sender": template['sender'],
            "message": template['text'],
            "trustScore": res.trustScore,
            "verdict": res.verdict,
            "category": res.scamCategory,
            "timestamp": DateTime.now(),
          });
        });
      }
    } catch (_) {
      if (mounted) {
        setState(() {
          _isScanningSimulation = false;
        });
      }
    }
  }

  void _copyToClipboard(String text, String message) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.cyan[800],
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _showAndroidPermissionInfoDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.security, color: Colors.cyanAccent),
            SizedBox(width: 8),
            Text(
              "Android Auto-Scan Architecture",
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                "How CyberShield Auto-Scans Notifications:",
                style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 13),
              ),
              const SizedBox(height: 8),
              _buildFeatureBullet(
                "1. NotificationListenerService",
                "Android native background service listens to WhatsApp notifications. When a message contains a URL, it is instantly intercepted before user taps it.",
              ),
              const SizedBox(height: 6),
              _buildFeatureBullet(
                "2. SMS BroadcastReceiver",
                "Listens to SMS_RECEIVED intent. Auto-extracts sender ID (DLT Header vs 10-digit mobile) and embedded short links.",
              ),
              const SizedBox(height: 6),
              _buildFeatureBullet(
                "3. Privacy-First Sandbox",
                "Only the extracted URL and threat keywords are evaluated. Private chat contents never leave your device.",
              ),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.cyan.withAlpha(25),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.cyan.withAlpha(60)),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.check_circle_outline, color: Colors.cyanAccent, size: 20),
                    SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        "Permissions configured in AndroidManifest.xml ready for phone deployment.",
                        style: TextStyle(color: Colors.white70, fontSize: 11),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("OK, Got It", style: TextStyle(color: Colors.cyanAccent)),
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureBullet(String title, String desc) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600)),
        const SizedBox(height: 2),
        Text(desc, style: const TextStyle(color: Colors.white60, fontSize: 11, height: 1.3)),
      ],
    );
  }

  Color _getVerdictColor(String verdict) {
    switch (verdict) {
      case "VERIFIED_SAFE":
        return const Color(0xFF00E676);
      case "CAUTION":
        return const Color(0xFFFFB300);
      default:
        return const Color(0xFFFF1744);
    }
  }

  IconData _getVerdictIcon(String verdict) {
    switch (verdict) {
      case "VERIFIED_SAFE":
        return Icons.verified_user_rounded;
      case "CAUTION":
        return Icons.warning_amber_rounded;
      default:
        return Icons.gpp_bad_rounded;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F0C29),
      appBar: AppBar(
        backgroundColor: const Color(0xFF16123D),
        elevation: 0,
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.cyanAccent.withAlpha(30),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.shield, color: Colors.cyanAccent, size: 20),
            ),
            const SizedBox(width: 10),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Message & SMS Shield",
                  style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                ),
                Text(
                  "WhatsApp & SMS Link Auto-Guard",
                  style: TextStyle(color: Colors.white54, fontSize: 11),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.tune, color: Colors.white70),
            tooltip: "API & MongoDB Settings",
            onPressed: () => ApiSettingsDialog.show(context),
          ),
          IconButton(
            icon: const Icon(Icons.info_outline, color: Colors.cyanAccent),
            tooltip: "How Auto-Scanning Works",
            onPressed: _showAndroidPermissionInfoDialog,
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          indicatorColor: Colors.cyanAccent,
          labelColor: Colors.cyanAccent,
          unselectedLabelColor: Colors.white54,
          labelStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
          tabs: const [
            Tab(icon: Icon(Icons.security, size: 18), text: "Auto Guard"),
            Tab(icon: Icon(Icons.manage_search, size: 18), text: "Analyzer"),
            Tab(icon: Icon(Icons.history, size: 18), text: "Scan Logs"),
          ],
        ),
      ),
      body: Stack(
        children: [
          TabBarView(
            controller: _tabController,
            children: [
              _buildAutoGuardTab(),
              _buildAnalyzerTab(),
              _buildHistoryTab(),
            ],
          ),
          if (_showSimulatedNotification && _activeSimulatedNotification != null)
            _buildFloatingNotificationBanner(),
        ],
      ),
    );
  }

  // ==========================================
  // TAB 1: Auto Guard & Simulation Lab
  // ==========================================
  Widget _buildAutoGuardTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Live Protection Banner
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                colors: (_whatsappGuardEnabled || _smsGuardEnabled)
                    ? [const Color(0xFF003B46), const Color(0xFF07575B)]
                    : [const Color(0xFF3E2723), const Color(0xFF4E342E)],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: (_whatsappGuardEnabled || _smsGuardEnabled)
                    ? Colors.cyanAccent.withAlpha(120)
                    : Colors.redAccent.withAlpha(100),
                width: 1.2,
              ),
              boxShadow: [
                BoxShadow(
                  color: (_whatsappGuardEnabled || _smsGuardEnabled)
                      ? Colors.cyanAccent.withAlpha(30)
                      : Colors.redAccent.withAlpha(30),
                  blurRadius: 12,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.black.withAlpha(70),
                    shape: BoxShape.circle,
                  ),
                  child: Icon(
                    (_whatsappGuardEnabled || _smsGuardEnabled)
                        ? Icons.verified_user
                        : Icons.shield_outlined,
                    color: (_whatsappGuardEnabled || _smsGuardEnabled)
                        ? Colors.cyanAccent
                        : Colors.redAccent,
                    size: 28,
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        (_whatsappGuardEnabled || _smsGuardEnabled)
                            ? "ACTIVE AUTO-PROTECTION"
                            : "AUTO-GUARD PAUSED",
                        style: TextStyle(
                          color: (_whatsappGuardEnabled || _smsGuardEnabled)
                              ? Colors.cyanAccent
                              : Colors.redAccent,
                          fontWeight: FontWeight.bold,
                          fontSize: 13,
                          letterSpacing: 0.8,
                        ),
                      ),
                      const SizedBox(height: 3),
                      Text(
                        (_whatsappGuardEnabled || _smsGuardEnabled)
                            ? "Incoming WhatsApp notifications & SMS links are monitored in real-time."
                            : "Enable toggles below to resume real-time link interception.",
                        style: const TextStyle(color: Colors.white70, fontSize: 11),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // Protection Toggles
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF1E1E2E),
              borderRadius: BorderRadius.circular(14),
              border: Border.all(color: Colors.white.withAlpha(15)),
            ),
            child: Column(
              children: [
                SwitchListTile(
                  value: _whatsappGuardEnabled,
                  onChanged: (val) {
                    setState(() => _whatsappGuardEnabled = val);
                  },
                  activeThumbColor: Colors.greenAccent,
                  activeTrackColor: Colors.green.withAlpha(100),
                  secondary: const CircleAvatar(
                    backgroundColor: Color(0xFF25D366),
                    radius: 16,
                    child: Icon(Icons.chat, color: Colors.white, size: 18),
                  ),
                  title: const Text(
                    "WhatsApp Notification Guard",
                    style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
                  ),
                  subtitle: const Text(
                    "Auto-extracts and scans links in WhatsApp preview alerts",
                    style: TextStyle(color: Colors.white54, fontSize: 11),
                  ),
                ),
                Divider(color: Colors.white.withAlpha(15), height: 1),
                SwitchListTile(
                  value: _smsGuardEnabled,
                  onChanged: (val) {
                    setState(() => _smsGuardEnabled = val);
                  },
                  activeThumbColor: Colors.cyanAccent,
                  activeTrackColor: Colors.cyan.withAlpha(100),
                  secondary: const CircleAvatar(
                    backgroundColor: Color(0xFF0288D1),
                    radius: 16,
                    child: Icon(Icons.sms, color: Colors.white, size: 18),
                  ),
                  title: const Text(
                    "SMS Phishing & KYC Guard",
                    style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
                  ),
                  subtitle: const Text(
                    "Validates TRAI DLT sender headers and scans SMS links",
                    style: TextStyle(color: Colors.white54, fontSize: 11),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 20),

          // Simulation Lab Section Header
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Row(
                children: [
                  Icon(Icons.science_outlined, color: Colors.cyanAccent, size: 18),
                  SizedBox(width: 8),
                  Text(
                    "Live Interception Test Lab",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: Colors.cyan.withAlpha(30),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: const Text(
                  "Tap to Test",
                  style: TextStyle(color: Colors.cyanAccent, fontSize: 10, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
          const SizedBox(height: 6),
          const Text(
            "Select any real-world WhatsApp scam or SMS threat below to simulate how CyberShield catches the notification and computes the Trust Score instantly:",
            style: TextStyle(color: Colors.white60, fontSize: 11),
          ),
          const SizedBox(height: 12),

          // Simulation preset buttons
          ..._presetTemplates.map((item) {
            final isScam = item['type'] == 'scam';
            final isWhatsApp = item['source'] == 'whatsapp';

            return Card(
              color: const Color(0xFF191637),
              margin: const EdgeInsets.only(bottom: 10),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(
                  color: isScam
                      ? Colors.redAccent.withAlpha(50)
                      : Colors.greenAccent.withAlpha(50),
                ),
              ),
              child: ListTile(
                contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                leading: CircleAvatar(
                  backgroundColor: isWhatsApp ? const Color(0xFF25D366) : const Color(0xFF0288D1),
                  child: Icon(
                    isWhatsApp ? Icons.chat : Icons.sms,
                    color: Colors.white,
                    size: 18,
                  ),
                ),
                title: Text(
                  item['title']!,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                subtitle: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const SizedBox(height: 3),
                    Text(
                      "Sender: ${item['sender']}",
                      style: TextStyle(
                        color: isScam ? Colors.orangeAccent : Colors.cyanAccent,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      item['text']!,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(color: Colors.white54, fontSize: 11),
                    ),
                  ],
                ),
                trailing: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: isScam
                        ? Colors.redAccent.withAlpha(40)
                        : Colors.greenAccent.withAlpha(40),
                    foregroundColor: isScam ? Colors.redAccent : Colors.greenAccent,
                    elevation: 0,
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                      side: BorderSide(
                        color: isScam ? Colors.redAccent : Colors.greenAccent,
                        width: 0.8,
                      ),
                    ),
                  ),
                  onPressed: () => _triggerSimulatedNotification(item),
                  child: const Text("Simulate", style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                ),
              ),
            );
          }),
        ],
      ),
    );
  }

  // Floating Notification Interceptor Widget (Heads-up Simulation)
  Widget _buildFloatingNotificationBanner() {
    final template = _activeSimulatedNotification!;
    final isWhatsApp = template['source'] == 'whatsapp';

    return Positioned(
      top: 10,
      left: 12,
      right: 12,
      child: Material(
        elevation: 12,
        borderRadius: BorderRadius.circular(16),
        color: Colors.transparent,
        child: Container(
          padding: const EdgeInsets.all(14),
          decoration: BoxDecoration(
            gradient: const LinearGradient(
              colors: [Color(0xFF1F1B3E), Color(0xFF13102C)],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(
              color: _simulatedScanResult != null
                  ? _getVerdictColor(_simulatedScanResult!.verdict)
                  : Colors.cyanAccent,
              width: 1.5,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withAlpha(160),
                blurRadius: 18,
                offset: const Offset(0, 6),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Row(
                children: [
                  CircleAvatar(
                    backgroundColor: isWhatsApp ? const Color(0xFF25D366) : const Color(0xFF0288D1),
                    radius: 12,
                    child: Icon(
                      isWhatsApp ? Icons.chat : Icons.sms,
                      color: Colors.white,
                      size: 13,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    isWhatsApp ? "WhatsApp Notification" : "Incoming SMS Alert",
                    style: const TextStyle(
                      color: Colors.white70,
                      fontSize: 11,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    padding: EdgeInsets.zero,
                    constraints: const BoxConstraints(),
                    icon: const Icon(Icons.close, color: Colors.white54, size: 18),
                    onPressed: () {
                      setState(() {
                        _showSimulatedNotification = false;
                      });
                    },
                  ),
                ],
              ),
              const SizedBox(height: 6),
              Text(
                template['sender'] ?? 'Unknown Sender',
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 13,
                ),
              ),
              const SizedBox(height: 2),
              Text(
                template['text']!,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: Colors.white70, fontSize: 11),
              ),
              const SizedBox(height: 10),

              // Scanning State or Result Pill
              if (_isScanningSimulation)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.cyan.withAlpha(30),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Row(
                    children: [
                      SpinKitThreeBounce(color: Colors.cyanAccent, size: 14),
                      SizedBox(width: 10),
                      Text(
                        "Auto-scanning embedded links with CyberShield AI...",
                        style: TextStyle(color: Colors.cyanAccent, fontSize: 11),
                      ),
                    ],
                  ),
                )
              else if (_simulatedScanResult != null)
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: _getVerdictColor(_simulatedScanResult!.verdict).withAlpha(25),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                      color: _getVerdictColor(_simulatedScanResult!.verdict).withAlpha(100),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            _getVerdictIcon(_simulatedScanResult!.verdict),
                            color: _getVerdictColor(_simulatedScanResult!.verdict),
                            size: 18,
                          ),
                          const SizedBox(width: 8),
                          Expanded(
                            child: Text(
                              _simulatedScanResult!.verdict == "MALICIOUS_SCAM"
                                  ? "🚨 DANGEROUS PHISHING SCAM DETECTED"
                                  : (_simulatedScanResult!.verdict == "CAUTION"
                                      ? "⚠️ CAUTION - SUSPICIOUS CONTENT"
                                      : "✅ VERIFIED AUTHENTIC & SAFE"),
                              style: TextStyle(
                                color: _getVerdictColor(_simulatedScanResult!.verdict),
                                fontWeight: FontWeight.bold,
                                fontSize: 11,
                              ),
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                            decoration: BoxDecoration(
                              color: _getVerdictColor(_simulatedScanResult!.verdict),
                              borderRadius: BorderRadius.circular(12),
                            ),
                            child: Text(
                              "Trust: ${_simulatedScanResult!.trustScore.toInt()}%",
                              style: const TextStyle(
                                color: Colors.black,
                                fontWeight: FontWeight.bold,
                                fontSize: 11,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Text(
                        _simulatedScanResult!.summaryAdvisory,
                        style: const TextStyle(color: Colors.white, fontSize: 11),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          TextButton(
                            style: TextButton.styleFrom(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                              foregroundColor: Colors.cyanAccent,
                            ),
                            onPressed: () {
                              setState(() {
                                _analysisResult = _simulatedScanResult;
                                _selectedSource = template['source']!;
                                _senderController.text = template['sender']!;
                                _messageController.text = template['text']!;
                                _showSimulatedNotification = false;
                                _tabController.animateTo(1); // Switch to Analyzer tab
                              });
                            },
                            child: const Text(
                              "View Full Trust Breakdown →",
                              style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  // ==========================================
  // TAB 2: Manual Message & Link Analyzer
  // ==========================================
  Widget _buildAnalyzerTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Channel selector chips
          Row(
            children: [
              const Text("Channel:", style: TextStyle(color: Colors.white70, fontSize: 13)),
              const SizedBox(width: 10),
              ChoiceChip(
                label: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.chat, size: 14, color: Colors.white),
                    SizedBox(width: 6),
                    Text("WhatsApp"),
                  ],
                ),
                selected: _selectedSource == 'whatsapp',
                selectedColor: const Color(0xFF25D366),
                backgroundColor: const Color(0xFF1E1E2E),
                labelStyle: TextStyle(
                  color: _selectedSource == 'whatsapp' ? Colors.black : Colors.white70,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
                onSelected: (selected) {
                  if (selected) setState(() => _selectedSource = 'whatsapp');
                },
              ),
              const SizedBox(width: 8),
              ChoiceChip(
                label: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.sms, size: 14, color: Colors.white),
                    SizedBox(width: 6),
                    Text("SMS"),
                  ],
                ),
                selected: _selectedSource == 'sms',
                selectedColor: const Color(0xFF0288D1),
                backgroundColor: const Color(0xFF1E1E2E),
                labelStyle: TextStyle(
                  color: _selectedSource == 'sms' ? Colors.white : Colors.white70,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
                onSelected: (selected) {
                  if (selected) setState(() => _selectedSource = 'sms');
                },
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Sender input
          TextField(
            controller: _senderController,
            style: const TextStyle(color: Colors.white, fontSize: 13),
            decoration: InputDecoration(
              labelText: _selectedSource == 'sms'
                  ? "Sender ID or Mobile Number (e.g., AD-SBIINB or +919876543210)"
                  : "WhatsApp Sender (e.g. +923012345678 or Group Name)",
              labelStyle: const TextStyle(color: Colors.white54, fontSize: 12),
              prefixIcon: Icon(
                _selectedSource == 'sms' ? Icons.phone_android : Icons.person_outline,
                color: Colors.cyanAccent,
                size: 20,
              ),
              filled: true,
              fillColor: const Color(0xFF1A173B),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.white.withAlpha(20)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.white.withAlpha(20)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Colors.cyanAccent),
              ),
            ),
          ),
          const SizedBox(height: 12),

          // Message input
          TextField(
            controller: _messageController,
            maxLines: 4,
            style: const TextStyle(color: Colors.white, fontSize: 13),
            decoration: InputDecoration(
              hintText: "Paste full WhatsApp message or SMS text here...\nAny embedded link will be automatically extracted, scanned, and scored.",
              hintStyle: const TextStyle(color: Colors.white38, fontSize: 12),
              filled: true,
              fillColor: const Color(0xFF1A173B),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.white.withAlpha(20)),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide(color: Colors.white.withAlpha(20)),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(color: Colors.cyanAccent),
              ),
            ),
          ),
          const SizedBox(height: 12),

          // Action row: Paste & Clear & Quick Samples
          Row(
            children: [
              OutlinedButton.icon(
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.cyanAccent,
                  side: const BorderSide(color: Colors.cyanAccent, width: 0.8),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                ),
                icon: const Icon(Icons.paste, size: 14),
                label: const Text("Paste", style: TextStyle(fontSize: 11)),
                onPressed: () async {
                  final data = await Clipboard.getData(Clipboard.kTextPlain);
                  if (data?.text != null) {
                    setState(() {
                      _messageController.text = data!.text!;
                    });
                  }
                },
              ),
              const SizedBox(width: 8),
              OutlinedButton.icon(
                style: OutlinedButton.styleFrom(
                  foregroundColor: Colors.white60,
                  side: BorderSide(color: Colors.white.withAlpha(30), width: 0.8),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                ),
                icon: const Icon(Icons.clear, size: 14),
                label: const Text("Clear", style: TextStyle(fontSize: 11)),
                onPressed: () {
                  setState(() {
                    _senderController.clear();
                    _messageController.clear();
                    _analysisResult = null;
                    _errorMessage = null;
                  });
                },
              ),
              const Spacer(),
              // Analyze Button
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.cyanAccent,
                  foregroundColor: Colors.black,
                  elevation: 4,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
                icon: _isAnalyzing
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2),
                      )
                    : const Icon(Icons.search_rounded, size: 18),
                label: Text(
                  _isAnalyzing ? "Scanning..." : "Scan & Build Trust",
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
                ),
                onPressed: _isAnalyzing ? null : () => _performAnalysis(),
              ),
            ],
          ),
          const SizedBox(height: 20),

          // Error Message
          if (_errorMessage != null)
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.red.withAlpha(30),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(color: Colors.redAccent),
              ),
              child: Row(
                children: [
                  const Icon(Icons.error_outline, color: Colors.redAccent),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      _errorMessage!,
                      style: const TextStyle(color: Colors.white, fontSize: 12),
                    ),
                  ),
                ],
              ),
            ),

          // Analysis Result Card (The Core Trust Building Report)
          if (_analysisResult != null) _buildTrustReportCard(_analysisResult!),
        ],
      ),
    );
  }

  // ==========================================
  // TRUST REPORT & EVIDENCE BREAKDOWN CARD
  // ==========================================
  Widget _buildTrustReportCard(MessageAnalysisResult result) {
    final verdictColor = _getVerdictColor(result.verdict);
    final verdictIcon = _getVerdictIcon(result.verdict);

    return Container(
      margin: const EdgeInsets.only(top: 8),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: const Color(0xFF17133B),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: verdictColor.withAlpha(120), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: verdictColor.withAlpha(35),
            blurRadius: 18,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Trust Score Meter Header
          Row(
            children: [
              Stack(
                alignment: Alignment.center,
                children: [
                  SizedBox(
                    width: 68,
                    height: 68,
                    child: CircularProgressIndicator(
                      value: result.trustScore / 100.0,
                      backgroundColor: Colors.white10,
                      color: verdictColor,
                      strokeWidth: 6,
                    ),
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        "${result.trustScore.toInt()}%",
                        style: TextStyle(
                          color: verdictColor,
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                      const Text(
                        "TRUST",
                        style: TextStyle(color: Colors.white54, fontSize: 8, letterSpacing: 0.5),
                      ),
                    ],
                  ),
                ],
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: verdictColor.withAlpha(30),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        result.verdict.replaceAll('_', ' '),
                        style: TextStyle(
                          color: verdictColor,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      result.scamCategory,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      "Source: ${result.source.toUpperCase()}",
                      style: const TextStyle(color: Colors.white54, fontSize: 11),
                    ),
                  ],
                ),
              ),
              Icon(verdictIcon, color: verdictColor, size: 36),
            ],
          ),
          const SizedBox(height: 16),

          // Advisory Banner
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.black.withAlpha(70),
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.white.withAlpha(15)),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  result.verdict == "MALICIOUS_SCAM" ? Icons.block : Icons.shield_outlined,
                  color: verdictColor,
                  size: 20,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        result.recommendedAction,
                        style: TextStyle(
                          color: verdictColor,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        result.summaryAdvisory,
                        style: const TextStyle(color: Colors.white70, fontSize: 11, height: 1.3),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),

          // SENDER AUTHENTICITY BADGE
          const Text(
            "1. SENDER AUTHENTICITY ANALYSIS",
            style: TextStyle(
              color: Colors.cyanAccent,
              fontSize: 11,
              fontWeight: FontWeight.bold,
              letterSpacing: 0.8,
            ),
          ),
          const SizedBox(height: 6),
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: const Color(0xFF1E1E2E),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Row(
              children: [
                Icon(
                  result.senderAnalysis['is_official_header'] == true
                      ? Icons.verified
                      : (result.senderAnalysis['is_personal_number'] == true
                          ? Icons.warning
                          : Icons.info_outline),
                  color: result.senderAnalysis['is_official_header'] == true
                      ? Colors.greenAccent
                      : (result.senderAnalysis['is_personal_number'] == true
                          ? Colors.redAccent
                          : Colors.amberAccent),
                  size: 18,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    result.senderAnalysis['notes'] ?? "Sender evaluated.",
                    style: const TextStyle(color: Colors.white, fontSize: 11),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),

          // EXTRACTED LINKS EXPLORER
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                "2. EMBEDDED LINKS & DESTINATIONS",
                style: TextStyle(
                  color: Colors.cyanAccent,
                  fontSize: 11,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 0.8,
                ),
              ),
              Text(
                "${result.extractedUrls.length} Link(s) Found",
                style: const TextStyle(color: Colors.white54, fontSize: 10),
              ),
            ],
          ),
          const SizedBox(height: 6),
          if (result.extractedUrls.isEmpty)
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: const Color(0xFF1E1E2E),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Row(
                children: [
                  Icon(Icons.link_off, color: Colors.white54, size: 18),
                  SizedBox(width: 10),
                  Text(
                    "No external hyperlinks found in message body.",
                    style: TextStyle(color: Colors.white70, fontSize: 11),
                  ),
                ],
              ),
            )
          else
            ...result.urlScanResults.map((item) {
              final isPhish = item.isPhishing;
              return Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E1E2E),
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(
                    color: isPhish ? Colors.redAccent.withAlpha(70) : Colors.greenAccent.withAlpha(70),
                  ),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          isPhish ? Icons.dangerous : Icons.check_circle,
                          color: isPhish ? Colors.redAccent : Colors.greenAccent,
                          size: 16,
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            item.url,
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              fontFamily: 'monospace',
                            ),
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: isPhish
                                ? Colors.redAccent.withAlpha(30)
                                : Colors.greenAccent.withAlpha(30),
                            borderRadius: BorderRadius.circular(6),
                          ),
                          child: Text(
                            isPhish ? "DANGER" : "SAFE",
                            style: TextStyle(
                              color: isPhish ? Colors.redAccent : Colors.greenAccent,
                              fontSize: 9,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Row(
                      children: [
                        Text(
                          "Risk Score: ${item.hybridScore.toInt()}%",
                          style: TextStyle(
                            color: isPhish ? Colors.redAccent : Colors.greenAccent,
                            fontSize: 10,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Icon(
                          item.sslValid ? Icons.lock : Icons.lock_open,
                          color: item.sslValid ? Colors.greenAccent : Colors.redAccent,
                          size: 12,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          item.sslValid ? "SSL Valid" : "No SSL / Untrusted",
                          style: TextStyle(
                            color: item.sslValid ? Colors.greenAccent : Colors.redAccent,
                            fontSize: 10,
                          ),
                        ),
                        const Spacer(),
                        if (!isPhish)
                          InkWell(
                            onTap: () async {
                              final uri = Uri.parse(item.url);
                              if (await canLaunchUrl(uri)) {
                                await launchUrl(uri, mode: LaunchMode.externalApplication);
                              }
                            },
                            child: const Text(
                              "Open Domain ↗",
                              style: TextStyle(color: Colors.cyanAccent, fontSize: 10),
                            ),
                          ),
                      ],
                    ),
                  ],
                ),
              );
            }),
          const SizedBox(height: 16),

          // WHY TRUST / WHY DANGER (Evidence Checklist)
          const Text(
            "3. TRUST & THREAT EVIDENCE CHECKLIST",
            style: TextStyle(
              color: Colors.cyanAccent,
              fontSize: 11,
              fontWeight: FontWeight.bold,
              letterSpacing: 0.8,
            ),
          ),
          const SizedBox(height: 8),

          // Positive Trust Reasons
          if (result.trustReasons.isNotEmpty)
            ...result.trustReasons.map((reason) => Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.check_circle, color: Color(0xFF00E676), size: 15),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          reason,
                          style: const TextStyle(color: Colors.white, fontSize: 11),
                        ),
                      ),
                    ],
                  ),
                )),

          // Danger Red Flag Reasons
          if (result.riskReasons.isNotEmpty)
            ...result.riskReasons.map((reason) => Padding(
                  padding: const EdgeInsets.only(bottom: 6),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.cancel, color: Color(0xFFFF1744), size: 15),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          reason,
                          style: const TextStyle(color: Colors.redAccent, fontSize: 11),
                        ),
                      ),
                    ],
                  ),
                )),

          const SizedBox(height: 18),

          // ACTION BUTTONS (Share Advisory to WhatsApp & Community Report)
          Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: const Color(0xFF25D366),
                    side: const BorderSide(color: Color(0xFF25D366), width: 1),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    padding: const EdgeInsets.symmetric(vertical: 12),
                  ),
                  icon: const Icon(Icons.share, size: 16),
                  label: const Text(
                    "Share Warning",
                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                  onPressed: () {
                    final shareText =
                        "🛡️ *CyberShield AI Security Alert*\n\n"
                        "⚠️ Verdict: *${result.verdict}* (Trust Score: ${result.trustScore.toInt()}%)\n"
                        "📂 Category: ${result.scamCategory}\n"
                        "🔗 Link Analyzed: ${result.extractedUrls.join(', ')}\n"
                        "🚨 Advisory: ${result.summaryAdvisory}\n\n"
                        "Stay safe and verify links before tapping!";
                    _copyToClipboard(shareText, "Security warning copied! Ready to paste into WhatsApp chat.");
                  },
                ),
              ),
              const SizedBox(width: 10),
              if (result.verdict == "MALICIOUS_SCAM" && result.extractedUrls.isNotEmpty)
                Expanded(
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.redAccent,
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                    icon: const Icon(Icons.report, size: 16),
                    label: const Text(
                      "Report Threat",
                      style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                    ),
                    onPressed: () async {
                      try {
                        await ApiService.submitCommunityReport(
                          url: result.extractedUrls.first,
                          userReportedLabel: "phishing",
                          questionsAnswers: {
                            "source": result.source,
                            "category": result.scamCategory,
                            "sender": result.sender,
                          },
                        );
                        if (!mounted) return;
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text("Threat reported to CyberShield Community Intelligence!"),
                            backgroundColor: Colors.green,
                          ),
                        );
                      } catch (_) {
                        if (!mounted) return;
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Threat report submission queued.")),
                        );
                      }
                    },
                  ),
                ),
            ],
          ),
        ],
      ),
    );
  }

  // ==========================================
  // TAB 3: Scan Logs & History
  // ==========================================
  Widget _buildHistoryTab() {
    if (_scanHistory.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.history, size: 48, color: Colors.white.withAlpha(50)),
            const SizedBox(height: 12),
            const Text(
              "No Messages Scanned Yet",
              style: TextStyle(color: Colors.white70, fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            const Text(
              "Simulate an incoming notification or paste a message to see logs.",
              style: TextStyle(color: Colors.white38, fontSize: 11),
            ),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _scanHistory.length,
      itemBuilder: (context, index) {
        final item = _scanHistory[index];
        final verdict = item['verdict'] as String? ?? 'UNKNOWN';
        final verdictColor = _getVerdictColor(verdict);
        final isWhatsApp = item['source'] == 'whatsapp';

        return Card(
          color: const Color(0xFF1A173B),
          margin: const EdgeInsets.only(bottom: 10),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
            side: BorderSide(color: verdictColor.withAlpha(50)),
          ),
          child: ListTile(
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
            leading: CircleAvatar(
              backgroundColor: isWhatsApp ? const Color(0xFF25D366) : const Color(0xFF0288D1),
              child: Icon(isWhatsApp ? Icons.chat : Icons.sms, color: Colors.white, size: 18),
            ),
            title: Row(
              children: [
                Expanded(
                  child: Text(
                    item['sender'] ?? 'Unknown',
                    style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                  decoration: BoxDecoration(
                    color: verdictColor.withAlpha(30),
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: Text(
                    "Trust: ${(item['trustScore'] as num).toInt()}%",
                    style: TextStyle(color: verdictColor, fontSize: 10, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 4),
                Text(
                  item['message'] ?? '',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: Colors.white70, fontSize: 11),
                ),
                const SizedBox(height: 4),
                Text(
                  item['category'] ?? 'General',
                  style: TextStyle(color: verdictColor, fontSize: 10, fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
