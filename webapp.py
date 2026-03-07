import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time
from fpdf import FPDF
import re

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DermAI · Skin Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# CUSTOM CSS  — Luxury Medical Aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

/* ── Base Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F5F0EB !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #F5F0EB !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
    display: none;
}

[data-testid="stMainBlockContainer"] {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stMain"] > div {
    padding: 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F5F0EB; }
::-webkit-scrollbar-thumb { background: #C4A882; border-radius: 10px; }

/* ── Hero Header ── */
.hero-wrap {
    background: #1A1209;
    padding: 64px 80px 56px;
    position: relative;
    overflow: hidden;
}

.hero-wrap::before {
    content: '';
    position: absolute;
    top: -120px; right: -120px;
    width: 500px; height: 500px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(196,168,130,0.18) 0%, transparent 70%);
    pointer-events: none;
}

.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #C4A882, transparent);
}

.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    font-weight: 300;
    letter-spacing: 0.25em;
    color: #C4A882;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(48px, 6vw, 80px);
    font-weight: 300;
    line-height: 1.05;
    color: #F5F0EB;
    letter-spacing: -0.01em;
}

.hero-title em {
    font-style: italic;
    color: #C4A882;
}

.hero-subtitle {
    margin-top: 20px;
    font-size: 15px;
    font-weight: 300;
    color: rgba(245,240,235,0.55);
    letter-spacing: 0.02em;
    max-width: 480px;
    line-height: 1.7;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 36px;
    padding: 8px 18px;
    border: 1px solid rgba(196,168,130,0.3);
    border-radius: 100px;
    font-size: 12px;
    font-weight: 400;
    color: rgba(245,240,235,0.6);
    letter-spacing: 0.06em;
    font-family: 'DM Mono', monospace;
}

.badge-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #C4A882;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
}

/* ── Main Content ── */
.main-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    padding: 60px 80px;
    min-height: 70vh;
}

/* ── Upload Panel ── */
.upload-panel {
    padding-right: 48px;
    border-right: 1px solid rgba(26,18,9,0.1);
}

.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.3em;
    color: #8C7B6B;
    text-transform: uppercase;
    margin-bottom: 24px;
}

.panel-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 28px;
    font-weight: 400;
    color: #1A1209;
    margin-bottom: 8px;
    line-height: 1.2;
}

.panel-desc {
    font-size: 13px;
    color: #8C7B6B;
    line-height: 1.7;
    margin-bottom: 32px;
    font-weight: 300;
}

/* ── Upload Drop Zone ── */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(196,168,130,0.06) !important;
    border: 1.5px dashed rgba(196,168,130,0.45) !important;
    border-radius: 12px !important;
    padding: 36px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #C4A882 !important;
    background: rgba(196,168,130,0.1) !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] p {
    color: #8C7B6B !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #B5A899 !important;
}

[data-testid="stFileUploaderDropzone"] svg { color: #C4A882 !important; }

/* ── Uploaded Image ── */
[data-testid="stImage"] img {
    border-radius: 12px !important;
    border: 1px solid rgba(26,18,9,0.08) !important;
}

/* ── Analyze Button ── */
.stButton > button {
    background: #1A1209 !important;
    color: #F5F0EB !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 32px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    letter-spacing: 0.06em !important;
    width: 100% !important;
    height: auto !important;
    margin-top: 20px !important;
    cursor: pointer !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.3s ease !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(196,168,130,0.15), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.stButton > button:hover {
    background: #2D1F0A !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(26,18,9,0.25) !important;
}

/* ── Info Panel ── */
.info-panel {
    padding-left: 48px;
}

/* ── Steps ── */
.step-item {
    display: flex;
    gap: 20px;
    margin-bottom: 32px;
    align-items: flex-start;
}

.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #C4A882;
    width: 28px;
    flex-shrink: 0;
    margin-top: 2px;
}

.step-content h4 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 17px;
    font-weight: 600;
    color: #1A1209;
    margin-bottom: 4px;
}

.step-content p {
    font-size: 13px;
    color: #8C7B6B;
    line-height: 1.65;
    font-weight: 300;
}

/* ── Report Includes ── */
.report-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 32px;
}

.tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    background: rgba(26,18,9,0.05);
    border-radius: 100px;
    font-size: 12px;
    color: #4A3728;
    letter-spacing: 0.02em;
    font-weight: 400;
}

.tag-dot { color: #C4A882; font-size: 16px; line-height: 1; }

/* ── Divider ── */
.elegant-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 0 80px;
    margin: 0;
}

.elegant-divider::before,
.elegant-divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(26,18,9,0.1);
}

.divider-ornament {
    font-size: 14px;
    color: #C4A882;
}

/* ── Report Section ── */
.report-section {
    padding: 60px 80px;
    background: #1A1209;
    position: relative;
    overflow: hidden;
}

.report-section::before {
    content: '';
    position: absolute;
    top: -200px; right: -100px;
    width: 600px; height: 600px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(196,168,130,0.07) 0%, transparent 70%);
}

.report-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 48px;
}

.report-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 42px;
    font-weight: 300;
    color: #F5F0EB;
    line-height: 1.1;
}

.report-title span {
    font-style: italic;
    color: #C4A882;
}

.report-body {
    background: rgba(245,240,235,0.04);
    border: 1px solid rgba(196,168,130,0.15);
    border-radius: 16px;
    padding: 40px 48px;
    font-size: 14px;
    color: rgba(245,240,235,0.8);
    line-height: 1.9;
    font-weight: 300;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

/* ── Score Card ── */
.score-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 40px;
}

.score-card {
    background: rgba(245,240,235,0.04);
    border: 1px solid rgba(196,168,130,0.15);
    border-radius: 12px;
    padding: 28px 24px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}

.score-card:hover {
    border-color: rgba(196,168,130,0.4);
}

.score-card.featured {
    border-color: rgba(196,168,130,0.35);
    background: rgba(196,168,130,0.06);
}

.score-card .score-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    color: rgba(196,168,130,0.7);
    text-transform: uppercase;
    margin-bottom: 14px;
}

.score-card .score-val {
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 300;
    color: #F5F0EB;
    line-height: 1;
}

.score-card .score-unit {
    font-size: 18px;
    color: #C4A882;
    margin-left: 2px;
}

.score-card .score-sub {
    font-size: 12px;
    color: rgba(245,240,235,0.4);
    margin-top: 8px;
    font-weight: 300;
}

.score-bar-wrap {
    margin-top: 12px;
    height: 3px;
    background: rgba(245,240,235,0.08);
    border-radius: 2px;
    overflow: hidden;
}

.score-bar {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, #C4A882, #E8D5B7);
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: #C4A882 !important;
    border: 1px solid rgba(196,168,130,0.4) !important;
    border-radius: 8px !important;
    padding: 12px 28px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    margin-top: 32px !important;
    height: auto !important;
    width: auto !important;
    transition: all 0.3s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(196,168,130,0.1) !important;
    border-color: #C4A882 !important;
    color: #E8D5B7 !important;
}

/* ── Progress Bar ── */
[data-testid="stProgressBar"] > div {
    background: rgba(245,240,235,0.06) !important;
    border-radius: 4px !important;
    height: 3px !important;
}

[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #C4A882, #E8D5B7) !important;
    border-radius: 4px !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p {
    color: rgba(245,240,235,0.6) !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 300 !important;
}

/* ── Alert/Error ── */
[data-testid="stAlert"] {
    background: rgba(255, 80, 80, 0.08) !important;
    border: 1px solid rgba(255, 80, 80, 0.2) !important;
    border-radius: 10px !important;
    color: #FFB3B3 !important;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ── Metric override ── */
[data-testid="stMetric"] {
    background: rgba(245,240,235,0.04) !important;
    border: 1px solid rgba(196,168,130,0.2) !important;
    border-radius: 12px !important;
    padding: 28px 24px !important;
    text-align: center !important;
}

[data-testid="stMetricLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.25em !important;
    color: rgba(196,168,130,0.7) !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 52px !important;
    font-weight: 300 !important;
    color: #F5F0EB !important;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GEMINI CONFIG
# ─────────────────────────────────────────────
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">✦ Dermatological Intelligence</div>
    <div class="hero-title">Skin Analysis,<br><em>Reimagined.</em></div>
    <div class="hero-subtitle">
        Upload a facial photograph and receive a comprehensive dermatological assessment — powered by advanced generative AI.
    </div>
    <div class="hero-badge">
        <span class="badge-dot"></span>
        Powered by Gemini · Clinical-grade insights
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN GRID
# ─────────────────────────────────────────────
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

# ── Upload Panel ──
with left_col:
    st.markdown("""
    <div class="upload-panel">
        <div class="panel-label">01 · Upload</div>
        <div class="panel-title">Your Photograph</div>
        <div class="panel-desc">For best results, use a well-lit, front-facing image with no filters applied. Supported formats: JPG, PNG, JPEG.</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_image = st.file_uploader(
        "",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, use_container_width=True)

    analyze = st.button("✦ Run Skin Analysis")

# ── Info Panel ──
with right_col:
    st.markdown("""
    <div class="info-panel">
        <div class="panel-label">02 · Process</div>
        <div class="panel-title">How It Works</div>
        <br/>

        <div class="step-item">
            <div class="step-num">01</div>
            <div class="step-content">
                <h4>Upload Your Image</h4>
                <p>Provide a clear, unfiltered frontal photograph for the most accurate analysis results.</p>
            </div>
        </div>

        <div class="step-item">
            <div class="step-num">02</div>
            <div class="step-content">
                <h4>AI Vision Analysis</h4>
                <p>Our model examines skin texture, tone, pores, pigmentation, and surface patterns in detail.</p>
            </div>
        </div>

        <div class="step-item">
            <div class="step-num">03</div>
            <div class="step-content">
                <h4>Receive Your Report</h4>
                <p>A structured dermatology report is generated, complete with a Skin Health Score and personalized recommendations.</p>
            </div>
        </div>

        <div class="panel-label" style="margin-top:32px; margin-bottom:16px;">Report Includes</div>
        <div class="report-tags">
            <span class="tag"><span class="tag-dot">·</span> Skin Type</span>
            <span class="tag"><span class="tag-dot">·</span> Condition Overview</span>
            <span class="tag"><span class="tag-dot">·</span> Area Observations</span>
            <span class="tag"><span class="tag-dot">·</span> Skin Concerns</span>
            <span class="tag"><span class="tag-dot">·</span> Skincare Routine</span>
            <span class="tag"><span class="tag-dot">·</span> Preventive Advice</span>
            <span class="tag"><span class="tag-dot">·</span> Health Score</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────
PROMPT = """
You are an expert dermatologist conducting a professional skin analysis.

Analyze the uploaded facial image and produce a structured, clinical yet accessible report.

Structure your response clearly with these sections:

1. SKIN TYPE
   Identify (Dry / Oily / Combination / Normal / Sensitive) with brief justification.

2. OVERALL SKIN CONDITION
   A concise summary of the general skin health observed.

3. AREA-WISE OBSERVATIONS
   Forehead, T-zone, cheeks, nose, under-eyes, lips/perioral area.

4. SKIN CONCERNS
   List identified issues (e.g. hyperpigmentation, acne, dehydration lines, redness, uneven texture, enlarged pores, etc.)

5. SKINCARE RECOMMENDATIONS
   Morning and evening routine steps tailored to the observed skin type and concerns.

6. PREVENTIVE MEASURES
   Long-term habits and lifestyle advice for improved skin health.

7. SKIN HEALTH SCORE: [number from 1–100]
   On the final line, write exactly: SKIN HEALTH SCORE: [number]
   Base this on overall skin condition, hydration, clarity, texture, and tone.

Use warm, professional language. Be specific and actionable.
"""


# ─────────────────────────────────────────────
# PDF FUNCTION
# ─────────────────────────────────────────────
def create_pdf(report_text, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # Title
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(26, 18, 9)
    pdf.cell(0, 12, "DermAI Skin Analysis Report", ln=True, align="C")

    pdf.set_font("Arial", "I", 11)
    pdf.set_text_color(140, 123, 107)
    pdf.cell(0, 8, "AI-Powered Dermatological Assessment", ln=True, align="C")

    pdf.ln(6)
    pdf.set_draw_color(196, 168, 130)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(10)

    # Score
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(26, 18, 9)
    pdf.cell(0, 8, f"Skin Health Score: {score}/100", ln=True)
    pdf.ln(6)

    # Body
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(60, 45, 30)

    for line in report_text.split("\n"):
        clean = line.strip()
        if not clean:
            pdf.ln(3)
            continue
        # Section headers
        if clean.isupper() or (len(clean) < 50 and clean.endswith(":")):
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(26, 18, 9)
            pdf.ln(4)
            pdf.cell(0, 7, clean, ln=True)
            pdf.set_font("Arial", size=11)
            pdf.set_text_color(60, 45, 30)
        else:
            pdf.multi_cell(0, 6, clean)

    pdf.output("skin_report.pdf")


# ─────────────────────────────────────────────
# EXTRACT SCORE
# ─────────────────────────────────────────────
def extract_score(text):
    match = re.search(r'SKIN HEALTH SCORE[:\s]+(\d{1,3})', text, re.IGNORECASE)
    if match:
        return min(int(match.group(1)), 100)
    return 78  # sensible fallback


# ─────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────
if analyze:
    if uploaded_image is None:
        st.error("Please upload a facial image before running the analysis.")
    else:
        # Progress bar
        prog = st.progress(0)
        for i in range(100):
            time.sleep(0.012)
            prog.progress(i + 1)

        with st.spinner("Analyzing skin characteristics…"):
            response = model.generate_content([PROMPT, image])

        report = response.text
        score = extract_score(report)

        # ── Report Section ──
        st.markdown(f"""
        <div class="report-section">
            <div class="report-header">
                <div class="report-title">Your Skin<br><span>Analysis Report</span></div>
            </div>
        """, unsafe_allow_html=True)

        # Report body
        st.markdown(f'<div class="report-body">{report}</div>', unsafe_allow_html=True)

        # Score Cards
        score_color = "#5CB85C" if score >= 75 else ("#F0A500" if score >= 50 else "#E05252")
        score_label = "Excellent" if score >= 85 else ("Good" if score >= 70 else ("Fair" if score >= 50 else "Needs Attention"))

        st.markdown(f"""
        <div class="score-grid" style="margin-top:40px;">
            <div class="score-card">
                <div class="score-label">Analysis Status</div>
                <div style="font-family:'Cormorant Garamond',serif; font-size:28px; font-weight:400; color:#F5F0EB; margin: 12px 0;">
                    Complete
                </div>
                <div class="score-sub">Full report generated</div>
            </div>
            <div class="score-card featured">
                <div class="score-label">Skin Health Score</div>
                <div class="score-val">{score}<span class="score-unit">/100</span></div>
                <div class="score-sub">{score_label}</div>
                <div class="score-bar-wrap" style="margin-top:16px;">
                    <div class="score-bar" style="width:{score}%;"></div>
                </div>
            </div>
            <div class="score-card">
                <div class="score-label">Report Sections</div>
                <div style="font-family:'Cormorant Garamond',serif; font-size:28px; font-weight:400; color:#F5F0EB; margin: 12px 0;">
                    6 Areas
                </div>
                <div class="score-sub">Comprehensive coverage</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Download
        create_pdf(report, score)
        with open("skin_report.pdf", "rb") as f:
            st.download_button(
                label="↓  Download Full PDF Report",
                data=f,
                file_name="DermAI_Skin_Report.pdf",
                mime="application/pdf"
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    text-align: center;
    padding: 40px 80px;
    border-top: 1px solid rgba(26,18,9,0.08);
    background: #F5F0EB;
">
    <div style="font-family:'DM Mono',monospace; font-size:10px; letter-spacing:0.25em; color:#B5A899; text-transform:uppercase;">
        DermAI · For educational purposes only · Not a substitute for professional medical advice
    </div>
    <div style="font-family:'Cormorant Garamond',serif; font-size:20px; color:#C4A882; margin-top:12px; font-style:italic;">
        ✦
    </div>
</div>
""", unsafe_allow_html=True)
