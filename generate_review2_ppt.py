"""
CyberShield Review 2 Presentation Generator
Builds a 14-slide (2 Heading + 11 Content + 1 Thank You) presentation
incorporating all Review 2 advancements, WhatsApp & SMS MessageShield,
Deep User Trust Engine, SSL Inspector, Dashboard, MongoDB Atlas, and 22 Automated Tests.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Color Palette (Dark Cybersecurity Theme matching Review 1 with modern polish)
BG_DARK = RGBColor(11, 15, 25)         # 0B0F19 - Main Background
PANEL_BG = RGBColor(21, 28, 44)        # 151C2C - Card / Panel Background
PANEL_BORDER = RGBColor(34, 211, 238)  # 22D3EE - Cyan Border
ACCENT_CYAN = RGBColor(34, 211, 238)   # 22D3EE - Primary Accent
ACCENT_GREEN = RGBColor(16, 185, 129)  # 10B981 - Safe / Success
ACCENT_RED = RGBColor(239, 68, 68)     # EF4444 - Threat / Danger
ACCENT_AMBER = RGBColor(245, 158, 11)  # F59E0B - Warning / Caution
TEXT_WHITE = RGBColor(248, 250, 252)   # F8FAFC - Main Headings
TEXT_MUTED = RGBColor(148, 163, 184)   # 94A3B8 - Body Text
TEXT_DIM = RGBColor(100, 116, 139)     # 64748B - Footers / Subtitles
CARD_HEADER_BG = RGBColor(28, 38, 60)  # 1C263C - Table/Card Header

IMG_DIR = r"D:\5th sem report\extracted_images"
CHARUSAT_LOGO = os.path.join(IMG_DIR, "Weekly Report - 12_img2.jpg")
DEPSTAR_LOGO = os.path.join(IMG_DIR, "Weekly Report - 12_img3.png")

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = BG_DARK
        bg_shape.line.fill.background()
        return bg_shape

    def add_header(slide, category_tag, slide_title):
        # Category Tag (Small Cyan Tracker)
        cat_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(10), Inches(0.3))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_tag.upper()
        p_c.font.size = Pt(9.5)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_CYAN
        p_c.font.name = "Segoe UI"

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.68), Inches(10.5), Inches(0.6))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = slide_title
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE
        p_t.font.name = "Segoe UI"

        # Accent Line under header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.32), Inches(12.133), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(30, 41, 59)
        line.line.fill.background()

    def add_footer(slide, slide_num, total_slides=14):
        # Footer text
        footer_box = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(10), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "CHARUSAT University  |  DEPSTAR  |  5th Semester B.Tech  |  Project Review 2  |  PRJ_CE_5_2026_2"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_DIM
        p.font.name = "Segoe UI"

        # Slide Number Badge
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.233), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{slide_num} / {total_slides}"
        p_n.font.size = Pt(9)
        p_n.font.bold = True
        p_n.font.color.rgb = ACCENT_CYAN
        p_n.font.name = "Segoe UI"

    def add_card(slide, left, top, width, height, border_color=None, bg_color=PANEL_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.color.rgb = RGBColor(30, 41, 59)
            card.line.width = Pt(0.8)
        return card

    # =========================================================================
    # SLIDE 1: [HEADING 1] TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Logos
    if os.path.exists(CHARUSAT_LOGO):
        s1.shapes.add_picture(CHARUSAT_LOGO, Inches(0.7), Inches(0.6), height=Inches(1.0))
    if os.path.exists(DEPSTAR_LOGO):
        s1.shapes.add_picture(DEPSTAR_LOGO, Inches(11.5), Inches(0.6), height=Inches(1.0))

    # University & Institute Header
    head_box = s1.shapes.add_textbox(Inches(2.0), Inches(0.6), Inches(9.333), Inches(0.9))
    tf_h = head_box.text_frame
    tf_h.word_wrap = True
    p1 = tf_h.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "CHAROTAR UNIVERSITY OF SCIENCE & TECHNOLOGY (CHARUSAT)"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.font.name = "Segoe UI"

    p2 = tf_h.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Devang Patel Institute of Advance Technology and Research (DEPSTAR) | Dept. of CE"
    p2.font.size = Pt(11)
    p2.font.color.rgb = ACCENT_CYAN
    p2.font.name = "Segoe UI"

    # Main Project Title Box (Center Hero)
    title_card = add_card(s1, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.0), border_color=ACCENT_CYAN)
    
    hero_box = s1.shapes.add_textbox(Inches(1.1), Inches(1.95), Inches(11.133), Inches(2.7))
    tf_hero = hero_box.text_frame
    tf_hero.word_wrap = True
    
    p_badge = tf_hero.paragraphs[0]
    p_badge.text = "PROJECT REVIEW 2 PRESENTATION  •  B.TECH 5TH SEMESTER"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_CYAN
    p_badge.font.name = "Segoe UI"

    p_mtitle = tf_hero.add_paragraph()
    p_mtitle.text = "CyberShield: AI-Based Real-Time Phishing Detection\n& Threat Intelligence System"
    p_mtitle.font.size = Pt(27)
    p_mtitle.font.bold = True
    p_mtitle.font.color.rgb = TEXT_WHITE
    p_mtitle.font.name = "Segoe UI"

    p_sub = tf_hero.add_paragraph()
    p_sub.text = "Multi-Platform Ecosystem: Chrome Extension • FastAPI AI Engine • Flutter Mobile • WhatsApp & SMS Guard • Cloud Telemetry"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_MUTED
    p_sub.font.name = "Segoe UI"

    # Bottom Metadata Cards (Team, Project ID, Domain)
    card_team = add_card(s1, Inches(0.8), Inches(5.0), Inches(5.7), Inches(1.75))
    tb_team = s1.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(5.3), Inches(1.55))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    p = tf_team.paragraphs[0]
    p.text = "PROJECT TEAM (5 MEMBERS)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    
    p = tf_team.add_paragraph()
    p.text = "Student IDs: 24DCE012, 24DCE013, 24DCE017, 24DCE028, 24DCE038"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    
    p = tf_team.add_paragraph()
    p.text = "Branch: Computer Engineering | Semester: 5th | Academic Year: 2026-27"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    card_meta = add_card(s1, Inches(6.8), Inches(5.0), Inches(5.733), Inches(1.75))
    tb_meta = s1.shapes.add_textbox(Inches(7.0), Inches(5.1), Inches(5.3), Inches(1.55))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True
    p = tf_meta.paragraphs[0]
    p.text = "PROJECT IDENTIFIERS & DOMAIN"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    
    p = tf_meta.add_paragraph()
    p.text = "Project ID: PRJ_CE_5_2026_2 (Proposal ID: 79) | Status: Production v4.0"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = tf_meta.add_paragraph()
    p.text = "Domain: Cybersecurity, Applied Machine Learning & Cloud Telemetry"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: [HEADING 2] AGENDA & REVIEW 1 VS REVIEW 2 PROGRESSION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "EXECUTIVE ROADMAP & TRANSITION", "Project Review 2: Presentation Agenda & Evolution")

    # 4 Pillar Cards
    pillars = [
        ("01. Architecture & Multi-Platform Defense", "System expansion across Chrome V3, FastAPI Backend, Flutter Mobile App, and live Telemetry Console.", ACCENT_CYAN),
        ("02. Machine Learning & 5-Layer Hybrid Pipeline", "30 URL lexical features, Shannon Entropy, Scraper Robot, Socket SSL handshake & Custom rules.", ACCENT_GREEN),
        ("03. WhatsApp & SMS Notification Auto-Guard", "NEW: Real-time link extraction, DLT Sender authenticity validation, and live Interception Lab.", ACCENT_AMBER),
        ("04. Deep User Trust Engine & 22 Automated Tests", "0-100% Trust Meter, 4-layer evidence breakdown, MongoDB Atlas telemetry & 100% test pass rate.", ACCENT_CYAN)
    ]

    for i, (title, desc, color) in enumerate(pillars):
        col = i % 2
        row = i // 2
        left = Inches(0.6 + col * 6.15)
        top = Inches(1.55 + row * 1.55)
        add_card(s2, left, top, Inches(5.95), Inches(1.35), border_color=color)
        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.55), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MUTED

    # Bottom Progression Banner (Review 1 vs Review 2 Milestone Summary)
    prog_card = add_card(s2, Inches(0.6), Inches(4.85), Inches(12.133), Inches(1.95), border_color=ACCENT_CYAN)
    tb_prog = s2.shapes.add_textbox(Inches(0.85), Inches(4.95), Inches(11.6), Inches(1.75))
    tf_prog = tb_prog.text_frame
    tf_prog.word_wrap = True
    p = tf_prog.paragraphs[0]
    p.text = "MILESTONE COMPARISON: REVIEW 1 (WEEKS 1–4)  VS  REVIEW 2 (WEEKS 5–12)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    bullets = [
        ("• Review 1 Focus (Initial Foundation):", "Basic Random Forest baseline (94.63%), Chrome Manifest V3 popup, simple /predict endpoint, local SQLite."),
        ("• Review 2 Focus (Production Multi-Platform):", "5-Layer Hybrid Pipeline (Content Robot + SSL Inspector), WhatsApp & SMS Notification Auto-Guard, Deep Trust Engine (0-100%), Glassmorphism Dashboard, MongoDB Atlas Cloud sync, and 22/22 Automated Tests Passed.")
    ]
    for b_title, b_desc in bullets:
        p = tf_prog.add_paragraph()
        p.text = f"{b_title} {b_desc}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: [CONTENT 1] PROBLEM EVOLUTION & REVIEW 2 EXTENDED SCOPE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "PROBLEM CONTEXT & STAKEHOLDER RELEVANCE", "Problem Statement Evolution & Extended Threat Landscape")

    # Left: The Escalating Problem & Industry Reality
    add_card(s3, Inches(0.6), Inches(1.55), Inches(5.9), Inches(5.2))
    tb_l = s3.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.4), Inches(4.9))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🚨  THE ESCALATING CYBER THREAT"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    points_l = [
        ("90%+ Social Engineering Vector:", "Phishing remains the #1 breach vector worldwide. Attackers trick users into revealing credentials, OTPs, and banking data."),
        ("Failure of Traditional Blacklists:", "Google Safe Browsing & PhishTank are purely reactive. Fresh zero-hour phishing domains stay active for 4-8 hours before being listed."),
        ("The Mobile Vulnerability Gap:", "Smartphones now account for 70%+ of messaging attacks. Users cannot hover to inspect links in WhatsApp chats, SMS, or QR codes."),
        ("Sophisticated Evasion Tactics:", "Cybercriminals use URL shorteners (bit.ly), free SSL certificates, and deceptive subdomains to bypass basic filters.")
    ]
    for h, b in points_l:
        p = tf_l.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    # Right: CyberShield Review 2 Solution & Stakeholders
    add_card(s3, Inches(6.8), Inches(1.55), Inches(5.933), Inches(5.2), border_color=ACCENT_GREEN)
    tb_r = s3.shapes.add_textbox(Inches(7.05), Inches(1.7), Inches(5.4), Inches(4.9))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "💡  OUR EXTENDED REVIEW 2 SOLUTION & STAKEHOLDERS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    points_r = [
        ("Multi-Platform Defense Ecosystem:", "Omnipresent protection covering Browser Tabs, Mobile QR Codes, and WhatsApp/SMS Message Notifications."),
        ("Zero-Dependency Localized AI:", "Custom-trained Random Forest model running locally in FastAPI. Zero recurring third-party API costs and complete data sovereignty."),
        ("Hybrid Verification Pipeline:", "Combines ML lexical scoring + Scraper robot (password field check) + Native SSL certificate handshake."),
        ("Key Stakeholders Protected:", "General internet users (Browser extension), Mobile banking users (Flutter app & SMS shield), Enterprise SOC analysts (Live Dashboard & Batch Scanner).")
    ]
    for h, b in points_r:
        p = tf_r.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: [CONTENT 2] SYSTEM ARCHITECTURE & MULTI-PLATFORM DATA FLOW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "SYSTEM ENGINEERING & INTEGRATION", "End-to-End System Architecture & Multi-Platform Data Flow")

    # 4 Architecture Horizontal Layer Cards
    layers = [
        ("LAYER 1: MULTI-PLATFORM CLIENT FRONTENDS", 
         "• Chrome / Edge Browser Extension (Manifest V3 Service Worker, activeTab monitoring, badge alerts)\n• Flutter Mobile Application (Cross-platform Dart UI, Camera QR Scanner, Message Shield Hub)\n• Live Threat Intelligence Web Console (HTML5/CSS3 glassmorphism dashboard, Chart.js analytics)", ACCENT_CYAN),
        ("LAYER 2: ASYNCHRONOUS FASTAPI PREDICTION ENGINE", 
         "• High-throughput Uvicorn ASGI Server exposing REST endpoints (/predict, /api/analyze-message, /api/batch-scan)\n• In-memory model caching, multi-threaded request handling, and sub-150ms end-to-end response latency", ACCENT_GREEN),
        ("LAYER 3: 5-TIER HYBRID DETECTION PIPELINE", 
         "• Tier 1: Trusted Whitelist (.gov.in, .edu.in, banking)  |  Tier 2: Admin Blacklist/Whitelist Policy\n• Tier 3: 30-Feature Random Forest ML  |  Tier 4: Live Content Robot  |  Tier 5: Socket SSL Inspector", ACCENT_AMBER),
        ("LAYER 4: RESILIENT DUAL DATABASE & TELEMETRY", 
         "• MongoDB Atlas Cloud: Real-time scan logs, community reports, admin policies, and threat statistics\n• Local SQLite Fallback: Automatic offline database synchronization ensuring zero downtime", ACCENT_CYAN)
    ]

    for i, (l_title, l_desc, col_accent) in enumerate(layers):
        top = Inches(1.55 + i * 1.32)
        add_card(s4, Inches(0.6), top, Inches(12.133), Inches(1.2), border_color=col_accent)
        tb = s4.shapes.add_textbox(Inches(0.85), top + Inches(0.1), Inches(11.6), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = l_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col_accent
        for line in l_desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_WHITE

    add_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: [CONTENT 3] MACHINE LEARNING ENGINE & 30 URL FEATURES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "ARTIFICIAL INTELLIGENCE & FEATURE ENGINEERING", "Machine Learning Pipeline & 30-Feature Vector Architecture")

    # Left: Dataset & Model Specifications
    add_card(s5, Inches(0.6), Inches(1.55), Inches(5.8), Inches(5.2))
    tb_m = s5.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.3), Inches(4.9))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "🧠  MODEL TRAINING & SHANNON ENTROPY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    specs = [
        ("Dataset Source:", "Kaggle malicious_phish.csv (651,191 raw URLs)."),
        ("Training Subset:", "100,000 balanced records (50,000 Benign + 50,000 Malicious)."),
        ("Model Algorithm:", "Random Forest Classifier (300 Decision Trees, n_jobs=-1)."),
        ("Validation Strategy:", "80/20 Stratified Train-Test split + 5-Fold Stratified CV."),
        ("Shannon Information Entropy:", "Calculates character randomness to detect Algorithmic Domain Generation (DGA):\n   H(X) = - Σ P(x) · log₂(P(x))\nHigh entropy (>4.2) strongly indicates obfuscated phishing hashes.")
    ]
    for h, b in specs:
        p = tf_m.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    # Right: 30 Extracted Feature Dimensions Table
    add_card(s5, Inches(6.7), Inches(1.55), Inches(6.033), Inches(5.2))
    tb_f = s5.shapes.add_textbox(Inches(6.95), Inches(1.7), Inches(5.5), Inches(4.9))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "🔬  30 EXTRACTED URL FEATURE DIMENSIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    feat_cats = [
        ("Length Metrics (4):", "url_length, domain_length, path_length, query_length"),
        ("Protocol Flags (2):", "has_https, has_http"),
        ("Delimiter Counts (9):", "dots, hyphens, underscores, slashes, ?, =, &, #, %"),
        ("Numerical Ratios (2):", "num_digits, digit_to_letter_ratio"),
        ("Structural Security (5):", "has_ip, has_at_symbol, has_double_slash, domain_has_hyphen, num_subdomains"),
        ("Deceptive Patterns (4):", "suspicious_word_count, http_in_path, brand_in_subdomain, is_shortened"),
        ("Statistical & TLD (4):", "url_entropy, domain_entropy, suspicious_tld (.xyz, .top), num_dots_domain")
    ]
    for h, b in feat_cats:
        p = tf_f.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: [CONTENT 4] MULTI-LAYER HYBRID CASCADING PIPELINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "DEFENSE-IN-DEPTH SECURITY ENGINE", "Multi-Layer Cascading Hybrid Detection Pipeline")

    # Left: Explanation of 5 Cascading Layers
    add_card(s6, Inches(0.6), Inches(1.55), Inches(6.2), Inches(5.2))
    tb_p = s6.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.7), Inches(4.9))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "🛡️  THE 5 CASCADING DETECTION TIERS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    tiers = [
        ("Tier 1: Verified Whitelist Filter", "Immediate 100% SAFE bypass for verified domains (.gov.in, .edu.in, charusat.ac.in, sbi.co.in) -> Zero false positives on government and banking sites."),
        ("Tier 2: Custom Policy Manager", "Deterministic override supporting custom domain blacklists and whitelists created by enterprise administrators."),
        ("Tier 3: Random Forest Machine Learning", "Evaluates 30-feature vector, computing baseline phishing probability score."),
        ("Tier 4: Live Content Scraping Robot", "Inspects live webpage HTML for credential harvesting: detects password inputs, external form action targets, and title-to-domain brand mismatches."),
        ("Tier 5: Native Socket SSL Inspector", "Executes live Python SSL handshake: checks certificate validity, issuer authority, and days until expiration. Self-signed or expired certs receive +25% threat penalty.")
    ]
    for h, b in tiers:
        p = tf_p.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Embedded Screenshot of SSL & Threat Categorization Evidence
    add_card(s6, Inches(7.1), Inches(1.55), Inches(5.633), Inches(5.2), border_color=ACCENT_CYAN)
    ssl_img = os.path.join(IMG_DIR, "Weekly Report - 7_img5.png")
    if os.path.exists(ssl_img):
        s6.shapes.add_picture(ssl_img, Inches(7.25), Inches(1.8), width=Inches(5.333))
    
    tb_c = s6.shapes.add_textbox(Inches(7.25), Inches(5.5), Inches(5.333), Inches(1.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "EVIDENCE: Real-time SSL certificate telemetry & automated threat classification (Banking, Social, E-Commerce, Lottery scams)."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: [CONTENT 5] NEW FEATURE: WHATSAPP & SMS NOTIFICATION AUTO-GUARD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "MAJOR REVIEW 2 INNOVATION", "WhatsApp Notification Link Auto-Guard & SMS Phishing Shield")

    # Left: Explanation of MessageShield Functionality
    add_card(s7, Inches(0.6), Inches(1.55), Inches(6.0), Inches(5.2), border_color=ACCENT_AMBER)
    tb_w = s7.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.5), Inches(4.9))
    tf_w = tb_w.text_frame
    tf_w.word_wrap = True
    p = tf_w.paragraphs[0]
    p.text = "📱  MESSAGESHIELD: HOW IT PROTECTS USERS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER

    points_w = [
        ("The Messaging Problem:", "Over 80% of Indian mobile fraud originates via WhatsApp messages and SMS (fake KYC updates, electricity cut warnings, lottery claims)."),
        ("Android Service Hooks:", "Configured with Android NotificationListenerService and SMS_RECEIVED BroadcastReceiver for background link interception."),
        ("Intelligent Link Extractor:", "Extracts standard URLs, shortened links (bit.ly, tinyurl), and bare domains from long, deceptive message bodies."),
        ("Live Interception Test Lab:", "Interactive in-app simulation engine testing realistic WhatsApp & SMS scams with floating heads-up alert banners."),
        ("FastAPI Endpoint:", "Backed by POST /api/analyze-message parsing message text, sender identity, urgency triggers, and computing trust metrics.")
    ]
    for h, b in points_w:
        p = tf_w.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Embedded Mobile App Screenshot
    add_card(s7, Inches(6.9), Inches(1.55), Inches(5.833), Inches(5.2))
    app_img = os.path.join(IMG_DIR, "Weekly Report - 12_img5.png")
    if os.path.exists(app_img):
        s7.shapes.add_picture(app_img, Inches(7.05), Inches(1.75), width=Inches(5.533))

    tb_app = s7.shapes.add_textbox(Inches(7.05), Inches(5.75), Inches(5.533), Inches(0.8))
    tf_app = tb_app.text_frame
    tf_app.word_wrap = True
    p = tf_app.paragraphs[0]
    p.text = "EVIDENCE: CyberShield MessageShield Flutter interface with Live Interception Lab, Auto-Guard toggles, and simulated alert banner."
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: [CONTENT 6] NEW INNOVATION: DEEP USER TRUST BUILDING ENGINE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "EXPLAINABLE AI & USER CONFIDENCE", "Deep User Trust Building Engine (0–100% Trust Meter)")

    # Left: The 4 Evidence Layers of Trust
    add_card(s8, Inches(0.6), Inches(1.55), Inches(6.2), Inches(5.2), border_color=ACCENT_GREEN)
    tb_t = s8.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.7), Inches(4.9))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "🛡️  THE 4 EVIDENCE LAYERS OF TRUST"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    layers_t = [
        ("Layer 1: Sender Authenticity Check", "TRAI DLT 6-character Alpha Headers (e.g. AD-SBIINB, AD-GOOGLE) verified vs Personal 10-digit mobile numbers sending bank/KYC links -> 99% Scam Flag!"),
        ("Layer 2: Domain Impersonation Detection", "Compares claimed brand against actual destination (e.g. sbi-card-kyc-verify-alert.top is NOT official sbi.co.in)."),
        ("Layer 3: Live SSL & Certificate Authority", "Verifies 256-bit encryption and trusted Certificate Authorities (DigiCert, Google Trust Services) vs missing/self-signed certs."),
        ("Layer 4: Psychological Coercion Detector", "Flags high-pressure urgency keywords ('account blocked', 'power cut tonight 9:30 PM', 'within 24 hours')."),
        ("Actionable User Safeguards:", "1-Tap 'Share Warning to WhatsApp' (copies pre-formatted alert) and 'Report Threat to Community Intel'.")
    ]
    for h, b in layers_t:
        p = tf_t.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Embedded Test Screenshot (Trust Breakdown Card)
    add_card(s8, Inches(7.1), Inches(1.55), Inches(5.633), Inches(5.2))
    trust_img = os.path.join(IMG_DIR, "Weekly Report - 12_img4.png")
    if os.path.exists(trust_img):
        s8.shapes.add_picture(trust_img, Inches(7.25), Inches(1.8), width=Inches(5.333))

    tb_ti = s8.shapes.add_textbox(Inches(7.25), Inches(5.5), Inches(5.333), Inches(1.0))
    tf_ti = tb_ti.text_frame
    tf_ti.word_wrap = True
    p = tf_ti.paragraphs[0]
    p.text = "EVIDENCE: Trust Score (5% Malicious Scam vs 99% Verified Safe) with full evidence checklist and actionable advisory."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: [CONTENT 7] THREAT INTELLIGENCE WEB CONSOLE & DUAL DATABASE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "ENTERPRISE TELEMETRY & CLOUD PERSISTENCE", "Threat Intelligence Web Console & Dual Database Architecture")

    # Left: Dashboard Architecture & Capabilities
    add_card(s9, Inches(0.6), Inches(1.55), Inches(5.6), Inches(5.2))
    tb_d = s9.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.1), Inches(4.9))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "📊  REAL-TIME THREAT TELEMETRY"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    points_d = [
        ("Live Web Console (/dashboard):", "HTML5, CSS3 glassmorphism, and Chart.js telemetry console providing organization-wide visibility."),
        ("Real-Time KPI Cards:", "Tracks Total Scans, Active Threats Blocked, Safe Sites, and Client Device Distribution (Extension vs Mobile App)."),
        ("Dual Database Synchronization:", "Primary: MongoDB Atlas Cloud storing scan_logs, custom_rules, and community_reports.\nLocal Fallback: SQLite sync ensuring uninterrupted operation when offline."),
        ("Interactive Management Tools:", "Active Whitelist/Blacklist policy manager, 1-Click CSV telemetry report export, and manual verification scanner.")
    ]
    for h, b in points_d:
        p = tf_d.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Embedded Dashboard Screenshot
    add_card(s9, Inches(6.5), Inches(1.55), Inches(6.233), Inches(5.2), border_color=ACCENT_CYAN)
    dash_img = os.path.join(IMG_DIR, "Weekly Report - 6_img7.png")
    if os.path.exists(dash_img):
        s9.shapes.add_picture(dash_img, Inches(6.65), Inches(1.8), width=Inches(5.933))

    tb_di = s9.shapes.add_textbox(Inches(6.65), Inches(5.5), Inches(5.933), Inches(1.0))
    tf_di = tb_di.text_frame
    tf_di.word_wrap = True
    p = tf_di.paragraphs[0]
    p.text = "EVIDENCE: CyberShield Threat Intelligence Dashboard displaying live telemetry graphs, activity trends, and recent multi-client scan logs."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s9, 9)

    # =========================================================================
    # SLIDE 10: [CONTENT 8] COMMUNITY THREAT FEED & BATCH SCANNER
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "CROWDSOURCED INTELLIGENCE & ENTERPRISE TOOLS", "Community Threat Feed & Enterprise Batch Scanner")

    # Left: Community Phishing Reports & Batch Scanner Specs
    add_card(s10, Inches(0.6), Inches(1.55), Inches(5.6), Inches(5.2))
    tb_c = s10.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.1), Inches(4.9))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "🌐  COMMUNITY AI & BATCH SCANNER"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    points_c = [
        ("Crowdsourced Phishing Reports:", "Users report suspicious URLs with 5 AI training questions (channel source, personal data requested, brand impersonation, suspicion level)."),
        ("Model Retraining Data Pipeline:", "User reports and false-positive feedback feed into MongoDB Atlas to continuously improve future model iterations."),
        ("Enterprise Batch Scanner API:", "Endpoint POST /api/batch-scan processes up to 20 URLs concurrently using asynchronous multi-pipeline execution."),
        ("Live Community Threat Feed:", "Accessible via both Web Console and Flutter Mobile App to view recently verified threats and community contributions.")
    ]
    for h, b in points_c:
        p = tf_c.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Embedded Batch Scanner / Metrics Screenshot
    add_card(s10, Inches(6.5), Inches(1.55), Inches(6.233), Inches(5.2), border_color=ACCENT_GREEN)
    batch_img = os.path.join(IMG_DIR, "Weekly Report - 9_img1.png")
    if os.path.exists(batch_img):
        s10.shapes.add_picture(batch_img, Inches(6.65), Inches(1.8), width=Inches(5.933))

    tb_bi = s10.shapes.add_textbox(Inches(6.65), Inches(5.5), Inches(5.933), Inches(1.0))
    tf_bi = tb_bi.text_frame
    tf_bi.word_wrap = True
    p = tf_bi.paragraphs[0]
    p.text = "EVIDENCE: Enterprise Batch URL Scanner interface and real-time confusion matrix metrics from the live dashboard."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s10, 10)

    # =========================================================================
    # SLIDE 11: [CONTENT 9] EXPERIMENTAL VALIDATION & 22 AUTOMATED TESTS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "EXPERIMENTAL RESULTS & VERIFICATION", "Model Evaluation Metrics & 22 Automated Integration Tests")

    # Left: Evaluation Metrics Table & Highlights
    add_card(s11, Inches(0.6), Inches(1.55), Inches(5.6), Inches(5.2))
    tb_e = s11.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(5.1), Inches(4.9))
    tf_e = tb_e.text_frame
    tf_e.word_wrap = True
    p = tf_e.paragraphs[0]
    p.text = "🏆  EVALUATION RESULTS (100K SAMPLES)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    metrics = [
        ("Model Accuracy:", "94.63% (Baseline)  |  95.10% (Hybrid Pipeline)"),
        ("Precision:", "90.50% (High confidence on detected phishing)"),
        ("Recall (Sensitivity):", "96.30% (Prioritized to catch dangerous threats)"),
        ("F1-Score:", "93.30% (Harmonic balance of precision & recall)"),
        ("ROC-AUC Score:", "98.90% (Near-perfect class separability)"),
        ("Cross-Validation:", "5-Fold Stratified CV confirms stability (< ±1.5%)"),
        ("Inference Latency:", "< 45ms ML inference  |  < 150ms full hybrid scan")
    ]
    for h, b in metrics:
        p = tf_e.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    # Right: Embedded Test Suite Passed Screenshot
    add_card(s11, Inches(6.5), Inches(1.55), Inches(6.233), Inches(5.2), border_color=ACCENT_CYAN)
    test_img = os.path.join(IMG_DIR, "Weekly Report - 11_img1.png")
    if os.path.exists(test_img):
        s11.shapes.add_picture(test_img, Inches(6.65), Inches(1.8), width=Inches(5.933))

    tb_ti2 = s11.shapes.add_textbox(Inches(6.65), Inches(5.5), Inches(5.933), Inches(1.0))
    tf_ti2 = tb_ti2.text_frame
    tf_ti2.word_wrap = True
    p = tf_ti2.paragraphs[0]
    p.text = "EVIDENCE: Automated Integration & Regression Test Suite (backend/test_integration.py) — 22 Out of 22 Tests Passed (100% Success Rate)."
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    add_footer(s11, 11)

    # =========================================================================
    # SLIDE 12: [CONTENT 10] REVIEW 1 VS REVIEW 2 COMPARATIVE MATRIX
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "PROGRESSION & MATURITY MATRIX", "Review 1 vs Review 2: Comprehensive Technical Advancements")

    # Full Width Matrix Card
    add_card(s12, Inches(0.6), Inches(1.55), Inches(12.133), Inches(5.2), border_color=ACCENT_CYAN)
    tb_m = s12.shapes.add_textbox(Inches(0.85), Inches(1.7), Inches(11.6), Inches(4.9))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "SIDE-BY-SIDE TECHNICAL PROGRESSION (WEEKS 1–4  VS  WEEKS 5–12)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    matrix_rows = [
        ("Dimension", "Review 1 Status (Weeks 1–4)", "Review 2 Status (Weeks 5–12 / Final)"),
        ("Detection Engine", "Single-tier Random Forest ML model on URL lexical features alone.", "5-Layer Cascading Hybrid Pipeline (ML + Content Robot + SSL Inspector + Custom Rules)."),
        ("Platform Coverage", "Chrome Manifest V3 extension & basic Flutter app structure.", "Full Multi-Platform Ecosystem: Chrome/Edge V3, Flutter Android/iOS, Web Console, WhatsApp/SMS Guard."),
        ("Messaging Phishing", "Not supported. URL scanning only.", "Advanced WhatsApp Notification Auto-Guard & SMS Link Shield with Live Interception Lab."),
        ("User Trust & Explainability", "Binary DANGER / SAFE badge with raw probability.", "Deep Trust Engine (0–100% Trust Meter) with 4-layer evidence breakdown & WhatsApp warning sharing."),
        ("Database & Telemetry", "Basic local SQLite logs.", "Dual Sync: MongoDB Atlas Cloud Cluster + Local SQLite fallback + Glassmorphism Dashboard."),
        ("Community Intelligence", "No reporting or feedback system.", "Community Threat Feed, Crowdsourced AI Training Q&A, and False-Positive Feedback API."),
        ("Testing & Verification", "Basic manual testing.", "22/22 Automated Integration & Regression Tests with 100% pass rate + Stratified 5-Fold CV.")
    ]

    for i, (dim, r1, r2) in enumerate(matrix_rows):
        p = tf_m.add_paragraph()
        if i == 0:
            p.text = f"{dim.upper():<22} | {r1.upper():<38} | {r2.upper()}"
            p.font.size = Pt(10)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
        else:
            p.text = f"• {dim}: {r2} (Review 1 was: {r1})"
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_WHITE

    add_footer(s12, 12)

    # =========================================================================
    # SLIDE 13: [CONTENT 11] LIVE DEMONSTRATION SCRIPT & VIVA FLOW
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "PRACTICAL EVALUATION & LIVE DEMO", "Live Demonstration Architecture & Step-by-Step Viva Script")

    # 6 Step Demo Cards
    steps = [
        ("Step 1: Backend Startup & Swagger Docs", "Launch run_server.py -> Verify Uvicorn server online at http://127.0.0.1:8000 -> Open /docs Swagger UI showing all endpoints.", ACCENT_CYAN),
        ("Step 2: Threat Intelligence Console", "Open http://127.0.0.1:8000/dashboard -> Demonstrate real-time KPI cards, Chart.js activity graph, and live telemetry log.", ACCENT_GREEN),
        ("Step 3: Chrome Extension Auto-Defense", "Browse to https://charusat.ac.in (Green SAFE badge verified). Browse to test phishing URL (Red DANGER overlay with 30-feature breakdown).", ACCENT_AMBER),
        ("Step 4: Mobile App & QR Code Scanner", "Open Flutter app -> Scan phishing_qr.png & safe_qr.png with camera -> Demonstrate instant real-time risk classification.", ACCENT_CYAN),
        ("Step 5: WhatsApp & SMS MessageShield", "Navigate to 'Msg Shield' tab -> Tap 'Simulate SBI KYC SMS' -> Demonstrate floating heads-up alert, 5% Trust Score, and evidence checklist.", ACCENT_RED),
        ("Step 6: Cloud Database Telemetry Sync", "Refresh MongoDB Atlas cloud console -> Verify live scan records logged across Chrome extension, mobile app, and message shield.", ACCENT_GREEN)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(steps):
        col = i % 2
        row = i // 2
        left = Inches(0.6 + col * 6.15)
        top = Inches(1.55 + row * 1.65)
        add_card(s13, left, top, Inches(5.95), Inches(1.45), border_color=scolor)
        tb = s13.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.55), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = scolor
        p = tf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s13, 13)

    # =========================================================================
    # SLIDE 14: [THANK YOU] CONCLUSION, FUTURE SCOPE & Q&A
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)

    # Hero Center Thank You Card
    hero_card = add_card(s14, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9), border_color=ACCENT_CYAN)
    
    tb_ty = s14.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.933), Inches(5.3))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p = tf_ty.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "🛡️  CyberShield"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "AI-Based Real-Time Phishing Detection & Threat Intelligence Ecosystem"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Successfully Engineered for 5th Semester B.Tech Project Review 2"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    p = tf_ty.add_paragraph()
    p.text = "\n📌  KEY REVIEW 2 ACHIEVEMENTS & FUTURE ROADMAP"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    achieve = [
        ("• Production Architecture Delivered:", "Manifest V3 Extension + FastAPI Microservice + Flutter Android App + Cloud Dashboard."),
        ("• Breakthrough Innovations:", "WhatsApp & SMS Notification Auto-Guard + Deep User Trust Building Engine (0-100%)."),
        ("• Enterprise Validation:", "94.63% Model Accuracy, 98.9% ROC-AUC, and 22 Out of 22 Automated Integration Tests Passed."),
        ("• Future Enhancements:", "On-Device TensorFlow Lite model for zero-connectivity scanning & Graph Neural Networks (GNN) for redirection chains.")
    ]
    for h, b in achieve:
        p = tf_ty.add_paragraph()
        p.text = f"{h} {b}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "\n❓  Thank You! Open for Questions & Evaluation Feedback"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Devang Patel Institute of Advance Technology and Research (DEPSTAR) | CHARUSAT University"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_DIM

    add_footer(s14, 14)

    # Save to both target directories
    out_dir_1 = r"D:\5th sem report"
    out_file_1 = os.path.join(out_dir_1, "CyberShield_Review2_Final.pptx")
    prs.save(out_file_1)
    print(f"[SUCCESS] Saved Review 2 Presentation to: {out_file_1}")

    out_dir_2 = r"D:\5TH SEM\extention"
    out_file_2 = os.path.join(out_dir_2, "CyberShield_Review2_Final.pptx")
    prs.save(out_file_2)
    print(f"[SUCCESS] Saved local copy to: {out_file_2}")

if __name__ == "__main__":
    create_deck()
