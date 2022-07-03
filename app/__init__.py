import os
# from turtle import color, fillcolor
from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
from app.data import header_info, about_info, images, workExperience, hobby_info
import folium
import pandas as pd
import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

# set the mydb variable to an in-memory sqlite database during testing
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])



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

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', False)
    email = request.form.get('email', False)
    content = request.form.get('content', False)
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<int:id>', methods=['DELETE'])
def delete_time_line_post(id):
    post_to_delete = TimelinePost.get(TimelinePost.id == id)
    post_to_delete.delete_instance()

    return "Deleted post."


@app.route("/timeline")
def timeline():
    return render_template('timeline.html', title="Timeline")

if __name__ == "__main__":
    app.run(debug=True)

