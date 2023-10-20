import datetime
from pydantic import BaseModel


class TemperatureData(BaseModel):

    device_id: str
    temperature:float
    

   