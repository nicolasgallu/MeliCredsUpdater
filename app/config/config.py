import os

GBQ_ACCOUNT = {
'type': os.getenv("type"),
'project_id': os.getenv("project_id"),
'private_key_id': os.getenv("private_key_id"),
'private_key': os.getenv("private_key").replace('\\n', '\n'),
'client_email': os.getenv("client_email"),
'client_id': os.getenv("client_id"),
'auth_uri': os.getenv("auth_uri"),
'token_uri': os.getenv("token_uri"),
'auth_provider_x509_cert_url': os.getenv("auth_provider_x509_cert_url"),
'client_x509_cert_url': os.getenv("client_x509_cert_url"),
'universe_domain': os.getenv("universe_domain")
}

DATASET_ID=os.getenv("DATASET_ID")

GBQ_CREDS_SCHEMA = {
    'credentials': {
        'field': ['app_id','client_secret','access_token','token_type','expires_in','scope','user_id','refresh_token','description','token_created_at','expiring_at'],
        'type': ['INTEGER','STRING','STRING','STRING','STRING','INTEGER','STRING','INTEGER','STRING','STRING','TIMESTAMP','TIMESTAMP'],
        'mode': ['REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED','REQUIRED']
    }
}


