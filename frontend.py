# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# frontend.py


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

# Importing the different sections
from backend import upload_image_to_imgbb, format_response, analyze_image
from dashboard import display_home_page
from capture_analyze import display_capture_analyze
from review_data import display_review_data
from seo import display_seo_optimization
from notifications import display_notifications

st.set_page_config(page_title="Fashion Attribution Dashboard", layout="wide")

# Main function to run the Streamlit app
def main():
    key_path_dict = {
      "type": "service_account",
      "project_id": "infosys-icets-project",
      "private_key_id": "35679620d0204386827944791395eb825b952c36",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDLS1dy4/bxwUOl\nAr8xLbs5mXo9hNRBV4+ych1Y/kMeM0F0LT8Vs8s6U7qRgsyuV76DMy3qiLkD/j+h\nBGWMOyuGNFzS4azL8HJ1jczt9BaMTxp5PYr3rdAx9zoxMecfZSVceyncj+vvKlMa\nvf/tmZLXvK+V/sFgt5TNXi9UVzjWtelbGfpM0nZcfbjKrIxywlPFOzOQjb8xTOLJ\nAnjyn7vUGPTjblpiKWTfVUwEv320hGCB9Es98g1KbyyrExqr946fGId4RjkV4wk6\n3/5HwHcRu43vtV6W8wE8wvN78qMn5vsyvdItiZQwIERX/WFoHKqNtYrPD5dsK71M\nm00ZfqUpAgMBAAECggEAMVdAqwWpyKzd0GWthk/hZl46BUbhJlfMbGTWeyRBIYoS\nq5IUwt1vqKEsQcdjirgIqPrJvOgAsbeqdVfmFqZAztKUKem0oQ3jleT79U/+DgFf\n/Uei3DDfPFVTFiAUxrGrovnQo/P5cUOORooRXPdeZMaqvibGBAWik8K1jYya4r92\nNVr0uHIj169h6We/BK73xZtqBhfnfLYkWNbHPg+TAEM8Wuh1Hs4QU67AyJypameN\nA4NXIUl6SE+tidFrnoLYqQ2teODLZGHuD2L/gHQUB9wgdtzoO3MOzcKMUWS8iVA7\nLRIU+QvaAFacrutEde1cuePY4Cao/4Yj2am8Gf6tdQKBgQD+Zj8r1iQrUi4z+9i9\nSl3zbNIt0+TwSMLfAlgSDuMpPNNOSOeL0fzUTTteqIKWfcYQZjtuxJmO23WxKN15\nncUhPB5BvRgJf3bn4arHgzUOkAThMcJx7XnyYAcYeNLBdmf2UWRFuWTA8KUNsKJq\nlnMkznPtnC7aduN/mhqQLowOxQKBgQDMksgMIGCb/UheCUBNWKatc7L8Vnc8indB\ngpOgjdYSsz17JY1cX7gezd2+OvW0n9Xx18pYaw9stHp6CDQJa4lUafYNHlptxetm\noiRs48AIZ5LqgxgYxEgExy+YsEMb8RzWADHEUKBlf3RPBibM6AMRlRiZ++MY+W6r\nDZ2J2dKjFQKBgEpzyhEePr+e8X6tOiVL2msfcfOPi/T2lnGF0hiW2sx6zKygkYNO\nFVxcrf9p+a3paUnrYYFtcDNq7urGNusczVCIs6IxoRNGhpoeZUi2kZSNeaAeW/XT\ntljE2c7DrYqJCKwB7gKp217MDsIO67meBlzDPxJPHzc4jCQQCa4gsUSxAoGAK8to\nhCASTpKkgW0dlPFbjVptgNPJ5u4FpcKcdAypPYudp9VcM+BR/FY6GFVq8GYfWQzH\nRrJ0tOLWLXXAHhwlZCri/9/1n/Z09J3VinIfVC1IKGg0Kmkqucsih1+EnmC5uZ6F\nCO/xxojIj3pTqB4rOgJfJ+fisCAF7xyVE0PMchkCgYEAo2Dz5+6OkCR4WWNKhY4l\np+EoGFGVDWxfuTtJSN23Q78sSeeqvGJ6uXGn78X7sO1hWWHSuPf6NyJai7TtIZ/d\n+duUTx8iMGYxqEjk3jbaWdUbApq1rOoKLAt9e7t/pUJUaAIwaUkK89FxrR9BYM4J\nrR2p+lUuJ0Cf5D41doG09kk=\n-----END PRIVATE KEY-----\n",
      "client_email": "firebase-adminsdk-v5vc8@infosys-icets-project.iam.gserviceaccount.com",
      "client_id": "114622023006963394675",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-v5vc8%40infosys-icets-project.iam.gserviceaccount.com",
      "universe_domain": "googleapis.com"
    }

    if not firebase_admin._apps:
        cred = credentials.Certificate(key_path_dict)
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    with st.sidebar:
        st.markdown("""
            <style>
            .sidebar-subtext {
                font-size: 16px;
                color: #FFFFFF; /* White color */
                text-align: center;
                margin-bottom: 20px;
            }
            .sidebar-header {
                font-size: 24px;
                font-weight: bold;
                color: #FF6347; /* Tomato color */
                text-align: center;
                margin-bottom: 10px; /* Reduced margin for separator */
            }
            .separator {
                border-top: 2px solid #FF6347; /* Tomato separator */
                margin-bottom: 20px;
            }
            .current-page {
                font-size: 18px;
                font-weight: bold;
                color: #FF6347; /* Tomato color for page */
                text-align: center;
                margin-top: 10px;
            }
            .stOptionMenu {
                margin-top: 20px;
            }
            </style>
            <div class="sidebar-header">Welcome to <span style="color: #FFFFFF;">Retail Classifier</span>!</div>
            <div class="separator"></div>
            <div class="sidebar-subtext">Please select a navigation page from the options below.</div>
        """, unsafe_allow_html=True)


        # Compute the current page selection
        page = option_menu(
            "Navigation",
            ["Dashboard", 'Extract Attributes', 'Show Database', 'SEO Optimization', 'Notifications', '---'],
            icons=['house', 'camera', 'code-slash', 'graph-up-arrow'],
            menu_icon="cast",
            default_index=0
        )

    st.title("Fashion Attribute Manager")

    if page == "Dashboard":
        display_home_page()
    elif page == 'Extract Attributes':
        display_capture_analyze(db)
    elif page == 'Show Database':
        display_review_data(db)
    elif page == 'SEO Optimization':
        display_seo_optimization(db)
    elif page == "Notifications":
        display_notifications()

if __name__ == "__main__":
    main()
