# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# review_data.py

import streamlit as st
from PIL import Image
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import base64
from io import BytesIO

# Fetch data from Firebase
def fetch_data_from_firestore(db):
    docs = db.collection("images").stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    return data

# Display images and attributes interactively
def display_review_data(db):
    st.title('Review Data')
    st.write('Welcome to the Review Data page!')

    data = fetch_data_from_firestore(db)

    # Display filters
    st.sidebar.header('Filters')
    # Extract categories, using an empty string if 'category' key is missing
    categories = list(set(item.get('category', 'Unknown') for item in data))
    selected_category = st.sidebar.selectbox('Select a Category', ['All'] + categories)

    # Filter data based on the selected category
    if selected_category != 'All':
        data = [item for item in data if item.get('category', 'Unknown') == selected_category]

    # Display data
    for item in data:
        st.subheader(item.get('name', 'No Name'))
        st.image(item.get('image_url', ''), use_column_width=True)
        st.write('**Attributes:**')
        # Handle attributes as a list
        attributes = item.get('attributes', [])
        if isinstance(attributes, list):
            for attribute in attributes:
                st.write(f"- {attribute}")
        else:
            st.write("No attributes available.")

        st.write("---")  # Separator for items
