# Disaster Response Pipeline Project

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python app/run.py`



# Project Overview
On this course, you have discovered and constructed on your facts data engineering talents to extend your possibilities and potential as a data scientist. On this challenge, you may practice these capabilities to investigate catastrophe statistics from discern eight to construct a model for an API that classifies disaster messages.

Within the assignment workspace, you'll discover a data set containing real messages that have been sent at some point of disaster activities. You'll be developing a system gaining knowledge of pipeline to categorize those activities so that you can send the messages to the best disaster comfort organization.

Your challenge will encompass a web app in which an emergency worker can input a new message and get type effects in numerous categories. The web app may also display visualizations of the data. This challenge will display off your software capabilities, including your potential to create primary facts pipelines and write clean, prepared code!


Below are a few screenshots of the web app.

[](images/disaster-response-project1.png![image](https://user-images.githubusercontent.com/69160473/117585870-9afb2f00-b0c9-11eb-8e92-18eb7e960fd4.png)


Project Components

There are three components you'll need to complete for this project.

1. ETL Pipeline

In a Python script, process_data.py, write a data cleaning pipeline that:

Loads the messages and categories datasets
Merges the two datasets
Cleans the data
Stores it in a SQLite database

2. ML Pipeline

In a Python script, train_classifier.py, write a machine learning pipeline that:

Loads data from the SQLite database
Splits the dataset into training and test sets
Builds a text processing and machine learning pipeline
Trains and tunes a model using GridSearchCV
Outputs results on the test set
Exports the final model as a pickle file

3. Flask Web App

We are providing much of the flask web app for you, but feel free to add extra features depending on your knowledge of flask, html, css and javascript. For this part, you'll need to:

Modify file paths for database and model as needed
Add data visualizations using Plotly in the web app. One example is provided for you
Github and Code Quality
Your project will also be graded based on the following:

Use of Git and Github
Strong documentation
Clean and modular code
Follow the RUBRIC when you work on your project to assure you meet all of the necessary criteria for developing the pipelines and web app.
