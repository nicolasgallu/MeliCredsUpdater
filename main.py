from app.services.refresh_token import meli_refresh_token
from app.services.init_creds import init_creds

#credenciales = {
#     1:{ 
#     "app_id" : "xxx" ,
#     "client_secret" : "xxx" ,
#     "refresh_token" : "xxx",
#     "description" : "xxx",}}
#    

if  __name__ == '__main__':   
    #init_creds (credenciales)
    meli_refresh_token()
        