# Music Map

### DESCRIPTION
[Music Map](https://musicmapapp.herokuapp.com/) is a project that allows users to log-in through Spotify, generating a personalized map of genres based on the user's 
listening habits and history. Using the Spotify Implicit Grant authorization code flow (see below), the user grants the application access to their top artists 
(in short-term, medium-term, and long-term), as well as their recently played songs. The application then compiles a list of the artists' genres, before tallying
them up and sorting them. Then, the genres are grouped by keywords into their parent genres. Finally, using [matplotlib pyplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html),
each genre is plotted, with proximity to other genres within the same parent genre.

![Music Taste Visualization](/static/imgs/example.PNG)

### AUTHENTICATION
Authentication is done though Spotify with [Implicit Grant Flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#implicit-grant-flow).
Requests are done through [Spotipy](https://spotipy.readthedocs.io/).

![Implicit Grant Flow Chart](https://developer.spotify.com/assets/AuthG_ImplicitGrant.png)

### TECHNOLOGIES & FRAMEWORKS
- Python (Flask)
- HTML, CSS (Bootstrap)
- Javascript
- Spotify API
- Data Visualization (MatPlotLib/PyPlot)
