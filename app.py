import streamlit as st
import requests
from PIL import Image
import io

# Define a list of API URLs
api_urls = [
    "https://carbotrackapi-qoz5nlx2ga-ew.a.run.app/predict",
    "https://carbo42-qoz5nlx2ga-ew.a.run.app/predict",
]

st.title('Food Image Analysis')

# Let the user select an API from the list
selected_api_url = st.selectbox("Select an API for prediction:", api_urls)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")

    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Store file as jpege as it's smaller to transfer
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    files = {"image": (uploaded_file.name, buffer, "image/jpeg")}

    with st.spinner('Processing... Please wait'):
        try:
            response = requests.post(selected_api_url, files=files)
            if response.status_code == 200:
                response_json = response.json()
                st.write(f"Food: {response_json['food_result']}")
                st.write(f"Carbohydrates: {response_json['carbs_result']} grams")
                st.write(f"Insulin: {response_json['insuline_result']} units")
            else:
                st.error(f"Failed to get a response from the server. Status code: {response.status_code}, Response: {response.text}")
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
