####################
# gpx_file_viewer.py
####################
# From a GPX file it returns an HTML with the map of the track and the summary.
#
# Usage:
# gpx_file_viewer.py filename.gpx
#
# Written by Nicola Rainiero
# https://rainnic.altervista.org/tag/python
#
# Source:
# http://research.ganse.org/datasci/gps/
# https://ocefpaf.github.io/python4oceanographers/blog/2014/08/18/gpx
#

import gpxpy
import sys
import os
##import gmplot   # (https://github.com/vgm64/gmplot)
import folium   # (https://pypi.python.org/pypi/folium)
from datetime import datetime
import pytz
from vincenty import vincenty

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def convert_datetime_timezone(dt, tz1, tz2):
    tz1 = pytz.timezone(tz1)
    tz2 = pytz.timezone(tz2)

    dt = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S+00:00")
    dt = tz1.localize(dt)
    dt = dt.astimezone(tz2)
    dt = dt.strftime("%Y-%m-%d %H:%M:%S+00:00")

    return dt


file = sys.argv[1]

##fileName = 'test_'+os.path.splitext(file)[0]+'.html'
##print("Il file creato è "+fileName)
##f = open(os.path.join(sys.path[0], fileName),'w')
##os.path.join(sys.path[0],



#import glob, os
#os.chdir(folder)
## sorted(glob.glob('*.png'))
#i = 0
#for file in sorted(glob.glob("*.gpx"), key=os.path.getmtime):
if file:

    print(file)
    #i = i+1
    #gpx = gpxpy.parse(open('./route1141462231.gpx'))
    gpx = gpxpy.parse(open(file))

    # Files can have more than one track, which can have more than one segment, which have more than one point...
    print('Num tracks: ' + str(len(gpx.tracks)))
    # If GPX does not contain tracks and segments
    if (len(gpx.tracks) == 0):
        # Read in the file
        with open(sys.argv[1], 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('rte', 'trk')
        filedata = filedata.replace('<trk>', '<trk><trkseg>')
        filedata = filedata.replace('</trk>', '</trkseg></trk>')

        # Write the file out again
        # with open('file.txt', 'w') as file:
        with open('Fixed_'+sys.argv[1], 'w') as file:
            file.write(filedata)

        # Load the new file with track and segment
        file = 'Fixed_'+sys.argv[1]
        gpx = gpxpy.parse(open(file))

    track = gpx.tracks[0]
    print('Num segments: ' + str(len(track.segments)))
    segment = track.segments[0]
    print('Num segments: ' + str(len(segment.points)))

    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude,point.elevation,
                     point.time, segment.get_speed(point_idx)])
    import pandas as pd
    columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
    df = pd.DataFrame(data, columns=columns)
    print('\nDataframe head:')
    print(df.head())
    print('\nBO:')
    print(df.iloc[0,0]) #first longitude
    print(df.iloc[-1,0]) #last longitude
    print(df.tail())
    print('\nNum non-None Longitude records: ' + str(len(df[~pd.isnull(df.Longitude)])))
    print('Num non-None Latitude records: ' + str(len(df[~pd.isnull(df.Latitude)])))
    print('Num non-None Altitude records: ' + str(len(df[~pd.isnull(df.Altitude)])))
    print('Num non-None Time records: ' + str(len(df[~pd.isnull(df.Time)])))
    print('Num non-None Speed records: ' + str(len(df[~pd.isnull(df.Speed)])))
    ##print('\nTitle string contained in track.name: ' + track.name)


    ## Define time and date for filename
    ## INITIAL DATE
    print('\nDate: ' + str(df.Time.iloc[0]))
    if (df.Time.iloc[0] is None):
        mydate = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S+00:00'))
    else:
        mydate = str(df.Time.iloc[0])
    #mydate = str(df.Time.iloc[0])
    #mydate = "2020-08-31 05:04:19+00:00"
    #mydate = datetime.strptime(mydate, '%Y-%m-%d %H:%M:%S+00:00')
    #mydate = str(df.Time.iloc[0])
    # obj = datetime.strptime('2018-03-01T12:00:00+01:00', '%Y-%m-%dT%H:%M:%S+01:00')
    #obj = datetime.strptime('2020-08-31 05:04:19+00:00', '%Y-%m-%d %H:%M:%S+00:00')
    #obj = datetime.strptime('2020-08-31 05:04:19', '%Y-%m-%d %H:%M:%S')

    print(convert_datetime_timezone(mydate, "UTC", "Europe/Rome"))
    newdate = convert_datetime_timezone(mydate, "UTC", "Europe/Rome")
    print(newdate)
    obj = datetime.strptime(newdate, '%Y-%m-%d %H:%M:%S+00:00')
    print(obj)
    print(obj.strftime('%y')+obj.strftime('%m')+obj.strftime('%d')) # date
    targetDate = obj.strftime('%y')+obj.strftime('%m')+obj.strftime('%d')
    targetTime = obj.strftime('%H')+'_'+obj.strftime('%M')
    print(obj.strftime('%H')+'_'+obj.strftime('%M')) # time
    ##datetime.datetime.strptime(df.Time.iloc[0]).strftime('%m/%d/%y')
    targetStringDate = obj.strftime('%d')+'/'+obj.strftime('%m')+'/'+obj.strftime('%Y')
    targetStringTime = obj.strftime('%H')+':'+obj.strftime('%M')

    ## FINAL DATE
    if (df.Time.iloc[-1] is None):
        myFinaldate = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S+00:00'))
    else:
        myFinaldate = str(df.Time.iloc[-1])
    #myFinaldate = str(df.Time.iloc[-1])
    print(convert_datetime_timezone(myFinaldate, "UTC", "Europe/Rome"))
    newFinaldate = convert_datetime_timezone(myFinaldate, "UTC", "Europe/Rome")
    print(newFinaldate)
    objFinal = datetime.strptime(newFinaldate, '%Y-%m-%d %H:%M:%S+00:00')
    print(objFinal)
    print(objFinal.strftime('%y')+objFinal.strftime('%m')+objFinal.strftime('%d')) # date
    targetFinalDate = objFinal.strftime('%y')+objFinal.strftime('%m')+objFinal.strftime('%d')
    targetFinalTime = objFinal.strftime('%H')+'_'+objFinal.strftime('%M')
    print(objFinal.strftime('%H')+'_'+objFinal.strftime('%M')) # time
    targetStringFinalDate = objFinal.strftime('%d')+'/'+objFinal.strftime('%m')+'/'+objFinal.strftime('%Y')
    targetStringFinalTime = objFinal.strftime('%H')+':'+objFinal.strftime('%M')

    # DURATION
    duration = objFinal - obj
    duration_in_s = duration.total_seconds()      
    days    = divmod(duration_in_s, 86400)        # Get days (without [0]!)
    hours   = divmod(days[1], 3600)               # Use remainder of days to calc hours
    minutes = divmod(hours[1], 60)                # Use remainder of hours to calc minutes
    seconds = divmod(minutes[1], 1)               # Use remainder of minutes to calc seconds
    print("Time between dates: %d days, %d hours, %d minutes and %d seconds" % (days[0], hours[0], minutes[0], seconds[0]))
    #durata = hours+':'+minutes+':'+seconds
    #durata = "Durata: %d giorno/i, %d:%d:%d" % (days[0], hours[0], minutes[0], seconds[0])
    durata = "Duration: %d:%d:%d" % (hours[0], minutes[0], seconds[0])
    print(durata)


    # tiles can be:
    # - CartoDB positron (i.e. light gray)
    # - Stamen Terrain (i.e. terrain map)
    # - OpenStreetMap, Stamen Toner (i.e. black and white)
    # - Stamen Watercolor (i.e. colorful map without any detail)
    # - CartoDB dark_matter (i.e the map is all black)
    mymap = folium.Map( location=[ df.Latitude.mean(), df.Longitude.mean() ], tiles='CartoDB positron', zoom_start=12)
    
    for coord in df[['Latitude','Longitude']].values:
        folium.CircleMarker(location=[coord[0],coord[1]], radius=2,color='blue').add_to(mymap)
    # Start point
    # folium.Marker(location=[df.iloc[0,1], df.iloc[0,0]],popup="Timberline Lodge",icon=folium.Icon(color="green"), ).add_to(mymap)
    folium.CircleMarker(location=[df.iloc[0,1], df.iloc[0,0]], radius=10,color='green').add_to(mymap)
    # Finish point
    # folium.Marker(location=[df.iloc[-1,1], df.iloc[-1,0]],popup="Timberline Lodge",icon=folium.Icon(color="red"), ).add_to(mymap)
    folium.CircleMarker(location=[df.iloc[-1,1], df.iloc[-1,0]], radius=10,color='red').add_to(mymap)
    #mymap   # shows map inline in Jupyter but takes up full width
    #mymap.save('fol.html')  # saves to html file for display below

    sw = df[['Latitude', 'Longitude']].min().values.tolist()
    ne = df[['Latitude', 'Longitude']].max().values.tolist()

    mymap.fit_bounds([sw, ne]) 

    mymap.save(os.path.splitext(file)[0]+'.html')  # saves to html file for display below
    # Source: https://stackoverflow.com/questions/58162200/pre-determine-optimal-level-of-zoom-in-folium



    df['lastLat']=df['Latitude'].shift(1)
    df['lastLong']=df['Longitude'].shift(1)
    df['dist(meters)'] = df.apply(lambda x: vincenty((x['Latitude'], x['Longitude']), (x['lastLat'], x['lastLong'])), axis = 1) * 1000.

    print('Total distance as summed between points in track:')
    print('   ' + str(sum(df['dist(meters)'][1:])*0.000621371) + ' mi')
    print('   ' + str(sum(df['dist(meters)'][1:])/1000) + ' km')
    # The df['dist'][1:] above is because the "shift" sets the first lastLon,lastLat as NaN.
    ##print('Comparing to total distance contained in track.name: ' + track.name)

    ## DEFINE fine km for filename
    #"{:.0f}".format(x)

    finalKm = "{:.0f}".format(sum(df['dist(meters)'][1:])/1000)+'km'
    print(finalKm)

    print(df.iloc[0,2])
    print(df.iloc[-1,2])
    if (df.iloc[0,2] is None): df.iloc[0,2] = 0
    if (df.iloc[-1,2] is None): df.iloc[-1,2] = 0
    elevationDelta = "{:.0f}".format(abs(df.iloc[-1,2]-df.iloc[0,2]))+' m'
    print('Dislivello di '+elevationDelta)

    #fileName = targetDate+'_track_'+targetTime+'_'+finalKm+'.html'
    fileName = targetDate+'_'+os.path.splitext(file)[0]+'_'+targetTime+'_'+finalKm+'.html' 
    f = open(fileName,'w')

    message = """<html>
    <head>
    <style>
    @media all {
    .page-break { display: none; }
    }

    @media print {
    .page-break { display: block; page-break-before: always; }
    }
    </style>
    </head>
    <body><h2>GPS track from the file: """+file+"""</h2>Without any break<br><hr>"""


    # "fol.html"
    message = message +"""
    Tracked on """+targetStringDate+""" and start at """+targetStringTime+"""<br>
    Stop on """+targetStringFinalDate+""" at """+targetStringFinalTime+"""<br>"""+durata+"""<br>
    Length path """+"{:.3f}".format(sum(df['dist(meters)'][1:])/1000)+' km'+"""<br>
    Difference in altitude """+"{:.0f}".format(df.iloc[-1,2]-df.iloc[0,2])+' m'+"""<br>
    <center><iframe width="680" height="300" """+"src=\""+os.path.splitext(file)[0]+'.html'+"\">""""</iframe>
    <br>(File: <b>"""+os.path.splitext(file)[0]+""".gpx</b>)<br><br></center><br><hr>"""

    gpx = None
    data = []


message = message +"""
</body></html>"""

f.write(message)
f.close()
