from flask import Flask, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import uuid
import base64


def shoot(url):
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--window-size=735,698')
  chrome_options.add_argument('--ignore-certificate-errors')
  chrome_options.add_argument('--allow-running-insecure-content')
  chrome_options.add_argument('--disable-dev-shm-usage')

  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  sleep(2)

  filename = uuid.uuid4()
  fullFilename = "charts/%s.png" % (filename)
  driver.get_screenshot_as_file(fullFilename)

  driver.quit()

  return img(fullFilename)

def img(filename):
  with open(filename, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    prefix = 'data:image/png;base64,'
    return prefix + encoded_string
    


app = Flask('app')

@app.route('/')
def home():
  img = shoot('http://chart-image.api.dabois.capital/chart/DOGEUSD/1h')

  return jsonify(img=img)

@app.route('/chart/<ticker_id>/<timeframe>')
def chart(ticker_id, timeframe):
  ticker_id = str(ticker_id)
  timeframe = str(timeframe)

  return render_template("chart.html", ticker_id=ticker_id, timeframe=timeframe)
    

app.run(host='0.0.0.0', port=8080)
    
