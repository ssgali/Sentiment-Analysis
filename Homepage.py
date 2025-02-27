import streamlit as st

def main():
    # Set page configuration
    st.set_page_config(page_title="Welcome to Our Dashboard", page_icon=":wave:", layout="wide")
    
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

    # Title with a welcoming message
    st.title("👋 Welcome to Our Website!")

    # Description
    st.markdown("""
    <div style="font-size: 20px; color: #f0f0f0;">
        <p>Welcome to the Restaurant Review Website. Here you can explore detailed reviews from customers, with insights on food quality, service, and ambience.</p>
        <p>Use the sidebar to navigate through different reviews and filters.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add some sections for the design
    st.markdown("---")
    
if __name__ == "__main__":
    main()
