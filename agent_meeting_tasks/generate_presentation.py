import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="TaskSync_AI_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_DARK = RGBColor(11, 15, 25)        # Slate 900
    CARD_BG = RGBColor(17, 24, 39)        # Slate 800
    TEXT_LIGHT = RGBColor(243, 244, 246)  # White / Slate 100
    TEXT_MUTED = RGBColor(156, 163, 175)  # Slate 400
    ACCENT_BLUE = RGBColor(59, 130, 246)  # Blue 500
    ACCENT_GREEN = RGBColor(16, 185, 129) # Emerald 500
    ACCENT_GOLD = RGBColor(245, 158, 11)  # Amber 500

    blank_layout = prs.slide_layouts[6]

    def set_slide_bg(slide, color=BG_DARK):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="TASKYSYNC AI • AGENTIC AI HACKATHON 2026"):
        # Category / Eyebrow
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(28)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # Glow card in center
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = ACCENT_BLUE
    card.line.width = Pt(1.5)

    tf1 = card.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    p0.text = "AGENTIC AI HACKATHON 2026 • POWERED BY ZIRO.DIGITAL"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE

    p1 = tf1.add_paragraph()
    p1.alignment = PP_ALIGN.CENTER
    p1.text = "TaskSync AI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Autonomous Meeting-to-Tasks Agent with Human Approval & Step 5 Independent Verification"
    p2.font.size = Pt(18)
    p2.font.color.rgb = TEXT_MUTED

    p3 = tf1.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "\n──────────────────────────────────────────"
    p3.font.size = Pt(12)
    p3.font.color.rgb = ACCENT_BLUE

    p4 = tf1.add_paragraph()
    p4.alignment = PP_ALIGN.CENTER
    p4.text = "Domain: Industry / Business & Productivity AI  |  Demo Target: Trello Free Board"
    p4.font.size = Pt(14)
    p4.font.bold = True
    p4.font.color.rgb = TEXT_LIGHT

    p5 = tf1.add_paragraph()
    p5.alignment = PP_ALIGN.CENTER
    p5.text = "Solo Builder: PIRUTHVI M K"
    p5.font.size = Pt(15)
    p5.font.bold = True
    p5.font.color.rgb = ACCENT_GREEN

    # ==========================================
    # SLIDE 2: THE PROBLEM
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "The Problem: Post-Meeting Action Item Decay")

    problems = [
        ("Action Items Get Lost", "Critical project tasks mentioned verbally in sprint calls are easily forgotten, lacking assigned owners and clear deadlines.", "📋"),
        ("Tentative Idea Pollution", "Speculative talk ('maybe next week we could consider X') frequently gets mistaken for committed sprint deliverables, creating clutter.", "💭"),
        ("Owner Ambiguity", "When two team members share the same first name (e.g. Priya Sharma & Priya Patel), standard automation blindly guesses or misassigns tasks.", "❓"),
        ("Duplicate Import Clutter", "Re-importing or reprocessing transcripts often spawns duplicate cards and creates confusion across boards without hash checks.", "🛡️")
    ]

    left_margin = Inches(0.8)
    col_width = Inches(2.7)
    gap = Inches(0.3)
    top_pos = Inches(2.0)
    card_height = Inches(4.7)

    for i, (title, desc, icon) in enumerate(problems):
        x = left_margin + i * (col_width + gap)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top_pos, col_width, card_height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = RGBColor(45, 55, 72)
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = f"{icon}\n\n{title}"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

        p_desc = tf.add_paragraph()
        p_desc.text = f"\n{desc}"
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 3: 5-STEP AGENTIC LIFECYCLE
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "Architecture: 5-Step Autonomous Agent Lifecycle")

    steps = [
        ("01", "Collect Details", "Ingests meeting transcript and team roster. Validates inputs & generates deterministic record IDs."),
        ("02", "Plan & Filter", "Differentiates confirmed decisions from tentative items. Detects name ambiguities & SHA-256 duplicates."),
        ("03", "Query Trello", "Live REST API connection queries target board ('My Trello board' -> 'This Week') and verifies state."),
        ("04", "Human Approval", "Safe execution gate: Shows proposed cards, owners, dates, and transcript evidence before pushing to Trello."),
        ("05", "Verify Card", "Step 5 Verification: Re-reads created cards via REST API to verify owner match, due date match, and quote link.")
    ]

    col_w = Inches(2.15)
    gap_w = Inches(0.24)
    for i, (num, name, details) in enumerate(steps):
        x = left_margin + i * (col_w + gap_w)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top_pos, col_w, card_height)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = ACCENT_GREEN if num == "05" else (ACCENT_GOLD if num == "04" else RGBColor(45, 55, 72))
        box.line.width = Pt(1.5)

        tf = box.text_frame
        tf.word_wrap = True

        p_num = tf.paragraphs[0]
        p_num.text = num
        p_num.font.size = Pt(28)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_GREEN if num == "05" else ACCENT_BLUE

        p_name = tf.add_paragraph()
        p_name.text = name
        p_name.font.size = Pt(15)
        p_name.font.bold = True
        p_name.font.color.rgb = TEXT_LIGHT

        p_det = tf.add_paragraph()
        p_det.text = f"\n{details}"
        p_det.font.size = Pt(11)
        p_det.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4: OFFICIAL TEST CASE RESULTS
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "Proof of Working Agent: 100% Score on Official Test Cases")

    test_cases = [
        ("TC1: Clear Decision with Owner & Date", "Extracted confirmed tasks for Rahul & Siddharth. Created card on Trello with due date after human approval. Step 5 independent audit re-read card and verified owner, date & transcript link.", "PASS ✅", ACCENT_GREEN),
        ("TC2: Two Team Members Named Priya", "Detected ambiguous owner ('Priya will redesign...'). Halted card creation and asked user: 'Did you mean Priya Sharma (Backend) or Priya Patel (UI/UX)?'. Created 0 cards until clarified.", "PASS ✅", ACCENT_GREEN),
        ("TC3: 'Maybe Next Week' (Tentative)", "Classified speculative language ('maybe next week', 'perhaps') as tentative discussion items. Created exactly 0 Trello cards as required by brief.", "PASS ✅", ACCENT_GREEN),
        ("TC4: Same Transcript Re-imported", "SHA-256 transcript fingerprint matched existing record RUN-TC1-001. Idempotent deduplication blocked all duplicate card creations.", "PASS ✅", ACCENT_GREEN)
    ]

    row_h = Inches(1.1)
    row_top = Inches(1.9)
    for i, (tc_title, tc_evidence, tc_status, status_col) in enumerate(test_cases):
        y = row_top + i * (row_h + Inches(0.18))
        card_row = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_margin, y, Inches(11.733), row_h)
        card_row.fill.solid()
        card_row.fill.fore_color.rgb = CARD_BG
        card_row.line.color.rgb = RGBColor(45, 55, 72)

        tf = card_row.text_frame
        tf.word_wrap = True

        p_title = tf.paragraphs[0]
        p_title.text = f"{tc_title}  ──  [{tc_status}]"
        p_title.font.size = Pt(14)
        p_title.font.bold = True
        p_title.font.color.rgb = status_col

        p_ev = tf.add_paragraph()
        p_ev.text = tc_evidence
        p_ev.font.size = Pt(11)
        p_ev.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5: TECH STACK & LIVE ARTIFACTS
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "Technical Implementation & Live Links")

    # Left Card: Tech Specs
    tech_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_margin, top_pos, Inches(5.6), card_height)
    tech_box.fill.solid()
    tech_box.fill.fore_color.rgb = CARD_BG
    tech_box.line.color.rgb = ACCENT_BLUE

    tf_tech = tech_box.text_frame
    tf_tech.word_wrap = True

    pt = tf_tech.paragraphs[0]
    pt.text = "⚙️ Core Technical Stack"
    pt.font.size = Pt(18)
    pt.font.bold = True
    pt.font.color.rgb = ACCENT_BLUE

    specs = [
        "Language & Framework: Python 3.14 + FastAPI Server",
        "Target Integration: Official Trello REST API (Free Board)",
        "Deduplication Engine: Cryptographic SHA-256 Hashing",
        "Decision Rules Engine: Regex NLP Action & Tentative Filter",
        "Audit Trail: SQLite3 Database with Execution Logging",
        "Frontend UI: Modern Dashboard with 1-Click Judge Scenarios"
    ]
    for s in specs:
        p_spec = tf_tech.add_paragraph()
        p_spec.text = f"• {s}"
        p_spec.font.size = Pt(12)
        p_spec.font.color.rgb = TEXT_LIGHT

    # Right Card: Live Links
    links_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), top_pos, Inches(5.6), card_height)
    links_box.fill.solid()
    links_box.fill.fore_color.rgb = CARD_BG
    links_box.line.color.rgb = ACCENT_GREEN

    tf_links = links_box.text_frame
    tf_links.word_wrap = True

    pl = tf_links.paragraphs[0]
    pl.text = "🔗 Live Verification & Links"
    pl.font.size = Pt(18)
    pl.font.bold = True
    pl.font.color.rgb = ACCENT_GREEN

    links_info = [
        "Live Trello Board (Public Demo Target):\nhttps://trello.com/b/6ad4e6a1950051dcf4dfb833",
        "Target List: 'This Week' with Synchronized Verified Cards",
        "GitHub Source Code:\nhttps://github.com/Piruthvi11/OmniTutor-AI/tree/main/agent_meeting_tasks",
        "Automated Test Suite Runner:\npython test_cases.py (100% Score Across 4/4 Scenarios)",
        "Built Solo by Piruthvi M K for Agentic AI Hackathon 2026"
    ]
    for li in links_info:
        p_link = tf_links.add_paragraph()
        p_link.text = f"✔ {li}"
        p_link.font.size = Pt(11)
        p_link.font.color.rgb = TEXT_LIGHT

    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_deck(r"c:\Users\pirut\OneDrive\Desktop\mini rpoj\HACKATON\agent_meeting_tasks\TaskSync_AI_Presentation.pptx")
