import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Estate Insights",
    page_icon="🏠"
)

# Title and subtitle
st.title("🏠 Estate Insights")
st.subheader("Explore Real Estate Trends, Predictions, and Personalized Recommendations")

# Overview of the application
st.markdown("""
Welcome to **Estate Insights**, your one-stop platform for exploring real estate data, predicting property prices, 
and receiving personalized apartment recommendations. This application offers three primary sections:

1. **Analytics Page**:  
   Dive deep into real estate data through insightful visualizations and trends. Discover patterns and factors 
   influencing property prices and neighborhood dynamics.  
   

2. **Price Prediction Page**:  
   Get accurate property price predictions based on multiple features. This tool helps homeowners and buyers make 
   informed decisions by forecasting market trends.  
 

3. **Recommendation Page**:  
   Find the perfect apartment based on your preferences and needs. The recommendation engine leverages advanced algorithms 
   to suggest apartments that match your criteria.  
   

---

Explore these features to make smarter real estate decisions, whether you are an investor, buyer, or simply curious about the market.
""")

# Footer
st.markdown("---")
st.markdown("© 2024 Estate Insights | All Rights Reserved")

