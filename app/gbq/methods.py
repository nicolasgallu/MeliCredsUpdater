from google.cloud import bigquery
from google.oauth2.service_account import Credentials
from app.config.config import GBQ_ACCOUNT,DATASET_ID
from app.utils.logger import logger
from app.services.email_notific import notify_human


credentials = Credentials.from_service_account_info(GBQ_ACCOUNT)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


def ensure_table(input_schema):
    table_name = list(input_schema)[0]
    table_path = client.dataset(DATASET_ID).table(table_name)
    try:
        client.get_table(table_path)
    except:
        schema = []
        for i in range(len(input_schema[table_name]['field'])):
            schema.append(
                bigquery.SchemaField(
                    input_schema[table_name]['field'][i], 
                    input_schema[table_name]['type'][i], 
                    mode=input_schema[table_name]['mode'][i])
                    )
        table = bigquery.Table(table_path, schema=schema)
        client.create_table(table)


def read_table(input_schema):
    try:
        table_name = list(input_schema)[0]
        table_path = client.dataset(DATASET_ID).table(table_name)
        query = (
            f'SELECT *'
            f'FROM `{table_path}` '
            'QUALIFY ROW_NUMBER() OVER(PARTITION BY app_id ORDER BY token_created_at DESC) = 1'
            )
        result = client.query(query).result()
        results_list_of_dicts = [dict(row.items()) for row in result]
        return results_list_of_dicts
    except Exception as e:
        logger.info("Fallo en la lectura de credenciales anteriores")
        notify_human("INCIDENTE: Renovacion Credenciales",e)



def trunc_table(input_schema, data):
    table_name = list(input_schema)[0]
    table_path = client.dataset(DATASET_ID).table(table_name)
    job_config = bigquery.LoadJobConfig(
                    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,) 
    try:
        load_job = client.load_table_from_json(
            json_rows=data,
            destination=table_path,
            job_config=job_config,) 
        load_job.result()
        logger.info(f"Table {table_path} truncated and loaded successfully!")
    except Exception as e:
        logger.info("Fallo en la escritura de credenciales")
        notify_human("INCIDENTE: Renovacion Credenciales",e)
