import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv

load_dotenv()
MY_LAT = 11.747378 
MY_LONG =79.846251 
my=os.environ.get("EMAIL_KEY")
password=os.environ.get("PASSWORD_KEY")
to=os.environ.get("TO_MAIL_ADDRESS")
def iss_ovrh():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5<=iss_latitude<=MY_LAT+5 and MY_LONG-5<=iss_longitude<=MY_LONG+5:
        return True

def is_dark():     
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    if time_now.hour>=sunset or time_now<=sunrise:
        return True
    
        
while True:
    
    time.sleep(60)
    if is_dark and iss_ovrh:
        with smtplib.SMTP("smtp.gmail.com") as c:
            c.starttls()
            c.login(user=my,password=password)
            c.sendmail(from_addr=my,
            to_addrs=to,
            msg="Subject:ISS is Above\n\nGO TO THE TERRACE AND LOOK UP"
            )





