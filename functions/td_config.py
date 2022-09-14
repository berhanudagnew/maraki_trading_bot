# Import the client
from td.client import TDClient
# Create a new session, credentials path is required.

TDSession = TDClient(
    client_id='3QXGY5GR5IPGQDSRYUYX9D4FCYJH4AFU',
    redirect_uri='http://localhost:8080/',
    credentials_path='td.json'
)