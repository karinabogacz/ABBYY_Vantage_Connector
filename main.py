import os
from typing import Text
import requests
import ast
import json
from requests import status_codes
from requests.api import request
import time
import shutil
from pathlib import Path
from requests.adapters import HTTPAdapter


head = {"Content-type": "application/x-www-form-urlencoded"}
obj = {"grant_type": "password", "scope": "openid permissions", "username": "", "password": "", "client_id": "ABBYY.Vantage", "client_secret": ""}

skill_name = ""
path_import = ""
path_export = ""
path_processed = ""

''' Authorize '''
def auth():

    try:
        auth = requests.post("https://vantage-eu.abbyy.com/auth2/connect/token", headers=head, data=obj)
        auth.encoding ="application/x-www-form-urlencoded"

    except requests.exceptions.ConnectionError:
        auth.status_code = "Connection refused"
        exit(0)

    access_token = ast.literal_eval(auth.text)
    token_header = "Bearer " + access_token["access_token"]
    return token_header


''' Receive a list of the available Skills '''

authorization = {"Authorization": auth()}
skills = requests.get("https://vantage-eu.abbyy.com/api/publicapi/v1/skills", headers=authorization)
skills_list = ast.literal_eval(skills.text)

skill_name_exist = False
skill_id = []

for skill in skills_list:
    for key in skill:
        if skill[key] == skill_name:
            skill_name_exist = True
            skill_id.append(skill["id"])

if not skill_name_exist:

    print("Skill does not exist")
    exit(0)

def process(skill_id, file):

    ''' Create an empty transaction to receive the transaction identifier '''

    authorization = {"Authorization": auth()}
    transaction_data = ast.literal_eval(json.dumps({"skillId": skill_id[0]}))
    transactions = requests.post("https://vantage-eu.abbyy.com/api/publicapi/v1/transactions", headers=authorization, json=transaction_data)

    transaction_id = ast.literal_eval(transactions.text)["transactionId"]
    #print(f"Trans stat code {transactions.status_code}")

    ''' Add a file to be processed in the transaction '''

    authorization = {"Authorization": auth()}
    url_trans = "https://vantage-eu.abbyy.com/api/publicapi/v1/transactions/"+transaction_id+"/files"

    files = {
    'Files': (file, open(path_import+file, 'rb'), 'image/tiff'),
    }

    files_transaction = requests.post(url_trans, headers=authorization, files=files)


    ''' Start the transaction to process files '''

    url_trans_start = "https://vantage-eu.abbyy.com/api/publicapi/v1/transactions/"+transaction_id+"/start/"
    transaction_start = requests.post(url_trans_start, headers=authorization)

    url_trans_launch = "https://vantage-eu.abbyy.com/api/publicapi/v1/transactions/launch?skillId="+str(skill_id[0])
    transaction_launch = requests.post(url_trans_start, headers=authorization, files=files)


    ''' Monitor the transaction status and get file id'''

    url_trans_monitor = "https://vantage-eu.abbyy.com/api/publicapi/v1/transactions/"+transaction_id
    print(f"\nFile: {file}")
    print("Processing...")
    for x in range(10):
        transaction_status = requests.get(url_trans_monitor, headers=authorization)
        if ast.literal_eval(transaction_status.text)["status"] == "Processed":
            print("Processed")
            break
        time.sleep(4)

    file_id = ast.literal_eval(transaction_status.text)["documents"][0]["resultFiles"][0]["fileId"]

    ''' Get result data '''

    url_output = "https://vantage-eu.abbyy.com/api/publicapi/v1/transactions/"+transaction_id+"/files/"+file_id+"/download"
    output_response = requests.get(url_output, headers=authorization)

    output_json = json.loads(output_response.text)
    return output_json

counter = 0

if len(os.listdir(path_import)) == 0:
    print("Waiting for files...")

while True:

    time.sleep(4)
    list_files =  os.listdir(path_import)

    for file in list_files:

        output_json = process(skill_id, str(file))

        with open(path_export+f"{Path(path_import+file).stem}.txt", "w+") as f:
            json.dump(output_json, f, ensure_ascii=False)
        counter += 1

        shutil.move(path_import+file, path_processed+file)
