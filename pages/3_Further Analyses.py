import streamlit as st
import pandas as pd
import altair as alt
from scrapper import get_dict
from data_filters import *

def create_comparison_graphs():
    # Sample data for two restaurants
    main_restaraunt = get_dict("reviews.json")
    second_restaraunt = get_dict(st.session_state["Scrapped"])
    
    start_date = st.session_state["start_date"]
    end_date = st.session_state["end_date"]
    
    filtered_1 = filter_reviews(main_restaraunt,start_date,end_date,True,key = "Rating")
    filtered_2 = filter_reviews(second_restaraunt,start_date,end_date,True,key = "Rating")

    data_1 = get_average_reviews(filtered_1)
    data_2 = get_average_reviews(filtered_2)
    category = ['Overall', 'Food', 'Service', 'Ambiance']

    metric = "Metric"
    restaraunt_name_1 = "Metropolitan Grill"                # Default Name
    restaraunt_name_2 = (str(st.session_state["Scrapped"])).removesuffix("_reviews.json").replace("_"," ")
    
    data = pd.DataFrame({
        metric: category,
        restaraunt_name_1: data_1,
        restaraunt_name_2: data_2
    })
    
    review_data = pd.DataFrame({
        'Rating': [1, 2, 3, 4, 5],
        restaraunt_name_2: get_ratings(filtered_2),
        restaraunt_name_1: get_ratings(filtered_1)
    })
    
    # Bar Chart for Restaurant 1
    bar_chart_1 = alt.Chart(data).mark_bar(opacity=0.8, color='#FF6347').encode(
    x=alt.X('Metric:N', title='Evaluation Metrics'),
    y=alt.Y(f'{restaraunt_name_1}:Q', title='Rating (out of 5)'),
    tooltip=['Metric', alt.Tooltip(f'{restaraunt_name_1}:Q', title='Rating')]
    ).properties(
    title=f'{restaraunt_name_1} Metrics Comparison'
    )

    # Bar Chart for Restaurant 2
    bar_chart_2 = alt.Chart(data).mark_bar(opacity=0.8, color='#FFD700').encode(
        x=alt.X('Metric:N', title='Evaluation Metrics'),
        y=alt.Y(f'{restaraunt_name_2}:Q', title='Rating (out of 5)'),
        tooltip=['Metric', alt.Tooltip(f'{restaraunt_name_2}:Q', title='Rating')]
    ).properties(
        title=f'{restaraunt_name_2} Metrics Comparison'
    )

    distribution_chart_1 = alt.Chart(review_data).mark_bar(opacity=0.8, color='#FF6347').encode(
    x=alt.X('Rating:O', title='Review Rating'),
    y=alt.Y(f'{restaraunt_name_1}:Q', title='Number of Reviews'),
    tooltip=[alt.Tooltip('Rating:O', title='Rating'),
             alt.Tooltip(f'{restaraunt_name_1}:Q', title='Number of Reviews')]
    ).properties(
        title=f'{restaraunt_name_1} Review Distribution'
    )

    # Bar Chart for Review Distribution - Restaurant 2
    distribution_chart_2 = alt.Chart(review_data).mark_bar(opacity=0.8, color='#FFD700').encode(
        x=alt.X('Rating:O', title='Review Rating'),
        y=alt.Y(f'{restaraunt_name_2}:Q', title='Number of Reviews'),
        tooltip=[alt.Tooltip('Rating:O', title='Rating'),
                alt.Tooltip(f'{restaraunt_name_2}:Q', title='Number of Reviews')]
    ).properties(
        title=f'{restaraunt_name_2} Review Distribution'
    )

    
    st.title("Restaurant Comparison Analysis")

    st.header(f"{restaraunt_name_1} Metrics Comparison")
    st.altair_chart(bar_chart_1, use_container_width=True)
    st.header(f"{restaraunt_name_2} Metrics Comparison")
    st.altair_chart(bar_chart_2, use_container_width=True)

    st.subheader(f"{restaraunt_name_1} Review Distribution")
    st.altair_chart(distribution_chart_1, use_container_width=True)
    st.subheader(f"{restaraunt_name_2} Review Distribution")
    st.altair_chart(distribution_chart_2, use_container_width=True)

    # Summary Statistics
    st.header("Summary Statistics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(restaraunt_name_1)
        st.metric("Overall Rating", round(sum(data_1)/len(data_1),2))
        st.metric("Total Reviews", len(filtered_1))
    
    with col2:
        st.subheader(restaraunt_name_2)
        st.metric("Overall Rating", round(sum(data_2)/len(data_2),2))
        st.metric("Total Reviews", len(filtered_2))
   

def main():
    # Initialize session state if not exists
    if "Further_analysis" not in st.session_state:
        st.session_state["Further_analysis"] = False
    # Conditional rendering
    if st.session_state["Further_analysis"]:
        # Call your existing create_comparison_graphs() function
        create_comparison_graphs()
    else:
        st.title("Analysis Prerequisite")
    
        st.markdown("""
        ## 🔍 Competitor Analysis Required
        
        Before accessing this detailed analysis, you must first:
        
        1. Navigate to the Competitor Analysis page
        2. Complete the initial competitor analysis
        3. Return to this page
        
        """)
        
        st.warning("Please go to the Competitor Analysis page to proceed.")
        
        st.image("https://img.icons8.com/ios/250/000000/cancel-2.png", width=200)

if __name__ == "__main__":
    main()