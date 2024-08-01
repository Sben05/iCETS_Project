# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# seo.py

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


# Fetch data from Firebase
def fetch_data_from_firestore(db):
    docs = db.collection("images").stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    return data

# Mock function to rank attributes based on SEO optimization
def rank_attributes(attributes):
    # Example: Return attributes ranked by a simple heuristic or predefined scores
    # In practice, this could be based on keyword analysis, search volume, etc.
    attribute_scores = {attr: len(attr) for attr in attributes}
    ranked_attributes = sorted(attribute_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_attributes

# Mock function to generate search terms
def generate_search_terms(name, attributes):
    # Example: Generate possible search terms based on product name and attributes
    search_terms = [name]
    for attr in attributes:
        search_terms.append(f"{name} {attr}")
    return list(set(search_terms))

# Display SEO Optimization results
def display_seo_optimization(db):
    st.title('SEO Optimization')
    st.write('Welcome to the SEO Optimization page!')

    data = fetch_data_from_firestore(db)

    # Select a product
    product_names = [item.get('name', 'Unknown') for item in data]
    selected_product = st.selectbox('Select a Product', product_names)

    # Find the selected product's data
    selected_data = next((item for item in data if item.get('name', 'Unknown') == selected_product), None)
    if selected_data:
        st.subheader(f"Selected Product: {selected_product}")
        attributes = selected_data.get('attributes', [])

        if isinstance(attributes, list) and attributes:
            ranked_attributes = rank_attributes(attributes)
            st.write('**Ranked Attributes:**')
            for attr, score in ranked_attributes:
                st.write(f"- **{attr}** (Score: {score})")

            search_terms = generate_search_terms(selected_product, attributes)
            st.write('**Possible Search Terms:**')
            for term in search_terms:
                st.write(f"- {term}")

        else:
            st.write("No attributes available for this product.")

    else:
        st.write("Product not found.")
