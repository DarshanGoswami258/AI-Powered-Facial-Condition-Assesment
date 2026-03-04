import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Streamlit page

st.sidebar.title('Upload Your Image')
uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_image:
    image = Image.open(uploaded_image)
    st.sidebar.image(image)

#Main Page
st.title('AI Powered Facial Condition Analysis')
Instructions = """ To Use this Application,
1. Upload a Clear Image of your Face.
2. Clicl the "Analyze" button to recieve insights about your facial condition.
Please ensure that the image is well-lit and shows your face clearly for accurate analysis."""

st.write(Instructions)

prompt = """
You are an Expert Dermatologist.
Task: Generate a Structured cometic facial assemsment report based on the image provided by the user. The report should include:
1. Skin Type: Classify the skin type (e.g., Oily, Dry, Combination, sensitive).
2. Skin Concerns: Identify any visible skin concerns (e.g., acne, wrinkles, hyperpigmentation).
3. Ensure that the recommendation are practical and actionable.

Output format:
1. Skin Type: [Identified Skin Type]
2. Overall Skin Condition: [Brief Description of Overall Skin Condition]
3. Area-wise observations
4. Skin Concerns: [Identified Skin Concerns]
5. Recommendations: [personalized Skincare Recommendations]
6. Preventive Measures: [General Tips for Maintaining Healthy skin]

"""

if st.button("Analyse"):
    if uploaded_image is None:
      st.error('Please upload an image to analyze.')

    else:
      with st.spinner('Analyzing the image...'):
         response = model.generate_content([prompt, image])
      st.subheader("Facial Condition Analysis Report")
      st.write(response.text)