import glob
import os
import requests
from flask import Flask, request, redirect, url_for ,jsonify

app = Flask(__name__)
app.debug = True

def find_images(country_name):
    all_png = glob.glob(os.path.join("static/png/*.png"))
    country_name_with_underscore = country_name.replace(" ","-")
    country_png = []
    for png  in all_png:
        if country_name in png:
            country_png.append(png)
        elif country_name_with_underscore in png :
            country_png.append(png)

    dict_country_png = {}
    arr_country_png = []
    image_sizes = ["256","128","64","48","32","24","16"]

    for cry_png in country_png:
        for imgsize in image_sizes:
            if imgsize in cry_png:
                dict_country_png[imgsize] = cry_png

    arr_country_png.append(dict_country_png)
    return arr_country_png

@app.route('/countries')
def root():
    response_data = requests.get("http://restcountries.eu/rest/v1/all",verify=False)
    country_json = {}
    for country in response_data.json():
        country['countryIcons'] = find_images(country['name'])
        country_json[country['name']] = country
    return jsonify(country_json)

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

if __name__ == '__main__':
  app.run()
