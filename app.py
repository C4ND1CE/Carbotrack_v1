import streamlit as st
import requests
from PIL import Image
import io

#colors

blue = "#26B8B9"
pink = "#D6489C"
grey = "#414546"
yellow = "#E19F3F"

# Define a list of API URLs
url  = "https://carbo42-qoz5nlx2ga-ew.a.run.app/predict"

logo = "logo.png"
text = "# Welcome to the Carbotrack ! #"

# Create columns for layout
col1, col2 = st.columns([1, 4])

# Display logo in the first column
with col1:
    st.image(logo, use_column_width=True)

# Display text in the second column
with col2:
    st.write(text)
    st.markdown(

    f'''
        <div style="border-radius: 20px; padding: 20px; background-color: #f0f0f0;">
            <p>Please be aware that our app and our models are still at an early stage and can lack accuracy or not be able to detect food type!</p>
            <p><strong>DO NOT</strong> use as a medical guidance, always follow recommendations from your doctor!</p>
        </div>
        ''',
        unsafe_allow_html=True
    )

#add empty space
st.write('')
st.write('')
st.write('')

st.subheader('Food Image Analysis')
st.write("Snap a photo of your meal to discover your personalized insulin dosage with our app's innovative image analysis feature!")


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
    # Write a markdown with a styled text to mimic a button
        st.write('')
        st.write('')
        st.write('')
        button_clicked = st.button("**FIND OUT !**", key='predict',
            help="This button triggers the detection of food type and provides insulin recommendation.")

        if button_clicked:
            with st.spinner('Processing... Please dance !'):
                st.image("https://media.giphy.com/media/LmNX3rP5s2bqzHgXph/giphy.gif?cid=ecf05e47kwwtirzrsdz3w2xakgs81lv5alh7jjeaer10f44u&ep=v1_gifs_search&rid=giphy.gif&ct=g", width=300)
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
