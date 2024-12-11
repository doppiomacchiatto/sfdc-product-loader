import csv
import string
from simple_salesforce import Salesforce, SalesforceAuthenticationFailed, SalesforceMalformedRequest, format_soql
from dotenv import load_dotenv
import os
import requests
import pandas as pd

sf = None

def get_token() -> string:
    """gets the Salesforce Access Token
    return: string token
    """
    load_dotenv()
    # Update the .env file with your Salesforce connected app's credentials
    client_id = os.getenv('client_id')
    client_secret = os.getenv('client_secret')
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    auth_url = os.getenv('auth_url')
    response = requests.post(auth_url, data={'client_id': client_id,
                                             'client_secret': client_secret,
                                             'grant_type': 'client_credentials'}, headers=headers)
    if "access_token" in response.json() and response.json()["access_token"]:
        print("Great Success!")
    else:
        print("Great Failure!")
        exit()
    json_res = response.json()
    return json_res['access_token']


def get_session(token):
    """
    Get the Session Token from salesforce
    :param access token:
    :return: Token
    """
    global sf
    print('Getting Salesforce session...')
    _instance_url = os.getenv('instance_url')
    try:
        sf = Salesforce(instance_url=_instance_url,session_id=token)
    except SalesforceAuthenticationFailed as sae:
        print(f'SF Oauth authentication failed: {sae}')
    return sf

# Retrieve Standard Price Book ID
def get_standard_pricebook_id(sfa):
    """get the standard price book
    :param sfa: Simple Salesforce Session
    :return: Id of the Standard Price Book
    """
    query = "SELECT Id FROM Pricebook2 WHERE IsStandard = true LIMIT 1"
    _result = sfa.query(query)
    if _result['totalSize'] == 0:
        raise Exception("Standard Price Book not found!")
    return _result['records'][0]['Id']

def create_pricebook(sfa, pbn, flag):
    """creates a new price book and add the products in the ProductsDF.csv
    :param flag:
    :param sfa: simple salesforce
    :param pbn: price book name
    :return: New Price Book Id
    """
    global result
    if flag == "True":
        pbexists = get_new_pb(sfa, pbn)
        print('creating pricebook')
        new_pb = {
            'Name': pbn,
            'Description': 'Products & SKUs for Air Gap Portfolio',
            'IsActive': True
        }
        try:
            response = sfa.Pricebook2.create(new_pb)
            print(response)
            # OrderedDict([('id', '01sHs000009MkAIIA0'), ('success', True), ('errors', [])])
            if response['success']:
                print("Pricebook created successfully!")
                return
            else:
                print("Error creating pricebook successfully!", response.errors)
        except SalesforceMalformedRequest as smr:
            print(f'Salesforce Malformed Request: {smr}')

    else:
        result = sfa.query(format_soql("SELECT Id,Name FROM Pricebook2 WHERE Name= {}",pbn))
        return result

def get_new_pb(sfa, pb):
    """get the new price book id
    :param pb:  price book name
    :param sfa: simple salesforce
    :return:
    """
    try:
        query = "SELECT Id, Name FROM Pricebook2 WHERE Name ='" + pb + "'LIMIT 1"
        result = sfa.query(query)
        if result['totalSize'] == 0:
            raise Exception(f"Price Book not found! {pb}")
        return result['records'][0]['Id']
    except Exception as e:
        print(f'Exception: {e}')
    print('processing')
# Load products from CSV and upload to Salesforce

def load_products(sfa, pb, file_path):
    """Load products from a csv file and creates a csv with result.
    :param sfa: simple salesforce session
    :param pb: Price Book Id
    :param file_path: csv file path
    :return: csv ProductsDF.csv
    """
    pricebook_id = pb
    new_rows = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create Product2 record
            product = sfa.Product2.create({
                'Name': row['Product Name'],
                'ProductCode': row['SKU'],
                'IsActive': True
            })
            print(f"Created Product: {row['Product Name']} (ID: {product['id']})")

            # Add product to Standard Price Book with default price
            sfa.PricebookEntry.create({
                'Pricebook2Id': pricebook_id,
                'Product2Id': product['id'],
                'UnitPrice': 1.0,  # Default price
                'IsActive': True
            })
            new_rows.append({'Pricebook2Id':pricebook_id, 'Product2Id': product['id'],'UnitPrice': 1.0, 'IsActive': True})
            print(f"Added {row['Product Name']} to Standard Price Book.")
        df = pd.DataFrame(new_rows)
        df_abf = pd.concat([df, df], ignore_index=True)
        print(df_abf.head())
        df.to_csv('ProductsDF'+pb, index=False)

def load_new_pb(sfa, pb, file_path):
    """ Loads products to pricebook.
    :param sfa:
    :param pb:
    :param file_path:
    :return:
    """
    new_products = []
    with open(file_path, 'r') as contacts:
        df = pd.read_csv(contacts, encoding="utf-8",dtype={'Pricebook2Id':str,'Product2Id':str,'UnitPrice':float,'IsActive':bool})
        # Add product to Standard Price Book with default price
    for index, row in df.iterrows():
        new_pbe = {
        'Pricebook2Id':pb,
        'Product2Id': row['Product2Id'],
        'UnitPrice': row['UnitPrice'],
        'IsActive':row['IsActive']
        }
        new_products.append(new_pbe)

    print(new_products)
    response = sfa.bulk.PricebookEntry.insert(new_products,batch_size=10000,use_serial=True)
    print(response)
    counter = 0
    _result = []
    for item in response:
        if not item['success']:
            _result.append(item)
            counter += 1
    if counter == 0:
        return 'Successfully added products to price book'
    else:
        print(f'Errors{_result}')

