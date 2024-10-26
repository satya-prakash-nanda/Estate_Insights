import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import wordcloud, WordCloud
import matplotlib.pyplot as plt
import ast
import seaborn as sns

st.set_page_config(page_title="Plotting Demo")

st.title('Analytics')

st.header('Sector Price per Sqft Geomap')

new_df = pd.read_csv('data_viz1.csv')

# Convert columns to numeric, forcing errors to NaN
new_df[['price','price_per_sqft','built_up_area','latitude','longitude']] = new_df[['price','price_per_sqft','built_up_area','latitude','longitude']].apply(pd.to_numeric, errors='coerce')

# Group by 'sector' and calculate the mean for only the numeric columns
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()


fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=8,
                  mapbox_style="open-street-map",
                  width=800, height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)







st.header('Features Wordcloud')

# # generate wordcloud of the facilities provided for all the sectors combined
# feature_text = pickle.load(open('feature_text.pkl','rb'))
#
# wordcloud = WordCloud(width=800, height=800,
#                       background_color='white',
#                       stopwords=set(['s']),  # Add other stopwords as needed
#                       min_font_size=10).generate(feature_text)
#
# # Set up the plot
# plt.figure(figsize=(8, 8), facecolor=None)
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.tight_layout(pad=0)
#
# # Display the word cloud using Streamlit
# st.pyplot(plt.gcf())




# generate wordcloud of the facilities provided for the sector selected
wordcloud_df = pd.read_csv('wordcloud_df.csv')

# Create a dropdown menu for sector selection
selected_sector = st.selectbox('Select a Sector', sorted(wordcloud_df['sector'].unique()))

# Filter the DataFrame based on the selected sector
sector_df = wordcloud_df[wordcloud_df['sector'] == selected_sector]

# Combine all features in the selected sector into a single text string
main = []
for item in sector_df['features'].dropna().apply(ast.literal_eval):
    main.extend(item)  # Extend the list with features

# Join the features into a single text string for the word cloud
feature_text = ' '.join(main)

st.write('Facilities Provided in' ,selected_sector)

# Generate the WordCloud
wordcloud = WordCloud(width=800, height=800,
                      background_color='white',
                      stopwords=set(['s']),  # Add other stopwords as needed
                      min_font_size=10).generate(feature_text)

# Set up the plot
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)

# Display the word cloud using Streamlit
st.pyplot(plt.gcf())






st.header('Area vs Price')
# new_df will be used for this analytics

property_type = st.selectbox('Select the Property Type',['Flat','House'])

if property_type == 'House':
    fig1 = px.scatter(new_df[new_df['property_type']== 'house'],
                     x="built_up_area",
                     y="price",
                     color="bedRoom",
                     labels={'built_up_area': 'Built Up Area (sq ft)', 'price': 'Price (Crores)',
                             'bedRoom': 'Bedrooms'})
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'],
                     x="built_up_area",
                     y="price",
                     color="bedRoom",
                     labels={'built_up_area': 'Built Up Area (sq ft)', 'price': 'Price (Crores)',
                             'bedRoom': 'Bedrooms'})

# Show the plot in Streamlit
st.plotly_chart(fig1)







st.header('BHK Pie Chart')

sector_options = new_df['sector'].unique().tolist()
sector_options.insert(0,'overall')
selected_sector_2 = st.selectbox('Select Sector',sector_options)


if selected_sector_2=='overall':
    fig2 = px.pie(new_df, names='bedRoom')
    # Show the plot in Streamlit
    st.plotly_chart(fig2)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector_2], names='bedRoom')
    # Show the plot in Streamlit
    st.plotly_chart(fig2)




st.header('Side by Side BHK price Comparision')

temp_df = new_df[new_df['bedRoom'] <= 4]
# Create side-by-side boxplots of the total bill amounts by day
fig3 = px.box(temp_df, x='bedRoom', y='price', title='BHK Price Range')

# Show the plot
st.plotly_chart(fig3)







# Set the header for the distplot
st.header('Overlayed Distplot for Property Type')

# Create dropdown for sector selection

selected_sector_3 = st.selectbox('Select Sector', sector_options, key='sector_selection_2')

# Set up the matplotlib figure
plt.figure(figsize=(10, 6))

# If 'overall' is selected, create the distplot for all sectors
if selected_sector_3 == 'overall':
    # Plot the distribution for houses
    sns.histplot(new_df[new_df['property_type'] == 'house']['price'],
                 kde=True,
                 color='blue',
                 label='House',
                 stat='density',
                 bins=30)

    # Plot the distribution for flats
    sns.histplot(new_df[new_df['property_type'] == 'flat']['price'],
                 kde=True,
                 color='orange',
                 label='Flat',
                 stat='density',
                 bins=30)

    # Add titles and labels
    plt.title('Price Distribution for House vs Flat (Overall)')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.legend()  # Add a legend to distinguish property types

else:
    # If a specific sector is selected, show the distplot for that sector
    sns.histplot(new_df[new_df['sector'] == selected_sector_3][new_df['property_type'] == 'house']['price'],
                 kde=True,
                 color='blue',
                 label='House',
                 stat='density',
                 bins=30)

    sns.histplot(new_df[new_df['sector'] == selected_sector_3][new_df['property_type'] == 'flat']['price'],
                 kde=True,
                 color='orange',
                 label='Flat',
                 stat='density',
                 bins=30)

    # Add titles and labels
    plt.title(f'Price Distribution for House vs Flat in {selected_sector_3}')
    plt.xlabel('Price')
    plt.ylabel('Density')
    plt.legend()  # Add a legend to distinguish property types

# Show the distplot in Streamlit
st.pyplot(plt)