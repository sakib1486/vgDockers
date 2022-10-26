import pandas as pd
import psycopg2
import schedule
import time
import numpy as np
import math
from urllib.request import urlopen
import json
from crate import client

## Establishing the Conenction to DB for direct execution
conn_p = psycopg2.connect(database="vgym", user='vgym', password='vgym123', host='localhost', port='5433')
conn_p.autocommit = True
cursor_p = conn_p.cursor()

conn_c = client.connect("http://129.128.184.214:4200", username="crate")
conn_c.autocommit = True
cursor_c = conn_c.cursor()


##our database connections for pandas operations
crate_connection = 'crate://129.128.184.214:4200/'
psql_connection = 'postgresql://vgym:vgym123@localhost:5433/vgym' ##change it to localhost:4355 when deploying in local envrionment



#gametime for a session
def gameTime(sessionid: str) -> float:
    """
    Parameter(s): sessionid of a game
    Returns one value: SessionTime in seconds
    """

    query = """
    SELECT TIME from frames WHERE "SessionId" = '{}' ORDER BY TIME;
    """.format(sessionid)

    df_session = pd.read_sql(query, con=crate_connection)

    #count session time in seconds
    minTime = df_session['time'].min(axis=0)
    maxTime = df_session['time'].max(axis=0)

    sessionTime = round(maxTime-minTime, 2)

    return sessionTime



#range of motion
#function ROM, counts range of motion from whatever dataframe is passed
def ROM(sessionData: pd.DataFrame):

  #HeadCenter Max, Min, Average taking 25 seconds as consideration
  h_left = sessionData['CenterEyeAnchor_posx'].idxmin(axis=0)
  h_right = sessionData['CenterEyeAnchor_posx'].idxmax(axis=0)
  h_up = sessionData['CenterEyeAnchor_posy'].idxmax(axis=0)
  h_down = sessionData['CenterEyeAnchor_posy'].idxmin(axis=0)

  lx = sessionData._get_value(h_left, 'CenterEyeAnchor_posx')-0
  ly = sessionData._get_value(h_left, 'CenterEyeAnchor_posy')-0
  lz = sessionData._get_value(h_left, 'CenterEyeAnchor_posz')-0

  rx = sessionData._get_value(h_right, 'CenterEyeAnchor_posx')-0
  ry = sessionData._get_value(h_right, 'CenterEyeAnchor_posy')-0
  rz = sessionData._get_value(h_right, 'CenterEyeAnchor_posz')-0

  ux = sessionData._get_value(h_up, 'CenterEyeAnchor_posx')-0
  uy = sessionData._get_value(h_up, 'CenterEyeAnchor_posy')-0
  uz = sessionData._get_value(h_up, 'CenterEyeAnchor_posz')-0

  dx = sessionData._get_value(h_down, 'CenterEyeAnchor_posx')-0
  dy = sessionData._get_value(h_down, 'CenterEyeAnchor_posy')-0
  dz = sessionData._get_value(h_down, 'CenterEyeAnchor_posz')-0

  #getting range of motion of Head Left, Right, Up and Down
  #print("Max Head Movement to Left is %.2f units" %(math.sqrt(lx*lx+ly*ly+lz*lz)))
  #print("Max Head Movement to Right is %.2f units" %(math.sqrt(rx*rx+ry*ry+rz*rz)))
  #print("Max Head Movement to Upwards is %.2f units" %(math.sqrt(ux*ux+uy*uy+uz*uz)))
  #print("Max Head Movement to Downwards is %.2f units" %(math.sqrt(dx*dx+dy*dy+dz*dz)))

  #LeftController
  #has to be calculated from the Relative position of the Controllers w.r.t. the CenterEyeAnchor
  left = (sessionData['CenterEyeAnchor_posx']-sessionData['LeftControllerAnchor_relx'])*(sessionData['CenterEyeAnchor_posx']-sessionData['LeftControllerAnchor_relx'])+(sessionData['CenterEyeAnchor_posy']-sessionData['LeftControllerAnchor_rely'])*(sessionData['CenterEyeAnchor_posy']-sessionData['LeftControllerAnchor_rely'])+(sessionData['CenterEyeAnchor_posz']-sessionData['LeftControllerAnchor_relz'])*(sessionData['CenterEyeAnchor_posz']-sessionData['LeftControllerAnchor_relz'])
  #print("Maximum Left Hand Stretch w.r.t. the Head Center Position is %.2f units" %(math.sqrt(left.max(axis=0))))


  #RightController
  #has to be calculated from the Relative position of the Controllers w.r.t. the CenterEyeAnchor
  right = (sessionData['CenterEyeAnchor_posx']-sessionData['RightControllerAnchor_relx'])*(sessionData['CenterEyeAnchor_posx']-sessionData['RightControllerAnchor_relx'])+(sessionData['CenterEyeAnchor_posy']-sessionData['RightControllerAnchor_rely'])*(sessionData['CenterEyeAnchor_posy']-sessionData['RightControllerAnchor_rely'])+(sessionData['CenterEyeAnchor_posz']-sessionData['RightControllerAnchor_relz'])*(sessionData['CenterEyeAnchor_posz']-sessionData['RightControllerAnchor_relz'])
  #print("Maximum Right Hand Stretch w.r.t. the Head Center Position is %.2f units" %(math.sqrt(right.max(axis=0))))

  return math.sqrt(lx*lx+ly*ly+lz*lz), math.sqrt(rx*rx+ry*ry+rz*rz), math.sqrt(ux*ux+uy*uy+uz*uz), math.sqrt(dx*dx+dy*dy+dz*dz), math.sqrt(left.max(axis=0)), math.sqrt(right.max(axis=0))


def range_of_motion(sessionid: str) -> dict:
    """
    Parameter(s): sessionid of a game
    Returns a python dictionary with: head movement left, right, down, up along with left&right hand max stretch
    """

    query = """
    SELECT * from frames WHERE "SessionId"='{}' ORDER BY time LIMIT 1000000;
    """.format(sessionid)

    ###split the data into 250 seconds dataframe
    nframes = 250
    sD = pd.read_sql(query, con=crate_connection)
    sessionData = [sD[i:i+nframes] for i in range(0, sD.shape[0], nframes)]

    ###Declaring empty dictionary and empty lists for window based collection
    rom = {}
    hleft, hright, hup, hdown, leftC, rightC = [],[],[],[],[],[]

    ###Calculating Range of Motion per 25 seconds
    for s in sessionData:
        hl, hr, hu, hd, lc, rc = ROM(s)
        hleft.append(hl)
        hright.append(hr)
        hup.append(hu)
        hdown.append(hd)
        leftC.append(lc)
        rightC.append(rc)

    rom['sessionid'] = sessionid
    rom['headleft'] = max(hleft, default=0)*100
    rom['headright'] = max(hright, default=0)*100
    rom['headup'] = max(hup, default=0)*100
    rom['headdown'] = max(hdown, default=0)*100
    rom['lefthand'] = max(leftC, default=0)*100
    try:
        rom['avgleft'] = (sum(leftC)/len(leftC))*100
    except ZeroDivisionError:
        rom['avgleft'] = 0
    rom['righthand'] = max(rightC, default=0)*100
    try:
        rom['avgright'] = (sum(rightC)/len(rightC))*100
    except ZeroDivisionError:
        rom['avgright'] = 0

    return rom


###function fov

def field_of_view(sessionid: str):
  
  fov_query = """
    SELECT * FROM "frames" WHERE "SessionId"= '{}' ORDER BY time;
    """.format(sessionid)
  sessionData = pd.read_sql(fov_query, con=crate_connection)

  x0 = 0
  y0 = 0
  z0 = 0

  #finding the left & right max point for the Head Center
  h_left = sessionData['CenterEyeAnchor_posx'].idxmin(axis=0)
  h_right = sessionData['CenterEyeAnchor_posx'].idxmax(axis=0)

  #coordinates of the left and right points
  lx = sessionData._get_value(h_left, 'CenterEyeAnchor_posx')
  ly = 0
  lz = sessionData._get_value(h_left, 'CenterEyeAnchor_posz')

  rx = sessionData._get_value(h_right, 'CenterEyeAnchor_posx')
  ry = 0
  rz = sessionData._get_value(h_left, 'CenterEyeAnchor_posz')

  #creating Lines from origin L1(with Left point) and L2(with right point)
  #L1 = Line((0,0), (lx, lz))
  #L2 = Line((0, 0), (rx, rz))

  #FOV in radians
  #rad = L1.angle_between(L2)

  #Slope of Left and Right FOV lines
  mleft = (lz-z0)/float(lx-x0)

  mright = (rz-z0)/float(rx-x0)
  angleR = abs(math.degrees(math.atan(mright)))

  fov = abs(math.degrees(math.atan((mright-mleft)/(1+(mright*mleft)))))

  return fov



#to be updated according to the new table "events_test"
def get_balloon_score(sessionid: str) -> list:
    """
    Parameter(s): balloon sessionid
    Returns three values: percentage of success, percentatge of miss, total no. of balloons
    """

    query = """
    SELECT * FROM events_test WHERE "sessionid" = '{}' ORDER BY "targetname", "gametime";
    """.format(sessionid)

    df_events = pd.read_sql(query, con=crate_connection)

    #count interactions

    count_Total = len(df_events[df_events['type']=='target_appear'])
    count_Interactions = len(df_events[df_events['type']=='interact-correct']) + len(df_events[df_events['type']=='interact-incorrect'])
    count_Correct = len(df_events[df_events['type']=='interact-correct'])

    totalReactionTime = 0
    crt = 0
    c = 0
    #reaction time
    for i, event in df_events.iterrows():
        
        if event['type']=='target_appear':
            crt = float(event['gametime'])
        if event['type']=='interact-correct' or event['type']=='interact-incorrect':
            crt = float(event['gametime'])-crt
            if crt>=0.1:
                totalReactionTime = totalReactionTime+crt
                c+=1

    return [c, totalReactionTime, count_Total, count_Interactions, count_Correct]


#main() function which calculates the new completed sessions' metrics and puts them into PSQL
def main():
    
    #getting current session from PSQL
    url = "http://129.128.184.214:8100/s/"

    #fetching the current sessions in 
    response = urlopen(url)
    data = response.read()
    data_json = json.loads(data)
    df_list = json.loads(data_json)
    df_sessions_psql = pd.DataFrame(df_list)

    #getting sessions from events_test in CrateDB
    """
    Query for DISTINCT sessionid
    """

    q = """
    SELECT DISTINCT("sessionid") from events_test;
    """

    df_sessions_events = pd.read_sql(q, con=crate_connection)


    #calculating metrics which has an end event in the database
    for session in df_sessions_events['sessionid']:
        #print(session)
        if session not in df_sessions_psql['sessionid'].unique():
            #print(session)
            """
            check with a query if session end is reached
            """

            checkq = """
            SELECT * from events_test WHERE "sessionid" = '{}' AND "type"='end';
            """.format(session)

            if len(pd.read_sql(checkq, con=crate_connection))>=1 and len(pd.read_sql(checkq, con=crate_connection))<=2:

                """
                retrieve session information from CrateDB
                """
                sessionq = """
                SELECT * from sessions WHERE "SessionId"='{}';
                """.format(session)

                #session information
                sessioninfo = pd.read_sql(sessionq, con=crate_connection)
                sessiontime = gameTime(session)



                #balloon game score: [c, totalReactionTime, totalObjects, totalInteractions, totalCorrect]
                interactions = get_balloon_score(session)
                
                #functional mobility scores
                r = range_of_motion(session)
                fov = field_of_view(session)
                
                '''
                Session information INSERT
                '''
                session_insert = """
                INSERT INTO sessions(sessionid, date, deviceid, game, gameversion, platform, username,sessiontime) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
                """.format(sessioninfo.iloc[0]['SessionId'], sessioninfo.iloc[0]['Date'], sessioninfo.iloc[0]['DeviceId'], sessioninfo.iloc[0]['Game'], float(sessioninfo.iloc[0]['Version']), sessioninfo.iloc[0]['Platform'], sessioninfo.iloc[0]['UserName'], float(sessiontime))
                
                cursor_p.execute(session_insert)


                '''
                Functional Mobility Insert
                '''
                func_insert = """
                INSERT INTO funcmobility(sessionid, headleft, headright, headup, headdown, lefthand, righthand, fov, avgleft, avgright, avgreactiontime) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
                """.format(r['sessionid'], r['headleft'], r['headright'], r['headup'], r['headdown'], r['lefthand'], r['righthand'], fov, r['avgleft'], r['avgright'], interactions[1]/interactions[0])
                
                cursor_p.execute(func_insert)
                cursor_c.execute(func_insert)

                '''
                Balloon Metrics Insert
                '''
                balloon_insert = """
                INSERT INTO balloonmetrics(sessionid, totalobjects, totalinteraction, successfulinteraction) VALUES('{}', '{}', '{}', '{}')
                """.format(session, interactions[2], interactions[3], interactions[4])

                cursor_p.execute(balloon_insert)
                cursor_c.execute(balloon_insert)


if __name__ == '__main__':
    #main()
    schedule.every(5).minutes.do(main)
 
    while True:
        schedule.run_pending()
        time.sleep(1)

