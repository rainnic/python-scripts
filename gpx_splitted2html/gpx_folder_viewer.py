# Source:
# http://research.ganse.org/datasci/gps/
# https://ocefpaf.github.io/python4oceanographers/blog/2014/08/18/gpx
#
# Written by Nicola Rainiero
# https://rainnic.altervista.org/tag/python
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


folder = sys.argv[1]

fileName = os.path.splitext(folder)[0]+'.html'
print("Il file creato è "+fileName)
f = open(os.path.join(sys.path[0], fileName),'w')
##os.path.join(sys.path[0],

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
<body><h2>Percorsi GPS della cartella: """+folder+"""</h2>Con intervalli di sosta inferiori a <b>10 minuti</b><br><hr>"""



import glob, os
os.chdir(folder)
## sorted(glob.glob('*.png'))
j = 0
for file in sorted(glob.glob("*.gpx"), key=os.path.getmtime):
    print('Il file in questione è il seguente -------->' + file)
    gpxCounter = len(glob.glob1(os.path.dirname(__file__), "*.gpx"))
    print('I gpx presenti sono ------------>' + str(gpxCounter))
    #i = i+1
    #gpx = gpxpy.parse(open('./route1141462231.gpx'))
    gpx = gpxpy.parse(open(file))

    # Files can have more than one track, which can have more than one segment, which have more than one point...
    print('Num tracks: ' + str(len(gpx.tracks)))
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
    print('\nNum non-None Longitude records: ' + str(len(df[~pd.isnull(df.Longitude)])))
    print('Num non-None Latitude records: ' + str(len(df[~pd.isnull(df.Latitude)])))
    print('Num non-None Altitude records: ' + str(len(df[~pd.isnull(df.Altitude)])))
    print('Num non-None Time records: ' + str(len(df[~pd.isnull(df.Time)])))
    print('Num non-None Speed records: ' + str(len(df[~pd.isnull(df.Speed)])))
    print('\nTitle string contained in track.name: ' + track.name)


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
    durata = "Durata: %d:%d:%d" % (hours[0], minutes[0], seconds[0])
    print(durata)


    # tiles can be:
    # - CartoDB positron (i.e. light gray)
    # - Stamen Terrain (i.e. terrain map)
    # - OpenStreetMap, Stamen Toner (i.e. black and white)
    # - Stamen Watercolor (i.e. colorful map without any detail)
    # - CartoDB dark_matter (i.e the map is all black)
    mymap = folium.Map( location=[ df.Latitude.mean(), df.Longitude.mean() ], tiles='CartoDB positron', zoom_start=12)
    #folium.PolyLine(df[['Latitude','Longitude']].values, color="red", weight=2.5, opacity=1).add_to(mymap)
    for coord in df[['Latitude','Longitude']].values:
        folium.CircleMarker(location=[coord[0],coord[1]], radius=5,color='red').add_to(mymap)
    # Start point
    folium.Marker(location=[df.iloc[0,1], df.iloc[0,0]],popup="Timberline Lodge",icon=folium.Icon(color="green"), ).add_to(mymap)
    # Finish point
    folium.Marker(location=[df.iloc[-1,1], df.iloc[-1,0]],popup="Timberline Lodge",icon=folium.Icon(color="red"), ).add_to(mymap)
    #mymap   # shows map inline in Jupyter but takes up full width
    #mymap.save('fol.html')  # saves to html file for display below

    sw = df[['Latitude', 'Longitude']].min().values.tolist()
    ne = df[['Latitude', 'Longitude']].max().values.tolist()
    mymap.fit_bounds([sw, ne]) 
    mymap.save(os.path.splitext(file)[0]+'.html')  # saves to html file for display below
    # Source: https://stackoverflow.com/questions/58162200/pre-determine-optimal-level-of-zoom-in-folium

    mymap.save(os.path.splitext(file)[0]+'.html')  # saves to html file for display below




    df['lastLat']=df['Latitude'].shift(1)
    df['lastLong']=df['Longitude'].shift(1)
    df['dist(meters)'] = df.apply(lambda x: vincenty((x['Latitude'], x['Longitude']), (x['lastLat'], x['lastLong'])), axis = 1) * 1000.

    print('Total distance as summed between points in track:')
    print('   ' + str(sum(df['dist(meters)'][1:])*0.000621371) + ' mi')
    print('   ' + str(sum(df['dist(meters)'][1:])/1000) + ' km')
    # The df['dist'][1:] above is because the "shift" sets the first lastLon,lastLat as NaN.
    print('Comparing to total distance contained in track.name: ' + track.name)

    ## DEFINE fine km for filename
    #"{:.0f}".format(x)

    finalKm = "{:.0f}".format(sum(df['dist(meters)'][1:])/1000)+'km'
    print('Total km are: '+finalKm)
    print('Total meters are: '+str(sum(df['dist(meters)'][1:])))

    # "fol.html"
    if ( sum(df['dist(meters)'][1:]) > 500):
        message = message +"""
        Tracciamento effettuato il """+targetStringDate+"""<br>
        Partenza alle """+targetStringTime+"""<br>
        Arrivo alle """+targetStringFinalTime+"""<br>"""+durata+"""<br>
        Percorsi """+"{:.3f}".format(sum(df['dist(meters)'][1:])/1000)+' km'+"""<br>
        Dislivello """+"{:.0f}".format(df.iloc[-1,2]-df.iloc[0,2])+' m'+"""<br>
        <center><iframe width="680" height="300" """+"src=\""+folder+"/"+os.path.splitext(file)[0]+'.html'+"\">""""</iframe>
        <br>(File: <b>"""+os.path.splitext(file)[0]+"""</b>)<br><br></center><hr>"""
        j += 1
        if ((j % 2 == 0)and(j < (gpxCounter-1))):
            message = message +""" <div class="page-break"></div> <h2>Percorsi GPS della cartella: """+folder+"""</h2>Con intervalli di sosta inferiori a <b>10 minuti</b><hr>"""

    gpx = None
    data = []


message = message +"""
</body></html>"""

f.write(message)
f.close()
