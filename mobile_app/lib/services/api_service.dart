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

/// Represents a single AI training question from the server
class CommunityQuestion {
  final String id;
  final String question;
  final List<String> options;
  final String type;

  CommunityQuestion({
    required this.id,
    required this.question,
    required this.options,
    required this.type,
  });

  factory CommunityQuestion.fromJson(Map<String, dynamic> json) {
    return CommunityQuestion(
      id: json['id'] ?? '',
      question: json['question'] ?? '',
      options: List<String>.from(json['options'] ?? []),
      type: json['type'] ?? 'single_choice',
    );
  }
}

/// Represents a community-reported threat
class CommunityReport {
  final String url;
  final String userReportedLabel;
  final bool autoScanPhishing;
  final double autoScanConfidence;
  final String autoScanRiskLevel;
  final String autoScanThreatCategory;
  final Map<String, dynamic> questionsAnswers;
  final String source;
  final String timestamp;
  final String status;

  CommunityReport({
    required this.url,
    required this.userReportedLabel,
    required this.autoScanPhishing,
    required this.autoScanConfidence,
    required this.autoScanRiskLevel,
    required this.autoScanThreatCategory,
    required this.questionsAnswers,
    required this.source,
    required this.timestamp,
    required this.status,
  });

  factory CommunityReport.fromJson(Map<String, dynamic> json) {
    return CommunityReport(
      url: json['url'] ?? '',
      userReportedLabel: json['user_reported_label'] ?? 'unsure',
      autoScanPhishing: json['auto_scan_phishing'] == true || json['auto_scan_phishing'] == 1,
      autoScanConfidence: (json['auto_scan_confidence'] as num?)?.toDouble() ?? 0.0,
      autoScanRiskLevel: json['auto_scan_risk_level'] ?? '',
      autoScanThreatCategory: json['auto_scan_threat_category'] ?? '',
      questionsAnswers: json['questions_answers'] is Map ? json['questions_answers'] : {},
      source: json['source'] ?? 'app',
      timestamp: json['timestamp'] ?? '',
      status: json['status'] ?? 'pending_review',
    );
  }
}

class ApiService {
  // Smart Default API endpoint:
  // Web Browser / Desktop -> http://127.0.0.1:8000
  // Real Phone / Emulator -> http://10.82.57.94:8000
  static String baseUrl = kIsWeb
      ? "http://127.0.0.1:8000/predict"
      : "http://10.82.57.94:8000/predict";

  static String get _apiBase {
    // Extract base URL without /predict
    return baseUrl.replaceAll('/predict', '');
  }

  /// Scans a URL using the hybrid AI engine
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

  /// Fetches AI training questions for community reports
  static Future<List<CommunityQuestion>> getCommunityQuestions() async {
    final response = await http.get(
      Uri.parse('$_apiBase/api/community-questions'),
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final questions = (data['questions'] as List)
          .map((q) => CommunityQuestion.fromJson(q))
          .toList();
      return questions;
    } else {
      throw Exception("Failed to load questions: ${response.statusCode}");
    }
  }

  /// Submits a community phishing report with optional answers
  static Future<Map<String, dynamic>> submitCommunityReport({
    required String url,
    required String userReportedLabel,
    Map<String, String> questionsAnswers = const {},
    String source = 'app',
  }) async {
    final response = await http.post(
      Uri.parse('$_apiBase/api/community-report'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'url': url,
        'user_reported_label': userReportedLabel,
        'questions_answers': questionsAnswers,
        'source': source,
      }),
    ).timeout(const Duration(seconds: 20));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Submit failed: ${response.statusCode}");
    }
  }

  /// Fetches recent community reports
  static Future<List<CommunityReport>> getCommunityReports({int limit = 30}) async {
    final response = await http.get(
      Uri.parse('$_apiBase/api/community-reports?limit=$limit'),
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      if (data is List) {
        return data.map((r) => CommunityReport.fromJson(r)).toList();
      }
      return [];
    } else {
      throw Exception("Failed to load reports: ${response.statusCode}");
    }
  }

  /// Fetches community contribution statistics
  static Future<Map<String, dynamic>> getCommunityStats() async {
    final response = await http.get(
      Uri.parse('$_apiBase/api/community-stats'),
    ).timeout(const Duration(seconds: 10));

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to load stats: ${response.statusCode}");
    }
  }

  /// Analyzes SMS or WhatsApp message text with link extraction and trust score
  static Future<MessageAnalysisResult> analyzeMessage({
    required String message,
    String source = 'whatsapp',
    String sender = '',
  }) async {
    final response = await http.post(
      Uri.parse('$_apiBase/api/analyze-message'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'message': message,
        'source': source,
        'sender': sender,
      }),
    ).timeout(const Duration(seconds: 25));

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return MessageAnalysisResult.fromJson(data);
    } else {
      throw Exception("Message analysis failed: ${response.statusCode}");
    }
  }
}

/// Represents individual URL analysis within a message
class UrlScanItem {
  final String url;
  final bool isPhishing;
  final String riskLevel;
  final double confidence;
  final double hybridScore;
  final String threatCategory;
  final bool sslValid;
  final String sslIssuer;
  final String? error;

  UrlScanItem({
    required this.url,
    required this.isPhishing,
    required this.riskLevel,
    required this.confidence,
    required this.hybridScore,
    required this.threatCategory,
    required this.sslValid,
    required this.sslIssuer,
    this.error,
  });

  factory UrlScanItem.fromJson(Map<String, dynamic> json) {
    return UrlScanItem(
      url: json['url'] ?? '',
      isPhishing: json['is_phishing'] ?? false,
      riskLevel: json['risk_level'] ?? 'UNKNOWN',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.0,
      hybridScore: (json['hybrid_score'] as num?)?.toDouble() ?? 0.0,
      threatCategory: json['threat_category'] ?? 'Generic',
      sslValid: json['ssl_valid'] ?? false,
      sslIssuer: json['ssl_issuer'] ?? 'Unknown',
      error: json['error'],
    );
  }
}

/// Represents full WhatsApp / SMS message analysis with trust building metrics
class MessageAnalysisResult {
  final String source;
  final String sender;
  final Map<String, dynamic> senderAnalysis;
  final List<String> extractedUrls;
  final List<UrlScanItem> urlScanResults;
  final List<String> urgencyFlags;
  final List<String> financialFlags;
  final String scamCategory;
  final double trustScore;
  final String verdict;
  final List<String> trustReasons;
  final List<String> riskReasons;
  final String recommendedAction;
  final String summaryAdvisory;

  MessageAnalysisResult({
    required this.source,
    required this.sender,
    required this.senderAnalysis,
    required this.extractedUrls,
    required this.urlScanResults,
    required this.urgencyFlags,
    required this.financialFlags,
    required this.scamCategory,
    required this.trustScore,
    required this.verdict,
    required this.trustReasons,
    required this.riskReasons,
    required this.recommendedAction,
    required this.summaryAdvisory,
  });

  factory MessageAnalysisResult.fromJson(Map<String, dynamic> json) {
    return MessageAnalysisResult(
      source: json['source'] ?? 'whatsapp',
      sender: json['sender'] ?? '',
      senderAnalysis: json['sender_analysis'] is Map ? Map<String, dynamic>.from(json['sender_analysis']) : {},
      extractedUrls: List<String>.from(json['extracted_urls'] ?? []),
      urlScanResults: (json['url_scan_results'] as List? ?? [])
          .map((item) => UrlScanItem.fromJson(item))
          .toList(),
      urgencyFlags: List<String>.from(json['urgency_flags'] ?? []),
      financialFlags: List<String>.from(json['financial_flags'] ?? []),
      scamCategory: json['scam_category'] ?? 'General',
      trustScore: (json['trust_score'] as num?)?.toDouble() ?? 0.0,
      verdict: json['verdict'] ?? 'UNKNOWN',
      trustReasons: List<String>.from(json['trust_reasons'] ?? []),
      riskReasons: List<String>.from(json['risk_reasons'] ?? []),
      recommendedAction: json['recommended_action'] ?? '',
      summaryAdvisory: json['summary_advisory'] ?? '',
    );
  }
}

