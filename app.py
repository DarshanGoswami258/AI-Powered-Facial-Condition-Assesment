import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time
from fpdf import FPDF
import re
import html

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
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@300;400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #F5F0EB !important;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stHeader"]{display:none!important;}
[data-testid="stDecoration"]{display:none!important;}
[data-testid="stToolbar"]{display:none!important;}
#MainMenu, footer{visibility:hidden;}

[data-testid="stMainBlockContainer"]{
    padding-top:0!important;
    max-width:100%!important;
}

.hero-wrap{
    background:#1A1209;
    padding:56px 64px 48px;
}

.hero-eyebrow{
    font-family:'DM Mono',monospace;
    font-size:11px;
    letter-spacing:.25em;
    color:#C4A882;
    text-transform:uppercase;
    margin-bottom:14px;
}

.hero-title{
    font-family:'Cormorant Garamond',serif;
    font-size:clamp(44px,5.5vw,76px);
    font-weight:300;
    line-height:1.05;
    color:#F5F0EB;
}

.hero-title em{
    font-style:italic;
    color:#C4A882;
}

.hero-sub{
    margin-top:18px;
    font-size:14px;
    font-weight:300;
    color:rgba(245,240,235,.55);
    line-height:1.75;
    max-width:460px;
}

.section-wrap{padding:48px 64px;background:#F5F0EB;}
.section-wrap-dark{padding:56px 64px;background:#1A1209;}

.plabel{
font-family:'DM Mono',monospace;
font-size:10px;
letter-spacing:.28em;
color:#8C7B6B;
text-transform:uppercase;
margin-bottom:6px;
}

.ptitle{
font-family:'Cormorant Garamond',serif;
font-size:26px;
font-weight:400;
color:#1A1209;
margin-bottom:6px;
}

.pdesc{
font-size:13px;
color:#8C7B6B;
line-height:1.75;
font-weight:300;
margin-bottom:28px;
}

.step{display:flex;gap:18px;margin-bottom:26px;}
.step-n{font-family:'DM Mono',monospace;font-size:11px;color:#C4A882;}

.tag{
display:inline-flex;
padding:5px 13px;
background:rgba(26,18,9,.05);
border-radius:100px;
font-size:12px;
color:#4A3728;
}

.col-div{
width:1px;
min-height:420px;
background:rgba(26,18,9,.1);
margin:auto;
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
    <div class="hero-title">Skin Analysis,&nbsp;<em>Reimagined.</em></div>
    <div class="hero-sub">
        Upload a facial photograph and receive a comprehensive dermatological
        assessment — powered by advanced generative AI.
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN SECTION
# ─────────────────────────────────────────────
st.markdown('<div class="section-wrap">', unsafe_allow_html=True)

col_left, col_mid, col_right = st.columns([10,1,10])

with col_left:

    st.markdown('<p class="plabel">01 · Upload</p>', unsafe_allow_html=True)
    st.markdown('<p class="ptitle">Your Photograph</p>', unsafe_allow_html=True)

    st.markdown(
        '<p class="pdesc">Use a well-lit, front-facing image with no filters applied.</p>',
        unsafe_allow_html=True
    )

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["jpg","png","jpeg"],
        label_visibility="collapsed"
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image,use_container_width=True)

    analyze = st.button("✦ Run Skin Analysis")

with col_mid:
    st.markdown('<div class="col-div"></div>', unsafe_allow_html=True)

with col_right:

    st.markdown('<p class="plabel">02 · Process</p>', unsafe_allow_html=True)
    st.markdown('<p class="ptitle">How It Works</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="step">
    <div class="step-n">01</div>
    <div>Upload your image</div>
    </div>

    <div class="step">
    <div class="step-n">02</div>
    <div>AI analyzes facial skin</div>
    </div>

    <div class="step">
    <div class="step-n">03</div>
    <div>Receive a full dermatology report</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PROMPT
# ─────────────────────────────────────────────
PROMPT = """
You are an expert dermatologist conducting a professional skin analysis.

Analyze the uploaded facial image and produce a structured report.

Include:

1. SKIN TYPE
2. OVERALL SKIN CONDITION
3. AREA-WISE OBSERVATIONS
4. SKIN CONCERNS
5. SKINCARE RECOMMENDATIONS
6. PREVENTIVE MEASURES

End with:

SKIN HEALTH SCORE: [1-100]
"""


# ─────────────────────────────────────────────
# SCORE EXTRACTION
# ─────────────────────────────────────────────
def extract_score(text):
    m = re.search(r'SKIN HEALTH SCORE[:\s]+(\d{1,3})', text, re.IGNORECASE)
    return min(int(m.group(1)),100) if m else 75


# ─────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────
if analyze:

    if uploaded_image is None:
        st.error("Please upload an image first.")

    else:

        prog = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            prog.progress(i+1)

        with st.spinner("Analyzing skin..."):
            response = model.generate_content([PROMPT,image])

        report = response.text
        score = extract_score(report)

        st.markdown("## Skin Analysis Report")
        st.write(report)
        st.metric("Skin Health Score", f"{score}/100")
