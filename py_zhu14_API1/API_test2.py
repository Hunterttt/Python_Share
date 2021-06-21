import requests
import json
import apicem


ip = "220.181.130.66:18443"
username = "admin"
password = "P@sw0rd@!@#$%"
version = "v6"

requests.packages.urllib3.disable_warnings()

#user = apicem.get(ip,version,username,password,api='object/users')

token = apicem.get_X_auth_token(ip,version,username,password)


