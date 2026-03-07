import streamlit as st
import google.generativeai as genai
import os
from PIL import Image
import time
from fpdf import FPDF

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="AI Dermatology Analyzer",
    page_icon="🧴",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.step-container{
    display:flex;
    align-items:center;
    margin-bottom:20px;
}

.number-tile{
    width:60px;
    height:60px;
    background:linear-gradient(145deg,#1e66c7,#2f7df0);
    color:white;
    font-size:30px;
    font-weight:bold;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:10px;
    box-shadow: 
        inset 0 3px 8px rgba(0,0,0,0.3),
        0 4px 10px rgba(0,0,0,0.2);
    margin-right:15px;
}

.step-text{
    font-size:20px;
}

</style>

<div class="step-container">
<div class="number-tile">1</div>
<div class="step-text">Upload a clear face image</div>
</div>

<div class="step-container">
<div class="number-tile">2</div>
<div class="step-text">AI analyzes skin texture, tone and patterns</div>
</div>

<div class="step-container">
<div class="number-tile">3</div>
<div class="step-text">Receive a personalized dermatology report</div>
</div>

""", unsafe_allow_html=True)

# --------------------------------
# GEMINI CONFIG
# --------------------------------
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)

model = genai.GenerativeModel("gemini-2.5-flash-lite")


# --------------------------------
# HERO SECTION
# --------------------------------
st.markdown("<div class='title'>AI Facial Skin Analyzer</div>", unsafe_allow_html=True)

st.markdown(
"<div class='subtitle'>Instant Dermatology Insights Powered by Generative AI</div>",
unsafe_allow_html=True
)

st.divider()

# --------------------------------
# LAYOUT
# --------------------------------
left, right = st.columns([1,1])

# --------------------------------
# IMAGE UPLOAD
# --------------------------------
with left:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Upload Facial Image")

    uploaded_image = st.file_uploader(
        "Upload a clear face image",
        type=["jpg","png","jpeg"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, use_container_width=True)

    analyze = st.button("Analyze Skin")

    st.markdown("</div>", unsafe_allow_html=True)


# --------------------------------
# INSTRUCTIONS
# --------------------------------
with right:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("How It Works")

    st.write("""
1 Upload a **clear face image**

2 AI analyzes **skin texture, tone and patterns**

3 Receive a **personalized dermatology report**

Report includes:

• Skin Type  
• Skin Concerns  
• Area Observations  
• Skincare Routine  
• Preventive Advice  
""")

    st.markdown("</div>", unsafe_allow_html=True)



# --------------------------------
# PROMPT
# --------------------------------
prompt = """
You are a professional dermatologist.

Generate a structured facial skin analysis.

Include:

1 Skin Type
2 Overall Skin Condition
3 Area-wise Observations
4 Skin Concerns
5 Recommendations
6 Preventive Measures

Also give a Skin Health Score from 1-100.

Use simple language.
"""


# --------------------------------
# PDF FUNCTION
# --------------------------------
def create_pdf(text):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.cell(200,10,txt=line,ln=True)

    pdf.output("skin_report.pdf")



# --------------------------------
# ANALYSIS
# --------------------------------
if analyze:

    if uploaded_image is None:

        st.error("Please upload an image first")

    else:

        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)

        with st.spinner("AI Dermatologist analyzing your skin..."):

            response = model.generate_content([prompt, image])

        report = response.text

        st.divider()

        st.markdown("<div class='report-card'>", unsafe_allow_html=True)

        st.subheader("Skin Analysis Report")

        st.write(report)

        st.markdown("</div>", unsafe_allow_html=True)


        # -----------------------
        # SKIN SCORE (DEMO)
        # -----------------------
        score = 82

        st.divider()

        c1,c2,c3 = st.columns(3)

        with c2:

            st.metric(
                label="Skin Health Score",
                value=f"{score}/100"
            )


        # -----------------------
        # DOWNLOAD REPORT
        # -----------------------
        create_pdf(report)

        with open("skin_report.pdf","rb") as f:

            st.download_button(
                label="Download Report",
                data=f,
                file_name="AI_Skin_Report.pdf",
                mime="application/pdf"
            )
