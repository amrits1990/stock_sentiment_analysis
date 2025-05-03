# Streamlit frontend
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

BACKEND_URL = 'http://localhost:9321'

st.title('Stock Sentiment Dashboard')
option = st.radio("Choose Input Method", ['Upload Company List', 'Select Index'])
since = st.text_input('Since Date (YYYY-MM-DD)', '2025-01-01')
num_items = st.number_input('Number of posts/articles per source', min_value=1, max_value=100, value=20)

if option == 'Upload Company List':
    file = st.file_uploader('Upload text file with company names')
    if file and st.button('Analyze'):
        files = {'file': file.getvalue()}
        params = {'since': since, 'num_items': num_items}
        res = requests.post(f'{BACKEND_URL}/analyze_list', files={'file': file}, params=params)
        data = res.json()

elif option == 'Select Index':
    index = st.selectbox('Select Index', ['NIFTY 50', 'SENSEX', 'BANK NIFTY'])
    if index and st.button('Analyze Index'):
        params = {'since': since, 'num_items': num_items}
        res = requests.get(f'{BACKEND_URL}/analyze_index/{index}', params=params)
        data = res.json()

if 'data' in locals():
    for company, score in data.items():
        st.subheader(company)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Sentiment %"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
        ))
        st.plotly_chart(fig, key=company)