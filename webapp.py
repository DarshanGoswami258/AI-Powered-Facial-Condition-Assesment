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
# CSS — global only, no HTML injected inside columns
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F5F0EB !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"]      { display: none !important; }
[data-testid="stDecoration"]  { display: none !important; }
[data-testid="stToolbar"]     { display: none !important; }
#MainMenu, footer             { visibility: hidden; }
[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stMain"] > div:first-child { padding-top: 0 !important; }

/* hero */
.hero-wrap {
    background: #1A1209;
    padding: 56px 64px 48px;
    position: relative; overflow: hidden;
}
.hero-wrap::after {
    content:''; position:absolute; bottom:0; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,#C4A882,transparent);
}
.hero-eyebrow {
    font-family:'DM Mono',monospace; font-size:11px;
    letter-spacing:.25em; color:#C4A882; text-transform:uppercase; margin-bottom:14px;
}
.hero-title {
    font-family:'Cormorant Garamond',serif;
    font-size:clamp(44px,5.5vw,76px); font-weight:300; line-height:1.05; color:#F5F0EB;
}
.hero-title em { font-style:italic; color:#C4A882; }
.hero-sub {
    margin-top:18px; font-size:14px; font-weight:300;
    color:rgba(245,240,235,.55); line-height:1.75; max-width:460px;
}
.badge {
    display:inline-flex; align-items:center; gap:8px; margin-top:32px;
    padding:8px 18px; border:1px solid rgba(196,168,130,.3); border-radius:100px;
    font-family:'DM Mono',monospace; font-size:11px;
    color:rgba(245,240,235,.6); letter-spacing:.06em;
}
.dot {
    width:7px; height:7px; border-radius:50%; background:#C4A882;
    animation:pulse 2s infinite;
}
@keyframes pulse {
    0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(.85)}
}

/* section wrappers */
.section-wrap      { padding: 48px 64px; background:#F5F0EB; }
.section-wrap-dark { padding: 56px 64px; background:#1A1209; }

/* panel typography */
.plabel {
    font-family:'DM Mono',monospace; font-size:10px;
    letter-spacing:.28em; color:#8C7B6B; text-transform:uppercase; margin-bottom:6px;
}
.ptitle {
    font-family:'Cormorant Garamond',serif;
    font-size:26px; font-weight:400; color:#1A1209; margin-bottom:6px; line-height:1.2;
}
.pdesc { font-size:13px; color:#8C7B6B; line-height:1.75; font-weight:300; margin-bottom:28px; }

/* steps */
.step { display:flex; gap:18px; align-items:flex-start; margin-bottom:26px; }
.step-n { font-family:'DM Mono',monospace; font-size:11px; color:#C4A882; min-width:26px; margin-top:3px; }
.step h4 { font-family:'Cormorant Garamond',serif; font-size:17px; font-weight:600; color:#1A1209; margin-bottom:3px; }
.step p  { font-size:13px; color:#8C7B6B; line-height:1.65; font-weight:300; }

/* tags */
.tags { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
.tag  {
    display:inline-flex; align-items:center; gap:5px; padding:5px 13px;
    background:rgba(26,18,9,.05); border-radius:100px; font-size:12px; color:#4A3728;
}
.tag-dot { color:#C4A882; font-size:15px; line-height:1; }

/* column divider */
.col-div { width:1px; min-height:420px; background:rgba(26,18,9,.1); margin:auto; }

/* file uploader */
[data-testid="stFileUploaderDropzone"] {
    background:rgba(196,168,130,.05) !important;
    border:1.5px dashed rgba(196,168,130,.45) !important;
    border-radius:12px !important;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color:#C4A882 !important; background:rgba(196,168,130,.09) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color:#8C7B6B !important; font-family:'DM Sans',sans-serif !important;
}
[data-testid="stFileUploaderDropzone"] svg { color:#C4A882 !important; }
[data-testid="stImage"] img { border-radius:12px !important; border:1px solid rgba(26,18,9,.08) !important; }

/* analyze button */
.stButton > button {
    background:#1A1209 !important; color:#F5F0EB !important;
    border:none !important; border-radius:8px !important;
    padding:14px 32px !important; font-family:'DM Sans',sans-serif !important;
    font-size:14px !important; font-weight:400 !important; letter-spacing:.06em !important;
    width:100% !important; height:auto !important; margin-top:16px !important;
    transition:all .25s ease !important;
}
.stButton > button:hover {
    background:#2D1F0A !important; transform:translateY(-1px) !important;
    box-shadow:0 8px 24px rgba(26,18,9,.25) !important;
}

/* report */
.report-title {
    font-family:'Cormorant Garamond',serif; font-size:40px; font-weight:300;
    color:#F5F0EB; line-height:1.1; margin-bottom:32px;
}
.report-title span { font-style:italic; color:#C4A882; }
.report-body {
    background:rgba(245,240,235,.04); border:1px solid rgba(196,168,130,.15);
    border-radius:16px; padding:36px 44px; font-size:14px;
    color:rgba(245,240,235,.82); line-height:1.95; font-weight:300;
    white-space:pre-wrap; font-family:'DM Sans',sans-serif;
}

/* score cards */
.score-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-top:36px; }
.sc {
    background:rgba(245,240,235,.04); border:1px solid rgba(196,168,130,.15);
    border-radius:12px; padding:28px 22px; text-align:center; transition:border-color .3s;
}
.sc:hover { border-color:rgba(196,168,130,.4); }
.sc.feat  { border-color:rgba(196,168,130,.35); background:rgba(196,168,130,.06); }
.sc .sl   { font-family:'DM Mono',monospace; font-size:10px; letter-spacing:.25em; color:rgba(196,168,130,.7); text-transform:uppercase; margin-bottom:12px; }
.sc .sv   { font-family:'Cormorant Garamond',serif; font-size:50px; font-weight:300; color:#F5F0EB; line-height:1; }
.sc .su   { font-size:18px; color:#C4A882; }
.sc .ss   { font-size:12px; color:rgba(245,240,235,.4); margin-top:7px; font-weight:300; }
.bar-wrap { margin-top:12px; height:3px; background:rgba(245,240,235,.08); border-radius:2px; overflow:hidden; }
.bar      { height:100%; border-radius:2px; background:linear-gradient(90deg,#C4A882,#E8D5B7); }

/* download button */
[data-testid="stDownloadButton"] > button {
    background:transparent !important; color:#C4A882 !important;
    border:1px solid rgba(196,168,130,.4) !important; border-radius:8px !important;
    padding:12px 28px !important; font-family:'DM Mono',monospace !important;
    font-size:11px !important; letter-spacing:.15em !important;
    text-transform:uppercase !important; margin-top:28px !important;
    height:auto !important; width:auto !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background:rgba(196,168,130,.1) !important; border-color:#C4A882 !important;
}

/* progress */
[data-testid="stProgressBar"] > div { background:rgba(26,18,9,.08) !important; border-radius:4px !important; height:3px !important; }
[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#C4A882,#E8D5B7) !important; border-radius:4px !important; }

/* spinner */
[data-testid="stSpinner"] p { color:rgba(245,240,235,.6) !important; font-size:13px !important; font-weight:300 !important; }

/* footer */
.footer { text-align:center; padding:36px 64px; border-top:1px solid rgba(26,18,9,.08); background:#F5F0EB; }
.footer p { font-family:'DM Mono',monospace; font-size:10px; letter-spacing:.22em; color:#B5A899; text-transform:uppercase; }
.footer .orn { font-family:'Cormorant Garamond',serif; font-size:20px; color:#C4A882; margin-top:10px; font-style:italic; }

::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#F5F0EB; }
::-webkit-scrollbar-thumb { background:#C4A882; border-radius:10px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GEMINI CONFIG
# ─────────────────────────────────────────────
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# ─────────────────────────────────────────────
# HERO  (safe — outside columns)
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">✦ Dermatological Intelligence</div>
    <div class="hero-title">Skin Analysis,&nbsp;<em>Reimagined.</em></div>
    <div class="hero-sub">
        Upload a facial photograph and receive a comprehensive dermatological
        assessment — powered by advanced generative AI.
    </div>
    <div class="badge">
        <span class="dot"></span>
        Powered by Gemini &nbsp;·&nbsp; Clinical-grade insights
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN COLUMNS
# The key fix: HTML inside columns is limited to
# SIMPLE one-element blocks (no nested divs with
# child elements that Streamlit might escape).
# All multi-element HTML lives OUTSIDE columns.
# ─────────────────────────────────────────────
st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([10, 1, 10])

with col_left:
    st.markdown('<p class="plabel">01 · Upload</p>', unsafe_allow_html=True)
    st.markdown('<p class="ptitle">Your Photograph</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="pdesc">Use a well-lit, front-facing image with no filters applied. '
        'Supported formats: JPG, PNG, JPEG.</p>',
        unsafe_allow_html=True
    )
    uploaded_image = st.file_uploader(
        "Drop your image here",
        type=["jpg", "png", "jpeg"],
        label_visibility="collapsed"
    )
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, use_container_width=True)

    analyze = st.button("✦  Run Skin Analysis")

with col_mid:
    st.markdown('<div class="col-div"></div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<p class="plabel">02 · Process</p>', unsafe_allow_html=True)
    st.markdown('<p class="ptitle">How It Works</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="step">
        <div class="step-n">01</div>
        <div><h4>Upload Your Image</h4>
        <p>Provide a clear, unfiltered frontal photograph for the most accurate analysis.</p></div>
    </div>
    <div class="step">
        <div class="step-n">02</div>
        <div><h4>AI Vision Analysis</h4>
        <p>Our model examines skin texture, tone, pores, pigmentation, and surface patterns.</p></div>
    </div>
    <div class="step">
        <div class="step-n">03</div>
        <div><h4>Receive Your Report</h4>
        <p>A structured dermatology report is generated with a Skin Health Score and personalised recommendations.</p></div>
    </div>
    <p class="plabel" style="margin-top:28px;margin-bottom:12px;">Report Includes</p>
    <div class="tags">
        <span class="tag"><span class="tag-dot">·</span> Skin Type</span>
        <span class="tag"><span class="tag-dot">·</span> Condition Overview</span>
        <span class="tag"><span class="tag-dot">·</span> Area Observations</span>
        <span class="tag"><span class="tag-dot">·</span> Skin Concerns</span>
        <span class="tag"><span class="tag-dot">·</span> Skincare Routine</span>
        <span class="tag"><span class="tag-dot">·</span> Preventive Advice</span>
        <span class="tag"><span class="tag-dot">·</span> Health Score</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)   # end section-wrap


# ─────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────
PROMPT = """
You are an expert dermatologist conducting a professional skin analysis.

Analyze the uploaded facial image and produce a structured, clinical yet accessible report.

Structure your response with these sections:

1. SKIN TYPE
   Identify (Dry / Oily / Combination / Normal / Sensitive) with brief justification.

2. OVERALL SKIN CONDITION
   A concise summary of the general skin health observed.

3. AREA-WISE OBSERVATIONS
   Forehead, T-zone, cheeks, nose, under-eyes, lips/perioral area.

4. SKIN CONCERNS
   List identified issues (e.g. hyperpigmentation, acne, dehydration, redness, enlarged pores, uneven texture).

5. SKINCARE RECOMMENDATIONS
   Morning and evening routine steps tailored to the observed skin type and concerns.

6. PREVENTIVE MEASURES
   Long-term habits and lifestyle advice for improved skin health.

7. SKIN HEALTH SCORE: [number from 1-100]
   On the final line write exactly: SKIN HEALTH SCORE: [number]

Use warm, professional language. Be specific and actionable.
"""


# ─────────────────────────────────────────────
# PDF
# ─────────────────────────────────────────────
def create_pdf(report_text, score):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(20, 20, 20)
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(26, 18, 9)
    pdf.cell(0, 12, "DermAI Skin Analysis Report", ln=True, align="C")
    pdf.set_font("Arial", "I", 11)
    pdf.set_text_color(140, 123, 107)
    pdf.cell(0, 8, "AI-Powered Dermatological Assessment", ln=True, align="C")
    pdf.ln(4)
    pdf.set_draw_color(196, 168, 130)
    pdf.set_line_width(0.5)
    pdf.line(20, pdf.get_y(), 190, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(26, 18, 9)
    pdf.cell(0, 8, f"Skin Health Score: {score}/100", ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(60, 45, 30)
    for line in report_text.split("\n"):
        clean = line.strip()
        if not clean:
            pdf.ln(3)
            continue
        if re.match(r'^\d+\.', clean) or clean.isupper():
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(26, 18, 9)
            pdf.ln(3)
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
    m = re.search(r'SKIN HEALTH SCORE[:\s]+(\d{1,3})', text, re.IGNORECASE)
    return min(int(m.group(1)), 100) if m else 78


# ─────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────
if analyze:
    if uploaded_image is None:
        st.error("Please upload a facial image before running the analysis.")
    else:
        prog = st.progress(0)
        for i in range(100):
            time.sleep(0.011)
            prog.progress(i + 1)

        with st.spinner("Analyzing skin characteristics…"):
            response = model.generate_content([PROMPT, image])

        report = response.text
        score  = extract_score(report)
        score_label = (
            "Excellent" if score >= 85 else
            "Good"      if score >= 70 else
            "Fair"      if score >= 50 else
            "Needs Attention"
        )

        # ── Single markdown block so the dark wrapper actually contains its children ──
        st.markdown(f"""
        <div style="
            background:#1A1209;
            padding:56px 64px;
            margin-top:0;
            border-radius:0;
        ">
            <div style="
                font-family:'Cormorant Garamond',serif;
                font-size:40px; font-weight:300;
                color:#F5F0EB; line-height:1.1; margin-bottom:32px;
            ">
                Your Skin <span style="font-style:italic;color:#C4A882;">Analysis Report</span>
            </div>

            <div style="
                background:rgba(245,240,235,.04);
                border:1px solid rgba(196,168,130,.2);
                border-radius:16px; padding:36px 44px;
                font-size:14px; color:rgba(245,240,235,.85);
                line-height:1.95; font-weight:300;
                white-space:pre-wrap;
                font-family:'DM Sans',sans-serif;
            ">{report}</div>

            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:36px;">
                <div style="background:rgba(245,240,235,.04);border:1px solid rgba(196,168,130,.15);border-radius:12px;padding:28px 22px;text-align:center;">
                    <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.25em;color:rgba(196,168,130,.7);text-transform:uppercase;margin-bottom:12px;">Analysis Status</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:400;color:#F5F0EB;margin:10px 0;">Complete</div>
                    <div style="font-size:12px;color:rgba(245,240,235,.4);font-weight:300;">Full report generated</div>
                </div>
                <div style="background:rgba(196,168,130,.06);border:1px solid rgba(196,168,130,.35);border-radius:12px;padding:28px 22px;text-align:center;">
                    <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.25em;color:rgba(196,168,130,.7);text-transform:uppercase;margin-bottom:12px;">Skin Health Score</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:50px;font-weight:300;color:#F5F0EB;line-height:1;">{score}<span style="font-size:18px;color:#C4A882;">/100</span></div>
                    <div style="font-size:12px;color:rgba(245,240,235,.4);margin-top:7px;font-weight:300;">{score_label}</div>
                    <div style="margin-top:12px;height:3px;background:rgba(245,240,235,.08);border-radius:2px;">
                        <div style="width:{score}%;height:100%;border-radius:2px;background:linear-gradient(90deg,#C4A882,#E8D5B7);"></div>
                    </div>
                </div>
                <div style="background:rgba(245,240,235,.04);border:1px solid rgba(196,168,130,.15);border-radius:12px;padding:28px 22px;text-align:center;">
                    <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.25em;color:rgba(196,168,130,.7);text-transform:uppercase;margin-bottom:12px;">Report Sections</div>
                    <div style="font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:400;color:#F5F0EB;margin:10px 0;">6 Areas</div>
                    <div style="font-size:12px;color:rgba(245,240,235,.4);font-weight:300;">Comprehensive coverage</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        create_pdf(report, score)
        with open("skin_report.pdf", "rb") as f:
            st.download_button(
                label="↓  Download Full PDF Report",
                data=f,
                file_name="DermAI_Skin_Report.pdf",
                mime="application/pdf"
            )


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p>DermAI &nbsp;·&nbsp; For educational purposes only &nbsp;·&nbsp; Not a substitute for professional medical advice</p>
    <div class="orn">✦</div>
</div>
""", unsafe_allow_html=True)
