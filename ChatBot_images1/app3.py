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
st.sidebar.title("📊 Visual AI ✨")
st.sidebar.write("Chat with Images/Graphs/Invoices")


# Sidebar for uploading an image or providing a URL inside a box
st.sidebar.markdown("""
<div style="border: 2px solid #ccc; padding: 10px; border-radius: 5px; background-color: #f9f9f9;">
    <h4 style="text-align: center;">Input Type</h4>
</div>
""", unsafe_allow_html=True)

option = st.sidebar.selectbox("Choose Input Type", ("Image URL", "Upload Image"))

image = None  # Initialize the image variable

if option == "Image URL":
    image_url = st.sidebar.text_input("Enter Image URL")
    if image_url:
        try:
            response = requests.get(image_url)
            image = PIL.Image.open(BytesIO(response.content))
            st.image(image, caption="Uploaded Image", use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

elif option == "Upload Image":
    uploaded_image = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        try:
            image = PIL.Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

# Centered main title
st.markdown("""
    <div style="text-align: center; font-size: 30px; font-weight: bold;">📊 VisualChat AI ✨</div>
""", unsafe_allow_html=True)

st.markdown('<div class="powered-by">Powered By UMC Data Fusion ⚙️</div>', unsafe_allow_html=True)

# Vision model setup
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# Input for user query
st.write("### Ask a question about the uploaded Image or Graph:")
user_input = st.text_input("Query", placeholder="Type your query here...")

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
