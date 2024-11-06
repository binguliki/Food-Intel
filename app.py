import streamlit as st
from PIL import Image
import google.generativeai as genai 
import os
import pytesseract
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.environ['api_key'])
model = genai.GenerativeModel('gemini-1.5-flash')
html_for_home = """
    <style>
        .header {
            background-color: transparent;
            text-align: center;
            text-decoration: underline;
            text-decoration-style: solid;
            text-underline-offset: 5px;
            text-decoration-thickness: 2px;
            text-decoration-color: orange;
        }

        .desc {
            font-size: 20px;
            font-family: 'Monospace';
            color: orange;
            text-align: center;
        }
    </style>
"""

def analyze_ingredients(image):
    extracted_text = pytesseract.image_to_string(image)
    full_prompt = f"Consider you are a doctor. Use the this text information about the product: \n {extracted_text} \n Give a detailed report on the product ingredients and also give a score on scale of 10."
    response = model.generate_content(full_prompt)
    return response.candidates[0].content.parts[0].text

st.markdown("<h1 class='header'> Food Intel - Ingredients Analysis </h1>", unsafe_allow_html=True)
st.markdown("<p class='desc'> Food Intel is a service that analyzes food ingredients to provide insights on quality, nutritional value, and potential allergens. Aimed at promoting transparency, it empowers consumers to make informed choices, catering to health-conscious individuals and those with dietary needs by breaking down the contents of food products in detail. <p>" , unsafe_allow_html = True)
st.markdown("### Enter the Image")
st.html(html_for_home)

uploaded_image = st.file_uploader("Upload an image of the product", type=["jpg", "jpeg", "png" , "webp"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

if st.button("Analyze"):
    if uploaded_image:
        analysis = analyze_ingredients(image)
        st.subheader("Analysis Results")
        st.markdown(analysis)
    else:
        st.error("Please add the image.")