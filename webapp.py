import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="AI Facial Skin Analyzer",
    page_icon="🧴",
    layout="wide"
)

# ----------------------------
# Configure Gemini
# ----------------------------
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# ----------------------------
# Custom CSS for Better UI
# ----------------------------
st.markdown("""
<style>

.main-title{
    font-size:38px;
    font-weight:700;
    text-align:center;
}

.sub-text{
    text-align:center;
    color:grey;
    margin-bottom:30px;
}

.result-box{
    background-color:#f7f7f7;
    padding:20px;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Title Section
# ----------------------------
st.markdown('<div class="main-title">🧴 AI Facial Skin Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Upload a facial image and receive an AI-powered dermatology style analysis.</div>', unsafe_allow_html=True)

# ----------------------------
# Layout Columns
# ----------------------------
col1, col2 = st.columns([1,1])

# ----------------------------
# Left Column (Upload Section)
# ----------------------------
with col1:

    st.subheader("📤 Upload Image")

    uploaded_image = st.file_uploader(
        "Upload a clear face image",
        type=["jpg","jpeg","png"]
    )

    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_container_width=True)

    st.info(
    """
    **Tips for best results**
    - Use good lighting
    - Face should be clearly visible
    - Avoid heavy filters
    """
    )

# ----------------------------
# Prompt
# ----------------------------
prompt = """
You are an Expert Dermatologist.

Generate a structured cosmetic facial assessment report based on the user's image.

Include:

1. Skin Type
2. Overall Skin Condition
3. Area-wise Observations
4. Skin Concerns
5. Skincare Recommendations
6. Preventive Measures

Ensure the advice is practical and helpful.
"""

# ----------------------------
# Right Column (Analysis)
# ----------------------------
with col2:

    st.subheader("🔎 Skin Analysis")

    if st.button("Analyze Skin", use_container_width=True):

        if uploaded_image is None:
            st.warning("Please upload an image first.")

        else:

            with st.spinner("AI is analyzing your skin..."):

                response = model.generate_content([prompt, image])

            st.success("Analysis Complete")

            st.markdown("### 🧾 Facial Skin Report")

            st.markdown(
                f"""
                <div class="result-box">
                {response.text}
                </div>
                """,
                unsafe_allow_html=True
            )

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")

st.caption("Built using Streamlit + Gemini Vision Model | AI Dermatology Assistant Demo")
