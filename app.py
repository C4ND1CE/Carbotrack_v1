import streamlit as st
import requests
from PIL import Image
import io

#colors
pastel_blue = "#aed9e0"
pastel_pink = "#f3c0c0"
pastel_green = "#b6e2bd"
pastel_yellow = "#fff7b5"

# Define a list of API URLs
url  = "https://carbo42-qoz5nlx2ga-ew.a.run.app/predict"

#"https://carbotrackapi-qoz5nlx2ga-ew.a.run.app/predict",

st.markdown("# Welcome to the Carbotrack app! #")
     
'''
Please be aware that our app and our models are still at an early stage and can lack accuracy or not be able to detect food type!

**DO NOT** use as a medical guidance, always follow recomendations from your doctor!

Please upload/take a picture and test our app and see how much dose of insuline you should take based on the picture of your food received!
'''

st.title('Food Image Analysis')


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
col1, col2, col3 = st.columns([1,2,1])  # Create columns for layout
      
with col2:  # Put the button in the middle column
    col2_1, col2_2, col2_3 = st.columns([1,4,1])  # Create sub-columns within col2
    with col2_2:  # Put the button in the middle sub-column
        if st.button("Let's try to detect food type and give you an insuline recomendation!", key='predict'):

            with st.spinner('Processing... Please wait'):
                try:
                    response = requests.post(url, files=files) # type: ignore
                    if response.status_code == 200:
                        response_json = response.json()
                        st.write(f"Food: {response_json['food_result'].capitalize()} :drooling_face:")
                        st.write(f"Carbohydrates: {response_json['carbs_result']} grams")
                        st.write(f"Insulin: {response_json['insuline_result']} units")
                    else:
                        st.error(f"Food not yet recognized, our model is still learning, sorry!") #f"Failed to get a response from the server. Status code: {response.status_code}, Response: {response.text}")
                except requests.RequestException as e:
                    st.error(f"Request failed: {e}")
                except Exception as e:
                    st.error(f"Food not yet recognized, our model is still learning, sorry!")
