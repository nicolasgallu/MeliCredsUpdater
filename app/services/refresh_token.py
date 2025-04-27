import requests
import json
from app.gbq.methods import read_table,trunc_table
from app.config.config import GBQ_CREDS_SCHEMA
from datetime import datetime, timedelta


def meli_refresh_token():

    credentials = read_table(GBQ_CREDS_SCHEMA)

    batch = []
    for credential in credentials:
        app_id = credential['app_id']
        client_secret = credential['client_secret']
        refresh_token = credential['refresh_token']
        description = credential['description']
        try:
            data = {
            'grant_type': 'refresh_token',
            'client_id': app_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            }
            headers = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded'}
            response = requests.post('https://api.mercadolibre.com/oauth/token', headers=headers, data=data)
            json_data = response.json()
        except:
            print("fallo en renovacion de token")

        created_data = datetime.now()
        expired_date_norm = datetime.now() + timedelta(hours = json_data["expires_in"]/3600)
        json_data["app_id"] = app_id
        json_data["client_secret"] = client_secret
        json_data["description"] = description
        json_data["token_created_at"] = str(created_data)
        json_data["expiring_normalized_at"] = str(expired_date_norm)
        batch.append(json_data)
    print(batch)
    print(type(batch))
    batch = json.dumps(batch)
    batch = json.loads(batch)
    trunc_table(GBQ_CREDS_SCHEMA,batch)

