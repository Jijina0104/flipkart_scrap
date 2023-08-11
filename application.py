from flask import Flask,render_template,request
import os
import requests
from bs4 import BeautifulSoup
import csv
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By


application=Flask(__name__)

@application.route('/')
def home():
    return render_template("index.html")

@application.route('/review', methods=['POST', 'GET'])
def review():
    if request.method=='POST':
        #driver = webdriver.Chrome()
        current_page=1
        query = request.form['content'].replace(" ","")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
        all_review_data=[]
        next_page=True
        while next_page: 
            url=f"https://www.flipkart.com/{query}/product-reviews/itmfbeb0684432d7?pid=MOBGHWFHR4ZYUPH5&lid=LSTMOBGHWFHR4ZYUPH5XVPV0K&marketplace=FLIPKART&page={current_page}"
            response = requests.get(url)
            #response_more=driver.get(url)
            #print(response_more)
            #driver.find_element('xpath', '//*[@id="container"]/div/div[3]/div/div/div[2]/div[3]/div/div/div/div[2]/div/div/div')
            #print(comment)
            
            #print(response.text)
            try:           
                soup=BeautifulSoup(response.content, "html.parser")
                reviews=[]
                #review_length=len(reviews)

                for i in soup.find_all("div", class_="_27M-vq"):
                    print(i)
                    review_title=i.find("p", class_= "_2-N8zT").get_text()
                    review_comment=i.find("div", class_= "").get_text()
                    review_rating=i.find("div", class_= "_3LWZlK").get_text()
                    review_author=i.find("p", class_= "_2sc7ZR").get_text()
                    reviews.append([review_title,review_author,review_rating,review_comment])
                        
                if not reviews:
                    break
                else:
                    all_review_data.extend(reviews)                      
                    current_page += 1

            except Exception as e:
                print(f"Error fetching reviews: {e}")
                print(traceback.format_exc())
                return f"Error: {str(e)}"

        save_directory= "review"
        csv_path = f"{save_directory}/reviews2.csv"
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(['review_title','review_author','review_rating','review_comment'])
            writer.writerows(all_review_data)
        return render_template('result.html', reviews=all_review_data)         
    else:
        return render_template('index.html')

if __name__=='__main__':
    application.run(debug=True)
