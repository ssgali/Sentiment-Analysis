import streamlit as st
from typing import Dict
from collections import OrderedDict
import json

@st.cache_data
def load_reviews() -> OrderedDict:
    """
    Load reviews from a JSON file with error handling.
    
    Returns:
        OrderedDict: Loaded reviews or empty OrderedDict if file not found
    """
    try:
        with open('merged_reviews.json', 'r') as file:
            return OrderedDict(json.load(file))
    except FileNotFoundError:
        st.error("Reviews file not found. Please ensure 'merged_reviews.json' exists.")
        return OrderedDict()

def filter_reviews(
    classified_reviews: OrderedDict, 
    search_query: str, 
    min_overall_rating: float,
    min_food_rating: float, 
    min_service_rating: float, 
    min_ambience_rating: float
) -> Dict:
    """
    Filter reviews based on search query and rating thresholds.
    
    Args:
        classified_reviews (OrderedDict): Original reviews
        search_query (str): Text to search in review content
        min_* (float): Minimum rating thresholds
    
    Returns:
        Dict: Filtered reviews
    """
    return {
        customer: review for customer, review in classified_reviews.items()
        if (search_query.lower() in review["Content"].lower()) and 
           (float(review["Rating"]["Overall"]) >= min_overall_rating) and
           (float(review["Rating"]["Food"]) >= min_food_rating) and
           (float(review["Rating"]["Service"]) >= min_service_rating) and
           (float(review["Rating"]["Ambience"]) >= min_ambience_rating)
    }
