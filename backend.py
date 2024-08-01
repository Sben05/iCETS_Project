
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
import os
import requests
import base64
import json
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Function to upload image to imgbb
def upload_image_to_imgbb(image_bytes, api_key):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": api_key,
        "image": base64.b64encode(image_bytes).decode('utf-8')
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    return response_data.get('data', {}).get('url')

# Function to format the response into markdown
def format_response(response_content):
    general_info = response_content.get("General Info", {})
    attributes = response_content.get("List of attributes", [])

    general_info_md = "### General Info\n"
    for key, value in general_info.items():
        general_info_md += f"- **{key}**: {value}\n"

    attributes_md = "### List of Attributes\n"
    for idx, attribute in enumerate(attributes, 1):
        attributes_md += f"{idx}. {attribute}\n"

    return general_info_md + "\n" + attributes_md, attributes

# Function to analyze the image using Google Generative AI
def analyze_image(image_url):
    os.environ["GOOGLE_API_KEY"] = "AIzaSyDsYq_gHrR7aXmD6rUFMbil2cu2BwIcvc4"
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    prompt_ocr = """
    Analyze the image of the retail product provided and categorize it into one of the following types: Shirt, Pants, Hoodie, Jacket, Hat, Accessory, Other. 
    Also, provide a product name, which is unique based on attributes. Make sure name is given, don't do unknown/null/etc.

    Extract the following general information from the image:
    - Brand name
    - Product category
    - Color
    - Size or dimensions
    - Material or fabric type
    - Usage or purpose
    - Unique selling points or features
    - Price range
    - Customer target group
    - Certifications or special labels

    Generate EXTREMELY UNIQUE product attributes (5-7) relevant for search terms. If any information is not visible, PREDICT what it is. Provide the response in JSON format with the following structure. Ensure your response doesn't have additional quotes and begins/ends with {}:

    {
        "General Info": {
            "Brand name": "value",
            "Product category": "value",
            "Color": "value",
            "Size or dimensions": "value",
            "Material or fabric type": "value",
            "Usage or purpose": "value",
            "Unique selling points or features": "value",
            "Price range": "value",
            "Customer target group": "value",
            "Certifications or special labels": "value"
        },
        "List of attributes": [
            "Attribute 1",
            "Attribute 2",
            "Attribute 3",
            "Attribute 4",
            "Attribute 5",
            "Attribute 6",
            "Attribute 7",
            "Attribute 8",
            "Attribute 9",
            "Attribute 10"
        ]
    }
    """

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt_ocr},
            {"type": "image_url", "image_url": image_url},
        ]
    )

    try:
        response = llm.invoke([message])
        response_content = json.loads(response.content)

        # Ensure category is one of the allowed options
        allowed_categories = ["Shirt", "Pants", "Hoodie", "Jacket", "Hat", "Accessory", "Other"]
        general_info = response_content.get("General Info", {})
        category = general_info.get("Product category", "Other")
        if category not in allowed_categories:
            category = "Other"
        general_info["Product category"] = category

        response_content["General Info"] = general_info
        return response_content
    except json.JSONDecodeError:
        st.write("here")
        return None

def store_image_data(image_url, response_content, db):
    """
    Store the image URL and attributes to Firestore.
    """
    # Extract general info and attributes from the response content
    general_info = response_content.get("General Info", {})
    attributes = response_content.get("List of attributes", [])

    # Prepare the data for Firestore
    data = {
        'image_url': image_url,
        'name': general_info.get("Brand name", "Unknown"),
        'category': general_info.get("Product category", "Other"),
        'attributes': attributes
    }

    doc_ref = db.collection('images').add(data)
    return doc_ref
