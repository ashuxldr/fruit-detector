import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup
# from .models import Calories
import cv2
import os
from django.shortcuts import render
from .models import Fruit, Session, Alert
# BASE_DIR / 'db.sqlite3'
from datetime import date
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

model = load_model(BASE_DIR/'core/FV.h5')

def cutImage():
    path_to_image = "./upload_images/together.png"
    image = cv2.imread(path_to_image)
    (h, w) = image.shape[:2]
    centerX, centerY = (w // 2), (h // 2)
    topLeft = image[0:centerY, 0:centerX]
    topRight = image[0:centerY, centerX:w]
    bottomLeft = image[centerY:h, 0:centerX]
    bottomRight = image[centerY:h, centerX:w]
    cv2.imshow("topLeft", topLeft)
    cv2.imshow("topRight", topRight)
    cv2.imshow("bottomLeft", bottomLeft)
    cv2.imshow("bottomRight", bottomRight)
    path = r"./upload_images"
    isWritten1 = cv2.imwrite(os.path.join(path, 'waka1.jpg'), topLeft)
    isWritten2 = cv2.imwrite(os.path.join(path, 'waka2.jpg'), topRight)
    isWritten3 = cv2.imwrite(os.path.join(path, 'waka3.jpg'), bottomLeft)
    isWritten4 = cv2.imwrite(os.path.join(path, 'waka4.jpg'), bottomRight)
    print(isWritten1, isWritten2, isWritten3, isWritten4)
    if isWritten1:
        print('Image is successfully saved as file.')
    return


labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']


def fetch_calories(prediction):
    try:
        # url = 'https://www.google.com/search?&q=calories in cabbage'
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        print("calories", calories)
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)

def fetch_fat(prediction):
    try:
        # url = 'https://www.google.com/search?&q=calories in cabbage'
        url = 'https://www.google.com/search?&q=fat in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        print("fat", calories)
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)

def fetch_protein(prediction):
    try:
        # url = 'https://www.google.com/search?&q=calories in cabbage'
        url = 'https://www.google.com/search?&q=protein in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        print("protein", calories)
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)

def fetch_carbohydrates(prediction):
    try:
        # url = 'https://www.google.com/search?&q=calories in cabbage'
        url = 'https://www.google.com/search?&q=carbohydrates in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        print("calories", calories)
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)

def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

def index(req):
    ctx = {}
    fruits = run()
    ctx['fruits'] = fruits
    calories = []
    fat = []
    protein = []
    carbohydrates = []
    ctx['total_calories'] = 0
    ctx['total_fat'] = 0
    ctx['total_protein'] = 0
    ctx['total_carbohydrates'] = 0
    for fruit in fruits:
        obj = Fruit.objects.filter(name=fruit)
        calories.append(obj[0].calorie)
        fat.append(obj[0].fat)
        protein.append(obj[0].protein)
        carbohydrates.append(obj[0].carbohydrate)
        ctx['total_calories'] = ctx['total_calories'] + obj[0].calorie
        ctx['total_fat'] = ctx['total_fat'] + obj[0].fat
        ctx['total_protein'] = ctx['total_protein'] + obj[0].protein
        ctx['total_carbohydrates'] = ctx['total_carbohydrates'] + obj[0].carbohydrate
    name = ' '.join(fruits)
    Session.objects.create(name=name, total_calorie=ctx['total_calories'], total_fat=ctx['total_fat'],
                                     total_protein=ctx['total_protein'], total_carbohydrate=ctx['total_carbohydrates'])
    ctx['calories'] = calories
    ctx['fat'] = fat
    ctx['protein'] = protein
    ctx['carbohydrates'] = carbohydrates
    return render(req, 'core/index.html', ctx)


def setAlert(req):
    alert = Alert.objects.get(pk=1)
    sessions = Session.objects.filter(date=date.today())
    day_calorie = 0
    day_fat = 0
    day_protein = 0
    day_carbohydrate = 0
    for session in sessions:
        day_calorie = day_calorie + session.total_calorie
        day_fat = day_fat + session.total_fat
        day_protein = day_protein + session.total_protein
        day_carbohydrate = day_carbohydrate + session.total_carbohydrate
    ctx = {}
    if req.method == 'POST':
        alert.alert_calorie = req.POST.get('calorie', '')
        alert.alert_fat = req.POST.get('fat', '')
        alert.alert_protein = req.POST.get('protein', '')
        alert.alert_carbohydrate = req.POST.get('carbohydrate', '')
        alert.save()
    ctx['message1'] = False
    ctx['message2'] = False
    ctx['message3'] = False
    ctx['message4'] = False
    if float(alert.alert_calorie)<day_calorie:
        ctx['message1'] = "CALORIE LIMIT EXCEEDED"
    if float(alert.alert_fat)<day_fat:
        ctx['message2'] = "FAT LIMIT EXCEEDED"
    if float(alert.alert_protein)<day_protein:
        ctx['message3'] = "PROTEIN LIMIT EXCEEDED"
    if float(alert.alert_carbohydrate)<day_carbohydrate:
        ctx['message4'] = "CARBOHYDRATE LIMIT EXCEEDED"
    ctx['alert_calorie'] = alert.alert_calorie
    ctx['alert_fat'] = alert.alert_fat
    ctx['alert_protein'] = alert.alert_protein
    ctx['alert_carbohydrate'] = alert.alert_carbohydrate
    return render(req, 'core/dashboard.html', ctx)



def run():
    lst = ['waka1.jpg', 'waka2.jpg', 'waka3.jpg', 'waka4.jpg']
    lst1 = []
    for img in lst:
        lst1.append(processed_img(BASE_DIR/'core/upload_images'/img))
    return lst1
        # obj = Calories.objects.create(name=res, calorie = '1', ca)
        # obj.save()
