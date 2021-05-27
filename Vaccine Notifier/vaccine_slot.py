from datetime import datetime
from enum import Enum
from typing import List
from uuid import UUID
from time import sleep
from plyer import notification
import requests


class Vaccine(Enum):
    COVISHIELD = "COVISHIELD"
    COVAXIN = "COVAXIN"


class Session:
    session_id: UUID
    date: str
    available_capacity: int
    min_age_limit: int
    vaccine: Vaccine
    slots: List[str]

    def __init__(
        self,
        session_id: UUID,
        date: str,
        available_capacity_dose1: int,
        min_age_limit: int,
        vaccine: Vaccine,
        slots: List[str],
        **kwargs
    ):
        self.session_id = session_id
        self.date = datetime.strptime(date, "%d-%m-%Y")
        self.available_capacity = available_capacity_dose1
        self.min_age_limit = min_age_limit
        self.vaccine = vaccine
        self.slots = slots

    def __str__(self):
        ret = str(self.session_id)
        ret = ret + "\n\t" + str(self.date)
        ret = ret + "\n\t" + str(self.available_capacity)
        ret = ret + "\n\t" + str(self.min_age_limit)
        ret = ret + "\n\t" + str(self.vaccine)
        ret = ret + "\n\t" + str(self.slots) + "\n"
        return ret


class Center:
    center_id: int
    name: str
    address: str
    state_name: str
    district_name: str
    block_name: str
    pincode: int
    lat: int
    long: int
    center_from: datetime
    to: datetime
    fee_type: str
    sessions: List[Session]

    @classmethod
    def from_json(cls, json):
        obj = cls()
        obj.center_id = json["center_id"]
        obj.name = json["name"]
        obj.address = json["address"]
        obj.state_name = json["state_name"]
        obj.district_name = json["district_name"]
        obj.block_name = json["block_name"]
        obj.pincode = json["pincode"]
        obj.lat = json["lat"]
        obj.long = json["long"]
        obj.center_from = datetime.strptime(json["from"], "%H:%M:%S")
        obj.to = datetime.strptime(json["to"], "%H:%M:%S")
        obj.fee_type = json["fee_type"]
        obj.sessions = [Session(**x) for x in json["sessions"]]
        return obj

    def __str__(self):
        ret = ""
        ret = ret + "\ncenter_id:" + str(self.center_id)
        ret = ret + "\nname:" + str(self.name)
        ret = ret + "\naddress:" + str(self.address)
        ret = ret + "\nstate_name:" + str(self.state_name)
        ret = ret + "\ndistrict_name:" + str(self.district_name)
        ret = ret + "\nblock_name:" + str(self.block_name)
        ret = ret + "\npincode:" + str(self.pincode)
        ret = ret + "\nCoordinates:" + str(self.lat) + "," + str(self.long)
        ret = ret + "\ncenter_from:" + str(self.center_from)
        ret = ret + "\nto:" + str(self.to)
        ret = ret + "\nfee_type:" + str(self.fee_type)
        return ret


def parse_centers(center_list):
    parsed_center_list = []
    for center in center_list:
        parsed_center_list.append(Center.from_json(center))
    return parsed_center_list


headers = {
    "authority": "cdn-api.co-vin.in",
    "method": "GET",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
}


def get_centers_by_pincode(pincode):
    query_params = {
        "pincode": pincode,
        "date": datetime.now().strftime("%d-%m-%Y"),
    }

    res = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin",
        params=query_params,
        headers=headers,
    )

    if res.status_code == 200:
        return parse_centers(res.json()["centers"])


def get_centers_by_district_id(district_id):
    query_params = {
        "district_id": district_id,
        "date": datetime.now().strftime("%d-%m-%Y"),
    }
    res = requests.get(
        "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict",
        params=query_params,
        headers=headers,
    )

    if res.status_code == 200:
        return parse_centers(res.json()["centers"])


title = "Slots"
message = "Vaccine Slots Found"

pinlist = [
    "110025",
    "110078",
    "122002",
    "122503",
    "122017",
    "122102",
    "122001",
    "122006",
    "122103",
    "122506",
    "122004",
    "121001",
    "201301",
    "201304",
    "203202",
    "203207",
    "203209",
    "203201",
    "201310",
    "203202",
    "203207",
]


while True:
    for pin in pinlist:
        r = get_centers_by_pincode(pin)
        for i in r:
            if i.fee_type != "Free":
                for j in i.sessions:
                    if j.min_age_limit == 18:
                        if j.available_capacity > 0:
                            if j.vaccine == "COVISHIELD":
                                print(
                                    "<==============================================================>"
                                )
                                print(i)
                                print(j)
                                print(
                                    "<==============================================================>"
                                )
                                notification.notify(
                                    title=title,
                                    message=message,
                                    app_icon=None,
                                    timeout=10,
                                    toast=False,
                                )
    sleep(900)