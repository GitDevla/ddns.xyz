# ddns.xyz
Dynamic DNS for [gen.xyz](https://gen.xyz/)

## Installation
1. Install dependencies
```shell
$ pip install -r requirements.txt
```
2. Edit `.env` to your needs

## Usage
Use `crontab` to run python script periodically.

Example for every 30 minutes: 

`*/30 * * * * /usr/bin/python3.9 pathTo/ddns.py >> pathTo/log`
