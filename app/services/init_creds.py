import requests
import pandas as pd
from datetime import datetime, timedelta
from app.utils.logger import logger

def init_creds (credenciales):
    batch = []
    for credencial in credenciales:
        credencial = credenciales[credencial]
        app_id = credencial['app_id']
        client_secret = credencial['client_secret']
        refresh_token = credencial['refresh_token']
        description = credencial['description']

        url = 'https://api.mercadolibre.com/oauth/token'
        header = {'accept': 'application/json','content-type': 'application/x-www-form-urlencoded'}
        body = {'grant_type':'authorization_code',
            'client_id':app_id,
            'client_secret':client_secret,
            'code':refresh_token,
            'redirect_uri':'https://httpbin.org/get',}
        
        response = requests.post(url,headers=header,params=body) 
        json_data = response.json()
        created_data = datetime.now()
        expired_date_norm = datetime.now() + timedelta(hours = json_data["expires_in"]/3600)
        json_data["app_id"] = app_id
        json_data["client_secret"] = client_secret
        json_data["description"] = description
        json_data["token_created_at"] = str(created_data)
        json_data["expiring_at"] = str(expired_date_norm)

        batch.append(json_data)
        logger.info("Renovacion de credenciales exitosa.")

    datafr = pd.DataFrame(batch)
    datafr.to_csv("new.csv",index=False)