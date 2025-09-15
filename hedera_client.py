import os
from dotenv import load_dotenv
from hiero_sdk_python import (
    Client,
    PrivateKey,
    AccountId,
    Hbar,
    Network
)

load_dotenv()

def get_client():
    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    
    if not operator_id_str or not operator_key_str:
        raise ValueError("OPERATOR_ID and OPERATOR_KEY environment variables are required")
    
    operator_id = AccountId.from_string(operator_id_str)
    operator_key = PrivateKey.from_string(operator_key_str)

    network = os.getenv('NETWORK', 'testnet')
    client = Client(Network(network=network))

    client.set_operator(operator_id, operator_key)
    # Note: set_default_max_transaction_fee method might not exist in current version
    # client.set_default_max_transaction_fee(Hbar(2))

    return client

if __name__ == "__main__":
    client = get_client()
    print("✅ Hedera Client configured successfully for", os.getenv('HEDERA_NETWORK'))