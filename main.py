import requests
from datetime import datetime

import api_keys
from api_keys import telegram_api
today=datetime.now()
today_date=today.strftime("%d-%m-%Y")

COWIN_ENDPOINT="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
TELEGRAM_ENDPOINT=api_keys.telegram_api;
# message="none"
def fetch_cowin_data(district_id):
    cowin_params = {
        "district_id": district_id,
        "date": today_date
    }
    response=requests.get(url=COWIN_ENDPOINT,params=cowin_params)
    data=response.json()["centers"]
    check_availability(data)

def check_availability(data):
    for center in data:
        for session in center["sessions"]:
            if session["available_capacity_dose1"] >0 and session["min_age_limit"] ==18:
                message=f" Pincode = {center['pincode']}\n Center name = {center['name']}\n Slots = {session['available_capacity_dose1']}\n Minimum age = {session['min_age_limit']}\n Date = {session['date']}\n Vaccine = {session['vaccine']}\n Fee type={center['fee_type']}"
                send_telegram_alert(message)

def send_telegram_alert(msg):
    telegram_params = {
        "chat_id": "@cowin_vaccination_alert",
        "text": msg
    }
    response = requests.get(url=TELEGRAM_ENDPOINT, params=telegram_params)
    print(response.text)


if __name__ == "__main__":
    fetch_cowin_data(147)