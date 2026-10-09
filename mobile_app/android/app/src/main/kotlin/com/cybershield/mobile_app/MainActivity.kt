package com.cybershield.mobile_app

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.os.Build
import android.provider.Settings
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.cybershield/notifications"
    private var methodChannel: MethodChannel? = null

    private val notificationReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            if (intent?.action == CyberShieldNotificationListener.ACTION_NOTIFICATION_RECEIVED) {
                val source = intent.getStringExtra("source") ?: "whatsapp"
                val sender = intent.getStringExtra("sender") ?: ""
                val text = intent.getStringExtra("text") ?: ""
                val data = mapOf(
                    "source" to source,
                    "sender" to sender,
                    "text" to text
                )
                runOnUiThread {
                    methodChannel?.invokeMethod("onNotificationReceived", data)
                }
            }
        }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        methodChannel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
        methodChannel?.setMethodCallHandler { call, result ->
            when (call.method) {
                "isNotificationAccessGranted" -> {
                    val flat = Settings.Secure.getString(contentResolver, "enabled_notification_listeners")
                    val isGranted = flat != null && flat.contains(packageName)
                    result.success(isGranted)
                }
                "openNotificationSettings" -> {
                    try {
                        val intent = Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)
                        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                        startActivity(intent)
                        result.success(true)
                    } catch (e: Exception) {
                        result.error("SETTINGS_ERROR", e.message, null)
                    }
                }
                "getLastCapturedNotification" -> {
                    result.success(CyberShieldNotificationListener.lastCapturedNotification)
                }
                "getSharedText" -> {
                    val sharedText = handleSendIntent(intent)
                    result.success(sharedText)
                }
                else -> result.notImplemented()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        val filter = IntentFilter(CyberShieldNotificationListener.ACTION_NOTIFICATION_RECEIVED)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            registerReceiver(notificationReceiver, filter, Context.RECEIVER_NOT_EXPORTED)
        } else {
            registerReceiver(notificationReceiver, filter)
        }
    }

    override fun onPause() {
        super.onPause()
        try {
            unregisterReceiver(notificationReceiver)
        } catch (_: Exception) {}
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        setIntent(intent)
        val text = handleSendIntent(intent)
        if (text != null) {
            methodChannel?.invokeMethod("onSharedTextReceived", text)
        }
    }

    private fun handleSendIntent(intent: Intent?): String? {
        if (intent != null && intent.action == Intent.ACTION_SEND && intent.type == "text/plain") {
            return intent.getStringExtra(Intent.EXTRA_TEXT)
        }
        return null
    }
}
