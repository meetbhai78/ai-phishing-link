import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class InterceptedNotification {
  final String source;
  final String sender;
  final String text;
  final DateTime timestamp;

  InterceptedNotification({
    required this.source,
    required this.sender,
    required this.text,
    required this.timestamp,
  });
}

class NotificationService {
  static const MethodChannel _channel = MethodChannel('com.cybershield/notifications');

  static Function(InterceptedNotification)? onNotificationCallback;
  static Function(String)? onSharedTextCallback;

  static bool _initialized = false;

  /// Initializes the bridge between native Android NotificationListener and Flutter
  static void initialize({
    Function(InterceptedNotification)? onNotification,
    Function(String)? onSharedText,
  }) {
    onNotificationCallback = onNotification;
    onSharedTextCallback = onSharedText;

    if (_initialized) return;
    _initialized = true;

    _channel.setMethodCallHandler((call) async {
      try {
        if (call.method == 'onNotificationReceived') {
          final Map<dynamic, dynamic> args = call.arguments as Map<dynamic, dynamic>;
          final item = InterceptedNotification(
            source: args['source']?.toString() ?? 'whatsapp',
            sender: args['sender']?.toString() ?? 'Unknown Contact',
            text: args['text']?.toString() ?? '',
            timestamp: DateTime.now(),
          );
          if (kDebugMode) {
            print("Intercepted Notification: [${item.source}] ${item.sender}: ${item.text}");
          }
          onNotificationCallback?.call(item);
        } else if (call.method == 'onSharedTextReceived') {
          final String sharedText = call.arguments?.toString() ?? '';
          if (sharedText.isNotEmpty) {
            onSharedTextCallback?.call(sharedText);
          }
        }
      } catch (e) {
        if (kDebugMode) {
          print("Error handling method channel notification: $e");
        }
      }
    });

    // Check if app was opened with shared text from WhatsApp
    checkForSharedText();
  }

  /// Checks whether Android has granted Notification Access permission to CyberShield
  static Future<bool> isNotificationAccessGranted() async {
    if (kIsWeb) return false;
    try {
      final bool? isGranted = await _channel.invokeMethod<bool>('isNotificationAccessGranted');
      return isGranted ?? false;
    } catch (_) {
      return false;
    }
  }

  /// Opens Android OS Special App Access -> Device & app notifications screen
  static Future<bool> openNotificationSettings() async {
    if (kIsWeb) return false;
    try {
      final bool? result = await _channel.invokeMethod<bool>('openNotificationSettings');
      return result ?? false;
    } catch (_) {
      return false;
    }
  }

  /// Checks if there was shared text when app launched
  static Future<String?> checkForSharedText() async {
    if (kIsWeb) return null;
    try {
      final String? text = await _channel.invokeMethod<String>('getSharedText');
      if (text != null && text.isNotEmpty) {
        onSharedTextCallback?.call(text);
        return text;
      }
    } catch (_) {}
    return null;
  }
}
