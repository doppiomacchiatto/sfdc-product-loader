#!/usr/bin/env python3
import pathlib

import click

from loader import create_pricebook, get_token, get_session, load_products


@click.command()
@click.option('--name','--prompt=PriceBook Name',help='The price book name that will be created')
@click.option('--flag','--prompt=Flag to create or search',help='Search first with False or Create with True')
@click.option('--products','--prompt=Create Products',help='True or False')
def manage_pricebook(name,flag, products):
    """
    This function needs a name to create a price book. Or checks if a Price Book exists!
    Args:
         :param name: The name of the price book.
         :param flag: True to create, False to search if exists
         :param products: True to create products
    """
    token: str = get_token()
    session = get_session(token)
    result = create_pricebook(session,name,flag)
    if result['totalSize'] == 0:
        print(f"Price book does not exist: {name}")
    else:
        print(f"Price book: {name}")
    if products == "False":
        add_products(name)


def add_products(name):
    """
    This function assumes that you need to create products for the first time.  It will call the loader function that
    creates the product and add it to the standard pricebook.  In Salesforce all products must be added to the standard
    pricebook.
    :param name: pricebook name
    """
    token: str = get_token()
    session = get_session(token)
    file = pathlib.Path("Products_Sample.csv")
    print(file)
    print(f'product flag: {name}')
    #load_products(session, pbname, file)


if __name__ == "__main__":
    manage_pricebook()