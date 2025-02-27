import streamlit as st
from review_loader import load_reviews, filter_reviews
from review_renderer import render_review

def main():
    # Configure page
    st.set_page_config(page_title="Restaurant Review Dashboard", page_icon=":restaurant:", layout="wide")
    
    # Optional: Set a dark theme for Streamlit
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1e1e;
    }
    .stMarkdown {
        color: #f0f0f0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🍽️ Restaurant Review Dashboard")

    # Load reviews
    classified_reviews = load_reviews()

    # Sidebar for filtering and search
    st.sidebar.header("Review Filters")
    
    # Search functionality
    search_query = st.sidebar.text_input("Search reviews", "")
    
    # Rating filters
    min_overall_rating = st.sidebar.slider("Minimum Overall Rating", 1, 5, 1)
    min_food_rating = st.sidebar.slider("Minimum Food Rating", 1, 5, 1)
    min_service_rating = st.sidebar.slider("Minimum Service Rating", 1, 5, 1)
    min_ambience_rating = st.sidebar.slider("Minimum Ambience Rating", 1, 5, 1)
    
    # Filter reviews
    filtered_reviews = filter_reviews(
        classified_reviews, 
        search_query, 
        min_overall_rating, 
        min_food_rating, 
        min_service_rating, 
        min_ambience_rating
    )

    # Pagination
    reviews_per_page = 10
    total_reviews = len(filtered_reviews)

    # Initialize page number if not exists
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0

    # Calculate start and end indices
    start_idx = st.session_state.current_page * reviews_per_page
    end_idx = min((st.session_state.current_page + 1) * reviews_per_page, total_reviews)

    # Get reviews to display
    reviews_to_display = list(filtered_reviews.items())[start_idx:end_idx]

    # Display total number of reviews and current page
    st.sidebar.text(f"Total Reviews: {total_reviews}")
    st.sidebar.text(f"Page {st.session_state.current_page + 1} of {(total_reviews // reviews_per_page) + 1}")

    # Display review key in sidebar
    st.sidebar.markdown("""
    ### Review Highlights
    - 🟢 Food-related comments
    - 🔵 Service-related comments
    - 🔴 Other comments
    """)

    # Main content area for reviews
    for customer, review in reviews_to_display:
        st.markdown(render_review(review), unsafe_allow_html=True)

    # Pagination controls
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        if st.button("⬅️ Previous", key="prev_page") and st.session_state.current_page > 0:
            st.session_state.current_page -= 1
            st.rerun()
    
    with col2:
        st.write(f"Page {st.session_state.current_page + 1}")
    
    with col3:
        total_pages = (total_reviews // reviews_per_page) + (1 if total_reviews % reviews_per_page > 0 else 0)
        if st.button("➡️ Next", key="next_page") and st.session_state.current_page < total_pages - 1:
            st.session_state.current_page += 1
            st.rerun()

if __name__ == "__main__":
    main()
