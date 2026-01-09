# KTP Project Group 3
Our project for the knowledge technology practical course is a knowledge systems which informs recreational divers wether they can safely enter the water. It does this by asking the user questions and determines wether they can based on their answers following provided rules. To draw a conclusion the system makes use of a backward chaining based inference engine that uses the questions and rules provided in the knowledge base (kb.xml).

## Installation
The application was built using Flask, a Python package for web servers. To install all the dependencies for this run the following (can be done globally or in a virtual environment):
```
pip install -r requirements.txt
```

## Running the application
The application can be run with python or flask run:

Using python:
```
python main.py
```

Using flask run:
```
flask --app main run
```

After this the application will be reachable on [http://127.0.0.1:5000](http://127.0.0.1:5000). If you open this URL in your webbrowser you will see the web interface which communicates with the Flask backend over HTTP.
