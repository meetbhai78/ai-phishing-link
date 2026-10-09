import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ApiSettingsDialog extends StatefulWidget {
  final VoidCallback? onSettingsSaved;

  const ApiSettingsDialog({super.key, this.onSettingsSaved});

  static Future<void> show(BuildContext context, {VoidCallback? onSettingsSaved}) {
    return showDialog(
      context: context,
      builder: (context) => ApiSettingsDialog(onSettingsSaved: onSettingsSaved),
    );
  }

  @override
  State<ApiSettingsDialog> createState() => _ApiSettingsDialogState();
}

class _ApiSettingsDialogState extends State<ApiSettingsDialog> {
  late TextEditingController _controller;
  bool _isTesting = false;
  Map<String, dynamic>? _testResult;

  final List<Map<String, String>> _presets = [
    {
      "label": "Host PC Wi-Fi (Tablet)",
      "url": "http://10.177.208.94:8000/predict",
    },
    {
      "label": "Localhost (Web/Desktop)",
      "url": "http://127.0.0.1:8000/predict",
    },
    {
      "label": "Android Emulator",
      "url": "http://10.0.2.2:8000/predict",
    },
  ];

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: ApiService.baseUrl);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _runConnectionTest() async {
    setState(() {
      _isTesting = true;
      _testResult = null;
    });

    // Temporarily apply input URL to test it
    final originalUrl = ApiService.baseUrl;
    ApiService.setServerUrl(_controller.text);

    final res = await ApiService.testConnection();

    if (!mounted) return;

    setState(() {
      _isTesting = false;
      _testResult = res;
    });

    // Revert if failed so we don't break existing state until user clicks Save
    if (res['success'] != true) {
      ApiService.baseUrl = originalUrl;
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      backgroundColor: const Color(0xFF1E1E2E),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      title: const Row(
        children: [
          Icon(Icons.hub, color: Colors.cyanAccent),
          SizedBox(width: 10),
          Text(
            "Backend & MongoDB Link",
            style: TextStyle(color: Colors.cyanAccent, fontSize: 16, fontWeight: FontWeight.bold),
          ),
        ],
      ),
      content: SizedBox(
        width: 420,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Configure FastAPI & MongoDB Atlas connectivity for physical tablet/phone:",
                style: TextStyle(color: Colors.white70, fontSize: 12),
              ),
              const SizedBox(height: 12),
              const Text(
                "Quick Presets (1-Tap):",
                style: TextStyle(color: Colors.white54, fontSize: 11, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 6),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: _presets.map((preset) {
                  final isSelected = _controller.text == preset["url"];
                  return InkWell(
                    onTap: () {
                      setState(() {
                        _controller.text = preset["url"]!;
                        _testResult = null;
                      });
                    },
                    borderRadius: BorderRadius.circular(8),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                      decoration: BoxDecoration(
                        color: isSelected ? Colors.cyan.withAlpha(40) : Colors.white.withAlpha(12),
                        borderRadius: BorderRadius.circular(8),
                        border: Border.all(
                          color: isSelected ? Colors.cyanAccent : Colors.white24,
                        ),
                      ),
                      child: Text(
                        preset["label"]!,
                        style: TextStyle(
                          color: isSelected ? Colors.cyanAccent : Colors.white70,
                          fontSize: 11,
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                        ),
                      ),
                    ),
                  );
                }).toList(),
              ),
              const SizedBox(height: 14),
              TextField(
                controller: _controller,
                style: const TextStyle(color: Colors.white, fontFamily: 'monospace', fontSize: 12),
                decoration: InputDecoration(
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                  labelText: "FastAPI Endpoint",
                  labelStyle: const TextStyle(color: Colors.cyanAccent, fontSize: 12),
                  hintText: "http://<PC_IP>:8000/predict",
                  hintStyle: const TextStyle(color: Colors.white24),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.cyanAccent),
                  ),
                  filled: true,
                  fillColor: Colors.black.withAlpha(90),
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.clear, color: Colors.white30, size: 16),
                    onPressed: () => _controller.clear(),
                  ),
                ),
              ),
              const SizedBox(height: 12),
              // Live Test Connection button
              SizedBox(
                width: double.infinity,
                child: OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.cyanAccent,
                    side: const BorderSide(color: Colors.cyanAccent),
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
                  onPressed: _isTesting ? null : _runConnectionTest,
                  icon: _isTesting
                      ? const SizedBox(
                          width: 14,
                          height: 14,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.cyanAccent),
                        )
                      : const Icon(Icons.wifi_tethering, size: 18),
                  label: Text(
                    _isTesting ? "Testing Handshake..." : "Test Connection & MongoDB",
                    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                ),
              ),
              if (_testResult != null) ...[
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: _testResult!['success'] == true
                        ? Colors.green.withAlpha(35)
                        : Colors.red.withAlpha(35),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(
                      color: _testResult!['success'] == true
                          ? Colors.greenAccent.withAlpha(120)
                          : Colors.redAccent.withAlpha(120),
                    ),
                  ),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(
                        _testResult!['success'] == true
                            ? Icons.check_circle_outline
                            : Icons.error_outline,
                        color: _testResult!['success'] == true
                            ? Colors.greenAccent
                            : Colors.redAccent,
                        size: 18,
                      ),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _testResult!['message'] ?? "",
                          style: TextStyle(
                            color: _testResult!['success'] == true
                                ? Colors.greenAccent
                                : Colors.redAccent,
                            fontSize: 11,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.white.withAlpha(8),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "💡 Note for Tablet / Phone:",
                      style: TextStyle(color: Colors.white70, fontWeight: FontWeight.bold, fontSize: 11),
                    ),
                    SizedBox(height: 4),
                    Text(
                      "1. Connect Tablet & Laptop to the same Wi-Fi (or turn on Laptop Mobile Hotspot).\n2. If disconnected, CyberShield automatically uses local offline heuristics so the app never freezes.",
                      style: TextStyle(color: Colors.white54, fontSize: 10, height: 1.4),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text("Cancel", style: TextStyle(color: Colors.white54)),
        ),
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.cyanAccent,
            foregroundColor: Colors.black,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          ),
          onPressed: () {
            ApiService.setServerUrl(_controller.text);
            widget.onSettingsSaved?.call();
            Navigator.pop(context);
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text("API Endpoint saved: ${ApiService.baseUrl}"),
                backgroundColor: const Color(0xFF1E1E2E),
              ),
            );
          },
          child: const Text("Save & Apply", style: TextStyle(fontWeight: FontWeight.bold)),
        ),
      ],
    );
  }
}
