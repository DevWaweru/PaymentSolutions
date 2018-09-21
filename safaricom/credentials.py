import requests
from requests.auth import HTTPBasicAuth
# from M2Crypto import RSA, X509
# from base64 import b64encode

# CERTIFICATE_FILE = 'certificate.cer'

# def encryptInitiatorPassword(INITIATOR_PASS, time_stamp):
#     cert_file = open(CERTIFICATE_FILE, 'r')
#     cert_data = cert_file.read() #read certificate file
#     cert_file.close()
#     cert = X509.load_cert_string(cert_data)
#     pub_key = cert.get_pubkey()
#     rsa_key = pub_key.get_rsa()
#     cipher = rsa_key.public_encrypt((f'{174379}{INITIATOR_PASS}{time_stamp}').encode('utf-8'), RSA.pkcs1_padding)
#     return b64encode(cipher)

def get_access_token(consumer_key, consumer_secret):
    # Validate the app 
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    get_token = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    token = get_token.json()['access_token']
    return token

def get_response(api_url, request, headers):
    response = requests.post(api_url, json = request, headers=headers)
    return response

def verify_response(api_url, request, headers):
    return requests.post(api_url, json = request, headers=headers)