# Utilizing Spotify API to Create Beautiful Data Visualizations

## DESCRIPTION
Music Map is a project that allows users to log-in through Spotify, generating a personalized map of genres based on the user's 
listening habits and history. Using the Spotify Implicit Grant authorization code flow (see below), the user grants the application access to their top artists 
(in short-term, medium-term, and long-term), as well as their recently played songs. The application then compiles a list of the artists' genres, before tallying
them up and sorting them. Then, the genres are grouped by keywords into their parent genres. Finally, using [matplotlib pyplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html),
each genre is plotted, with proximity to other genres within the same parent genre.<br><br>

## INSTALLATION
1.) Create and activate virtual environment
```
python3 -m venv .venv
. .venv/bin/activate
```
2.) Install dependencies
```
pip install -r requirements.txt
```
## RUN
1.) Set app.py to flask app
```
set FLASK_APP=app.py
```
2.) Run app by running the app.py file or by running the flask app through the terminal
```
flask run
```

## APP
<br>

![Music Taste Visualization](/static/imgs/demo.gif)


Resulting image:
<br>

![Music Taste Visualization](/static/imgs/example.PNG)

<br>

## AUTHENTICATION
Authentication is done though Spotify with [Authorization Code Flow](https://developer.spotify.com/documentation/general/guides/authorization/code-flow/).
Requests are done through [Spotipy](https://spotipy.readthedocs.io/).

![Authorization Code Flow Chart](https://developer.spotify.com/assets/AuthG_AuthoriztionCode.png)

## TECHNOLOGIES & FRAMEWORKS
- Data Visualization (MatPlotLib/PyPlot)
- Python (Flask)
- HTML, CSS (Bootstrap)
- Javascript
- Spotify API
