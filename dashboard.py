# Main Author: Shreeniket Bendre
# Northwestern University
# Infosys InStep
# Jun 24 2024
# dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
import subprocess
import json
import requests
from bs4 import BeautifulSoup
from time import sleep


def display_home_page():
    display_dashboard()
def scrape_google_search_results(term, site=None):
    query = f"site:{site} {term}" if site else term
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.find_all('h3'):
        title = item.get_text()
        parent = item.find_parent('a')
        link = parent['href'] if parent and 'href' in parent.attrs else 'No link found'
        results.append({'title': title, 'url': link, 'query': term, 'site': site or 'our platform'})

    return results

def rank_terms_by_seo(df_results):
    term_counts = df_results['query'].value_counts().reset_index()
    term_counts.columns = ['Term', 'Count']
    
    # Rank by count
    term_counts['Rank'] = term_counts['Count'].rank(ascending=False)
    
    return term_counts

def display_dashboard():
    st.title('SEO Term Comparison Dashboard')
    st.write('Welcome to the SEO Term Comparison Dashboard!')

    term = st.text_input('Enter a search term', '')
    sites = ["shein.com", "temu.com", "amazon.com", "ebay.com", "walmart.com", "bestbuy.com", "target.com", "etsy.com", "aliexpress.com", "homedepot.com"]
    if not term:
        st.warning('Please enter a search term.')
        return

    st.write('Fetching data...')
    all_results = []
    
    # Perform Google search for each site
    for site in sites:
        site_results = scrape_google_search_results(term, site)
        all_results.extend(site_results)
    
    # Perform a generic Google search
    google_results = scrape_google_search_results(term)
    all_results.extend(google_results)

    # Create DataFrame
    df_results = pd.DataFrame(all_results)

    # Display results
    st.subheader('Search Results Comparison')
    if not df_results.empty:
        chart = alt.Chart(df_results).mark_bar().encode(
            x=alt.X('site:N', title='Site'),
            y='count():Q',
            color='site:N',
            tooltip=['site:N', 'count():Q']
        ).properties(title='Search Results Count by Site')

        st.altair_chart(chart, use_container_width=True)
    
    # Rank sites based on result count
    st.subheader('SEO Optimization Ranking')
    site_ranking = df_results['site'].value_counts().reset_index()
    site_ranking.columns = ['Site', 'Result Count']

    st.write(site_ranking)

    # Rank terms based on their SEO strength
    st.subheader('Term Strength Ranking')
    term_strength = rank_terms_by_seo(df_results)
    st.write(term_strength)

    # Suggest possible search terms
    st.subheader('Suggested Search Terms')
    suggested_terms = [f"{term} {site.split('.')[0]}" for site in sites]
    st.write(suggested_terms)

def display_seo_optimization():
    st.title('SEO Optimization')
    st.write('Welcome to the SEO Optimization')

    term = st.text_input('Enter a search term for optimization', '')
    if not term:
        st.warning('Please enter a search term.')
        return

    # Scrape data for the term
    st.write('Fetching data...')
    results = scrape_google_search_results(term)
    df_results = pd.DataFrame(results)

    # Display results
    st.subheader('Search Results')
    if not df_results.empty:
        st.write(df_results)
    
    # Rank terms based on their SEO strength
    st.subheader('Term Strength Ranking')
    term_strength = rank_terms_by_seo(df_results)
    st.write(term_strength)

    # Suggest possible search terms
    st.subheader('Suggested Search Terms')
    suggested_terms = [f"{term} suggestion {i}" for i in range(1, 6)]
    st.write(suggested_terms)
