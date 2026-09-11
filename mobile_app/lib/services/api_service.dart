import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class PredictionResult {
  final String url;
  final bool isPhishing;
  final double confidence;
  final String riskLevel;
  final double hybridScore;
  final String threatCategory;
  final Map<String, dynamic> sslInfo;
  final Map<String, dynamic> contentAnalysis;
  final Map<String, dynamic> features;

  PredictionResult({
    required this.url,
    required this.isPhishing,
    required this.confidence,
    required this.riskLevel,
    required this.hybridScore,
    required this.threatCategory,
    required this.sslInfo,
    required this.contentAnalysis,
    required this.features,
  });

  factory PredictionResult.fromJson(Map<String, dynamic> json) {
    return PredictionResult(
      url: json['url'] ?? '',
      isPhishing: json['is_phishing'] ?? false,
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      riskLevel: json['risk_level'] ?? 'UNKNOWN',
      hybridScore: (json['hybrid_score'] as num?)?.toDouble() ?? 0.0,
      threatCategory: json['threat_category'] ?? 'Generic',
      sslInfo: json['ssl_info'] ?? {},
      contentAnalysis: json['content_analysis'] ?? {},
      features: json['features'] ?? {},
    );
  }
}

class ApiService {
  // Smart Default API endpoint:
  // Web Browser / Desktop -> http://127.0.0.1:8000/predict
  // Real Phone / Emulator -> http://10.82.57.94:8000/predict
  static String baseUrl = kIsWeb
      ? "http://127.0.0.1:8000/predict"
      : "http://10.82.57.94:8000/predict";

  static Future<PredictionResult> scanUrl(String url) async {
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'url': url, 'client_type': 'mobile_app'}),
    ).timeout(const Duration(seconds: 20));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return PredictionResult.fromJson(data);
    } else {
      throw Exception("Server Error: ${response.statusCode}");
    }
  }
}
