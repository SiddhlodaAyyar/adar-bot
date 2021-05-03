# State ID - 21
# District ID - 363

import requests
import json
import time
from datetime import datetime


def getAvl(pincode, date):
    # req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + pincode + "&date=" + date
    req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + pincode + "&date=" + date
    li = requests.get(req).json()["centers"]
    return li


pincodes = ["411011", "411001", "411033", "411006"]
check_date = "03-05-2021"

while 1:

    for pins in pincodes:

        li_centers = getAvl(pins, check_date)

        # for x in li_centers:
        #     print(json.dumps(x, indent=4, sort_keys=False))

        for x in li_centers:
            center_name = x["name"]
            pincode = x["pincode"]
            fee_type = x["fee_type"]
            for y in x["sessions"]:
                date = y["date"]
                avl = y["available_capacity"]
                age_limit = y["min_age_limit"]
                log_time = datetime.now().strftime("%H:%M:%S")
                if (avl > 0) and (age_limit == 18):
                    data = {
                        'chat_id': '-599964487',
                        'text': 'Vaccine aya hai bsdk, book karle.\n ' + center_name + ' : idhar jaake marwa ke le.\n' + str(pincode) + ' : iss pincode pe.\n'+'age_limit : ' + str(age_limit) + '. 18 saal ka hoga toh jaa nahi toh gharmei baithke porn dekh.\n'+'Last Checked availability : ' + log_time
                    }

                    requests.post('https://api.telegram.org/bot1797289547:AAE-8ENA0LyzCQZdPm0SXwDkTYEGTPZQruk/sendMessage',
                                 data=data)
    time.sleep(360)
