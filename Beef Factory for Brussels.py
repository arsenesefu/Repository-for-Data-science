#!/usr/bin/env python
# coding: utf-8

# Introduction

# Beef Factory is a company based in Paris for selling burgers and sandwiches, currently it works on a project to launch a shop in Brussels .The company has to do a research of the best neighbourhood to launch the new shop. The company is looking for interesting spots including university neighbourhoods, Touristic spots or business districts. So the company’s purpose is to make a list of places of landscape in Brussels, including the nearest univercities, cafes, and shopping stores for each place and business districts.

# Data

# The data used in this project is provided by Foursquare location data. The data are grouped by landscape area, and each area included the information about this area and all information about restaurants, cafes, and stores which in this area.

# Methodology

# Import Libraries ; Define Foursquare Credentials ; Define the city and get its latitude & longitude ; Search for Universities & clean dataframe ; Search for Parks & clean dataframe ; Search for Restaurants & clean dataframe ; Search for Cafeteria & clean dataframe ; Search for Shopping Stores & clean dataframe ; Generate map to visualize hotels, shopping stores and Cafeteria and how they cluster together and Generate map to visualize Park, Restaurant and Cafeteria and how they cluster together.

# Results 

# In[1]:


import requests # to handle requests
import pandas as pd # for data analsysis
import numpy as np # to handle data in a vectorized manner

get_ipython().system('conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
#tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library


# In[2]:


import matplotlib.pyplot as plt


# In[3]:


from sklearn.cluster import KMeans 
from sklearn.datasets.samples_generator import make_blobs


# Define Foursquare Credentials

# In[4]:


ClIENT_ID = 'B43WK3HLCWU3OFUWICBX4CKFQPNIOYAC4FEHYHMZMSRGL2BG' # your Foursquare ID
ClIENT_SECRET = '4PN315EEKH4NUDEVAHJCH0RBLWAENSM2R0N5JQWVJ2O1IOU5' # your Foursquare Secret
VERSION = '20191216'
LIMIT =30
print('Your credentails:')
print('Foursquare_ID: ' + ClIENT_ID)
print('Foursquare_Secret:' + ClIENT_SECRET)


# Define the city and get its latitude & longitude

# In[5]:



# define the city and get its latitude & longitude 
city = 'Brussels'
geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(city)
latitude = location.latitude
longitude = location.longitude
print(latitude, longitude)


# Search for universities

# In[6]:


# search for hotels
search_query = 'université'
radius = 10000

# Define the corresponding URL
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(ClIENT_ID, ClIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[7]:


# Send the GET Request and examine the results
results = requests.get(url).json()
#results


# In[9]:


# assign relevant part of JSON to venues
venues = results['response']['venues']

# tranform venues into a dataframe
dataframe = json_normalize(venues)
dataframe.head()


# 
# Clean university Dataframe

# In[10]:


# keep only columns that include venue name, and anything that is associated with location
clean_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')]+ ['id']
clean_dataframe = dataframe.loc[:,clean_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
clean_dataframe['categories'] = clean_dataframe.apply(get_category_type, axis=1)

# clean column names by keeping only last term
clean_dataframe.columns = [column.split('.')[-1] for column in clean_dataframe.columns]

clean_dataframe.head()


# In[11]:


# delete unnecessary columns
clean_dataframe2= clean_dataframe.drop(['cc', 'city', 'country', 'crossStreet', 'distance', 'formattedAddress',                                        'labeledLatLngs','neighborhood', 'id'], axis=1)
clean_dataframe2


# In[12]:


# delete rows with none values
clean_dataframe3 = clean_dataframe2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
clean_dataframe3


# In[13]:


# delete rows which its category is not university or College library
array= ['University', 'College Library','College Academic Building' ]
university_dataframe= clean_dataframe3.loc[clean_dataframe3['categories'].isin(array)]
university_dataframe


# In[14]:


# delete rows which has duplicate university's name
df_university = university_dataframe.drop_duplicates(subset='name', keep="first")
df_university


# In[ ]:





# Search for Parks

# In[15]:


# search for Parks
search_query = 'Parc'
radius = 10000

# Define the corresponding URL
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(ClIENT_ID, ClIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[16]:


# Send the GET Request and examine the results
presults = requests.get(url).json()
#presults


# In[21]:


# assign relevant part of JSON to venues
venues = presults['response']['venues']

# tranform venues into a dataframe
park_dataframe = json_normalize(venues)
park_dataframe.head()


# Clean Park Dataframe

# In[22]:


# keep only columns that include venue name, and anything that is associated with location
park_clean_columns = ['name', 'categories'] + [col for col in park_dataframe.columns if col.startswith('location.')]+ ['id']
clean_park_dataframe = park_dataframe.loc[:,park_clean_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list1 = row['categories']
    except:
        categories_list1 = row['venue.categories']
        
    if len(categories_list1) == 0:
        return None
    else:
        return categories_list1[0]['name']

# filter the category for each row
clean_park_dataframe['categories'] = clean_park_dataframe.apply(get_category_type, axis=1)

# clean column names by keeping only last term
clean_park_dataframe.columns = [column.split('.')[-1] for column in clean_park_dataframe.columns]

clean_park_dataframe.head()


# In[23]:


# delete unnecessary columns
clean_park_dataframe2= clean_park_dataframe.drop(['cc', 'city', 'country', 'crossStreet', 'distance', 'formattedAddress',                                        'labeledLatLngs', 'id'], axis=1)
clean_park_dataframe2


# In[24]:


# delete rows which its category is not Park
df_park = clean_park_dataframe2[clean_park_dataframe2.categories == 'Park']
df_park


# In[ ]:





# Search for Restaurants

# In[25]:


# search for Restaurants
search_query = 'Restaurant'
radius = 10000

# Define the corresponding URL
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(ClIENT_ID, ClIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[26]:


# Send the GET Request and examine the results
Rresults = requests.get(url).json()
#Rresults


# In[31]:


# assign relevant part of JSON to venues
venues = Rresults['response']['venues']

# tranform venues into a dataframe
Restaurant_dataframe = json_normalize(venues)
Restaurant_dataframe.head()


# Clean Restaurant Dataframe

# In[32]:


Restaurant_clean_columns = ['name', 'categories'] + [col for col in Restaurant_dataframe.columns if col.startswith('location.')]+ ['id']
clean_Restaurant_dataframe = Restaurant_dataframe.loc[:,Restaurant_clean_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list3 = row['categories']
    except:
        categories_list3 = row['venue.categories']
        
    if len(categories_list3) == 0:
        return None
    else:
        return categories_list3[0]['name']

# filter the category for each row
clean_Restaurant_dataframe['categories'] = clean_Restaurant_dataframe.apply(get_category_type, axis=1)

# clean column names by keeping only last term
clean_Restaurant_dataframe.columns = [column.split('.')[-1] for column in clean_Restaurant_dataframe.columns]

clean_Restaurant_dataframe.head()


# In[33]:


# delete unnecessary columns
clean_Restaurant_dataframe2= clean_Restaurant_dataframe.drop(['cc', 'city', 'country', 'crossStreet', 'distance', 'formattedAddress',                                        'labeledLatLngs', 'neighborhood', 'id'], axis=1)
clean_Restaurant_dataframe2


# In[34]:


# delete rows with none values
df_Restaurant = clean_Restaurant_dataframe2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
df_Restaurant


# Search for Cafeteria

# In[35]:


# search for Cafeteria
search_query = 'Cafeteria'
radius = 10000

# Define the corresponding URL
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(ClIENT_ID, ClIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[36]:


# Send the GET Request and examine the results
cresults = requests.get(url).json()
#cresults


# In[38]:


# assign relevant part of JSON to venues
venues = cresults['response']['venues']

# tranform venues into a dataframe
Cafeteria_dataframe = json_normalize(venues)
Cafeteria_dataframe.head()


# Clean Cafeteria Dataframe

# In[39]:


# keep only columns that include venue name, and anything that is associated with location
Cafeteria_clean_columns = ['name', 'categories'] + [col for col in Cafeteria_dataframe.columns if col.startswith('location.')]+ ['id']
clean_Cafeteria_dataframe = Cafeteria_dataframe.loc[:,Cafeteria_clean_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list4 = row['categories']
    except:
        categories_list4 = row['venue.categories']
        
    if len(categories_list4) == 0:
        return None
    else:
        return categories_list4[0]['name']

# filter the category for each row
clean_Cafeteria_dataframe['categories'] = clean_Cafeteria_dataframe.apply(get_category_type, axis=1)

# clean column names by keeping only last term
clean_Cafeteria_dataframe.columns = [column.split('.')[-1] for column in clean_Cafeteria_dataframe.columns]

clean_Cafeteria_dataframe.head()


# In[40]:


# delete unnecessary columns
clean_Cafeteria_dataframe2= clean_Cafeteria_dataframe.drop(['cc', 'city', 'country', 'distance', 'formattedAddress',                                        'labeledLatLngs', 'id'], axis=1)
clean_Cafeteria_dataframe2


# In[41]:


# delete rows with none values
df_Cafeteria = clean_Cafeteria_dataframe2.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
df_Cafeteria


# Search for Shopping Stores

# In[42]:


# search for Shopping
search_query = 'Shopping'
radius = 10000

# Define the corresponding URL
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&v={}&query={}&radius={}&limit={}'.format(ClIENT_ID, ClIENT_SECRET, latitude, longitude, VERSION, search_query, radius, LIMIT)
url


# In[43]:


# Send the GET Request and examine the results
sresults = requests.get(url).json()
#sresults


# In[45]:


# assign relevant part of JSON to venues
venues = sresults['response']['venues']

# tranform venues into a dataframe
Shopping_dataframe = json_normalize(venues)
Shopping_dataframe.head()


# Clean Shopping Dataframe

# In[46]:


# keep only columns that include venue name, and anything that is associated with location
Shopping_clean_columns = ['name', 'categories'] + [col for col in Shopping_dataframe.columns if col.startswith('location.')]+ ['id']
clean_Shopping_dataframe = Shopping_dataframe.loc[:,Shopping_clean_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list5 = row['categories']
    except:
        categories_list5 = row['venue.categories']
        
    if len(categories_list5) == 0:
        return None
    else:
        return categories_list5[0]['name']

# filter the category for each row
clean_Shopping_dataframe['categories'] = clean_Shopping_dataframe.apply(get_category_type, axis=1)

# clean column names by keeping only last term
clean_Shopping_dataframe.columns = [column.split('.')[-1] for column in clean_Shopping_dataframe.columns]

clean_Shopping_dataframe.head()


# In[48]:


# delete unnecessary columns
clean_Shopping_dataframe2= clean_Shopping_dataframe.drop(['cc', 'city', 'country', 'crossStreet', 'distance', 'formattedAddress',                                        'labeledLatLngs', 'neighborhood', 'id'], axis=1)
clean_Shopping_dataframe2


# In[49]:


# delete rows which its category is not Shopping Mall
df_Shopping = clean_Shopping_dataframe2[clean_Shopping_dataframe2.categories == 'Shopping Mall']
df_Shopping


# Generate map to visualize universities, hotels, shopping stores and Cafeteria and how they cluster together¶

# In[50]:


from ipykernel import kernelapp as app


# In[51]:


# create dataframe of hotels, shopping stores and Cafeteria
university_neighbourhood_df = pd.concat([df_university, df_Cafeteria, df_Shopping, ], ignore_index=True)
university_neighbourhood_df


# In[52]:


# Generate map to visualize hotel neighbourhood including shopping stores and Cafeteria 
hotel_map = folium.Map(location=[latitude, longitude], zoom_start=14)

for lat, lng, name, categories, address in zip(university_neighbourhood_df['lat'], university_neighbourhood_df['lng'], 
                                           university_neighbourhood_df['name'], university_neighbourhood_df['categories'],\
                                              university_neighbourhood_df['address']):
    label = '{}, {}'.format(name, address)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.7,
        parse_html=False).add_to(hotel_map)  
    
hotel_map


# Generate map to visualize Park, Restaurant and Cafeteria and how they cluster together

# In[54]:


# create dataframe of Park, Restaurant and Cafeteria
park_neighbourhood_df = pd.concat([df_park, df_Restaurant, df_Cafeteria,], ignore_index=True)
park_neighbourhood_df


# In[55]:


# Generate map to visualize park neighbourhood including Restaurant and Cafeteria 
park_map = folium.Map(location=[latitude, longitude], zoom_start=14)

for lat, lng, name, categories, address in zip(park_neighbourhood_df['lat'], park_neighbourhood_df['lng'], 
                                           park_neighbourhood_df['name'], park_neighbourhood_df['categories'],\
                                               park_neighbourhood_df['address']):
    label = '{}, {}'.format(name, address)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.7,
        parse_html=False).add_to(park_map)  
    
park_map


# Discussion

# In[1]:



import types
import pandas as pd
from botocore.client import Config
import ibm_boto3

def __iter__(self): return 0

# @hidden_cell
# The following code accesses a file in your IBM Cloud Object Storage. It includes your credentials.
# You might want to remove those credentials before you share the notebook.
client_54b74f92cda64c0da2a207bcff06fcc1 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='fFvM53d9U-NAGIbM60G0nkVr6Myn0eVxm2701kjSEnB3',
    ibm_auth_endpoint="https://iam.eu-de.bluemix.net/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3.eu-geo.objectstorage.service.networklayer.com')

body = client_54b74f92cda64c0da2a207bcff06fcc1.get_object(Bucket='beeffactoryinbrussels-donotdelete-pr-unhtnsaeb0w8bo',Key='Revenus par habitant  - Copie.xlsx')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )

df_commune = pd.read_excel(body)
df_commune.head(20)


# In[2]:


df_commune.rename(columns={'Unnamed: 0':'Commune'}, inplace=True)
df_commune.columns


# In[3]:


df_commune.head(20)


# Discussion

# We see that the area of "Rogier" and the center of Brussels have the highest concentration of Univercities and related instititions.
# Besides that, we see that there is a great amount of restaurant, coffee shop et other shops in the same area. 
# This confirms our impression about the attractivity of this area. 
# 
# The area also possesses a good level of average available  income 

# Conclusion 

# We think "Beef factory" would be better off opening its first shop/restaurant nearby Rogier in the center of Brussels. 
