import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ThreatFeedScreen extends StatefulWidget {
  const ThreatFeedScreen({super.key});

  @override
  State<ThreatFeedScreen> createState() => _ThreatFeedScreenState();
}

class _ThreatFeedScreenState extends State<ThreatFeedScreen> {
  List<CommunityReport> _reports = [];
  Map<String, dynamic> _stats = {};
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final results = await Future.wait([
        ApiService.getCommunityReports(limit: 30),
        ApiService.getCommunityStats(),
      ]);
      setState(() {
        _reports = results[0] as List<CommunityReport>;
        _stats = results[1] as Map<String, dynamic>;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = "Could not connect to server.\nMake sure FastAPI is running.";
        _isLoading = false;
      });
    }
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
            Icon(Icons.radar, color: Color(0xFFA78BFA)),
            SizedBox(width: 8),
            Text(
              "Threat Feed",
              style: TextStyle(
                color: Color(0xFFA78BFA),
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            onPressed: _loadData,
            icon: const Icon(Icons.refresh, color: Colors.white54),
          ),
        ],
      ),
      body: _isLoading
          ? const Center(
              child: CircularProgressIndicator(color: Color(0xFFA78BFA)),
            )
          : _error != null
              ? _buildErrorView()
              : RefreshIndicator(
                  onRefresh: _loadData,
                  color: const Color(0xFFA78BFA),
                  child: ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      _buildStatsCard(),
                      const SizedBox(height: 16),
                      _buildReportsHeader(),
                      const SizedBox(height: 10),
                      if (_reports.isEmpty)
                        _buildEmptyReports()
                      else
                        ..._reports.map((r) => _buildReportCard(r)),
                    ],
                  ),
                ),
    );
  }

  Widget _buildErrorView() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.cloud_off, color: Colors.white.withAlpha(50), size: 64),
            const SizedBox(height: 16),
            Text(
              _error!,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white38, fontSize: 13),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              onPressed: _loadData,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF7C3AED),
                foregroundColor: Colors.white,
              ),
              icon: const Icon(Icons.refresh),
              label: const Text("Retry"),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatsCard() {
    final total = _stats['total_reports'] ?? 0;
    final phishing = _stats['phishing_reports'] ?? 0;
    final safe = _stats['safe_reports'] ?? 0;
    final unsure = _stats['unsure_reports'] ?? 0;

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            const Color(0xFF7C3AED).withAlpha(25),
            const Color(0xFF0D1B2A).withAlpha(200),
          ],
        ),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFF7C3AED).withAlpha(50)),
      ),
      child: Column(
        children: [
          const Row(
            children: [
              Icon(Icons.groups_outlined, color: Color(0xFFA78BFA), size: 20),
              SizedBox(width: 8),
              Text(
                "Community Intelligence",
                style: TextStyle(
                  color: Color(0xFFA78BFA),
                  fontWeight: FontWeight.bold,
                  fontSize: 14,
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              _buildStatItem("Total", total.toString(), Colors.cyanAccent),
              _buildStatItem("Phishing", phishing.toString(), Colors.redAccent),
              _buildStatItem("Safe", safe.toString(), Colors.greenAccent),
              _buildStatItem("Unsure", unsure.toString(), Colors.amberAccent),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, String value, Color color) {
    return Expanded(
      child: Column(
        children: [
          Text(
            value,
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.bold,
              fontSize: 22,
            ),
          ),
          const SizedBox(height: 2),
          Text(
            label,
            style: const TextStyle(
              color: Colors.white38,
              fontSize: 10,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReportsHeader() {
    return Row(
      children: [
        const Icon(Icons.list_alt, color: Colors.white38, size: 16),
        const SizedBox(width: 6),
        const Text(
          "Recent Community Reports",
          style: TextStyle(
            color: Colors.white54,
            fontSize: 13,
            fontWeight: FontWeight.w600,
          ),
        ),
        const Spacer(),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
          decoration: BoxDecoration(
            color: Colors.white.withAlpha(8),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Text(
            "${_reports.length} reports",
            style: const TextStyle(color: Colors.white30, fontSize: 10),
          ),
        ),
      ],
    );
  }

  Widget _buildEmptyReports() {
    return Container(
      padding: const EdgeInsets.all(32),
      child: const Column(
        children: [
          Icon(Icons.inbox_outlined, color: Colors.white24, size: 48),
          SizedBox(height: 12),
          Text(
            "No community reports yet.\nBe the first to report a suspicious link!",
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.white30, fontSize: 12),
          ),
        ],
      ),
    );
  }

  Widget _buildReportCard(CommunityReport report) {
    Color labelColor;
    IconData labelIcon;
    String labelText;

    switch (report.userReportedLabel) {
      case 'phishing':
        labelColor = Colors.redAccent;
        labelIcon = Icons.warning_amber_rounded;
        labelText = "PHISHING";
        break;
      case 'safe':
        labelColor = Colors.greenAccent;
        labelIcon = Icons.verified_outlined;
        labelText = "SAFE";
        break;
      default:
        labelColor = Colors.amberAccent;
        labelIcon = Icons.help_outline;
        labelText = "UNSURE";
    }

    // Format timestamp
    String timeAgo = _formatTimeAgo(report.timestamp);

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white.withAlpha(5),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: labelColor.withAlpha(25)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(labelIcon, color: labelColor, size: 18),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: labelColor.withAlpha(25),
                  borderRadius: BorderRadius.circular(6),
                  border: Border.all(color: labelColor.withAlpha(50)),
                ),
                child: Text(
                  labelText,
                  style: TextStyle(
                    color: labelColor,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: Colors.white.withAlpha(5),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      report.source == 'app' ? Icons.phone_android : Icons.extension,
                      color: Colors.white24,
                      size: 10,
                    ),
                    const SizedBox(width: 3),
                    Text(
                      report.source,
                      style: const TextStyle(
                        color: Colors.white30,
                        fontSize: 9,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 6),
              Text(
                timeAgo,
                style: const TextStyle(color: Colors.white24, fontSize: 10),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            report.url.length > 60
                ? "${report.url.substring(0, 60)}..."
                : report.url,
            style: const TextStyle(
              color: Colors.white60,
              fontSize: 11,
              fontFamily: 'monospace',
            ),
          ),
          if (report.autoScanRiskLevel.isNotEmpty &&
              report.autoScanRiskLevel != 'SCAN_FAILED') ...[
            const SizedBox(height: 6),
            Row(
              children: [
                const Icon(Icons.smart_toy_outlined, color: Colors.cyanAccent, size: 12),
                const SizedBox(width: 4),
                Text(
                  "AI: ${report.autoScanRiskLevel} (${report.autoScanConfidence}%)",
                  style: TextStyle(
                    color: report.autoScanPhishing
                        ? Colors.redAccent.withAlpha(180)
                        : Colors.greenAccent.withAlpha(180),
                    fontSize: 10,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
    );
  }

  String _formatTimeAgo(String isoStr) {
    try {
      final dt = DateTime.parse(isoStr);
      final now = DateTime.now().toUtc();
      final diff = now.difference(dt);

      if (diff.inSeconds < 60) return "just now";
      if (diff.inMinutes < 60) return "${diff.inMinutes}m ago";
      if (diff.inHours < 24) return "${diff.inHours}h ago";
      if (diff.inDays < 7) return "${diff.inDays}d ago";
      return "${(diff.inDays / 7).floor()}w ago";
    } catch (e) {
      return "";
    }
  }
}
