import streamlit as st
import validators
import altair as alt
from datetime import datetime
from scrapper import scrape_website,get_dict
from data_filters import *
import pandas as pd

if "Scrapped" not in st.session_state:
    st.session_state["Scrapped"] = ""

if "url" not in st.session_state:
    st.session_state["url"] = ""

if "allow" not in st.session_state:
    st.session_state["allow"] = False

if "Further_analysis" not in st.session_state:
    st.session_state["Further_analysis"] = False
    
if "start_date" not in st.session_state:
    st.session_state["start_date"] = datetime(2023, 1, 1)

if "end_date" not in st.session_state:
    st.session_state["end_date"] = datetime.now().date()

main_restaraunt = get_dict("reviews.json")

def create_review_chart(combined_reviews: pd.DataFrame) -> alt.Chart:
    """
    Create an interactive Altair chart for restaurant reviews.
    
    Args:
        combined_reviews (pd.DataFrame): Combined review data
    
    Returns:
        alt.Chart: Interactive Altair chart
    """
    # Interactive hover selection
    hover = alt.selection_point(
        fields=["Date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Base line chart
    lines = (
        alt.Chart(combined_reviews, title="Competitor Analysis")
        .mark_line()
        .encode(
            x="Date",
            y="Ratings",
            color="Restaurant",
        )
    )
    # Hover points
    points = lines.transform_filter(hover).mark_circle(size=65)

    tooltips = (
        alt.Chart(combined_reviews)
        .mark_rule()
        .encode(
            x="yearmonthdate(Date)",
            y="Ratings",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Date", title="Date"),
                alt.Tooltip("Ratings", title="Rating(Out of 5)"),
            ],
        )
        .add_params(hover)
    )
    datalayers = lines + points + tooltips
    st.altair_chart(datalayers, use_container_width=True)

def comperator(url: str):
    st.write("🔄 **Scraping the website... Please wait.**")
    if st.session_state["Scrapped"] == "":
        file_name = scrape_website(url)
        st.session_state["Scrapped"] = file_name
        st.balloons()
    else:
        file_name = st.session_state["Scrapped"]
    st.success("✅ Scraping completed successfully!")
    
    second_restraunt = get_dict(file_name)
    
    st.subheader("Select Date Range")
    # Create columns for date inputs
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date", 
            max_value=datetime.now().date(),
            value=datetime(2023, 1, 1),
        )
    
    with col2:
        end_date = st.date_input(
            "End Date", 
            min_value=st.session_state["start_date"],
            max_value= datetime.now().date(),
            value= datetime.now().date(),
        )
    st.session_state["start_date"] = start_date
    st.session_state["end_date"] = end_date
    st.success(f"Selected Date Range: {start_date} to {end_date}")
    
    filtered_reviews_1 = filter_reviews(main_restaraunt,start_date,end_date)
    filtered_reviews_2 = filter_reviews(second_restraunt,start_date,end_date) 
    
    restaurant1_df = create_review_df(filtered_reviews_1, "Metropolitan Grill")
    restaurant2_df = create_review_df(filtered_reviews_2, file_name.removesuffix("_reviews.json"))
    combined_reviews = pd.concat([restaurant1_df, restaurant2_df])       
    # Create and display chart
    create_review_chart(combined_reviews)
    st.session_state["Further_analysis"] = True

def main():
    # Configure page
    st.set_page_config(page_title="Competitor Analysis", page_icon=":mag:", layout="wide")
    
    # Apply dark theme similar to previous app
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
    }
    .stMarkdown {
        color: #f0f0f0;
    }
    .stTextInput > div > div > input {
        background-color: #2c2c2c;
        color: #f0f0f0;
        border: 1px solid #444;
    }
    .stButton > button {
        background-color: #4a4a4a;
        color: #f0f0f0;
        border: 1px solid #666;
    }
    .stButton > button:hover {
        background-color: #5a5a5a;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.title("🔍 Competitor Analysis Tool")
    
    # URL input section
    st.markdown("""
    ### Enter Competitor's URL
    Provide the URL of a restaurant or food-related website you want to analyze.
    """)
    url = st.text_input("Website URL", placeholder="https://example.com")
    
    if st.button("Analyze Competitor") or st.session_state["allow"]:
        # Validate URL
        if not url:
            st.error("Please enter a URL")
            st.session_state["url"] = st.session_state["Scrapped"] = ""
            st.session_state["allow"] = st.session_state["Further_analysis"] = False
        elif not validators.url(url):
            st.error("Invalid URL. Please enter a valid web address.")
            st.session_state["url"] = st.session_state["Scrapped"] = ""
            st.session_state["allow"] = st.session_state["Further_analysis"] = False
        else:
            st.info(f"Analyzing URL: {url}")
            st.markdown("""
            - URL validation complete
            - Preparing for Scrapping
            """)
            st.session_state["allow"] = True
            if st.session_state["url"] == "":
                st.session_state["url"] = url
            elif st.session_state["url"] != url:
                st.session_state["Scrapped"] = ""
            comperator(url)


    # Sidebar for additional information
    st.sidebar.header("Competitor Analysis Guide")
    st.sidebar.markdown("""
    ### How to Use
    1. Enter a complete website URL
    2. Click "Analyze Competitor"
    3. Wait for the Website Scrapping
    4. Select Start and End Date
    5. Time Series Graph will be Plotted
    """)

if __name__ == "__main__":
    main()