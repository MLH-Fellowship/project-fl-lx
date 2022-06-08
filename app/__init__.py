import os
# from turtle import color, fillcolor
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
from app.data import header_info, about_info, images, workExperience, hobby_info
import folium
import pandas as pd

load_dotenv()
app = Flask(__name__)


@app.route('/home')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), header_info=header_info, about_info=about_info, images=images, workExperience=workExperience)


@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), hobby_info = hobby_info)


@ app.route('/map')
def map():
    folium_map = folium.Map(
        location=[20, 16],
        zoom_start=2,
        zoom_control=False,
        scrollWheelZoom=False,
        dragging=False
    )
    places_visited = pd.read_csv('app/places.csv')
    for _, place in places_visited.iterrows():
        folium.Marker(
            location=[place['latitude'], place['longitude']],
            tooltip=place['City'] + ", " + place['Country'],
            icon=folium.Icon(color="red", icon='check', prefix='fa')
        ).add_to(folium_map)

    folium_map.save('app/templates/interactivemap.html')

    return render_template('map.html')


@app.route('/interactivemap')
def interactivemap():
    return render_template('interactivemap.html')


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    app.run(debug=True)
