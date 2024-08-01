# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# risk_analysis.py

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


# Initialize Firebase
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': 'your-project-id',
        })
    return firestore.client()

# Fetch data from Firebase
def fetch_data_from_firestore(db):
    docs = db.collection("images").stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    return data

# Function to rank attributes based on SEO optimization
def rank_attributes(attributes, search_terms):
    # Placeholder for a real SEO ranking algorithm
    # For demonstration, sort attributes by length (example criterion)
    sorted_attributes = sorted(attributes, key=len, reverse=True)
    return sorted_attributes

# Function to generate possible search terms based on product attributes
def generate_search_terms(product_name, attributes):
    search_terms = [product_name]
    search_terms.extend(attributes)
    return list(set(search_terms))  # Remove duplicates

# Display SEO optimization results
def display_seo_optimization():
    st.title('SEO Optimization')
    st.write('Welcome to the SEO Optimization page!')

    db = init_firebase()
    data = fetch_data_from_firestore(db)

    # Select product
    product_names = [item.get('name', 'No Name') for item in data]
    selected_product = st.selectbox('Select a Product', product_names)

    # Find selected product's data
    selected_product_data = next((item for item in data if item.get('name') == selected_product), None)
    if not selected_product_data:
        st.error("Product not found.")
        return

    st.subheader(f"SEO Optimization for: {selected_product}")

    # Get attributes and rank them
    attributes = selected_product_data.get('attributes', [])
    ranked_attributes = rank_attributes(attributes, [])
    
    # Generate possible search terms
    search_terms = generate_search_terms(selected_product, ranked_attributes)
    
    # Display ranked attributes
    st.write("### Ranked Attributes")
    for idx, attr in enumerate(ranked_attributes, 1):
        st.write(f"{idx}. {attr}")

    # Display possible search terms
    st.write("### Possible Search Terms")
    for term in search_terms:
        st.write(f"- {term}")
