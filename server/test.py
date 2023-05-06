import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
import pickle
import pandas as pd
import urllib.parse
import warnings
warnings.filterwarnings("ignore")
# Use a service account.
cred = credentials.Certificate(
    './inspiron23-dc43d-firebase-adminsdk-t4x52-97182a033b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()
# INITIALIZING
with open('scaler_pickle', 'rb') as f:
    # copying prev prediction model to new pred model
    scaler = pickle.load(f)

with open('model_pickle', 'rb') as f:
    km = pickle.load(f)

df = pd.read_csv('finaldata.csv')

config = {
    "apiKey": "AIzaSyDRC582FlBbZhcdRi6kUSDsoYjRThLm7pw",
    "authDomain": "inspiron23-dc43d.firebaseapp.com",
    "projectId": "inspiron23-dc43d",
    "storageBucket": "inspiron23-dc43d.appspot.com",
    "messagingSenderId": "452111001252",
    "appId": "1:452111001252:web:aedb4943d9cb1d96c12831",
    "measurementId": "G-3KX461QBCV"
}


def get_location_id(city):
    url = "https://travel-advisor.p.rapidapi.com/locations/search"

    querystring = {"query": f"{city}",
                   "limit": "1", "offset": "0",
                   "units": "km",
                   "location_id": "1",
                   "currency": "USD",
                   "sort": "relevance",
                   "lang": "en_US",
                   }

    headers = {
        "X-RapidAPI-Key": "83d63c611cmsh6a9cecaa73cff36p1d031cjsnb629fadada79",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        location_id = data['data'][0]['result_object']['location_id']
        return location_id
    else:
        print(f"Error: {response.status_code}")
        return None


def get_attractions(city):
    url = "https://travel-advisor.p.rapidapi.com/attractions/list"

    querystring = {"location_id": f"{get_location_id(city)}", "currency": "USD",
                   "lang": "en_US", "lunit": "km", "sort": "recommended", "limit": "5"}
    # print(querystring["location_id"])
    headers = {
        "X-RapidAPI-Key": "83d63c611cmsh6a9cecaa73cff36p1d031cjsnb629fadada79",
        "X-RapidAPI-Host": "travel-advisor.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    # if response.status_code == 200:
    #     data = response.json()
    #     attractions = [attraction['name'] for attraction in data['data']]
    #     return attractions
    # else:
    #     print(f"Error: {response.status_code}")
    #     return []
    # print(response.text)
    return response.json()


def getSearches():
    search_ref = db.collection(u'Users').document(
        u'dMSIQew0myPrFokkJbOv').collection(u'Searches')

    search = search_ref.get()
    searches = []
    for doc in search:
        dictt = doc.to_dict()
        searches.insert(0, dictt['search'])
    return searches


def getLatandLong(city):
    address = city
    url = 'https://nominatim.openstreetmap.org/search/' + \
        urllib.parse.quote(address) + '?format=json'
    response = requests.get(url).json()
    return [float(response[0]["lat"]), float(response[0]["lon"])]


def getRecommendations():
    cities = getSearches()
    ansc = []
    for i in range(min(5, len(cities))):
        latlong = getLatandLong(cities[i])
        latlongscaled = [scaler.transform([[i]])[0] for i in latlong]
        # print(latlongscaled)
        ans = km.predict([[latlongscaled[0][0], latlongscaled[1][0]]])
        ansdf = df[df['cluster'] == ans[0]].sort_values(
            by='Tourist(Millions)', ascending=0)
        ansdf = ansdf.head(3)
        for c in ansdf.City:
            if (c != cities[i] and c not in ansc):
                ansc.append(c)
    attractions = []
    for city in ansc:
        attractions.append(get_attractions(city))
    return attractions


homepageRecommendations = getRecommendations()
print(homepageRecommendations[0])
