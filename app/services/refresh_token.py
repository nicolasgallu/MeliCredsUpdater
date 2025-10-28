import json
import requests
from app.gbq.methods import read_table,trunc_table
from app.config.config import GBQ_CREDS_SCHEMA
from app.utils.logger import logger
from datetime import datetime, timedelta
from app.services.email_notific import notify_human

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
            if response.status_code == 200:
                created_data = datetime.now()
                expired_date_norm = datetime.now() + timedelta(hours = json_data["expires_in"]/3600)
                json_data["app_id"] = app_id
                json_data["client_secret"] = client_secret
                json_data["description"] = description
                json_data["token_created_at"] = str(created_data)
                json_data["expiring_at"] = str(expired_date_norm)
                batch.append(json_data)
                logger.info("Renovacion de credenciales exitosa.")
                logger.info("Cargando credenciales en GBQ...")
            else:
                logger.info("Fallo en renovacion de token")
        except Exception as e:
            logger.info("Fallo en renovacion de token")
            notify_human("INCIDENTE: Renovacion Credenciales",e)

    batch = json.dumps(batch)
    batch = json.loads(batch)
    trunc_table(GBQ_CREDS_SCHEMA,batch)

