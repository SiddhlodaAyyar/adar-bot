import requests
from loguru import logger
import time


def sink(message):
    record = message.record
    if record.get("name") == "your_specific_logger":
        print("Log comes from your specific logger")


logger = logger.bind(name="your_specific_logger")


def getAvl(pincode, date):
    req = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + pincode + "&date=" + date
    headers = {'Accept': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    try:
        data = requests.get((req) , headers=headers)
        #li = data.json()["centers"]
        data.raise_for_status()
        return data
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
        try:
            print(li_centers.json())
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logger.info(message)




    time.sleep(150)

