# State ID - 21
# District ID - 363

import requests
import json
import time
from datetime import datetime
import sys

from loguru import logger


def sink(message):
    record = message.record
    if record.get("name") == "your_specific_logger":
        print("Log comes from your specific logger")


logger = logger.bind(name="your_specific_logger")


def getAvl(pincode, date):
    # req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=" + pincode + "&date=" + date

    req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + pincode + "&date=" + date
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        data = requests.get(req, headers=headers)
        li = data.json()["centers"]
        data.raise_for_status()
        return li
    except requests.exceptions.HTTPError as errh:
        logger.info(errh)
        return []
    except requests.exceptions.ConnectionError as errc:
        logger.info(errc)
        return []
    except requests.exceptions.Timeout as errt:
        logger.info(errt)
        return []
    except requests.exceptions.RequestException as err:
        logger.info(err)
        return []
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        logger.info(message)
        return []


pincodes = ["411011", "411001", "411033", "411006", "411028", "411038", "411041", "411027", "411018", "411035",
            "411026", "411017", "411044"]
check_date = "05-05-2021"

while 1:

    for pins in pincodes:

        li_centers = getAvl(pins, check_date)

        logger.info(li_centers)

        if not li_centers:
            logger.info('Server not returning any data.')
            pass
            # data = {
            #    'chat_id': '-599964487',
            #    'text': 'Server not returning any data.'
            # }

            # requests.post('https://api.telegram.org/bot1797289547:AAE-8ENA0LyzCQZdPm0SXwDkTYEGTPZQruk/sendMessage',
            #             data=data)

        else:

            # for x in li_centers:
            # logger.info(json.dumps(x, indent=4, sort_keys=False))
            # print(json.dumps(x, indent=4, sort_keys=False))

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
                            'text': 'Vaccine incoming.\n\n ' + 'Vaccine Capacity : ' + str(
                                avl) + '\n\n' + fee_type + ' : Fee Type\n\n' + date + ' : Date\n\n' + center_name + ' : Center Name.\n\n' + str(
                                pincode) + ' : Pincode \n\n' + 'Age Limit : ' + str(
                                age_limit) + '\n\nLast Checked availability : ' + log_time
                        }

                        requests.post(
                            'https://api.telegram.org/bot1797289547:AAE-8ENA0LyzCQZdPm0SXwDkTYEGTPZQruk/sendMessage',
                            data=data)
    time.sleep(150)
