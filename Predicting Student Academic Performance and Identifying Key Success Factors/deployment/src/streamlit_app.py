import streamlit as st
import eda_manzo
import prediction_manzo

page = st.sidebar.selectbox('Choose page', ('Exploratory Data Analysis', 'Prediction'))

if page == 'Exploratory Data Analysis':
    eda_manzo.run()
else:
    prediction_manzo.run()