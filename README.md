# Product Loader Project #
This project loads products into the Salesforce product2 object.
Next, it associates the products to the standard price book. The Products_Sample.csv 
file contains sample products that we need to load.

Finally, we will create a custom price-book with the
products that were created earlier.

## Application Files ##
- controller.py: controls the flow.  Checks if a pricebook exists or it can create a price book.  Look at the parameters
- loader.py: this is where the magic happens.  Creates new produdcts and adds them to the Standard PriceBook.
- 
# Pre-Requisite Connected Application #

Create a Salesforce Connected Application.

**SFDC Oauth Scopes**
* Manage Data via API (web)
* Manage Users Data via API (web)
* Perform Requests at any time (refresh_token, offline_access)
* Access Salesforce API (sfap_api)

**Callback URL:** https://localhost:1717/OauthRedirect
- **Manage:** Admin Approved Users are pre-authorized
- **Client Credentials Flow:** Run As User (Lookup User)
- **Manage Profiles:** Assign Profile

# Configure the Project Properties #
This project uses a .env file that stores the following:

| Key           | Value                                                           |
|---------------|-----------------------------------------------------------------|
| client_id     | The connected apps' Consumer Key                                |
| client_secret | The connected app's Consumer Secret                             |
| redirect_url  | https://<name--alias>.my.salesforce.com/services/oauth2/success |
| auth_url      | https://<name--alias>.my.salesforce.com/services/oauth2/token   |
| instance_url  | https://<base-url>.my.salesforce.com                            |

Don't check in the client_id nor client_secret into git. Make sure that those two keys are
not shared with **anyone**.  If you want to store the values in git, make sure to encrypt the .env file.

# Running the Python Scritps #
- flag is False - this will only check if the Price Book exists
- products False - optional will be refactored later or will call a function to check if product exists in the standard price book.
```bash
./controller.py --name=Test --flag=False --products=False
```
If you want to create a custom pricebook and add products in a csv file...

```bash
./controller.py --name=Naughty_List --flag=True --products=True
```