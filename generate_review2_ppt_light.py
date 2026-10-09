"""
CyberShield Review 2 Presentation Generator (Executive Light Theme)
Crafted to look human-designed, professional, clean, and university-grade.
Features:
- Pure white / executive light slate canvas with royal blue / deep navy accents
- High-contrast, clean human typography with presenter tags on every slide
- Embedded high-resolution screenshots with proportional aspect ratios & card frames
- 14 slides total (2 Heading + 11 Content + 1 Thank You) adhering strictly to requirements
"""

import os
import sys
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Professional Light Executive Color Palette
BG_WHITE = RGBColor(255, 255, 255)         # Pure White Canvas
BG_SLATE_TINT = RGBColor(248, 250, 252)    # F8FAFC - Soft canvas tint
CARD_BG = RGBColor(255, 255, 255)          # White Card
CARD_BG_TINT = RGBColor(241, 245, 249)     # F1F5F9 - Soft Card Tint
CARD_BORDER = RGBColor(203, 213, 225)      # CBD5E1 - Elegant Light Border
CARD_BORDER_ACCENT = RGBColor(37, 99, 235) # 2563EB - Royal Blue Accent Border

NAVY_HEADER = RGBColor(15, 23, 42)         # 0F172A - Deep Midnight Header Text
TEXT_DARK = RGBColor(30, 41, 59)           # 1E293B - High Contrast Body Text
TEXT_MUTED = RGBColor(100, 116, 139)       # 64748B - Secondary / Captions
ROYAL_BLUE = RGBColor(37, 99, 235)         # 2563EB - Primary Brand Accent
CYAN_ACCENT = RGBColor(2, 132, 199)        # 0284C7 - Secondary Tech Accent
EMERALD_SAFE = RGBColor(5, 150, 105)       # 059669 - Safe / Verified / Passed
CRIMSON_DANGER = RGBColor(220, 38, 38)     # DC2626 - Threat / Phishing Alert
AMBER_WARN = RGBColor(217, 119, 6)         # D97706 - Warning / Caution

IMG_DIR = r"D:\5th sem report\extracted_images"
CHARUSAT_LOGO = os.path.join(IMG_DIR, "Weekly Report - 12_img2.jpg")
DEPSTAR_LOGO = os.path.join(IMG_DIR, "Weekly Report - 12_img3.png")

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_light_background(slide):
        # Base white background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_SLATE_TINT
        bg.line.fill.background()

        # Top elegant accent bar (Royal Blue 4px strip)
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = ROYAL_BLUE
        top_bar.line.fill.background()
        return bg

    def add_header(slide, category_tag, slide_title, presenter=""):
        # Category Tag & Presenter chip
        tag_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.25), Inches(11.9), Inches(0.3))
        tf_c = tag_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_tag.upper()
        p_c.font.size = Pt(9.5)
        p_c.font.bold = True
        p_c.font.color.rgb = ROYAL_BLUE
        p_c.font.name = "Segoe UI"

        if presenter:
            p_pres = p_c.add_run()
            p_pres.text = f"   •   PRESENTER: {presenter.upper()}"
            p_pres.font.size = Pt(9.5)
            p_pres.font.bold = True
            p_pres.font.color.rgb = CYAN_ACCENT

        # Main Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(0.55), Inches(11.9), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = slide_title
        p_t.font.size = Pt(21)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY_HEADER
        p_t.font.name = "Segoe UI"

        # Subtle divider line
        divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.22), Inches(11.933), Inches(0.015))
        divider.fill.solid()
        divider.fill.fore_color.rgb = CARD_BORDER
        divider.line.fill.background()

    def add_footer(slide, slide_num, total_slides=14):
        # Bottom divider
        b_div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(7.0), Inches(11.933), Inches(0.012))
        b_div.fill.solid()
        b_div.fill.fore_color.rgb = RGBColor(226, 232, 240)
        b_div.line.fill.background()

        # Footer Left text
        footer_box = slide.shapes.add_textbox(Inches(0.7), Inches(7.08), Inches(10), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "CHARUSAT University  |  DEPSTAR  |  5th Semester B.Tech  |  Project Review 2  |  Project ID: PRJ_CE_5_2026_2"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED
        p.font.name = "Segoe UI"

        # Slide Number Badge (Right)
        num_box = slide.shapes.add_textbox(Inches(11.3), Inches(7.08), Inches(1.333), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{slide_num} / {total_slides}"
        p_n.font.size = Pt(9.5)
        p_n.font.bold = True
        p_n.font.color.rgb = ROYAL_BLUE
        p_n.font.name = "Segoe UI"

    def add_clean_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER, border_width=1):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
        return card

    def add_image_proportional(slide, image_path, left, top, max_width, max_height, caption=""):
        if not os.path.exists(image_path):
            return None
        with Image.open(image_path) as im:
            orig_w, orig_h = im.size
        aspect = orig_w / orig_h

        # Fit within max_width and max_height preserving aspect ratio
        calc_w = max_width
        calc_h = calc_w / aspect
        if calc_h > max_height:
            calc_h = max_height
            calc_w = calc_h * aspect

        # Center horizontally in the allocated box
        offset_x = (max_width - calc_w) / 2
        offset_y = (max_height - calc_h) / 2

        # Card container behind image
        add_clean_card(slide, left, top, max_width, max_height + (Inches(0.4) if caption else Inches(0)), bg_color=CARD_BG, border_color=CARD_BORDER)
        pic = slide.shapes.add_picture(image_path, left + offset_x, top + offset_y, width=calc_w, height=calc_h)

        if caption:
            cap_box = slide.shapes.add_textbox(left + Inches(0.1), top + max_height + Inches(0.05), max_width - Inches(0.2), Inches(0.3))
            tf = cap_box.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            p.text = caption
            p.font.size = Pt(8.5)
            p.font.bold = True
            p.font.color.rgb = TEXT_MUTED
            p.font.name = "Segoe UI"
        return pic

    # =========================================================================
    # SLIDE 1: [HEADING 1] TITLE SLIDE (Clean Light Academic Excellence)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_light_background(s1)

    # University Logos
    if os.path.exists(CHARUSAT_LOGO):
        s1.shapes.add_picture(CHARUSAT_LOGO, Inches(0.8), Inches(0.55), height=Inches(1.05))
    if os.path.exists(DEPSTAR_LOGO):
        s1.shapes.add_picture(DEPSTAR_LOGO, Inches(11.4), Inches(0.55), height=Inches(1.05))

    # University & Department Heading
    head_box = s1.shapes.add_textbox(Inches(2.1), Inches(0.55), Inches(9.133), Inches(0.95))
    tf_h = head_box.text_frame
    tf_h.word_wrap = True
    p1 = tf_h.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "CHAROTAR UNIVERSITY OF SCIENCE & TECHNOLOGY (CHARUSAT)"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = NAVY_HEADER
    p1.font.name = "Segoe UI"

    p2 = tf_h.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Devang Patel Institute of Advance Technology and Research (DEPSTAR)"
    p2.font.size = Pt(11.5)
    p2.font.bold = True
    p2.font.color.rgb = ROYAL_BLUE
    p2.font.name = "Segoe UI"

    p3 = tf_h.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "Department of Computer Engineering  •  5th Semester B.Tech Project"
    p3.font.size = Pt(10)
    p3.font.color.rgb = TEXT_MUTED
    p3.font.name = "Segoe UI"

    # Main Center Hero Card
    hero_card = add_clean_card(s1, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.95), bg_color=RGBColor(241, 245, 249), border_color=ROYAL_BLUE, border_width=1.5)
    
    tb_hero = s1.shapes.add_textbox(Inches(1.1), Inches(1.95), Inches(11.133), Inches(2.65))
    tf_hero = tb_hero.text_frame
    tf_hero.word_wrap = True
    
    p_tag = tf_hero.paragraphs[0]
    p_tag.alignment = PP_ALIGN.CENTER
    p_tag.text = "PROJECT REVIEW 2 PRESENTATION  •  v4.0 INTEGRATED REVIEW-2 SYSTEM"
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ROYAL_BLUE
    p_tag.font.name = "Segoe UI"

    p_t = tf_hero.add_paragraph()
    p_t.alignment = PP_ALIGN.CENTER
    p_t.text = "CyberShield: AI-Based Real-Time Phishing Detection\n& Threat Intelligence Ecosystem"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_HEADER
    p_t.font.name = "Segoe UI"

    p_sub = tf_hero.add_paragraph()
    p_sub.alignment = PP_ALIGN.CENTER
    p_sub.text = "Multi-Platform Defense: Chrome Manifest V3 • FastAPI AI Engine • Flutter Mobile • WhatsApp & SMS Guard • Cloud Telemetry"
    p_sub.font.size = Pt(11.5)
    p_sub.font.color.rgb = TEXT_DARK
    p_sub.font.name = "Segoe UI"

    # Bottom Two Info Cards: Team Members & Project Metadata
    card_team = add_clean_card(s1, Inches(0.8), Inches(4.95), Inches(5.75), Inches(1.85), bg_color=CARD_BG, border_color=CARD_BORDER)
    tb_team = s1.shapes.add_textbox(Inches(1.0), Inches(5.05), Inches(5.35), Inches(1.65))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    p = tf_team.paragraphs[0]
    p.text = "PROJECT TEAM (5 MEMBERS) & ROLES"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    members = [
        ("24DCE012", "Team Lead & FastAPI Backend Developer"),
        ("24DCE028", "Chrome Extension & Security Architecture"),
        ("24DCE017", "Machine Learning & Flutter Mobile Developer"),
        ("24DCE013", "Full-Stack Integration & Automated Testing"),
        ("24DCE038", "UI/UX, MessageShield & Documentation Lead")
    ]
    for sid, role in members:
        p = tf_team.add_paragraph()
        p.text = f"• {sid} : {role}"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_DARK

    card_meta = add_clean_card(s1, Inches(6.75), Inches(4.95), Inches(5.783), Inches(1.85), bg_color=CARD_BG, border_color=CARD_BORDER)
    tb_meta = s1.shapes.add_textbox(Inches(6.95), Inches(5.05), Inches(5.383), Inches(1.65))
    tf_meta = tb_meta.text_frame
    tf_meta.word_wrap = True
    p = tf_meta.paragraphs[0]
    p.text = "PROJECT IDENTIFIERS & DOMAIN"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE
    
    p = tf_meta.add_paragraph()
    p.text = "• Project ID: PRJ_CE_5_2026_2 (Proposal ID: 79)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_HEADER

    p = tf_meta.add_paragraph()
    p.text = "• Domain: Cyber Security, Applied Machine Learning, Web & Mobile Defense"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    p = tf_meta.add_paragraph()
    p.text = "• Tech Stack: Python 3.14, FastAPI, Scikit-Learn, Flutter, MongoDB Atlas"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_DARK

    p = tf_meta.add_paragraph()
    p.text = "• System Status: v4.0 Integrated & Review-2 Ready (22/22 Automated Tests Passed)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_SAFE

    add_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: [HEADING 2] AGENDA & REVIEW 1 VS REVIEW 2 ROADMAP
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_light_background(s2)
    add_header(s2, "EXECUTIVE ROADMAP & TRANSITION", "Project Review 2: Presentation Agenda & Team Distribution", "24DCE012")

    # 4 Module Pillar Cards (2x2 Grid)
    pillars = [
        ("MODULE 1: ARCHITECTURE & MULTI-PLATFORM ECOSYSTEM", 
         "• Presenters: 24DCE012 & 24DCE028\n• Covers: Problem context, end-to-end architecture (tested low-latency local API), Chrome V3 extension, FastAPI service, and dual database synchronization.", ROYAL_BLUE),
        ("MODULE 2: MACHINE LEARNING & 5-TIER HYBRID PIPELINE", 
         "• Presenters: 24DCE017 & 24DCE013\n• Covers: 30 URL lexical features, Shannon Information Entropy, Kaggle 100k balanced dataset, Scraper Robot, and native socket SSL certificate verification.", CYAN_ACCENT),
        ("MODULE 3: WHATSAPP/SMS AUTO-GUARD & DEEP TRUST ENGINE", 
         "• Presenters: 24DCE038 & 24DCE012\n• Covers: NEW Review 2 breakthroughs — WhatsApp & SMS message analysis, in-app Live Interception Simulator, sender authenticity heuristics, and the 0–100% Trust Meter.", AMBER_WARN),
        ("MODULE 4: EXPERIMENTAL RESULTS, DASHBOARD & LIVE DEMO", 
         "• Presenters: 24DCE013 & Team Lead\n• Covers: 94.63% baseline ML / 95.10% hybrid accuracy, 98.9% ROC-AUC, 22/22 Automated Tests Passed, Live Threat Dashboard, and Step-by-Step Viva Execution script.", EMERALD_SAFE)
    ]

    for i, (title, desc, col) in enumerate(pillars):
        col_idx = i % 2
        row_idx = i // 2
        left = Inches(0.7 + col_idx * 6.05)
        top = Inches(1.45 + row_idx * 1.55)
        add_clean_card(s2, left, top, Inches(5.85), Inches(1.4), border_color=col, border_width=1.2)
        tb = s2.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.45), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = col
        for line in desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

    # Bottom Progression Banner (Review 1 vs Review 2 Milestone Summary)
    add_clean_card(s2, Inches(0.7), Inches(4.75), Inches(11.9), Inches(2.05), bg_color=RGBColor(241, 245, 249), border_color=ROYAL_BLUE, border_width=1.5)
    tb_p = s2.shapes.add_textbox(Inches(0.95), Inches(4.88), Inches(11.4), Inches(1.8))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "MILESTONE EVOLUTION: REVIEW 1 (WEEKS 1–4)  VS  REVIEW 2 (WEEKS 5–12)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    milestones = [
        ("• Review 1 Deliverable (Initial Prototype):", "Evaluated basic Random Forest baseline (94.63%) on raw URLs, simple Chrome Manifest V3 popup, minimal /predict endpoint, and standalone SQLite logging."),
        ("• Review 2 Deliverable (Integrated Ecosystem):", "Engineered 5-Layer Hybrid Pipeline (Content Robot + Socket SSL Inspector), WhatsApp & SMS MessageShield & Live Interception Lab, Deep Trust Building Engine (0–100%), Threat Intelligence Web Console, MongoDB Atlas Cloud sync, and 22/22 Automated Tests Passed.")
    ]
    for h, b in milestones:
        p = tf_p.add_paragraph()
        p.text = f"{h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    add_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: [CONTENT 1] PROBLEM STATEMENT & REAL-WORLD THREAT EVOLUTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_light_background(s3)
    add_header(s3, "PROBLEM CONTEXT & MOTIVATION", "Problem Statement Evolution & Extended Threat Landscape", "24DCE012")

    # Left: The Escalating Threat Reality
    add_clean_card(s3, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=CRIMSON_DANGER)
    tb_l = s3.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "🚨  THE ESCALATING REAL-WORLD THREAT"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = CRIMSON_DANGER

    points_l = [
        ("Social Engineering Attack Vectors:", "Phishing remains a primary initial compromise vector. Modern attackers increasingly bypass email filters by delivering malicious lures directly through SMS and WhatsApp chats."),
        ("Failure of Reactive Blacklists:", "Static blacklist services (Google Safe Browsing, PhishTank) depend on human discovery and reporting. Zero-day phishing websites actively compromise users during the initial discovery window before listings update."),
        ("The Mobile Vulnerability Gap:", "Mobile messaging interfaces lack link-hover inspection tools. Smartphone users cannot easily examine underlying domain hierarchies before clicking shortened or obfuscated URLs."),
        ("Deceptive Obfuscation Techniques:", "Fraudsters exploit URL shorteners (bit.ly, tinyurl), deceptive subdomains (sbi-kyc-verify.top), and free short-lived SSL certs to mimic legitimate organizations."),
        ("High-Impact Targeted Scenarios:", "Attackers heavily impersonate banking KYC alerts (SBI, HDFC), urgent utility service disconnection warnings, and promotional lottery schemes.")
    ]
    for h, b in points_l:
        p = tf_l.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: CyberShield Review 2 Extended Solution & Stakeholders
    add_clean_card(s3, Inches(6.8), Inches(1.45), Inches(5.8), Inches(5.35), border_color=EMERALD_SAFE)
    tb_r = s3.shapes.add_textbox(Inches(7.05), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "💡  OUR EXTENDED REVIEW 2 SOLUTION & STAKEHOLDERS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_SAFE

    points_r = [
        ("Multi-Platform Defense Shield:", "Continuous protection across Browser Tabs (Chrome/Edge V3), Mobile Devices (Flutter QR scanner), and Messaging Feeds (WhatsApp & SMS MessageShield)."),
        ("Zero-Dependency Localized AI:", "Custom-trained Random Forest model running inside local FastAPI. Eliminates third-party API dependencies, token costs, user privacy risks, and external network latency."),
        ("Multi-Layer Hybrid Verification:", "Blends 30-feature lexical ML + Scraper Robot (checks login password fields & form targets) + Native socket SSL certificate inspection."),
        ("Deep Explainable Trust Engine:", "Computes a transparent 0–100% Trust Meter and provides clear evidence reasons so users understand why a link is dangerous or safe."),
        ("Protected Stakeholders:", "1. Web Surfers (Chrome extension)  •  2. Mobile Consumers (Flutter app & SMS shield)  •  3. Enterprise SOC Teams (Web Dashboard & Batch Scanner).")
    ]
    for h, b in points_r:
        p = tf_r.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    add_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: [CONTENT 2] SYSTEM ARCHITECTURE & MULTI-PLATFORM ECOSYSTEM
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_light_background(s4)
    add_header(s4, "SYSTEM ENGINEERING & INTEGRATION", "End-to-End System Architecture & Multi-Platform Data Flow", "24DCE028")

    # 4 Architecture Horizontal Layer Cards
    layers = [
        ("TIER 1: MULTI-PLATFORM CLIENT FRONTENDS", 
         "• Chrome / Edge Browser Extension (Manifest V3 Service Worker, activeTab DOM capture, instant danger badge & overlay)\n• Flutter Mobile Application (Cross-platform Dart UI, Camera QR Scanner, Threat Feed, and MessageShield Hub)\n• Live Threat Intelligence Web Console (HTML5/CSS3 glassmorphism dashboard, Chart.js telemetry graphs, CSV export)", ROYAL_BLUE),
        ("TIER 2: ASYNCHRONOUS FASTAPI PREDICTION ENGINE", 
         "• High-throughput Uvicorn ASGI Server exposing endpoints (/predict, /api/analyze-message, /api/batch-scan, /api/rules)\n• In-memory model caching, asynchronous request processing, and tested low-latency local API prediction pipeline", CYAN_ACCENT),
        ("TIER 3: 5-TIER HYBRID DETECTION PIPELINE", 
         "• Layer 1: Trusted Whitelist (.gov.in, .edu.in, verified banks)  |  Layer 2: Custom Admin Blacklist / Whitelist Policy\n• Layer 3: 30-Feature Random Forest ML  |  Layer 4: Real-time Content Robot  |  Layer 5: Native Socket SSL Inspector", AMBER_WARN),
        ("TIER 4: RESILIENT DUAL DATABASE & CLOUD TELEMETRY", 
         "• MongoDB Atlas Cloud: Centralized telemetry for scan logs, community reports, admin policies, and live analytics\n• Local SQLite Fallback: Automatic offline database synchronization ensuring continuous operation if cloud network is unavailable", EMERALD_SAFE)
    ]

    for i, (l_title, l_desc, col_accent) in enumerate(layers):
        top = Inches(1.45 + i * 1.35)
        add_clean_card(s4, Inches(0.7), top, Inches(11.9), Inches(1.22), border_color=col_accent, border_width=1.2)
        tb = s4.shapes.add_textbox(Inches(0.95), top + Inches(0.1), Inches(11.4), Inches(1.02))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = l_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = col_accent
        for line in l_desc.split('\n'):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_DARK

    add_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: [CONTENT 3] MACHINE LEARNING ENGINE & 30 URL FEATURES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_light_background(s5)
    add_header(s5, "ARTIFICIAL INTELLIGENCE & FEATURE ENGINEERING", "Machine Learning Pipeline & 30-Feature Vector Architecture", "24DCE017")

    # Left: Dataset & Shannon Information Entropy
    add_clean_card(s5, Inches(0.7), Inches(1.45), Inches(5.7), Inches(5.35), border_color=ROYAL_BLUE)
    tb_m = s5.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.2), Inches(5.0))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "🧠  MODEL TRAINING & SHANNON ENTROPY"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    specs = [
        ("Dataset Source:", "Kaggle malicious_phish.csv (651,191 raw labeled URLs)."),
        ("Balanced Training Set:", "100,000 URLs (50,000 Benign + 50,000 Phishing)."),
        ("Model Algorithm:", "Random Forest Classifier (300 Decision Trees, n_jobs=-1)."),
        ("Validation Strategy:", "80/20 Stratified Train-Test split + 5-Fold Stratified CV."),
        ("Shannon Information Entropy:", "Measures character randomness to detect Algorithmic Domain Generation (DGA):\n   H(X) = - Σ P(x) · log₂(P(x))\nHigh entropy (>4.2) strongly indicates obfuscated phishing hashes (e.g. x7k2m9p4.xyz)."),
        ("Feature Importance Ranking:", "Top discriminators: Shannon entropy, domain length, number of dots, brand name in subdomain, and suspicious TLD presence.")
    ]
    for h, b in specs:
        p = tf_m.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: 30 Feature Categories Table
    add_clean_card(s5, Inches(6.7), Inches(1.45), Inches(5.9), Inches(5.35), border_color=CYAN_ACCENT)
    tb_f = s5.shapes.add_textbox(Inches(6.95), Inches(1.6), Inches(5.4), Inches(5.0))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "🔬  30 EXTRACTED URL FEATURE DIMENSIONS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    feat_cats = [
        ("Length Metrics (4):", "url_length, domain_length, path_length, query_length"),
        ("Protocol Indicators (2):", "has_https, has_http"),
        ("Delimiter Counts (9):", "dots, hyphens, underscores, slashes, ?, =, &, #, %"),
        ("Numerical Ratios (2):", "num_digits, digit_to_letter_ratio"),
        ("Structural Anomalies (5):", "has_ip, has_at_symbol, has_double_slash, domain_has_hyphen, num_subdomains"),
        ("Deceptive Patterns (4):", "suspicious_word_count, http_in_path, brand_in_subdomain, is_shortened"),
        ("Statistical & TLD Flags (4):", "url_entropy, domain_entropy, suspicious_tld (.xyz, .top, .tk), num_dots_domain")
    ]
    for h, b in feat_cats:
        p = tf_f.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    add_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: [CONTENT 4] MULTI-LAYER HYBRID CASCADING PIPELINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_light_background(s6)
    add_header(s6, "DEFENSE-IN-DEPTH SECURITY ENGINE", "Multi-Layer Cascading Hybrid Detection Pipeline", "24DCE013")

    # Left: Explanation of 5 Cascading Tiers
    add_clean_card(s6, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=ROYAL_BLUE)
    tb_p = s6.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p = tf_p.paragraphs[0]
    p.text = "🛡️  THE 5 CASCADING DETECTION TIERS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    tiers = [
        ("Tier 1: Verified Whitelist Filter", "Verified official domains (.gov.in, .edu.in, trusted banking portals) treated as high-trust references to eliminate false positives on known services."),
        ("Tier 2: Custom Policy Manager", "Deterministic override supporting custom domain blacklists and whitelists configured by administrators."),
        ("Tier 3: Random Forest Machine Learning", "Evaluates 30-feature lexical vector, computing baseline statistical phishing risk."),
        ("Tier 4: Live Content Scraping Robot", "Fetches live webpage HTML: detects password inputs on unencrypted pages, external form action targets, and brand-name-to-domain mismatches."),
        ("Tier 5: Native Socket SSL Inspector", "Executes live Python SSL handshake: validates certificate issuer authority, validity period, and identifies self-signed or unencrypted login portals.")
    ]
    for h, b in tiers:
        p = tf_p.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Embedded SSL Inspector & Threat Categorization Screenshot
    ssl_img = os.path.join(IMG_DIR, "Weekly Report - 7_img5.png")
    add_image_proportional(s6, ssl_img, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.8), 
                           caption="Screenshot: SSL Certificate Telemetry & Automated Threat Categorization")

    add_footer(s6, 6)

    # =========================================================================
    # SLIDE 7: [CONTENT 5] NEW FEATURE: WHATSAPP & SMS NOTIFICATION AUTO-GUARD
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_light_background(s7)
    add_header(s7, "MAJOR REVIEW 2 INNOVATION", "WhatsApp Notification Link Auto-Guard & SMS Phishing Shield", "24DCE038")

    # Left: Explanation of MessageShield
    add_clean_card(s7, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=AMBER_WARN)
    tb_w = s7.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_w = tb_w.text_frame
    tf_w.word_wrap = True
    p = tf_w.paragraphs[0]
    p.text = "📱  MESSAGESHIELD: ADVANCED MOBILE PROTECTION"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = AMBER_WARN

    points_w = [
        ("The Mobile Threat Reality:", "Social-engineering attacks increasingly target messaging platforms (fake banking KYC suspension, electricity cutoffs, and reward voucher links)."),
        ("Android Integration Prepared:", "Android message-security integration prepared for SMS/notification monitoring, with an in-app Live Interception Simulator for testing and demonstration."),
        ("Intelligent Regex URL Extractor:", "Extracts standard URLs, shortened links (bit.ly, tinyurl), and suspicious TLDs (.xyz, .top) from lengthy conversational messages."),
        ("Interactive Live Interception Lab:", "Built-in simulation lab inside Flutter allowing 1-tap testing of realistic WhatsApp & SMS scams with floating heads-up alert cards."),
        ("Dedicated Backend API:", "Backed by POST /api/analyze-message in FastAPI, evaluating sender authenticity heuristics, urgency indicators, and destination risk.")
    ]
    for h, b in points_w:
        p = tf_w.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Embedded Mobile App MessageShield Screenshot
    app_img = os.path.join(IMG_DIR, "Weekly Report - 12_img5.png")
    add_image_proportional(s7, app_img, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.8),
                           caption="Screenshot: CyberShield MessageShield Flutter Hub & Live Interception Lab")

    add_footer(s7, 7)

    # =========================================================================
    # SLIDE 8: [CONTENT 6] NEW INNOVATION: DEEP USER TRUST BUILDING ENGINE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_light_background(s8)
    add_header(s8, "EXPLAINABLE AI & USER CONFIDENCE", "Deep User Trust Building Engine (0–100% Trust Meter)", "24DCE012")

    # Left: The 4 Evidence Layers of Trust
    add_clean_card(s8, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=EMERALD_SAFE)
    tb_t = s8.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p = tf_t.paragraphs[0]
    p.text = "🛡️  THE 4 EVIDENCE LAYERS OF USER TRUST"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_SAFE

    layers_t = [
        ("Layer 1: Sender Authenticity Heuristics", "Official-looking alphanumeric sender headers (e.g. AD-SBIINB, AD-GOOGLE) receive an authenticity bonus, while personal 10-digit mobile numbers sending banking/KYC links are flagged as highly suspicious."),
        ("Layer 2: Domain Impersonation Detection", "Compares claimed brand identity against actual destination (e.g. sbi-card-kyc-verify-alert.top is NOT official sbi.co.in)."),
        ("Layer 3: Live SSL & Certificate Authority", "Verifies active encryption certificates and trusted Certificate Authorities (DigiCert, Google Trust Services) vs missing or self-signed certificates."),
        ("Layer 4: Psychological Coercion Detector", "Flags high-pressure urgency triggers ('account suspended today', 'power cut tonight 9:30 PM', 'within 24 hours')."),
        ("Actionable User Safeguards:", "1-Tap 'Share Warning to WhatsApp' (copies formatted advisory to alert family/colleagues) and 'Report Threat to Community'.")
    ]
    for h, b in layers_t:
        p = tf_t.add_paragraph()
        p.text = f"• {h}: {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Embedded Trust Breakdown Screenshot
    trust_img = os.path.join(IMG_DIR, "Weekly Report - 12_img4.png")
    add_image_proportional(s8, trust_img, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.8),
                           caption="Screenshot: Trust Meter (5% Malicious Scam vs 99% Verified Safe) & Evidence Checklist")

    add_footer(s8, 8)

    # =========================================================================
    # SLIDE 9: [CONTENT 7] THREAT INTELLIGENCE WEB CONSOLE & DUAL DATABASE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_light_background(s9)
    add_header(s9, "ENTERPRISE TELEMETRY & CLOUD PERSISTENCE", "Threat Intelligence Web Console & Dual Database Architecture", "24DCE028")

    # Left: Web Console Features & Dual DB Sync
    add_clean_card(s9, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=ROYAL_BLUE)
    tb_d = s9.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_d = tb_d.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = "📊  REAL-TIME THREAT TELEMETRY CONSOLE"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    points_d = [
        ("Live Web Console (/dashboard):", "HTML5, CSS3 glassmorphism, and Chart.js telemetry dashboard providing organization-wide visibility across all connected endpoints."),
        ("Real-Time KPI Cards:", "Displays Total Scans, Active Threats Blocked, Safe Sites, and Client Device Distribution (Browser Extension vs Flutter Mobile App)."),
        ("Interactive Visual Analytics:", "Live line chart showing Daily Scan Activity Trends and Doughnut chart showing Threat Category breakdown."),
        ("Dual Database Synchronization:", "Primary: MongoDB Atlas Cloud Cluster storing scan_logs, custom_rules, and community_reports.\nLocal Fallback: SQLite sync guaranteeing 100% offline continuity."),
        ("Enterprise Audit Tools:", "1-Click CSV telemetry report export, active Whitelist/Blacklist policy manager, and on-demand manual verification scanner.")
    ]
    for h, b in points_d:
        p = tf_d.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Embedded Dashboard Screenshot
    dash_img = os.path.join(IMG_DIR, "Weekly Report - 6_img7.png")
    add_image_proportional(s9, dash_img, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.8),
                           caption="Screenshot: CyberShield Live Threat Intelligence Dashboard & Telemetry Graphs")

    add_footer(s9, 9)

    # =========================================================================
    # SLIDE 10: [CONTENT 8] COMMUNITY THREAT FEED & BATCH SCANNER
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_light_background(s10)
    add_header(s10, "CROWDSOURCED INTELLIGENCE & ENTERPRISE TOOLS", "Community Threat Feed & Enterprise Batch Scanner", "24DCE017")

    # Left: Community Phishing Intelligence & Batch Scanner
    add_clean_card(s10, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=CYAN_ACCENT)
    tb_c = s10.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "🌐  COMMUNITY AI & ENTERPRISE BATCH SCANNER"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT

    points_c = [
        ("Crowdsourced Phishing Reporting:", "Users report suspicious URLs with 5 optional AI training questions (channel source, personal data requested, brand impersonation, suspicion level)."),
        ("Training-Data Enrichment Pipeline:", "User-reported threats and community feedback are stored in MongoDB Atlas as candidate datasets for future model improvement cycles."),
        ("Enterprise Batch URL Scanner:", "Endpoint POST /api/batch-scan inspects up to 20 URLs concurrently using asynchronous multi-pipeline execution for security analysis."),
        ("Live Community Threat Feed:", "Accessible via both Web Console and Flutter Mobile App to view verified threats and community intelligence submissions in real-time.")
    ]
    for h, b in points_c:
        p = tf_c.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Embedded Batch Scanner / Metrics Screenshot
    batch_img = os.path.join(IMG_DIR, "Weekly Report - 9_img1.png")
    add_image_proportional(s10, batch_img, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.8),
                           caption="Screenshot: Enterprise Batch Scanner & Real-Time Confusion Matrix Metrics")

    add_footer(s10, 10)

    # =========================================================================
    # SLIDE 11: [CONTENT 9] EXPERIMENTAL RESULTS & 22 AUTOMATED TESTS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_light_background(s11)
    add_header(s11, "EXPERIMENTAL RESULTS & VERIFICATION", "Model Evaluation Metrics & 22 Automated Integration Tests", "24DCE013")

    # Left: Evaluation Metrics Table
    add_clean_card(s11, Inches(0.7), Inches(1.45), Inches(5.8), Inches(5.35), border_color=EMERALD_SAFE)
    tb_e = s11.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(5.3), Inches(5.0))
    tf_e = tb_e.text_frame
    tf_e.word_wrap = True
    p = tf_e.paragraphs[0]
    p.text = "🏆  MODEL PERFORMANCE (100K SAMPLES)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_SAFE

    metrics = [
        ("Model Accuracy:", "94.63% (Baseline Random Forest)  |  95.10% (Hybrid Calibrated)"),
        ("Precision:", "90.50% (High confidence on detected phishing)"),
        ("Recall (Sensitivity):", "96.30% (Prioritized to minimize dangerous false negatives)"),
        ("F1-Score:", "93.30% (Harmonic balance of precision & recall)"),
        ("ROC-AUC Score:", "98.90% (Near-perfect class separability)"),
        ("5-Fold Cross-Validation:", "Stratified CV confirms model stability (< ±1.5% variance)"),
        ("Inference Speed:", "< 45ms local ML inference  |  Tested low-latency local hybrid pipeline")
    ]
    for h, b in metrics:
        p = tf_e.add_paragraph()
        p.text = f"• {h} {b}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Right: Embedded Test Suite Passed Screenshot
    test_img = os.path.join(IMG_DIR, "Weekly Report - 11_img1.png")
    add_image_proportional(s11, test_img, Inches(6.8), Inches(1.45), Inches(5.8), Inches(4.8),
                           caption="Screenshot: Automated Regression Test Suite (backend/test_integration.py) — 22/22 Tests Passed")

    add_footer(s11, 11)

    # =========================================================================
    # SLIDE 12: [CONTENT 10] REVIEW 1 VS REVIEW 2 COMPARATIVE MATRIX
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_light_background(s12)
    add_header(s12, "PROGRESSION & MATURITY MATRIX", "Review 1 vs Review 2: Comprehensive Technical Advancements", "24DCE038")

    # Full Width Matrix Card
    add_clean_card(s12, Inches(0.7), Inches(1.45), Inches(11.9), Inches(5.35), border_color=ROYAL_BLUE)
    tb_m = s12.shapes.add_textbox(Inches(0.95), Inches(1.6), Inches(11.4), Inches(5.0))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "SIDE-BY-SIDE TECHNICAL PROGRESSION (WEEKS 1–4  VS  WEEKS 5–12)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    matrix_rows = [
        ("Detection Engine", "Single-tier Random Forest ML model evaluating URL lexical features only.", "5-Layer Cascading Hybrid Pipeline (ML + Content Robot + SSL Inspector + Custom Rules)."),
        ("Platform Coverage", "Chrome Manifest V3 extension & basic Flutter app structure.", "Full Multi-Platform Ecosystem: Chrome/Edge V3, Flutter Android + Web Testing with QR, Web Console, WhatsApp/SMS Guard."),
        ("Messaging Phishing", "Not supported. URL scanning only.", "WhatsApp & SMS MessageShield with in-app Live Interception Simulator & Trust Engine."),
        ("User Trust & Explainability", "Binary DANGER / SAFE badge with raw probability.", "Deep Trust Engine (0–100% Trust Meter) with 4-layer evidence breakdown & WhatsApp warning sharing."),
        ("Database & Telemetry", "Basic standalone SQLite logging.", "Dual Sync: MongoDB Atlas Cloud Cluster + Local SQLite fallback + Live Glassmorphism Dashboard."),
        ("Community Intelligence", "No reporting or feedback system.", "Community Threat Feed, Crowdsourced Q&A, and candidate data collection for future model improvement."),
        ("Testing & Verification", "Basic manual testing.", "22/22 Automated Integration & Regression Tests with 100% pass rate + Stratified 5-Fold CV.")
    ]

    for dim, r1, r2 in matrix_rows:
        p = tf_m.add_paragraph()
        p.text = f"• {dim}:"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = ROYAL_BLUE
        
        p_desc = tf_m.add_paragraph()
        p_desc.text = f"   - Review 1: {r1}\n   - Review 2: {r2}"
        p_desc.font.size = Pt(9)
        p_desc.font.color.rgb = TEXT_DARK

    add_footer(s12, 12)

    # =========================================================================
    # SLIDE 13: [CONTENT 11] LIVE DEMONSTRATION SCRIPT & VIVA FLOW
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_light_background(s13)
    add_header(s13, "PRACTICAL EVALUATION & LIVE DEMO", "Live Demonstration Architecture & Step-by-Step Viva Script", "24DCE012")

    # 6 Step Demo Cards (2x3 Grid)
    steps = [
        ("Step 1: Backend Startup & Swagger Docs", "Launch python run_server.py -> Verify Uvicorn server running at http://127.0.0.1:8000 -> Open /docs Swagger UI showing all endpoints.", ROYAL_BLUE),
        ("Step 2: Threat Intelligence Console", "Open http://127.0.0.1:8000/dashboard -> Demonstrate real-time KPI cards, Chart.js activity graph, and live telemetry log.", CYAN_ACCENT),
        ("Step 3: Chrome Extension URL Defense", "Browse to https://charusat.ac.in (Green SAFE badge verified). Browse to test phishing URL (Red DANGER overlay with 30-feature breakdown).", EMERALD_SAFE),
        ("Step 4: Mobile App & QR Code Scanner", "Open Flutter app -> Scan phishing_qr.png & safe_qr.png with camera -> Demonstrate instant real-time risk classification.", AMBER_WARN),
        ("Step 5: WhatsApp & SMS MessageShield", "Navigate to 'Msg Shield' tab -> Tap 'Simulate SBI KYC SMS' (5% Trust Score) -> Then simulate 'Google SMS' (99% Trust Score) with evidence breakdown.", CRIMSON_DANGER),
        ("Step 6: MongoDB Telemetry & Test Suite", "Verify MongoDB Atlas telemetry records across clients -> Run python backend/test_integration.py -> 22/22 Tests Passed successfully.", ROYAL_BLUE)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(steps):
        col_idx = i % 2
        row_idx = i // 2
        left = Inches(0.7 + col_idx * 6.05)
        top = Inches(1.45 + row_idx * 1.65)
        add_clean_card(s13, left, top, Inches(5.85), Inches(1.48), border_color=scolor, border_width=1.2)
        tb = s13.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.45), Inches(1.25))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = scolor
        p = tf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    add_footer(s13, 13)

    # =========================================================================
    # SLIDE 14: [THANK YOU] CONCLUSION, FUTURE ROADMAP & Q&A
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_light_background(s14)

    # Hero Center Thank You Card
    hero_card = add_clean_card(s14, Inches(0.8), Inches(0.7), Inches(11.733), Inches(6.0), bg_color=RGBColor(241, 245, 249), border_color=ROYAL_BLUE, border_width=1.5)
    
    tb_ty = s14.shapes.add_textbox(Inches(1.2), Inches(0.9), Inches(10.933), Inches(5.5))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p = tf_ty.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "🛡️  CyberShield"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "AI-Based Real-Time Phishing Detection & Threat Intelligence Ecosystem"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY_HEADER

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Successfully Engineered for 5th Semester B.Tech Project Review 2"
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXT_MUTED

    p = tf_ty.add_paragraph()
    p.text = "\n📌  KEY REVIEW 2 DELIVERABLES & FUTURE ENHANCEMENTS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    achieve = [
        ("• Integrated Multi-Platform Architecture:", "Manifest V3 Extension + FastAPI Microservice + Flutter Android & Web App + Cloud Dashboard."),
        ("• Breakthrough Innovations:", "WhatsApp & SMS MessageShield + Live Interception Simulator + Deep User Trust Building Engine (0-100%)."),
        ("• Automated System Validation:", "94.63% Baseline ML / 95.10% Hybrid Accuracy, 98.9% ROC-AUC, and 22 Out of 22 Automated Integration Tests Passed."),
        ("• Future Roadmap:", "On-Device TensorFlow Lite model for zero-connectivity scanning & Graph Neural Networks (GNN) for redirection chains.")
    ]
    for h, b in achieve:
        p = tf_ty.add_paragraph()
        p.text = f"{h} {b}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_DARK

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "\n❓  Thank You! Open for Questions & Evaluation Feedback"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ROYAL_BLUE

    p = tf_ty.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Devang Patel Institute of Advance Technology and Research (DEPSTAR) | CHARUSAT University"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED

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
    create_presentation()
