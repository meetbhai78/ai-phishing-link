import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/home_screen.dart';
import 'screens/message_shield_screen.dart';
import 'screens/qr_scan_screen.dart';
import 'screens/report_phishing_screen.dart';
import 'screens/threat_feed_screen.dart';

void main() {
  runApp(const CyberShieldApp());
}

class CyberShieldApp extends StatelessWidget {
  const CyberShieldApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CyberShield AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0F0C29),
        primaryColor: Colors.cyan,
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
        useMaterial3: true,
      ),
      home: const MainNavigationScreen(),
    );
  }
}

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = [
    const HomeScreen(),
    const MessageShieldScreen(),
    const QrScanScreen(),
    const ReportPhishingScreen(),
    const ThreatFeedScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: const Color(0xFF1E1E2E),
          border: Border(top: BorderSide(color: Colors.white.withAlpha(15))),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withAlpha(80),
              blurRadius: 10,
              offset: const Offset(0, -2),
            ),
          ],
        ),
        child: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (index) {
            setState(() {
              _currentIndex = index;
            });
          },
          backgroundColor: Colors.transparent,
          elevation: 0,
          type: BottomNavigationBarType.fixed,
          selectedItemColor: Colors.cyanAccent,
          unselectedItemColor: Colors.white30,
          selectedFontSize: 11,
          unselectedFontSize: 10,
          items: const [
            BottomNavigationBarItem(
              icon: Icon(Icons.link),
              activeIcon: Icon(Icons.link, size: 26),
              label: "URL Scan",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.shield_outlined),
              activeIcon: Icon(Icons.shield, size: 26),
              label: "Msg Shield",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.qr_code_scanner),
              activeIcon: Icon(Icons.qr_code_scanner, size: 26),
              label: "QR Scan",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.report_problem_outlined),
              activeIcon: Icon(Icons.report_problem, size: 26),
              label: "Report",
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.radar),
              activeIcon: Icon(Icons.radar, size: 26),
              label: "Threat Feed",
            ),
          ],
        ),
      ),
    );
  }
}

