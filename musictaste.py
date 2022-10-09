import matplotlib.pyplot as plt
import random
import matplotlib
from matplotlib import rcParams
# import matplotlib.style as mplstyle
# mplstyle.use('fast')
import io
import time

def random_color():
    r = lambda: random.randint(135,255)
    return ('#%02X%02X%02X' % (r(),r(),r()))

def main(sp, recently_played_json, short_artists_json, med_artists_json, long_artists_json):
    genres=[]
    recentlyplayed = []
    currenttime = time.time()

    # open json objects with Spotify artist/genre data
    for i in short_artists_json[0]['items']:
        for j in i['genres']:
            genres.append(j)

    for i in recently_played_json[0]['items']:
        recentlyplayed.append(i['track']['album']['artists'][0]['uri'])

    for artist in recentlyplayed:
        ar = sp.artist(artist)
        for j in ar['genres']:
            genres.append(j)

    for i in med_artists_json[0]['items']:
        for j in i['genres']:
            genres.append(j)

    for i in long_artists_json[0]['items']:
        for j in i['genres']:
            genres.append(j)

    # tally occurences of genres
    d = {x:genres.count(x) for x in genres}

    # create dictionary for genres, sorted by occurences (high to low)
    dictionary = dict(sorted(d.items(), key=lambda item: item[1]))
    dictionary = {key:val for key, val in dictionary.items() if val != 1}   # excludes genres with only one occurence

    # initialize subgenres in each genre
    subgenres = {
        "pop" : ['pop', 'electropop', 'z', 'group', 'band', 'poptimism', 'stars', 'synth-pop', 'singer-songwriter', 'soundtrack'],
        "rap" : ['rap', 'hop', 'trap', 'drill', 'conscient', 'plugg', 'roots', 'experimental'],
        "edm" : ['house', 'edm', 'indietronica', 'dance', 'electronic', 'dubstep', 'dancehall', 'techno', 'disco', 'grime'],
        "r&b" : ['r&b', 'soul', 'afrofuturism', 'funk', 'reggaeton', 'reggae', 'blues', 'jazz', 'bop', 'bebop', 'storm', 'motown', 'contemporary', 'doo-wop', 'pluggnb'],
        "rock": ['rock', 'grunge', 'punk', 'metal', 'dreamo', 'metalcore', 'emo', 'hardcore', 'pyschedelic', 'psych', 'neo-psychedelic', 'alternative', 'indie'],
        "country" : ['country', 'jamgrass', 'bluegrass', 'folk', 'dirt', 'redneck', 'americana'],
    }
    groups = {
        "pop" : [],
        "rap" : [],
        "edm" : [],
        "r&b" : [],
        "rock": [],
        "country" : [],
        "other" : []
    }

    # organize genres/occurances dictionary into groups by major genre
    for k in dictionary:
        macrogenre = k.split()
        genre = macrogenre[-1]
        taken=False
        for key in subgenres:
            for value in subgenres[key]:
                if genre == value:
                    taken = True
                    listname = str(key)
                    item = {}
                    item[k] = dictionary[k]
                    groups[listname].append(item)
        else:
            if taken==False:
                item = {}
                item[k] = dictionary[k]
                groups["other"].append(item)

    # sort into new dictionary
    groups_new = {}
    for k in sorted(groups, key=lambda k: len(groups[k]), reverse=True):
        groups_new[k] = groups[k]

    numgenre = -1
    # initial points for genres
    initialpoints = [(0,0),(1,0.5635),(-1,-0.5635),(1,-0.5635),(-1,0.5635),(0.8,0),(-0.8,0)]
    figure, axes = plt.subplots()
    graphs = {}
    for genre in groups_new:
        numgenre+=1
        # genre is the larger genre (rap, pop, etc)
        # groups_new[genre] is the subgenre dictionary
        iteration = 0
        clockorder = 0
        for subgenre in reversed(groups_new[genre]):
            for key, value in subgenre.items():
                list = []
                if iteration == 0:
                    x, y = initialpoints[numgenre]
                else:
                    adjust_exception = 0.35
                    if value < 40:  # medium circles
                        if (len(groups_new[genre])) > 12:
                            x = random.uniform(initialpoints[numgenre][0]-0.44, initialpoints[numgenre][0]+0.44)
                            y = random.uniform(initialpoints[numgenre][1]-0.25, initialpoints[numgenre][1]+0.25)
                        else:
                            x = random.uniform(initialpoints[numgenre][0]-0.15, initialpoints[numgenre][0]+0.15)
                            y = random.uniform(initialpoints[numgenre][1]-0.1, initialpoints[numgenre][1]+0.1)
                            adjust_exception = 0.15
                        
                        beginning_x, beginning_y = x, y
                        end_x, end_y = None, None
                        # iterate until x and y values at beginning precisely match the x and y values after checking for overlapping
                        while beginning_x != end_x and beginning_y != end_y:
                            beginning_x = x
                            beginning_y = y
                            for item in graphs:
                                while abs(x-graphs[item][0]) < graphs[item][2]/300 and abs(y-graphs[item][1]) < graphs[item][2]/200:
                                    x = random.uniform(initialpoints[numgenre][0]-(1.3*adjust_exception), initialpoints[numgenre][0]+(1.3*adjust_exception))
                                    y = random.uniform(initialpoints[numgenre][1]-(0.8*adjust_exception), initialpoints[numgenre][1]+(0.8*adjust_exception))
                            end_x = x
                            end_y = y

                        if value < 14:  # small circles
                            if (len(groups_new[genre])) > 12:
                                x = random.uniform(initialpoints[numgenre][0]-0.44, initialpoints[numgenre][0]+0.44)
                                y = random.uniform(initialpoints[numgenre][1]-0.44, initialpoints[numgenre][1]+0.44)
                            else:
                                x = random.uniform(initialpoints[numgenre][0]-0.1, initialpoints[numgenre][0]+0.1)
                                y = random.uniform(initialpoints[numgenre][1]-0.05, initialpoints[numgenre][1]+0.05)
                                adjust_exception = 0.15

                            beginning_x, beginning_y = x, y
                            end_x, end_y = None, None
                            # iterate until x and y values at beginning precisely match the x and y values after checking for overlapping
                            while beginning_x != end_x and beginning_y != end_y:
                                beginning_x = x
                                beginning_y = y
                                for item in graphs:
                                    while abs(x-graphs[item][0]) < ((graphs[item][2]/500) + 0.1) and abs(y-graphs[item][1]) < ((graphs[item][2]/500) + (0.1/4)):
                                        x = random.uniform(initialpoints[numgenre][0]-(1.7*adjust_exception), initialpoints[numgenre][0]+(1.7*adjust_exception))
                                        y = random.uniform(initialpoints[numgenre][1]-adjust_exception, initialpoints[numgenre][1]+adjust_exception)
                                end_x = x
                                end_y = y
                    else:
                        # large circles
                        if clockorder == 1:
                            # quad 1 (x pos, y pos)
                            x = (initialpoints[numgenre][0])+(prev_value/(300))
                            y = (initialpoints[numgenre][1])+(prev_value/(300))
                        elif clockorder == 2:
                            # quad 2 (x neg, y pos)
                            x = (initialpoints[numgenre][0])-(prev_value/(266))
                            y = (initialpoints[numgenre][1])+(prev_value/(266))
                        elif clockorder == 3:
                            # quad 3 (x neg, y neg)
                            x = (initialpoints[numgenre][0])-(prev_value/(233))
                            y = (initialpoints[numgenre][1])-(prev_value/(233))
                        else:
                            # quad 4 (x pos, y neg)
                            x = (initialpoints[numgenre][0])+(prev_value/(200))
                            y = (initialpoints[numgenre][1])-(prev_value/(200))
                prev_value = value
                
                # create list with coordinates
                list.append(x)
                list.append(y)
                list.append(value)

                # attach list to dictionary
                graphs[key]=list

                if iteration == 200:
                    break
                iteration+=1
                clockorder+=1
                if clockorder > 4:
                    clockorder = 1

            rcParams['font.family'] = 'montserrat'
            rcParams['font.weight'] = 300  #can omit this, it's the default

            # iterate through coordinate dictionary and plot circles
            for key, value in graphs.items():
                x = value[0]
                y = value[1]
                var = plt.Circle(( x , y ), value[2]*0.002, color=random_color())
                axes.add_patch(var)

                if value[2] >= 70:
                    fontsz = 7
                elif value[2] >= 25:
                    fontsz = 4
                else:
                    fontsz = 2.4

                # set labels (name) for each circle
                label = axes.annotate(key, xy=(x, y), fontsize=10, ha="center", va="center", color='#75726f')
                label.set_fontsize(fontsz)

    # graph settings (auto-scale, turn off axis/ticks, etc)
    axes.set_aspect('equal')
    axes.autoscale_view()
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    plt.axis('off')

    # save figure as svg
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=600)

    return buffer

if __name__ == "__main__":
    main()
