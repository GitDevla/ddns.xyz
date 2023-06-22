import requests
import os
from dotenv import dotenv_values

config = {**dotenv_values(".env")}


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


def update_ddns(session, domainId, host, newIP):
    url = "https://gen.xyz/account/clientarea.php"
    querystring = {"action": "domaindns"}
    payload = {
        "masked-redirect": "",
        "sub": "save",
        "domainid": domainId,
        "dnsrecordhost[]": host,
        "dnsrecordtype[]": "A",
        "dnsrecordaddress[]": newIP,
    }
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

    session = requests.session()
    login(session, config["LOGIN_MAIL"], config["LOGIN_PASSWORD"])
    res = update_ddns(session, config["DOMAIN_ID"], config["DNS_HOST"], newIP)
    if res.ok:
        print("Updated")
    else:
        print("Something went wrong")
