#!/bin/bash 

curl --request POST http://localhost:5000/api/timeline_post -d 'name=Jessica&email=Jessica.Jones@gmail.com&content=Testing curl using bash script'

curl --request GET http://localhost:5000/api/timeline_post

