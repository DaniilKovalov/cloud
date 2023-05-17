import pandas as pd 
import requests 
from datetime import datetime 
import boto3
from botocore.exceptions import ClientError
import io

def create_cvs_file(variable):
    url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode={variable}&sort=exchangedate&order=desc&json'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        info = pd.DataFrame(data)
        info.to_csv(f'create_{variable}.csv', index=False)       
    else:
        print("Error while getting data.")
create_cvs_file ("EUR")
create_cvs_file ("USD")

s3_client = boto3.client('s3', region_name='eu-west-3', 
aws_access_key_id = 'AKIA2K2R5AKF3R6JZ5DU', aws_secret_access_key = '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')
     
def upload(bucket, bfile, filename):
        bfile = io.BytesIO(bfile)
        try:
            s3_client.upload_fileobj(bfile, bucket, filename)
        except ClientError as e:
            print(e)
            return False
        return True
 
bfile = open("create_USD.csv", "rb").read()
upload("iptlab2kovalov", bfile, "usd.csv")
 
 
bfile = open("create_EUR.csv", "rb").read()
upload("iptlab2kovalov", bfile, "eur.csv")

data_USD = pd.read_csv('create_USD.csv') 
data_EUR = pd.read_csv('create_EUR.csv')

fig, ax = plt.subplots(1, 1)

data_USD.plot(y='rate', color='yellow', ax=ax, label='$')
data_EUR.plot(y= 'rate', color='blue', ax=ax, label='€')
ax.set_xlabel('day')
ax.set_title('Exchange rate of hryvnia against foreign currencies (Dollar and Euro) for 2021')
ax.legend()
plt.savefig("chart.png")

bfile = open("chart.png", "rb").read()
upload("iptlab2kovalov", bfile, "chart.png")

plt.show()
