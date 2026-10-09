package com.cybershield.mobile_app

import android.app.Notification
import android.content.Intent
import android.os.Bundle
import android.service.notification.NotificationListenerService
import android.service.notification.StatusBarNotification
import android.util.Log

class CyberShieldNotificationListener : NotificationListenerService() {

    companion object {
        const val ACTION_NOTIFICATION_RECEIVED = "com.cybershield.NOTIFICATION_RECEIVED"
        var lastCapturedNotification: Map<String, String>? = null
    }

    override fun onNotificationPosted(sbn: StatusBarNotification?) {
        if (sbn == null) return

        val packageName = sbn.packageName ?: return
        val isWhatsApp = packageName == "com.whatsapp" || packageName == "com.whatsapp.w4b"
        val isSms = packageName == "com.google.android.apps.messaging" ||
                    packageName == "com.samsung.android.messaging" ||
                    packageName == "com.android.mms"
        val isTelegram = packageName == "org.telegram.messenger"

        if (!isWhatsApp && !isSms && !isTelegram) {
            return
        }

        val extras: Bundle = sbn.notification.extras ?: return
        val title = extras.getCharSequence(Notification.EXTRA_TITLE)?.toString() ?: ""
        val text = extras.getCharSequence(Notification.EXTRA_BIG_TEXT)?.toString()
            ?: extras.getCharSequence(Notification.EXTRA_TEXT)?.toString()
            ?: ""

        if (text.isBlank()) return

        val source = when {
            isWhatsApp -> "whatsapp"
            isSms -> "sms"
            isTelegram -> "telegram"
            else -> "message"
        }

        val data = mapOf(
            "source" to source,
            "sender" to title,
            "text" to text,
            "package" to packageName,
            "timestamp" to System.currentTimeMillis().toString()
        )

        lastCapturedNotification = data
        Log.d("CyberShieldGuard", "Notification intercepted from $packageName: $title -> $text")

        // Broadcast to MainActivity / Flutter
        val intent = Intent(ACTION_NOTIFICATION_RECEIVED).apply {
            setPackage(this@CyberShieldNotificationListener.packageName)
            putExtra("source", source)
            putExtra("sender", title)
            putExtra("text", text)
            putExtra("package", packageName)
        }
        sendBroadcast(intent)
    }

    override fun onNotificationRemoved(sbn: StatusBarNotification?) {}
}
