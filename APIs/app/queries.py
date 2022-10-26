import pandas as pd
import numpy as np
import math

crate_connection = 'crate://129.128.184.214:4200/'
psql_connection = 'postgresql://vgym:vgym123@172.17.0.1:5433/vgym'


def get_sessions(username: str) -> pd.DataFrame:
    """
    Parameter(s): username
    Returns a dataframe of sessions for a user
    """
    query = """
        SELECT *
        FROM sessions
        WHERE "UserName" = '{}';
    """.format(username)
    #df = pd.read_sql(query, con=crate_connection)
    #df['Date'] = pd.to_datetime(df['Date'].map(lambda x: x.replace('.', ':')))
    df = pd.read_sql(query, con=crate_connection)
    df['Date'] = pd.to_datetime(df['Date'].map(lambda x:x.replace('.', ':')))
    df = df.sort_values('Date', ascending=False)
    return df




###Get sessions from PSQL for a username
def get_sessions_psql(username: str) -> pd.DataFrame:
    """
    Parameter(s): username
    Returns a dataframe of session info for a user
    """

    query = """
    SELECT * FROM sessions
    WHERE "username" = '{}';
    """.format(username)

    df = pd.read_sql(query, con=psql_connection)
    df['date'] = pd.to_datetime(df['date'].map(lambda x: x.replace('.', ':')))
    df = df.sort_values('date', ascending=False)
    return df


###Scores for a balloon session for a balloon sessionid from PSQL
def balloon_session_metrics(sessionid: str) -> pd.DataFrame:

    """
    Parameter(s): sessionid of a balloon game
    Returns a dataframe of information about the balloon session
    """

    query = """
    SELECT * 
    FROM balloonmetrics
    WHERE "sessionid" = '{}';
    """.format(sessionid)

    df = pd.read_sql(query, con=psql_connection)
    return df

###Functional Mobillity Score for any game with a sessionid from PSQL
def functional_mobility(sessionid: str) -> pd.DataFrame:
    """
    Parameter(s): sessionid of any game
    Returns a dataframe of functional mobility scores of a session
    """

    query = """
    SELECT *
    FROM funcmobility
    WHERE "sessionid" = '{}';
    """.format(sessionid)

    df = pd.read_sql(query, con=psql_connection)
    return df


def get_balloon_score(sessionid: str) -> list:
    """
    Parameter(s): balloon sessionid
    Returns three values: percentage of success, percentatge of miss, total no. of balloons
    """

    query = """
    SELECT * FROM events WHERE "session_id" = '{}';
    """.format(sessionid)

    df_events = pd.read_sql(query, con=crate_connection)

    #count interactions

    count_Total = len(df_events)
    count_Interactions = len(df_events[df_events['event_type']=='contact-correct']) + len(df_events[df_events['event_type']=='contact-incorrect'])
    count_Correct = len(df_events[df_events['event_type']=='contact-correct'])

    return [count_Total, count_Interactions, count_Correct]

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
  print("Max Head Movement to Left is %.2f units" %(math.sqrt(lx*lx+ly*ly+lz*lz)))
  print("Max Head Movement to Right is %.2f units" %(math.sqrt(rx*rx+ry*ry+rz*rz)))
  print("Max Head Movement to Upwards is %.2f units" %(math.sqrt(ux*ux+uy*uy+uz*uz)))
  print("Max Head Movement to Downwards is %.2f units" %(math.sqrt(dx*dx+dy*dy+dz*dz)))

  #LeftController
  #has to be calculated from the Relative position of the Controllers w.r.t. the CenterEyeAnchor
  left = (sessionData['CenterEyeAnchor_posx']-sessionData['LeftControllerAnchor_relx'])*(sessionData['CenterEyeAnchor_posx']-sessionData['LeftControllerAnchor_relx'])+(sessionData['CenterEyeAnchor_posy']-sessionData['LeftControllerAnchor_rely'])*(sessionData['CenterEyeAnchor_posy']-sessionData['LeftControllerAnchor_rely'])+(sessionData['CenterEyeAnchor_posz']-sessionData['LeftControllerAnchor_relz'])*(sessionData['CenterEyeAnchor_posz']-sessionData['LeftControllerAnchor_relz'])
  print("Maximum Left Hand Stretch w.r.t. the Head Center Position is %.2f units" %(math.sqrt(left.max(axis=0))))


  #RightController
  #has to be calculated from the Relative position of the Controllers w.r.t. the CenterEyeAnchor
  right = (sessionData['CenterEyeAnchor_posx']-sessionData['RightControllerAnchor_relx'])*(sessionData['CenterEyeAnchor_posx']-sessionData['RightControllerAnchor_relx'])+(sessionData['CenterEyeAnchor_posy']-sessionData['RightControllerAnchor_rely'])*(sessionData['CenterEyeAnchor_posy']-sessionData['RightControllerAnchor_rely'])+(sessionData['CenterEyeAnchor_posz']-sessionData['RightControllerAnchor_relz'])*(sessionData['CenterEyeAnchor_posz']-sessionData['RightControllerAnchor_relz'])
  print("Maximum Right Hand Stretch w.r.t. the Head Center Position is %.2f units" %(math.sqrt(right.max(axis=0))))

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

    rom['Session Id'] = sessionid
    rom['Max Head Left'] = max(hleft)*100
    rom['Max Head Right'] = max(hright)*100
    rom['Max head Up'] = max(hup)*100
    rom['Max Head Down'] = max(hdown)*100
    rom['Max Left Hand Stretch'] = max(leftC)*100
    rom['Average Left Hand Stretch'] = (sum(leftC)/len(leftC))*100
    rom['Max Right Hand Stretch'] = max(rightC)*100
    rom['Average Right Hand Stretch'] = (sum(rightC)/len(rightC))*100

    return rom



def s():
    query = """
    Select sessionid from sessions;
    """

    df = pd.read_sql(query, psql_connection)

    return df

