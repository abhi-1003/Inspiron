from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import time
from flask import Flask, request, jsonify, render_template, url_for
import smtplib
import requests
import numpy as np
import os
import openai
import random
import wandb
import email.utils
from email.mime.text import MIMEText

import pickle
import pandas as pd
import urllib.parse
import warnings
warnings.filterwarnings("ignore")

with open('scaler_pickle', 'rb') as f:
    # copying prev prediction model to new pred model
    scaler = pickle.load(f)

with open('model_pickle', 'rb') as f:
    km = pickle.load(f)

df = pd.read_csv('finaldata.csv')


cred = credentials.Certificate(
    './inspiron23-dc43d-firebase-adminsdk-t4x52-97182a033b.json')

firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

openai.organization = "org-P8vmiq4LzokCYkuhcwFE0W4z"
openai.api_key = "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"


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
        "X-RapidAPI-Key": "082d24c497mshea617f946d1d0d6p133cacjsn9381bd5534b6",
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
                   "lang": "en_US", "lunit": "km", "sort": "recommended"}
    # print(querystring["location_id"])
    headers = {
        "X-RapidAPI-Key": "082d24c497mshea617f946d1d0d6p133cacjsn9381bd5534b6",
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


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/getattractions/<city>/<email>')
def getattractions(city, email):
    cities = ["Jaipur", "Agra", "New Delhi", "Mumbai", "Bangalore",
              "Chennai", "Kolkata", "Varanasi", "Udaipur", "Amritsar"]
    ipCity = city
    print(ipCity)
    ans = get_attractions(ipCity)
    locations = ans['data']
    ranked_location = {}
    for location in locations:
        if ('name' in location and 'ranking_position' in location and 'photo' in location and 'booking' in location and 'description' in location and 'open_now_text' in location and 'write_review' in location):
            locationInfo = {}
            # name
            locationInfo['name'] = location['name']
            # description
            locationInfo['description'] = location['description']
            # number of reviews
            locationInfo['numberofreviews'] = location['num_reviews']
            # stars
            locationInfo['stars'] = location['rating']
            # photo URL
            if ('medium' in location['photo']['images']):
                locationInfo['photoUrl'] = location['photo']['images']['medium']
            # booking
            bookingOptions = {}
            bookingOptions['provider'] = location['booking']['provider']
            bookingOptions['url'] = location['booking']['url']
            locationInfo['bookingOptions'] = bookingOptions
            # open?
            locationInfo['open_now_text'] = location['open_now_text']
            # Review?
            locationInfo['write_review'] = location['write_review']
            ranked_location[location['ranking_position']] = locationInfo

    myKeys = list(int(i) for i in ranked_location.keys())
    myKeys.sort()
    sorted_ranked_locations = []
    for i in myKeys:
        sorted_ranked_locations.append(ranked_location[str(i)])
    locations = sorted_ranked_locations
    recommended_cities = []

    # adding search to user database
    search = {
        "search": city,
        "createdAt": time.time()
    }

    if (email != "default"):
        db.collection(u'Users').document(email).collection(
            u'Searches').document(city).set(search)

    for i in range(3):
        i = random.randint(0, len(cities)-1)
        if (cities[i] not in recommended_cities):
            recommended_cities.append(cities[i])
    if (len(recommended_cities) > 0):
        return {"locations": locations}
    else:
        return {"locations": locations}


def sendMail(finalans):
    receiver = 'abhikurule24@gmail.com'
    server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    server.ehlo()
    server.login('onlyhacks96@yahoo.com', 'hellolove69#')
    server.sendmail('onlyhacks96@yahoo.com', receiver, str(finalans))
    server.quit()


@app.route('/getitinerary/<city>/<duration>')
def getitenary(city, duration):
    ip = "asdasd"
    finalans = []
    if (len(ip) > 0):
        gpt_prompt = "Generate a detailed " + \
            duration+" travel itenarary for a trip to " + city
        print(gpt_prompt)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=gpt_prompt,
            temperature=0.5,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        ans = response['choices'][0]["text"]
        ans = ans.split("Day")

        for day in ans:
            if (day != '' and day != " " and day != "\n\n" and day != "\n"):
                finalans.append(day)
        print(finalans)

    return {"response": finalans}


@app.route("/addUser/<email>")
def addUser(email):
    user = {
        u'email': email
    }

    db.collection(u'Users').document(email).set(user)
    return "True"


def getSearches(email):
    search_ref = db.collection(u'Users').document(
        email).collection(u'Searches')

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


def getRecommendations(email):
    cities = getSearches(email)
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


@app.route("/getRecommendations/<email>")
def getRecs(email):
    print("Fetching")
    recoms = getRecommendations(email)
    sorted_ranked_locations = []
    for ans in recoms:
        locations = ans['data']
        ranked_location = {}
        for location in locations:
            if ('name' in location and 'ranking_position' in location and 'photo' in location and 'booking' in location and 'description' in location and 'open_now_text' in location and 'write_review' in location):
                locationInfo = {}
            # name
                locationInfo['name'] = location['name']
                print(location['name'])
            # description
                locationInfo['description'] = location['description']
            # number of reviews
                locationInfo['numberofreviews'] = location['num_reviews']
            # stars
                locationInfo['stars'] = location['rating']
            # photo URL
                if ('medium' in location['photo']['images']):
                    locationInfo['photoUrl'] = location['photo']['images']['medium']
            # booking
                bookingOptions = {}
                bookingOptions['provider'] = location['booking']['provider']
                bookingOptions['url'] = location['booking']['url']
                locationInfo['bookingOptions'] = bookingOptions
            # open?
                locationInfo['open_now_text'] = location['open_now_text']
            # Review?
                locationInfo['write_review'] = location['write_review']
                ranked_location[location['ranking_position']] = locationInfo

        myKeys = list(int(i) for i in ranked_location.keys())
        myKeys.sort()

        for i in myKeys:
            sorted_ranked_locations.append(ranked_location[str(i)])
        locations = sorted_ranked_locations
    return {"recoms": sorted_ranked_locations}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
