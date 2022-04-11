import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup
# from .models import Calories


import cv2
import os
def cutImage():
    path_to_image="./upload_images/together.png"
    image= cv2.imread(path_to_image)
    (h,w) = image.shape[:2]
    centerX, centerY = (w//2), (h//2)
    topLeft = image[0:centerY, 0:centerX]
    topRight = image[0:centerY, centerX:w]
    bottomLeft=image[centerY:h,0:centerX]
    bottomRight = image[centerY:h , centerX:w]
    cv2.imshow("topLeft" , topLeft)
    cv2.imshow("topRight" , topRight)
    cv2.imshow("bottomLeft" , bottomLeft)
    cv2.imshow("bottomRight" , bottomRight)
    path =r"./upload_images"
    isWritten1= cv2.imwrite(os.path.join(path , 'waka1.jpg'), topLeft)
    isWritten2= cv2.imwrite(os.path.join(path , 'waka2.jpg'), topRight)
    isWritten3= cv2.imwrite(os.path.join(path , 'waka3.jpg'), bottomLeft)
    isWritten4= cv2.imwrite(os.path.join(path , 'waka4.jpg'), bottomRight)
    print(isWritten1, isWritten2, isWritten3, isWritten4)
    if isWritten1:
        print('Image is successfully saved as file.')
    return
cutImage()


model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot', 7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger', 14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple', 26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn', 32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple','Banana','Bello Pepper','Chilli Pepper','Grapes','Jalepeno','Kiwi','Lemon','Mango','Orange','Paprika','Pear','Pineapple','Pomegranate','Watermelon']
vegetables = ['Beetroot','Cabbage','Capsicum','Carrot','Cauliflower','Corn','Cucumber','Eggplant','Ginger','Lettuce','Onion','Peas','Potato','Raddish','Soy Beans','Spinach','Sweetcorn','Sweetpotato','Tomato','Turnip']

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

def processed_img(img_path):
    img=load_img(img_path, target_size=(224,224,3))
    # img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

def run():
    lst = ['waka1.jpg', 'waka2.jpg','waka3.jpg','waka4.jpg']
    for img in lst:
        res = processed_img('./upload_images/'+img)
        print(res)
        # obj = Calories.objects.create(name=res, calorie = '1', ca)
        # obj.save()
run()

