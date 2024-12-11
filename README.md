# Product Loader Project #
This project load products into the Salesforce product2 object.
Next, it associates the products to the standard price book.

For the final phase, we will enable the creation of a custom price-book with the
products that were created earlier, which are stored in a csv file.

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

Don't check in the client_id nor client_secret into git. Make sure that those to keys are
not shared with anyone.  If you want to store the values, make sure to encrypt the .env file.