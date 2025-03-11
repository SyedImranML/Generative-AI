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

# Check if GPU is enabled
is_gpu_enabled = torch.cuda.is_available()

# Sidebar title with emoji
st.sidebar.title("📊 VisualChat AI ✨")
st.sidebar.write("Chat with Images/Graphs/Invoices")

# Removed the input type box from the sidebar

# Powered by text in sidebar with navy blue background
st.sidebar.markdown("""
<div style="text-align: center; font-size: 14px; font-weight: bold; margin-top: 50px; padding: 10px; background-color: navy; color: white; border-radius: 5px;">Powered By UMC Data Fusion ⚙️</div>
""", unsafe_allow_html=True)

# Centered main title
st.markdown("""
    <div style="text-align: center; font-size: 30px; font-weight: bold;">📊 VisualChat AI ✨</div>
""", unsafe_allow_html=True)

# Reduce space between the titles
st.markdown("<br>", unsafe_allow_html=True)  # Reduced space

# Ask a question section with larger text size
st.markdown("""
    <div style="text-align: center; font-size: 28px; font-weight: bold;">Ask a question about the uploaded Image or Graph:</div>
""", unsafe_allow_html=True)

# Add space below the question section
st.markdown("<br><br>", unsafe_allow_html=True)  # Adds space

# Increase the size of the query input box
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

# Sidebar for uploading an image or providing a URL inside a box
st.sidebar.markdown("""
<div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
    <h4 style="text-align: center;">Upload an Image</h4>
</div>
""", unsafe_allow_html=True)

# Allow image upload or URL input
image = None  # Initialize the image variable

uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    try:
        image = PIL.Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

image_url = st.sidebar.text_input("Enter Image URL")
if image_url:
    try:
        response = requests.get(image_url)
        image = PIL.Image.open(BytesIO(response.content))
        st.image(image, caption="Uploaded Image", use_column_width=True)
    except Exception as e:
        st.error(f"Error loading image: {e}")

# Submit and display result
if user_input and image:  # Only proceed if there's a user query and an image
    st.write("### Response:")
    result = generate_image_response(image, user_input)
    st.write(result)
