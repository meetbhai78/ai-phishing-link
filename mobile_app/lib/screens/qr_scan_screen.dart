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
                  return const Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      CircularProgressIndicator(color: Colors.cyan),
                      SizedBox(height: 16),
                      Text("Scanning QR Code URL with AI...", style: TextStyle(color: Colors.white70)),
                    ],
                  );
                }

                if (snapshot.hasError) {
                  return Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.error_outline, color: Colors.redAccent, size: 40),
                      const SizedBox(height: 10),
                      Text(
                        "Scanned URL:\n$scannedUrl",
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
                        Icon(isDanger ? Icons.warning : Icons.check_circle, color: color, size: 32),
                        const SizedBox(width: 10),
                        Text(
                          isDanger ? "DANGER: PHISHING QR CODE!" : "SAFE QR CODE",
                          style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 16),
                        ),
                      ],
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "QR URL: $scannedUrl",
                      style: const TextStyle(color: Colors.white70, fontSize: 11, fontFamily: 'monospace'),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      "Confidence: ${res.confidence}% | Risk Level: ${res.riskLevel}",
                      style: const TextStyle(color: Colors.white54, fontSize: 12),
                    ),
                    const SizedBox(height: 20),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.cyan),
                        onPressed: () {
                          Navigator.pop(context);
                          setState(() {
                            _isProcessing = false;
                          });
                        },
                        child: const Text("Scan Another QR Code", style: TextStyle(color: Colors.black)),
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
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F0C29),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: const Text("QR Code Phishing Scanner", style: TextStyle(color: Colors.cyan)),
        actions: [
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
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: _controller,
            onDetect: _onDetect,
          ),
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(color: Colors.cyan, width: 3),
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(
                    color: Colors.cyan.withOpacity(0.3),
                    spreadRadius: 4,
                    blurRadius: 10,
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            bottom: 40,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Text(
                "Align QR Code inside the box to scan for Phishing Threats",
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white70, fontSize: 13),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
