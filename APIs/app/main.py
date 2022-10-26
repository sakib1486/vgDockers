
from enum import Enum
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from typing import List, Optional, Set
from pydantic import BaseModel
import re
import json
from fastapi.encoders import jsonable_encoder
from crate import client
import datetime
from string import digits
from brotli_asgi import BrotliMiddleware

from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as sa
from fastapi_socketio import SocketManager
from prescription_generator import *
from fastapi.responses import *
from fastapi.middleware.cors import CORSMiddleware

from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
from queries import *
from datetime import datetime
import pytz

app = FastAPI(
    title = "APIs",
    description = "Endpoints to retrieve data",
    version="0.1",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://virtual-gym-dashboard.web.app",
    "http://129.128.184.214:8099"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}



@app.get("/test")
async def test_localhost():
    try:
        df = connect_psql()
        return {"msg": "successfl connection"}
    except Exception as e:
        return {"error": str(e)}




# make a get request endpoint called "/sessions" that takes a username parameter and can retrieve session names in a specified data range
@app.get("/sessions/{username}")
async def read_sessions(username: str, start_date: int = None, end_date: int = None):
    try:
        df = get_sessions(username)
        if start_date and end_date:
            # convert int to datetime
            start_date = datetime.datetime.fromtimestamp(start_date)
            end_date = datetime.datetime.fromtimestamp(end_date)
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        return df.to_json(orient='records')
    except Exception as e:
        return {"error": str(e)}



'''
APPIs to make communication with PSQL
'''

#sessions list from psql
@app.get("/s/")
async def se():
    try:
        df = s()
        return df.to_json(orient='records')
    except Except as e:
        return {"error": str(e)}



#make a get request to retrieve session for a username
@app.get("/sessionsList/{username}")
async def read_sessions_psql(username: str, start_date: int = None, end_date: int = None):
    try:
        df = get_sessions_psql(username)
        if start_date and end_date:
            # convert int to datetime
            start_date = datetime.datetime.fromtimestamp(start_date)
            end_date = datetime.datetime.fromtimestamp(end_date)
            df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        return df.to_json(orient='records')
    except Exception as e:
        return {"error": str(e)}


# make a get request to retrieve the balloon score metrics from PSQL database with a session id
@app.get("/balloon/{sessionid}")
async def read_balloon_metric(sessionid: str):
    try:
        df = balloon_session_metrics(sessionid)

        return df.to_json(orient='records')
    except Exception as e:
        return {'error': str(e)}


# make a get request to retrieve functional mobility scores from PSQL with a sessionid
@app.get("/functional/{sessionid}")
async def read_funcmobility(sessionid: str):
    try:
        df = functional_mobility(sessionid)

        return df.to_json(orient='records')
    except Exception as e:
        return {'error' : str(e)}
'''
Other APIs for CrateDB, Kafka etc. etc.
'''


# testing kafka with a test message
@app.get("/test-kafka")
async def test_kafka():
    producer.send("session_meta", '{"Game":"testing", "Platform":"Fake"}'.encode())
    return {"success": "check the topic session_data"}

# API to generate random bubbles prescription
@app.get("/bubbles-prescription", response_class=PlainTextResponse)
async def bubbles_prescription():
    return generate_bubbles() 


# API which receives a Sessionid for the balloon game, and can retrieve the balloon scores from CrateDB: [TotalObjects, InteractedObjects, CorrectlyInteracted]
@app.get("/balloonscore/{sessionid}")
async def balloon_score(sessionid: str):
    try:
        counts = get_balloon_score(sessionid)
        collect = {
                "TotalObjects" : counts[0],
                "InteractedObjects" : counts[1],
                "CorrectlyInteracted" : counts[2]
                }
        return json.dumps(collect)
    except Exception as e:
        return {"error":str(e)}

# API to generate sessionTime for any session when called with a sessionid from CrateDB in seconds
@app.get("/sessionTime/{sessionid}")
async def sessionTime(sessionid: str):
    try:
        sessionTime = gameTime(sessionid)

        collect = {
                "Total Session Time":sessionTime
                }
        return json.dumps(collect)

    except Exception as e:
        return {"error":str(e)}

# API to measure the range of motions for a specified session when called with a sessionid, returns a JSON object 
@app.get("/rom/{sessionid}")
async def rom(sessionid: str):
    try:
        ranges = range_of_motion(sessionid)
        return json.dumps(ranges)
    except Exception as e:
        return {"error":str(e)}


# API to measure retrieve current server time
@app.get("/servertime")
async def servertime():
    try:
        today = datetime.now(pytz.timezone('Canada/Mountain')).isoformat()
        return {"servertime": today}
    except Exception as e:
        return {"error":str(e)}

@app.get("/hi")
async def hi():
    try:
        return {"message": "hello"}
    except Exception as e:
        return {"error":str(e)}



'''
WEBSOCKET FOR STREAMING DATA
'''

# API websocket to connect to the kafka topic and stream the data through to Spark -> CrateDB from the Oculus
@app.websocket("/ws")
async def websocket_event_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        raw_data = await websocket.receive_text()
        try:
            message = json.loads(raw_data)
        except:
            break
        if message.get("type") == "frame":
            topic = 'session_frame'
        elif message.get("type") == "event":
            topic = 'session_event'
        elif message.get("type") == "session":
            topic = 'session_meta'
        else:
            producer.send("session_data", str(raw_data).encode('utf-8'))
            continue
        producer.send(topic, str(message.get("content")).encode('utf-8'))


producer = KafkaProducer(bootstrap_servers=['broker:29092'])
socket_manager = SocketManager(app=app)

