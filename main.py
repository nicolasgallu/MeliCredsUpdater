from app.services.refresh_token import meli_refresh_token
from app.services.init_creds import init_creds
import time
#testear este codigo de tokens en contenedor, cada 4min para ver que corra bien el schedule.


if  __name__ == '__main__':   
    # init_creds (credenciales)
    while True:
        meli_refresh_token()
        time.sleep(3*60*60)
        