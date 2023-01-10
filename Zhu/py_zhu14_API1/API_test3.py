import requests
def get_access_token(host, port, user, passwd):
    """
    Requires Python 3.0 or greater and requests lib.
    Login to FTD device and obtain an access token. The access token is required so that the user can
    connect to the device to send REST API requests. 
    :param host: ftd host address
    :param port: ftd port
    :param user: login user name
    :param passwd: login password
    :return: OAUTH access token
    """
    access_token = None
    requests.packages.urllib3.disable_warnings()
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(user, passwd)
    auth_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        response = requests.post("https://{}:{}/api/fdm/latest/fdm/token".format(host, port),
                                 data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print("Login successful, access_token obtained")
    except Exception as e:
        print("Unable to POST access token request: {}".format(str(e)))
    return access_token


def iget(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a GET rquest to obtain the pending changes from the FTD device
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :return: True if changes are pending, otherwise False
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    #state = None
    pending_changes_url = 'api/fdm/latest/object/users'
    #pending_changes_url = 'api/slot'
    response = requests.get('https://{host}:{port}/{url}'.format(host=host, port=port, url=pending_changes_url),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET pending changes response {} {}".format(response.status_code, response.json()))
    

    else:
        #state = response.json()#.get('state')
        print(response.json())
        #print(state)
        #return state

    '''
    else:
        print(response.json())
        if response.json().get('items'):
            changes_found = True
    return changes_found
    '''

def main():
   access_token = get_access_token('220.181.130.66','18443','admin','P@sw0rd@!@#$%')
   #print(access_token)
   iget('220.181.130.66','18443',access_token)
   #print(user)

if __name__ == '__main__':
    main()