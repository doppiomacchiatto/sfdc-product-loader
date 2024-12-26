#!/usr/bin/env python3
import pathlib
from pathlib import Path

import click

from loader import create_pricebook, get_token, get_session, load_products, load_products_custom, \
    get_standard_pricebook_id, get_new_pb


@click.command()
@click.option('--name',prompt='PriceBook Name',help='The price book name that will be created')
@click.option('--create',prompt='Create or search pricebook(True | False)',help='Search first with False or Create with True')
@click.option('--products',prompt='Create Products (True | False)',help='True or False')
@click.option('--stdpb',prompt='Add products to std pricebook (True | False)',help='add products to std pricebook')
@click.option('--pbe',prompt='Add products to custom pricebook (True | False)',help='add products to custom pricebook')
def manage_pricebook(name,create, products, stdpb, pbe):
    """
    This function needs a name to create a price book. Or checks if a Price Book exists!
    Args:
         :param name: The name of the price book.
         :param create: True to create, False to search if exists
         :param products: True to create products
    """
    token: str = get_token()
    session = get_session(token)
    result = create_pricebook(session,name,create)
    if result['totalSize'] == 0:
        print("Price book does not exist.  Create with True or python ./controller.py --help")
    else:
        print(f"Price book Exists: {name}")
    if products == "True" or pbe == "True":
        add_products(name,stdpb,pbe)
    else:
        print("You chose not to add products.  Run python ./controller.py --help again if you want to add products.")


def add_products(name, std, pbe):
    """
    This function assumes that you need to create products for the first time.  It will call the loader function that
    creates the product and add it to the standard pricebook.  In Salesforce all products must be added to the standard
    pricebook.
    :param name: pricebook name
    """
    global prod_file
    global file_name

    token: str = get_token()
    session = get_session(token)
    file = pathlib.Path("Products_Sample.csv")
    print(file)
    print(f'product flag: {name}')
    # Add Products to standard pricebook
    # TODO - Refactor with Luigi
    if std == "True":
        std_id = get_standard_pricebook_id(session)
        file_name = load_products(session,std_id,file)
        file_df = pathlib.Path(file_name)
        prod_file = pathlib.Path(file_df)

    # Add products to custom pricebook
    if pbe == "True":
        file_name = 'Products_DF'
        pbid = get_new_pb(session,name)
        file_df = pathlib.Path(file_name)
        prod_file = pathlib.Path(file_df)
        result = load_products_custom(session, pbid, prod_file)
        # add logic to parse result its list of dictionary
        # {'success': True, 'created': True, 'id': '01uHs00000XF7v4IAD', 'errors': []},
        print(result)


if __name__ == "__main__":
    manage_pricebook()