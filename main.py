from app.services.refresh_token import meli_refresh_token
from app.services.init_creds import init_creds
import time

#credenciales = {
#     1:{ 
#     "app_id" : "xxx" ,
#     "client_secret" : "xxx" ,
#     "refresh_token" : "xxx",
#     "description" : "xxx",}}
#    

if  __name__ == '__main__':   
    #init_creds (credenciales)
    while True:
        meli_refresh_token()
        #time.sleep(3*60*60) > se setea desde GCP JOB
        