import threading
import json
import schedule
import time
from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import TempData
from config import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
session = Session(engine)

origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/temp_data/")
def getTemperatureData():
    with open('/home/ubuntu/lyv_project/config.json', 'r') as config_file:
        config = json.load(config_file)
    try:
        temp_data = TempData(temperature=config['devices'][0]['temperature'], temp_scales='celcius')
        session.add(temp_data)
        session.commit()
        return {'message': 'temperature added successfully!'}
        
    except Exception as e:
        return {'error': e}

interval_minutes = 1
def scheduled_task():
    schedule.every(interval_minutes).minutes.do(getTemperatureData)
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=scheduled_task)
scheduler_thread.start()

@app.get('/fetch_latest_data/')
def fetchLatestTemp():
    temp_list = []
    try:
        fetch_data = session.query(TempData).order_by(TempData.creation_datetime.desc()).limit(1)
        for i in fetch_data:
           temp_list.append({'temp':i.temperature})
        return {'message':'success', 'data': temp_list}
        
    except Exception as e:
        print(e)
        return {'error': e}


@app.get('/fetch_temp_details/')
def fetchLatestTempDetails():
    temp_list = []
    try:
        fetch_data = session.query(TempData).order_by(TempData.creation_datetime.desc())
        print(fetch_data,'==================================')
        for i in fetch_data:
           temp_list.append({'time':i.creation_datetime, 'temp':i.temperature})
        return {'message':'success', 'data': temp_list}
        
    except Exception as e:
        return {'error': e}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)