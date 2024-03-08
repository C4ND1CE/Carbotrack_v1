import streamlit as st
import requests
import pandas as pd
import numpy as np
import datetime
import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()


#If api in the cloud please update the url with the url
# url = 'https://cabotrack-qoz5nlx2ga-ew.a.run.app' v0
url = 'https://carbotrackapi-qoz5nlx2ga-ew.a.run.app'

st.markdown("# Welcome to the Carbotrack app! #")
    
    
'''
Please be aware that our app and our models are still at an early stage and can lack accuracy or not be able to detect food type!

**DO NOT** use as a medical guidance, always follow recomendations from your doctor!

Please upload/take a picture and test our app and see how much dose of insuline you should take based on the picture of your food received!
'''
uploaded_file = st.file_uploader('Photo of your meal', type=['png', 'jpg', 'jpeg'], accept_multiple_files=False, help='Upload your photo')

if uploaded_file is not None:
    col1, col2, col3 = st.columns([1,2,1])  # Create columns for layout
    with col2:  # Display the uploaded image in the middle column
        st.image(uploaded_file, width=340)
        
col1, col2, col3 = st.columns([1,2,1])  # Create columns for layout
      
with col2:  # Put the button in the middle column
    col2_1, col2_2, col2_3 = st.columns([1,4,1])  # Create sub-columns within col2
    with col2_2:  # Put the button in the middle sub-column
        if st.button("Let's try to detect food type and give you an insuline recomendation!", key='predict'):
            if uploaded_file is not None:
                files = {'image': uploaded_file}
                with st.spinner('Trying to detect food type and give you an insuline recommendation!'):
                    response = requests.post(url + '/predict', files=files)
                if response.status_code == 200:
                    result = response.json()
                    food_result = result.get('food_result', 'Unknown')
                    carbs_result = result.get('carbs_result', 'Unknown')
                    insuline_result = result.get('insuline_result', 'Unknown')

                    st.markdown(f"**Food detected:** {food_result} :drooling_face:")  # Replace :pizza: with the appropriate emoji
                    st.markdown(f"**Estimated carbs:** {carbs_result:.2f} g")
                    st.markdown(f"**Recommended insuline dose (not a medical advice, please use your common sense):** {insuline_result} dose")
                else:
                    st.write("Food not yet recognized, our model is still learning, sorry!")
            else:
                st.write("Please upload an image")
