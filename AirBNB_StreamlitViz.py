import streamlit as st
import emoji
import mysql.connector
import openpyxl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk

mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='ne09ft#rt12gs',
            database='capstone3'
        )
pointer = mydb.cursor(buffered=True)

st.markdown("""
    <style>
        /* Adjust padding in columns */
        .css-1d391kg {
            padding: 4000px;
        }

        /* Adjust the padding and background color of the block container */
        .block-container {
            padding: 5px;
            margin: 2px;  /* Add a semicolon here */
            background-color: #90FF65;
        }

        /* Adjust body styling */
        body {
            line-height: 1.3; 
        }

        /* Change the background color of the main container */
        .main {
            background-color: #90FF65; /* Specify any background color here */
        }
         
        /* Change the background color of the sidebar */
        [data-testid="stSidebar"] {
            background-color: #90FF65; /* Light blue color */
        }
            
        /* Set background color of the chart */
            div[data-testid="stPlotlyChart"] div.plotly-graph-div {
            background-color: transparent !important;
            }
    </style>
""", unsafe_allow_html=True)

top_bar = st.container()
with top_bar:
    my_sticker = emoji.emojize (':love_hotel:')
    st.write(my_sticker)
    html_string = f"<div style='text-align: left;'><h1 style='font-family: aptos display; color:purple; font-size:30px;'>AIRBNB {my_sticker}</h1></div>"
    st.markdown(html_string, unsafe_allow_html=True)
    st.markdown(':rainbow[**_- Data Visualization & Insights_**]', unsafe_allow_html=True)

st.write("\n")

queryt = """SELECT  Market, Country, COUNT(MONTH(Date_Stamp)) as Agg_Listings FROM Air_BNB2 GROUP BY Market, Country;"""
dft = pd.read_sql(queryt, mydb)


querys = """SELECT  COUNT(Listing_url) as Agg_Listings, MONTH(Date_Stamp) as Months FROM Air_BNB2 GROUP BY Months;"""
dfs = pd.read_sql(querys, mydb)
# Plot the seasonality trends
sns.set_style('whitegrid')
plt.figure(figsize=(25, 15))
plt.gcf().set_facecolor('none')

ax = sns.lineplot(data=dfs, x='Months', y='Agg_Listings', marker='o')
ax.set_title('Seasonality Trends in Airbnb Listings', fontsize=30)
ax.set_xlabel('Month', fontsize=20)
ax.set_ylabel('Number of Listings', fontsize=20)
ax.grid(True)

# Increase x-ticks and y-ticks font size
ax.tick_params(axis='x', labelsize=16)
ax.tick_params(axis='y', labelsize=16)

st.pyplot(plt.gcf())  # Show the figure

plt.clf()  # Clear the figure

st.write("\n")

st.write(dft)

st.write("\n")

with st.expander("Observations & Insights"):
    st.write("""Given the locations, we can infer some reasons for the peak months under two categories:
             \n Holidays & Festivities:
             \n   January: Winter holidays and New Year celebrations.
             \n   July: Peak summer vacation period.
             \n   August: Summer vacation period in many countries, leading to increased travel.
             \n   September: End of summer and beginning of fall, still a popular travel time.
             \n   October: Fall season in the Northern Hemisphere, popular for travel due to pleasant weather and events like Halloween.
             \n
             \n Weather Patterns in Peak Months:
             \n   October:
             \n      New York: Mild fall weather, popular for fall foliage.
             \n      Istanbul: Pleasant autumn weather, fewer tourists.
             \n      Hong Kong: End of typhoon season, cooler temperatures.
             \n      Sydney: Spring season, mild and pleasant weather.
             \n      Rio De Janeiro: Spring season, warm weather.
             \n   August:
             \n      New York: Hot and humid summer weather.
             \n      Istanbul: Hot summer weather, peak tourist season.
             \n      Hong Kong: Hot and humid, typhoon season.
             \n      Sydney: Winter season, mild weather.
             \n      Rio De Janeiro: Winter season, mild weather.
             \n   September:
             \n      New York: End of summer, beginning of fall, pleasant weather.
             \n      Istanbul: End of summer, beginning of fall, pleasant weather.
             \n      Hong Kong: End of typhoon season, cooler temperatures.
             \n      Sydney: Spring season, mild and pleasant weather.
             \n      Rio De Janeiro: Spring season, warm weather.
             \n   July:
             \n      New York: Hot and humid summer weather.
             \n      Istanbul: Hot summer weather, peak tourist season.
             \n      Hong Kong: Hot and humid, typhoon season.
             \n      Sydney: Winter season, mild weather.
             \n      Rio De Janeiro: Winter season, mild weather.
             \n   January:
             \n      New York: Cold winter weather, holiday season.
             \n      Istanbul: Cold winter weather, fewer tourists.
             \n      Hong Kong: Mild winter weather, Chinese New Year preparations.
             \n      Sydney: Summer season, hot weather, peak tourist season.
             \n      Rio De Janeiro: Summer season, hot weather, peak tourist season.
             \n Summary:
             \n October and September: Pleasant fall weather in many locations, fewer tourists, and events like Halloween.
             \n August and July: Peak summer vacation period, hot weather, and high tourist activity.
             \n January: Winter holidays, New Year celebrations, and peak summer season in the Southern Hemisphere.
             \n These weather patterns and seasonal events likely contribute to the increase in Airbnb listings during these peak months.
             """)
    
st.divider()

queryk = """Select Country, ROUND(Avg(Price),2) as Average_Price FROM Air_BNB2 Group by Country;"""
dfk = pd.read_sql(queryk, mydb)
sns.set_style('whitegrid')
ax = sns.barplot(x='Average_Price', y='Country', data=dfk)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=17)
ax.set_yticklabels(ax.get_yticklabels(), fontsize=17)
ax.set_xlabel('Average Price($)', fontsize=24, fontstyle='italic')
ax.set_ylabel('Country', fontsize=24, fontstyle='italic')
ax.set_title('Average Price of Listings By Country', fontsize=35, fontstyle='italic', fontweight='bold')
ax.set_facecolor('none')
ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
plt.gcf().set_facecolor('none')

st.pyplot(plt.gcf())

plt.close()

with st.expander(""):
    st.write("""The price distribution shows a right-skewed distribution with most listings having lower prices, but a few listings have very high prices.
             \n The top 5 countries with the highest average price for Airbnb listings are:
             \n Hong Kong: 714.32$
             \n China: 384.22$
             \n Turkey: 253.78$
             \n Brazil: 242.60$
             \n Australia: 164.61$ """)

st.divider()


querym = """SELECT Country, ROUND(AVG(CAST(Security_deposit AS DECIMAL(10, 2))),2) AS Average_Security_Deposit, COUNT(LISTING_URL) AS Aggregate_Listing,
MAX(LATITUDE) AS Latitude, 
MAX(LONGITUDE) AS Longitude
FROM Air_bnb2
GROUP BY Country;"""
st.write ("Average Security Deposit Required")
st.image('C:/Users/my pc/Pictures/AirBNB Charts/AvgSD.png', caption='Optional caption', use_column_width=True)
with st.expander("The top 5 countries with the highest security deposits for Airbnb listings are:"):
    st.write("""Hong Kong: 701.5$
             \n Brazil: 809.3$
             \n China: 440.4$
             \n Australia: 294.6$
             \n Turkey: 229.7$
              """)
# tooltip = 
# st.map(data=dfm, latitude='Latitude', longitude='Longitude', color='#f56342', size=None, 
#        zoom=None, use_container_width=True tooltip = )
# Error: Framebuffer error 36061

st.divider()
st.write('\n')
dfm = pd.read_sql(querym,mydb)

# Create choropleth map
fig = px.choropleth(
    dfm,
    locations="Country",
    locationmode="country names",
    color="Average_Security_Deposit",
    hover_name="Average_Security_Deposit",
    color_continuous_scale=px.colors.sequential.Plasma
)

# Update layout
fig.update_layout(
    title="",
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

# Display the choropleth map in Streamlit
st.title("Average Security Deposit Required by Country")
st.plotly_chart(fig)


queryc = """SELECT Country, Property_type,
    MIN(Cleaning_Fee) AS Min_Cleaning_Fee, 
    MAX(Cleaning_Fee) AS Max_Cleaning_Fee,
    (SELECT MIN(Cleaning_Fee)
     FROM Air_BNB2 AS sub
     WHERE sub.Country = main.Country AND sub.Cleaning_Fee > 0) AS Next_Min_Cleaning_Fee
FROM 
    Air_BNB2 AS main
GROUP BY 
    Country, Property_type; """
dfc = pd.read_sql(queryc, mydb)
Max_Cleaning_Fee = dfc['Max_Cleaning_Fee']
Next_Min_Cleaning_Fee = dfc['Next_Min_Cleaning_Fee']
df_long = pd.melt(dfc, id_vars=['Country','Property_type'], value_vars=['Max_Cleaning_Fee', 'Next_Min_Cleaning_Fee'], 
                  var_name='Fee_Type', value_name='Cleaning_Fee')

sns.set_style('whitegrid')
plt.figure(figsize=(15, 10))
plt.gcf().set_facecolor('none')
ax = sns.barplot(data=df_long, x='Country', y='Cleaning_Fee', hue='Fee_Type')
ax.set_title('Max and Next Min Cleaning Fee by Country', fontsize=20)
ax.set_xlabel('Country', fontsize=16)
ax.set_ylabel('Cleaning Fee', fontsize=16)
ax.tick_params(axis='x', labelsize=14, rotation=45)
ax.tick_params(axis='y', labelsize=14)

plt.legend(title='Fee Type', fontsize=14)
st.pyplot(plt.gcf())  # Show the figure

plt.clf()  # Clear the figure

st.write(dfc)
with st.expander("The top 5 countries with the highest cleaning fee for Airbnb listings are:"):
    st.write("""Brazil: 2000 to 19 $
             \n Hong Kong: 701.5 to 30 $
             \n US: 910 to 5$
             \n Australia: 693 to 7 $
             \n Turkey: 596 t0 22 $ 
              """)
st.write('\n')

st.write("Property Types of Listings by Country")
u_choice = st.selectbox("Country", ("United States", "Turkey", "Hong Kong", "Australia", "Brazil", "Portugal", "Canada", "Spain", "China" ))
queryp = f"""SELECT Country, Property_type, COUNT(Listing_url) as Aggregate_Listings from Air_BNB2 WHERE Country = "{u_choice}" GROUP BY Country, Property_Type;""" 
dfp = pd.read_sql(queryp, mydb)
fig = px.sunburst(data_frame=dfp,path=['Country','Property_type','Aggregate_Listings'],maxdepth=3,width=800,height=600,color_discrete_sequence=px.colors.qualitative.Dark24 ) 
st.plotly_chart(fig)



st.write('\n')

queryo = """
WITH MaxProperty AS (
    SELECT 
        Country, 
        Property_type, 
        COUNT(Listing_url) AS Aggregate_Listings,
        ROW_NUMBER() OVER (PARTITION BY Country ORDER BY COUNT(Listing_url) DESC) AS rn
    FROM 
        Air_BNB2
    GROUP BY 
        Country, Property_type
)
SELECT 
    Country, 
    Property_type, 
    Aggregate_Listings
FROM 
    MaxProperty
WHERE 
    rn = 1;
"""
df = pd.read_sql(queryo, mydb)
st.write(df)

st.write('\n')

st. markdown("TOP TOURISTS SPOTS")
v_choice = st.select_slider("Country", ("United States", "Turkey", "Hong Kong", "Australia", "Brazil", "Portugal", "Canada", "Spain", "China" ))
queryq = f"""SELECT Country, Market, Suburb, COUNT(Listing_url) as Aggregate_Listings from Air_BNB2 WHERE Country = "{v_choice}" GROUP BY Country, Market, Suburb;""" 
dfq = pd.read_sql(queryq, mydb)
for index, row in dfq.iterrows():
    # If 'Market' is empty string and 'Suburb' is not empty string, fill 'Market' with the value of 'Suburb'
    if row['Market'] == '' and row['Suburb'] != '':
        dfq.at[index, 'Market'] = row['Suburb']
    # If 'Suburb' is empty string and 'Market' is not empty string, fill 'Suburb' with the value of 'Market'
    elif row['Suburb'] == '' and row['Market'] != '':
        dfq.at[index, 'Suburb'] = row['Market']
dfq_sorted = dfq.sort_values(by='Aggregate_Listings', ascending=False)
fig = px.sunburst(data_frame=dfq,path=['Country','Market', 'Suburb','Aggregate_Listings'],maxdepth=3,width=800,height=600,color_discrete_sequence=px.colors.qualitative.Dark24 ) 
st.plotly_chart(fig)

st.write(dfq_sorted)

st.write('\n')

st.markdown("Current & Future Trends")
st.image('C:/Users/my pc/Pictures/AirBNB Charts/Current Trends.png', caption='Optional caption', use_column_width=True)
with st.expander("Click for an overview"):
    st.write("""The from the charts seen thus far it can be observed that the AirBNB has been maintaining almost steady pricing.
             \n The available accomodations trend line also merges with the average availability line showing there is a steady but sure flow of occupants for the listings.
             \n Also the trend line of rating plot shows shows a remarkable explosion in customer base and/or the services offered.
              """)
st.write('\n')
st.image('C:/Users/my pc/Pictures/AirBNB Charts/Future Trends.png', caption='Optional caption', use_column_width=True)
with st.expander("Click for an overview"):
    st.write("""•	The most common property type is "Apartment".
•	The most common room type is "Entire home/apt".
•	The price distribution shows a right-skewed distribution with most listings having lower prices, but a few listings have very high prices.
•	The listings sorted by price, showshighest-priced listings for each property type.
    The review of listing locations/amenities/and avarage availabilty shows preference of people for short vacations/with access to action if needed/affordable rates.
Local policies and regulations can significantly impact Airbnb listings, especially during peak months. Here are some key factors to consider:
1. Regulations on Short-Term Rentals:
•	New York: Strict regulations limit short-term rentals to 30 days or less unless the host is present. This can reduce the number of available listings during peak months.
•	Istanbul: Regulations are less stringent, allowing for more flexibility in short-term rentals.
•	Hong Kong: Requires a license for short-term rentals, which can limit the number of listings.
•	Sydney: Regulations vary by region, with some areas imposing limits on the number of days a property can be rented short-term.
•	Rio De Janeiro: Regulations are relatively lenient, allowing for a higher number of listings.
2. Taxation Policies:
•	New York: Hosts are required to pay hotel taxes, which can increase the cost for guests and potentially reduce demand.
•	Istanbul: Tax policies are less stringent, making it more attractive for hosts.
•	Hong Kong: Hosts must pay taxes on rental income, which can impact profitability.
•	Sydney: Hosts are required to pay income tax on rental earnings, which can affect the number of listings.
•	Rio De Janeiro: Tax policies are relatively lenient, encouraging more listings.
3. Zoning Laws:
•	New York: Zoning laws restrict short-term rentals in certain areas, reducing the number of available listings.
•	Istanbul: Zoning laws are less restrictive, allowing for more flexibility in short-term rentals.
•	Hong Kong: Zoning laws can limit the availability of short-term rentals in certain areas.
•	Sydney: Zoning laws vary by region, with some areas imposing restrictions on short-term rentals.
•	Rio De Janeiro: Zoning laws are relatively lenient, allowing for more listings.
4. Licensing Requirements:
•	New York: Requires hosts to register with the city, which can limit the number of listings.
•	Istanbul: Licensing requirements are less stringent, allowing for more flexibility.
•	Hong Kong: Requires a license for short-term rentals, which can limit the number of listings.
•	Sydney: Licensing requirements vary by region, with some areas imposing strict requirements.
•	Rio De Janeiro: Licensing requirements are relatively lenient, encouraging more listings.
5. Impact of Events and Festivals:
•	New York: Events like Halloween and New Year's Eve can increase demand for short-term rentals.
•	Istanbul: Cultural festivals and events can attract tourists, increasing demand.
•	Hong Kong: Events like Chinese New Year can increase demand for short-term rentals.
•	Sydney: Events like New Year's Eve and the Sydney Festival can increase demand.
•	Rio De Janeiro: Events like Carnival can significantly increase demand for short-term rentals.
Summary:
Local policies and regulations can either restrict or encourage the number of Airbnb listings during peak months. 
Stricter regulations, higher taxes, and stringent zoning laws can reduce the number of available listings, while lenient policies and 
high-demand events can increase the number of listings""")



    










