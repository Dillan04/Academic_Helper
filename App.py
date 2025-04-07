from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Simulated database for storing profiles
user_profiles = {}

# Your YouTube API key here
YOUTUBE_API_KEY = 'AIzaSyAX3Qh0YhFqAA-SWjjVQuE34S7yQ8Nu1Is'

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# NLP Question-Answering function
def answer_question(question, context):
    try:
        qa_pipeline = pipeline("question-answering")
        result = qa_pipeline(question=question, context=context)
        return result['answer']
    except Exception as e:
        print(f"Error in QA pipeline: {e}")
        return "An error occurred while answering the question."

context = """
Artificial Intelligence is a branch of computer science concerned with building smart machines 
capable of performing tasks that typically require human intelligence. AI is an interdisciplinary 
science with multiple approaches, but advancements in machine learning and deep learning are creating 
a paradigm shift in virtually every sector of the tech industry.
"""

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Profile page route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        course = request.form.get('course')
        level = request.form.get('level')

        if name and course and level:
            user_profiles[name] = {"course": course, "level": level}
            return redirect(url_for('home', name=name))
        else:
            return render_template('profile.html', error="Please fill in all profile details.")
    return render_template('profile.html')

# Help page route
@app.route('/help')
def help():
    return render_template('help.html')

# Resource page route for YouTube video search
@app.route('/resources', methods=['GET', 'POST'])
def resources():
    videos = []
    if request.method == 'POST':
        query = request.form['video_query']
        # Fetch YouTube videos based on the search query
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=5  # You can adjust the number of results
        ).execute()

        # Extract video details from the API response
        videos = [
            {
                'title': item['snippet']['title'],
                'id': item['id']['videoId']
            }
            for item in search_response['items']
        ]
    
    # Render the resources page with the videos
    return render_template('resources.html', videos=videos)

if __name__ == "__main__":
    app.run(debug=True)