# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# capture_analyze.py


import streamlit as st
from PIL import Image
from pytrends.request import TrendReq
from datetime import datetime
import urllib.request
import requests
from time import sleep
from stqdm import stqdm
from streamlit_custom_notification_box import custom_notification_box
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import time
import altair as alt
from io import BytesIO
from google.cloud import firestore

from backend import upload_image_to_imgbb, analyze_image, format_response, store_image_data


def analyze_uploaded_image(image_url):
    if image_url:
        with st.spinner('Analyzing the image...'):
            response_content = analyze_image(image_url)
        st.success('Analysis complete!')
        return response_content
    return None

def display_analysis_results(response_content):
    attributes = None
    if response_content:
        formatted_response, attributes = format_response(response_content)
        st.markdown(formatted_response)
    else:
        st.error("Failed to parse the response. Please ensure the model is providing a valid JSON response.")
    return attributes

def display_capture_analyze(db):
    st.title('Capture & Analyze')
    st.write('Welcome to the Capture & Analyze page!')

    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
        }
        .highlighted-text {
            color: #FF69B4; /* Pink color */
        }
        </style>
        <h2 class="centered-title">Capture and Analyze</h2>
        <p class="highlighted-text">Capture an image and analyze product information.</p>
    """, unsafe_allow_html=True)

    option = st.selectbox("Choose an option", ["Upload Image", "Take Picture with Camera"])

    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    else:
        uploaded_file = st.camera_input("Take a picture")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        st.write("Analyzing...")

        img_bytes = uploaded_file.getvalue()

        api_key = "67ed5f7c63f0e60043f2617d0320df6c"
        image_url = upload_image_to_imgbb(img_bytes, api_key)
        if image_url:
            st.write(f"Image uploaded to imgbb: {image_url}")

            response_content = analyze_uploaded_image(image_url)
            if response_content:
                attributes = display_analysis_results(response_content)

                # Ensure attributes is properly formatted
                if attributes:
                    # Prepare data for Firebase
                    image_data = {
                        "image_url": image_url,
                        "name": response_content.get("General Info", {}).get("Brand name", "Unknown"),
                        "category": response_content.get("General Info", {}).get("Product category", "Other"),
                        "attributes": attributes
                    }
                    st.write("Image data prepared for Firebase:", image_data)

                    # Store data in Firebase
                    store_image_data(image_url, response_content, db)
                    st.success("Image data stored in Firebase successfully!")
