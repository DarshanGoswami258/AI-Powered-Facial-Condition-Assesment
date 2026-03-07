import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Facial Skin Analyzer",
    page_icon="🧴",
    layout="wide"
)

# -----------------------------
# Custom CSS (Professional UI)
# -----------------------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

h1 {
    text-align:center;
    color:white;
    font-size:45px;
}

.subtitle{
    text-align:center;
    color:#cbd5f5;
    font-size:18px;
    margin-bottom:30px;
}

.card{
    background: rgba(255,255,255,0.05);
    padding:30px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
}

.result-card{
    background:#ffffff;
    padding:30px;
    border-radius:12px;
    box-shadow:0px 10px 25px rgba(0,0,0,0.15);
}

.upload-box{
    border:2px dashed #64748b;
    padding:30px;
    border-radius:12px;
    text-align:center;
}

.stButton>button{
    background:linear-gradient(45deg,#6366f1,#8b5cf6);
    color:white;
    font-size:18px;
    border-radius:10px;
    height:50px;
    width:100%;
}

.stButton>button:hover{
    transform:scale(1.03);
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Configure Gemini
# -----------------------------
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# -----------------------------
# Header Section
# -----------------------------
st.markdown("<h1>AI Powered Facial Skin Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Upload your photo and receive an instant AI powered dermatology report</div>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Layout (Two Columns)
# -----------------------------
col1, col2 = st.columns([1,1])

# -----------------------------
# LEFT SIDE - IMAGE UPLOAD
# -----------------------------
with col1:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("Upload Image")

    uploaded_image = st.file_uploader(
        "Upload a clear photo of your face",
        type=["jpg","jpeg","png"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# RIGHT SIDE - INSTRUCTIONS
# -----------------------------
with col2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("How It Works")

    st.markdown("""
    1️⃣ Upload a **clear front facing photo**

    2️⃣ Click **Analyze Skin**

    3️⃣ AI will generate a **dermatology report**

    ✔ Skin Type  
    ✔ Skin Concerns  
    ✔ Area-wise observations  
    ✔ Personalized Skincare Tips  
    ✔ Preventive measures
    """)

    analyze = st.button("Analyze Skin")

    st.markdown("</div>", unsafe_allow_html=True)



# -----------------------------
# AI PROMPT
# -----------------------------
prompt = """
You are an Expert Dermatologist.

Generate a structured cosmetic facial assessment report.

Include:

1. Skin Type
2. Overall Skin Condition
3. Area-wise Observations
4. Skin Concerns
5. Recommendations
6. Preventive Measures

Use simple language.
Keep the report concise.
"""


# -----------------------------
# ANALYSIS SECTION
# -----------------------------
if analyze:

    if uploaded_image is None:
        st.error("Please upload an image first")

    else:

        progress = st.progress(0)

        for i in range(100):
            progress.progress(i+1)

        with st.spinner("AI Dermatologist is analyzing your skin..."):

            response = model.generate_content([prompt, image])

        st.divider()

        st.markdown("<div class='result-card'>", unsafe_allow_html=True)

        st.subheader("Facial Skin Analysis Report")

        st.write(response.text)

        st.markdown("</div>", unsafe_allow_html=True)
