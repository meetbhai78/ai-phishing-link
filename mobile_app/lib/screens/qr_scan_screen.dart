import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../services/api_service.dart';

class QrScanScreen extends StatefulWidget {
  const QrScanScreen({super.key});

  @override
  State<QrScanScreen> createState() => _QrScanScreenState();
}

class _QrScanScreenState extends State<QrScanScreen> {
  final MobileScannerController _controller = MobileScannerController();
  bool _isProcessing = false;
  final TextEditingController _manualUrlController = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    _manualUrlController.dispose();
    super.dispose();
  }

  void _onDetect(BarcodeCapture capture) async {
    if (_isProcessing) return;

    final List<Barcode> barcodes = capture.barcodes;
    for (final barcode in barcodes) {
      final String? code = barcode.rawValue;
      if (code != null && code.isNotEmpty) {
        setState(() {
          _isProcessing = true;
        });

        _showScanResultModal(code);
        break;
      }
    }
  }

  void _testSampleQr(String url) {
    if (_isProcessing) return;
    setState(() {
      _isProcessing = true;
    });
    _showScanResultModal(url);
  }

  void _showManualInputDialog() {
    _manualUrlController.clear();
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF1E1E2E),
        title: const Row(
          children: [
            Icon(Icons.qr_code, color: Colors.cyanAccent),
            SizedBox(width: 8),
            Text("Simulate QR Scanned URL", style: TextStyle(color: Colors.cyanAccent, fontSize: 16)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Enter any URL decoded from a QR Code:",
              style: TextStyle(color: Colors.white70, fontSize: 12),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _manualUrlController,
              style: const TextStyle(color: Colors.white, fontFamily: 'monospace', fontSize: 13),
              decoration: InputDecoration(
                hintText: "http://paypal-security-login.xyz/signin.html",
                hintStyle: TextStyle(color: Colors.white.withAlpha(60), fontSize: 12),
                border: const OutlineInputBorder(),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.cyanAccent),
                ),
                filled: true,
                fillColor: Colors.black.withAlpha(80),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text("Cancel", style: TextStyle(color: Colors.white54)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.cyanAccent),
            onPressed: () {
              final text = _manualUrlController.text.trim();
              Navigator.pop(context);
              if (text.isNotEmpty) {
                _testSampleQr(text);
              }
            },
            child: const Text("Scan with AI", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  void _showScanResultModal(String scannedUrl) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1E1E2E),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (context) => StatefulBuilder(
        builder: (context, setModalState) {
          return Padding(
            padding: EdgeInsets.only(
              left: 20,
              right: 20,
              top: 20,
              bottom: MediaQuery.of(context).viewInsets.bottom + 30,
            ),
            child: FutureBuilder<PredictionResult>(
              future: ApiService.scanUrl(scannedUrl),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Padding(
                    padding: EdgeInsets.all(24.0),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        CircularProgressIndicator(color: Colors.cyanAccent),
                        SizedBox(height: 16),
                        Text(
                          "Scanning QR Code Payload with AI Engine...",
                          style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold),
                        ),
                        SizedBox(height: 6),
                        Text(
                          "Checking 30 Lexical Anomalies, SSL Handshake & Fake Brand Spoofing",
                          style: TextStyle(color: Colors.white54, fontSize: 11),
                        ),
                      ],
                    ),
                  );
                }

                if (snapshot.hasError) {
                  return Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.error_outline, color: Colors.redAccent, size: 40),
                      const SizedBox(height: 10),
                      Text(
                        "Scanned QR Payload:\n$scannedUrl",
                        style: const TextStyle(color: Colors.cyanAccent, fontFamily: 'monospace', fontSize: 12),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 12),
                      Text(
                        "Error: ${snapshot.error}",
                        style: const TextStyle(color: Colors.redAccent, fontSize: 12),
                      ),
                    ],
                  );
                }

                final res = snapshot.data!;
                final isDanger = res.isPhishing;
                final color = isDanger ? Colors.redAccent : Colors.greenAccent;

                return Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Center(
                      child: Container(
                        width: 40,
                        height: 4,
                        decoration: BoxDecoration(
                          color: Colors.white24,
                          borderRadius: BorderRadius.circular(2),
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: color.withAlpha(35),
                            shape: BoxShape.circle,
                          ),
                          child: Icon(isDanger ? Icons.gpp_bad : Icons.verified, color: color, size: 28),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                isDanger ? "CRITICAL: PHISHING QR CODE!" : "SAFE & VERIFIED QR CODE",
                                style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 16),
                              ),
                              Text(
                                isDanger ? "Malicious URL hidden inside barcode" : "Legitimate destination verified",
                                style: const TextStyle(color: Colors.white54, fontSize: 11),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.black.withAlpha(90),
                        borderRadius: BorderRadius.circular(10),
                        border: Border.all(color: Colors.white12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text("Decoded QR Target URL:", style: TextStyle(color: Colors.white54, fontSize: 11)),
                          const SizedBox(height: 4),
                          Text(
                            scannedUrl,
                            style: const TextStyle(color: Colors.cyanAccent, fontSize: 12, fontFamily: 'monospace'),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 14),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          "Risk Level: ${res.riskLevel}",
                          style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12),
                        ),
                        Text(
                          "Threat Class: ${res.threatCategory}",
                          style: const TextStyle(color: Colors.white70, fontSize: 12),
                        ),
                        Text(
                          "Confidence: ${res.confidence}%",
                          style: const TextStyle(color: Colors.white70, fontSize: 12),
                        ),
                      ],
                    ),
                    const SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity,
                      height: 44,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.cyanAccent),
                        onPressed: () {
                          Navigator.pop(context);
                          setState(() {
                            _isProcessing = false;
                          });
                        },
                        child: const Text("Scan Another QR Code", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
                      ),
                    ),
                  ],
                );
              },
            ),
          );
        },
      ),
    ).then((_) {
      setState(() {
        _isProcessing = false;
      });
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
            Icon(Icons.qr_code_scanner, color: Colors.cyanAccent),
            SizedBox(width: 8),
            Text(
              "QR Phishing Scanner",
              style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 17),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.keyboard, color: Colors.cyanAccent),
            onPressed: _showManualInputDialog,
            tooltip: "Manual QR Input",
          ),
          if (!kIsWeb) ...[
            IconButton(
              icon: ValueListenableBuilder(
                valueListenable: _controller,
                builder: (context, state, child) {
                  if (state.torchState == TorchState.on) {
                    return const Icon(Icons.flash_on, color: Colors.amber);
                  }
                  return const Icon(Icons.flash_off, color: Colors.grey);
                },
              ),
              onPressed: () => _controller.toggleTorch(),
            ),
            IconButton(
              icon: const Icon(Icons.cameraswitch, color: Colors.white70),
              onPressed: () => _controller.switchCamera(),
            ),
          ],
        ],
      ),
      body: Stack(
        children: [
          // Live Camera viewfinder (or fallback placeholder on Web if no cam)
          if (!kIsWeb)
            MobileScanner(
              controller: _controller,
              onDetect: _onDetect,
            )
          else
            Container(
              color: Colors.black,
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.qr_code_2, size: 100, color: Colors.cyanAccent.withAlpha(100)),
                    const SizedBox(height: 12),
                    const Text(
                      "Web Mode QR Engine Ready",
                      style: TextStyle(color: Colors.cyanAccent, fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      "Point a camera or use 1-tap test buttons below",
                      style: TextStyle(color: Colors.white54, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ),

          // Cyber Neon Viewfinder Box
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.cyanAccent, width: 2.5),
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: Colors.cyanAccent.withAlpha(70),
                    spreadRadius: 3,
                    blurRadius: 12,
                  ),
                ],
              ),
            ),
          ),

          // Bottom Action Panel with 1-Tap QR Simulators
          Positioned(
            bottom: 20,
            left: 16,
            right: 16,
            child: Container(
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                color: const Color(0xFF1E1E2E).withAlpha(235),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.white.withAlpha(25)),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withAlpha(120),
                    blurRadius: 10,
                  ),
                ],
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text(
                    "⚡ 1-Tap QR Phishing Test Bench (Chrome / Desktop):",
                    style: TextStyle(color: Colors.white70, fontSize: 12, fontWeight: FontWeight.w600),
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => _testSampleQr("http://paypal-security-login.xyz/signin.html"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red.withAlpha(40),
                            foregroundColor: Colors.redAccent,
                            side: const BorderSide(color: Colors.redAccent),
                            padding: const EdgeInsets.symmetric(vertical: 10),
                          ),
                          icon: const Icon(Icons.warning, size: 16),
                          label: const Text("Test Phishing QR", style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                        ),
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => _testSampleQr("https://google.com"),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.green.withAlpha(40),
                            foregroundColor: Colors.greenAccent,
                            side: const BorderSide(color: Colors.greenAccent),
                            padding: const EdgeInsets.symmetric(vertical: 10),
                          ),
                          icon: const Icon(Icons.check_circle, size: 16),
                          label: const Text("Test Safe QR", style: TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
