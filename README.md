# ddns.xyz
Dynamic DNS for [gen.xyz](https://gen.xyz/)

I'm not affiliated with the Register in any way. This is a script for personal use, but welcome to suggestions.

## Installation
1. Install dependencies
```shell
$ pip install -r requirements.txt
```
2. Edit `env.json` to your needs

## Usage
Use `crontab` to run python script periodically.

Example for every 30 minutes: 

`*/30 * * * * /usr/bin/python3.9 pathTo/ddns.py >> pathTo/log`
