import streamlit as st
import google.generativeai as genai
import requests
from io import BytesIO
import PIL.Image
import torch

# Set API key for Google Generative AI
GOOGLE_API_KEY = 'AIzaSyDchZ1PS_Rg3Xws61AkZPrQPKio5ANBMdM'  # Replace with your actual Google API Key
genai.configure(api_key=GOOGLE_API_KEY)

# Set Streamlit page title
st.set_page_config(page_title="VisualAI", layout="wide")

# Sidebar title with emoji
st.sidebar.title("📊 VisualChat AI ✨")
st.sidebar.write("Chat with Images/Graphs/Invoices")

# Sidebar for uploading an image or providing a URL without the border box
image = None  # Initialize the image variable

uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    try:
        image = PIL.Image.open(uploaded_image)
    except Exception as e:
        st.error(f"Error loading image: {e}")

#image_url = st.sidebar.text_input("Enter Image URL", value="https://www.w3schools.com/w3images/apple.jpg")
image_url = st.sidebar.text_input("Enter Image URL", value="")
if image_url:
    try:
        st.write(f"Attempting to load image from URL: {image_url}")
        
        # Check if the URL is valid and the image can be fetched
        response = requests.get(image_url)
        st.write(f"HTTP Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check if the response is an actual image
            try:
                image = PIL.Image.open(BytesIO(response.content))
                st.write("Successfully retrieved image")
            except Exception as e:
                st.error(f"Error processing image data: {e}")
        else:
            st.error(f"Failed to load image. HTTP Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error loading image: {e}")

# Powered by text in sidebar with navy blue background at the bottom
st.sidebar.markdown("""
<div style="text-align: center; font-size: 14px; font-weight: bold; margin-top: 50px; padding: 10px; background-color: navy; color: white; border-radius: 5px;">Powered By UMC Data Fusion ⚙️</div>
""", unsafe_allow_html=True)

# Centered main title
st.markdown("""
    <div style="text-align: center; font-size: 30px; font-weight: bold;">📊 VisualChat AI ✨</div>
""", unsafe_allow_html=True)

# Add space below the main title
st.markdown("<br>", unsafe_allow_html=True)

# Display the uploaded image below the title
if image:
    st.image(image, caption="Uploaded Image", use_column_width=False)  # Medium size, not full-width

# Add space between the image and the question section
st.markdown("<br><br>", unsafe_allow_html=True)

# Ask a question section with larger text size
st.markdown("""
    <div style="text-align: center; font-size: 28px; font-weight: bold;">Ask a question about the uploaded Image or Graph </div>
""", unsafe_allow_html=True)

# Add space below the question section
st.markdown("<br><br>", unsafe_allow_html=True)

# Input box for the query
user_input = st.text_input("Query", placeholder="Type your query here...", max_chars=100, key="query_input")

# Vision model setup
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# Function to process image and query
def generate_image_response(image, query):
    try:
        response = vision_model.generate_content([query, image])
        return response.text
    except Exception as e:
        return f"Error processing query: {e}"

# Submit and display result
if user_input and image:  # Only proceed if there's a user query and an image
    st.write("### Response:")
    result = generate_image_response(image, user_input)
    st.write(result)
