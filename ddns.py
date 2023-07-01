import requests
import os
import json
from urllib.parse import urlencode


class Record:
    def __init__(self, host, type, address):
        self.host = host
        self.type = type
        self.address = address

    def urlencode(self):
        url = {
            "dnsrecordhost[]": self.host,
            "dnsrecordtype[]": self.type,
            "dnsrecordaddress[]": self.address,
        }
        return urlencode(url)


def read_previous_ip():
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/last_ip"
    if not os.path.exists(dir_path):
        with open(dir_path, "w") as file:
            file.write("0.0.0.0")
    oldIPFile = open(dir_path, "r")
    oldIP = oldIPFile.readlines()[0]
    oldIPFile.close()
    return oldIP


def read_current_ip():
    res = requests.get("https://ipinfo.io/ip")
    res.raise_for_status()
    return res.text


def write_new_ip(newIP):
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/last_ip"
    oldIPFile = open(dir_path, "w")
    oldIPFile.write(newIP)
    oldIPFile.close()


def login(session, mail, password):
    url = "https://gen.xyz/account/dologin.php"
    payload = {"username": mail, "password": password}
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = session.request(
        "POST", url, data=payload, headers=headers, allow_redirects=False
    )
    return response


def update_ddns(session, domainId, hosts):
    url = "https://gen.xyz/account/clientarea.php"
    querystring = {"action": "domaindns"}
    payloadHead = {
        "masked-redirect": "",
        "sub": "save",
        "domainid": domainId,
    }

    payloadHosts = [i.urlencode() for i in hosts]

    payload = urlencode(payloadHead) + "&" + "&".join(payloadHosts)
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = session.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        params=querystring,
        allow_redirects=False,
    )
    return response


def read_env():
    with open("env.json") as file:
        return json.load(file)


if __name__ == "__main__":
    try:
        newIP = read_current_ip()
    except:
        print("Can't connect to ipinfo.io, aborting...")
        quit()
    oldIP = read_previous_ip()
    print("Old: " + oldIP + " vs New: " + newIP)

    if newIP == oldIP:
        quit()

    write_new_ip(newIP)

    config = read_env()

    hosts = [
        Record(i["name"], i["type"], i["address"] or newIP) for i in config["hosts"]
    ]

    session = requests.session()
    login(session, config["user"]["mail"], config["user"]["password"])
    res = update_ddns(session, config["domainID"], hosts)

    if res.ok:
        print("Updated")
    else:
        print("Something went wrong")
