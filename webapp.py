import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

# configure the model
key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# Streamlit page

#sidebar
st.sidebar.title("Upload your Image")
uploaded_image = st.sidebar.file_uploader("Uplaod Image", type=["jpg", "jpeg", "png"])
if uploaded_image:
   image = Image.open(uploaded_image)
   st.sidebar.image(image)

#mainpage
st.title('AI Powered Facial Condition Analysis')

Instructions = """To use this application,
1. Upload a clear image of your face.
2. Click the "Analyze" button to receive insights about your facial condition.
Please ensure that the image is well-lit and shows your face clearly for accurate analysis."""

st.write(Instructions)

prompt = """
You are an Expert Dermatologist

Task : Generate a structured cosmetic facial assesment report based on the image provided by the user. The report should include:
1. Skin Type: Classify the skin type (e.g., oily, dry, combination, sensitive).
2. Skin Concerns: Identify any visible skin concerns (e.g., acne, wrinkles, hyperpigmentation).
3. Recommendations: Provide personalized skincare recommendations based on the identified skin type and concerns.

constraints:
1. The report should be concise and easy to understand.
2. Use non-technical language suitable for a general audience.
3. Ensure that the recommendations are practical and actionable.

Output format:
1. Skin Type: [Identified Skin Type]
2. Overall Skin Condition: [Brief Description of Overall Skin Condition]
3. Area-wise observations
4. Skin Concerns: [Identified Skin Concerns]
5. Recommendations: [Personalized Skincare Recommendations] 
6. Preventive Measures: [General Tips for Maintaining Healthy Skin]

"""

if st.button("Analyse"):
    if uploaded_image is None:
      st.error('Please upload an image to analyze.')

    else:
      with st.spinner('Analyzing the image...'):
         response = model.generate_content([prompt, image])
      st.subheader("Facial Condition Analysis Report")
      st.write(response.text)
