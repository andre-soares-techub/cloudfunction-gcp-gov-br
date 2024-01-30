import functions_framework
import pandas as pd 
import requests 
import io
from google.cloud import storage
from datetime import datetime

@functions_framework.http
def call_api(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    URL_API= request.args.get('URL_API')
    PROJECT_ID= request.args.get('PROJECT_ID')
    BUCKET_NAME= request.args.get('BUCKET_NAME')
    PATH_FILE= request.args.get('PATH_FILE')

    if URL_API is not None and PROJECT_ID is not None and BUCKET_NAME is not None and PATH_FILE is not None:
      data = requests.get(URL_API)

      if data.status_code == 200:
        df_data = pd.read_csv(io.StringIO(data.content.decode('utf-8'))).astype(str)

        print(df_data.columns)
        print(df_data.info())
        print(df_data.head(10))

        storage_client = storage.Client(project=PROJECT_ID)

        bucket = storage_client.get_bucket(BUCKET_NAME)
        bucket.blob(PATH_FILE).upload_from_string(df_data.to_csv(sep=',', header='True', index=False), 'text/csv')
        print(f'status {data.status_code} e arquivos salvos em {PATH_FILE}')
      else:
        print(f'algo errado não esta certo jovem ,status {data.status_code}')
      return "Os parâmetros foram passados"
    else:
        "Os parâmetros não foram passados"

