import boto3
import sys
import requests
import json
import logging
import time

logging.captureWarnings(True)


##
##    function to obtain a new OAuth 2.0 token from the authentication server
##
def get_new_token(authUrl, clientId, clientSecret):

    auth_server_url = authUrl
    client_id = clientId
    client_secret = clientSecret

    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url,
    data=token_req_payload, verify=False, allow_redirects=False,
    auth=(client_id, client_secret))
                
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)

    print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

##
##    function to obtain a new OAuth 2.0 token from the authentication server
##
def create_new_appflow_connection(name, accessToken, instanceUrl):

    client = boto3.client('appflow')

    response = client.create_connector_profile(
        connectorProfileName=name,
        connectorType='Salesforce',
        connectionMode='Public',
        connectorProfileConfig={
            'connectorProfileProperties': {
                'Salesforce': {
                'instanceUrl': instanceUrl,
                'isSandboxEnvironment': False
                }
            },
            'connectorProfileCredentials': {
                'Salesforce': {
                'accessToken': accessToken,
                'refreshToken': 'none'
                  }
            }
        }
    )

    return response


instanceUrl = 'https://xyz-org-inst.my.salesforce.com'
aUrl = "https://xyz-org-inst.my.salesforce.com/services/oauth2/token"
#replace <client_id>, <client_secret> and <connection_name> with actual values
cId = '<client_id>'
cSecret = '<client_secret>'
name = '<connection_name>'

token = get_new_token(aUrl, cId, cSecret)
response = create_new_appflow_connection(name, token, instanceUrl)
print(response)
