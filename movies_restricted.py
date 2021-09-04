
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote  
import time
import re
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os
import json
import urllib.request as urllib2
import smtplib, ssl


PATH = '/Users/rafaelllopisgarijo/chromedriver'
driver = webdriver.Chrome(PATH)
api_key = 'xxxx'

driver.get("https://kinepolis.es/cines/kinepolis-valencia?main-section=now")

time.sleep(0.25)
driver.find_element_by_id("onetrust-accept-btn-handler").click()



try:
	main = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "movie-container-content"))
		)
	titles = main.find_elements_by_class_name("movie-overview-title")
	times = main.find_elements_by_xpath("//*[contains(@id,'movie-detail-info-purchase-timeline')]")
	titles_list = []
	times_list = []
	for i in titles:
		titles_list.append(i.text)
	for i in times:
		raw = re.findall(r'(\d{1,2}:\d{1,2})?', i.text)
		times_list.append(list(filter(None, raw)))
	times_list_dt = []
	for film in times_list:
		films_times = []
		for i in film:
			films_times.append(datetime.strptime(i, '%H:%M'))
		times_list_dt.append(sorted(films_times))
	titles_times_zip = zip(titles_list, times_list_dt)
	titles_times = list(titles_times_zip)
	movies_today = {}
	for i in titles_times:
		movies_today[i[0]] = i[1]
finally:
	driver.quit()


url = 'https://api.themoviedb.org/3/search/movie?api_key=xxxx&language=es&query='

movies_desc = {}


def find_info(movie):
	movie_url = url + str(quote(movie)).replace(" ", "+")
	json_obj = urllib2.urlopen(movie_url)
	data = json.load(json_obj)
	try:
		movie_obj = data['results'][0]
		movies_desc[movie] = [movie_obj['overview'], movie_obj['vote_average']]
	except:
		movies_desc[movie] = ["No data found", "No rating found"]

for movie in movies_today:
	find_info(movie)



if os.path.exists("kinepolis.txt"):
	os.remove("kinepolis.txt")
new_file = open("kinepolis.txt", "x")
for movie in movies_today:
	new_file.write("{}:".format(movie))
	for time in movies_today[movie]:
		new_file.write(" {}".format(datetime.strftime(time, '%H:%M')))
	new_file.write("\n\n")
	new_file.write("{}:".format(movies_desc[movie][0]))
	new_file.write("\n\n")
	new_file.write("Rating: {}".format(movies_desc[movie][1]))
	new_file.write("\n\n\n\n")
new_file.close()

port = 465
password = 'xxxx'

context = ssl.create_default_context()

with open('kinepolis.txt') as f:
	email = f.read()

receiver_email = "xxxx@gmail.com"
sender_email = "xxxx@gmail.com"
email_message = EmailMessage()
email_message.set_content(email)
email_message["Subject"] = "Hoy, en Kinépolis Valencia"
email_message["From"] = sender_email
email_message["To"] = receiver_email


with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
	server.login("xxxx@gmail.com", password)
	print("Succesful login")
	server.send_message(email_message)







