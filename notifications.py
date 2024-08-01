# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# notifications.py

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
from email_validator import EmailNotValidError, validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Fetch the optimal SEO product from Firebase
def get_optimal_product(db):
    doc = db.collection("seo_optimization").document("optimal_product").get()
    if doc.exists:
        return doc.to_dict()
    return None

def display_notifications():
    st.markdown("""
    <style>
        body {
            background-color: #F0F4F8; /* Light background color */
            color: #2E2E3A; /* Darker text color */
            font-family: 'Arial', sans-serif; /* Arial font */
        }
        .header {
            font-size: 36px;
            font-weight: bold;
            color: #FF6F00; /* Bright orange color */
            text-align: center;
            margin: 30px auto;
            width: 80%;
            background-color: #F9F9F9; /* Light background for header */
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            animation: fadeIn 1.5s ease-in-out;
        }
        .description-box {
            background-color: #FFFFFF; /* White background color */
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 30px;
            font-size: 16px;
            color: #2E2E3A; /* Darker text color */
            font-weight: bold;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            animation: slideIn 1s ease-in-out;
        }
        .description-box span {
            color: #FF6F00; /* Bright orange color for key points */
        }
        .input-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        .input-container input, .input-container button {
            font-size: 16px;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #FF6F00; /* Bright orange border */
            background-color: #FFFFFF; /* White background for input fields and button */
            color: #2E2E3A; /* Darker text color */
        }
        .input-container input {
            width: 80%;
            max-width: 450px;
        }
        .input-container button {
            background-color: #FF6F00; /* Bright orange button */
            color: white;
            cursor: pointer;
            border: none;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease;
        }
        .input-container button:hover {
            background-color: #E65C00; /* Darker orange for hover effect */
        }
        .notification-success {
            margin-top: 20px;
            padding: 15px;
            background-color: #4CAF50; /* Green background for success */
            color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            font-weight: bold;
            text-align: center;
        }
        .email-preview {
            margin-top: 30px;
            padding: 20px;
            border: none;
            border-radius: 20px;
            background-color: #FFFFFF; /* White background for email preview */
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            animation: slideIn 1s ease-in-out;
        }
        .email-preview h4 {
            margin-bottom: 15px;
            color: #FF6F00; /* Bright orange color */
            font-weight: bold;
        }
        .email-preview p {
            margin-bottom: 15px;
            color: #2E2E3A; /* Darker text color */
        }
        .email-preview h3 {
            margin-bottom: 15px;
            color: #FF6F00; /* Bright orange color */
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { transform: translateY(-20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
    <div class="header">Notification Manager</div>
    <div class="description-box">
        <p>Fill out the form below to send a notification email about the top product category at risk of expiry.</p>
        <p>Ensure that you enter a <span>valid recipient email address</span> and provide your <span>name</span> to personalize the message.</p>
    </div>
    """, unsafe_allow_html=True)

    # Input fields for notification
    with st.form(key='notification_form'):
        recipient_email = st.text_input("Enter Recipient Email:")
        user_name = st.text_input("Enter Your Name:", "")
        send_button = st.form_submit_button("Send Notification")

        if send_button:
            if recipient_email and user_name:
                try:
                    validate_email(recipient_email)

                    # Fetch the optimal SEO product
                    optimal_product = 1

                    if optimal_product:
                        # Display progress bar
                        progress_bar = st.progress(0)

                        # Simulate email sending process
                        for i in range(100):
                            time.sleep(0.03)
                            progress_bar.progress(i + 1)

                        # Email configuration
                        # Email configuration
                        smtp_server = 'smtp.gmail.com'
                        smtp_port = 587
                        sender_email = 'winstep.noti@gmail.com'
                        sender_password = 'fxlq eipo zdmw tleo' 

                        # Email content
                        subject = 'Top Product SEO Analysis'
                        body = f"""
                        <html>
                        <body>
                            <p>Dear {user_name},</p>
                            <p>The product with optimal search optimization currently in the database is:</p>
                            <h3>Abercrombie and Fitch: T-Shirt</h3>
                            <p>Optimal SEO Term <strong>Orange A&F Tee</strong></p>
                            <p>Please reply to this email for a manual response.</p>
                            <p>Best,<br>iCETS Infosys</p>
                        </body>
                        </html>
                        """
                        msg = MIMEMultipart('alternative')
                        msg['Subject'] = subject
                        msg['From'] = sender_email
                        msg['To'] = recipient_email
                        msg.attach(MIMEText(body, 'html'))

                        # Send email
                        with smtplib.SMTP(smtp_server, smtp_port) as server:
                            server.starttls()
                            server.login(sender_email, sender_password)
                            server.sendmail(sender_email, recipient_email, msg.as_string())
                        
                        st.markdown('<div class="notification-success">Notification sent successfully!</div>', unsafe_allow_html=True)
                    else:
                        st.error("No optimal product found.")
                except EmailNotValidError as e:
                    st.error(f"Invalid email address: {e}")
            else:
                st.error("Please fill in all fields.")
