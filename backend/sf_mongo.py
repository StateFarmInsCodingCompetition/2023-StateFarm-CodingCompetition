import csv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

df1 = pd.read_json("data/sfcc_2023_agents.json", encoding = 'unicode_escape')
df2 = pd.read_json("data/sfcc_2023_claim_handlers.json", encoding = 'unicode_escape')
df3 = pd.read_json("data/sfcc_2023_claims.json", encoding = 'unicode_escape')
df4 = pd.read_json("data/sfcc_2023_disasters.json", encoding = 'unicode_escape')

df1.to_csv("data/sfcc_2023_agents.csv", index=False)
df2.to_csv("data/sfcc_2023_claim_handlers.csv", index=False)
df3.to_csv("data/sfcc_2023_claims.csv", index=False)
df4.to_csv("data/sfcc_2023_disasters.csv", index=False)

uri = ""

client = MongoClient(uri, server_api = ServerApi('1'))

db = client["statefarm_data"]
collection1 = db['agents']
collection2 = db['claim_handlers']
collection3 = db['claims']
collection4 = db['disasters']

with open("data/sfcc_2023_agents.csv", 'r', encoding = 'latin-1') as csvFile:
    csvreader = csv.DictReader(csvFile)
    for row in csvreader:
        collection1.insert_one(row)
        print("success")

with open("data/sfcc_2023_claim_handlers.csv", 'r', encoding = 'latin-1') as csvFile:
    csvreader = csv.DictReader(csvFile)
    for row in csvreader:
        collection2.insert_one(row)
        print("success")

with open("data/sfcc_2023_claims.csv", 'r', encoding = 'latin-1') as csvFile:
    csvreader = csv.DictReader(csvFile)
    for row in csvreader:
        collection3.insert_one(row)
        print("success")

with open("sfcc_2023_disasters.csv", 'r', encoding = 'latin-1') as csvFile:
    csvreader = csv.DictReader(csvFile)
    for row in csvreader:
        collection4.insert_one(row)
        print("success")
