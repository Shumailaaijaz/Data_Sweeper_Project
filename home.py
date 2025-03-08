# First Project of Data Sweeper App in Streamlit Python by Shumaila Aijaz. Part of Growth Mindset. 
# This is the Home Page of the App.
import streamlit as st
import pandas as pd
import plotly.express as px 
from streamlit_option_menu import option_menu

# Page Configurations   
st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="expanded",
)   

# Custom CSS with background image
def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1499750310107-5fef28a66643?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .main-container {
            background: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin: 2rem auto;
            max-width: 800px;
        }
        .header-text {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 1.5rem;
        }
        .feature-card {
            padding: 1.5rem;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
            margin: 1rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# Main Content Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header Section
st.markdown('<div class="header-text">', unsafe_allow_html=True)
st.title("📊 Data Sweeper App")
st.subheader("By Shumaila Aijaz")
st.markdown("</div>", unsafe_allow_html=True)

# Rest of your content remains the same until the button section...

# CTA Section
st.markdown("---")
st.markdown("### Ready to Transform Your Data?")
st.markdown("""
Explore the app's capabilities and start your data transformation journey today!
""")

# Corrected Button Section using Streamlit navigation
if st.button("🧹 Start Cleaning Now →", 
            use_container_width=True,
            type="primary",
            help="Click to go to Data Sweeper App"):
    st.switch_page("pages/data_sweeper.py")  # Assuming your main app is in pages directory

 
#             icon="🧹", use_container_width=True)

# Footer remains the same...