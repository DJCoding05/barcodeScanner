from argparse import ArgumentParser
import requests
import json
import os
import dotenv

dotenv.load_dotenv()

API_KEY = os.environ['key']


def barcodeQuery(upc_code) -> json:
    return requests.get(
        f"https://api.barcodelookup.com/v3/products?barcode={upc_code}&key={API_KEY}").json()


def search(barcode) -> None:
    if barcode.isnumeric():
        data = dict(barcodeQuery(barcode))
        print(data['products'][0]['title'])
