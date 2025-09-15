from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from hedera_client import get_client
from sensor_simulator import simulate_sensor_data
import threading
import time
import os
from datetime import datetime

from hiero_sdk_python import (
    PrivateKey,
    AccountId,
    TokenId,
    TokenType,
    SupplyType,
    TokenMintTransaction,
    TransferTransaction,
    Hbar,
    TokenAssociateTransaction,
    TokenCreateTransaction
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

panel_data = {}
token_id = None
nft_serial = None
total_energy_generated = 0.0

def mint_solar_panel_nft():
    global token_id, nft_serial
    print("🛠️  Minting Solar Panel NFT...")

    client = get_client()

    transaction = (
        TokenCreateTransaction()
        .set_token_name("Solirium Solar Panel #001")
        .set_token_symbol("SOL")
        .set_token_type(TokenType.NON_FUNGIBLE_UNIQUE)
        .set_decimals(0)
        .set_initial_supply(0)
        .set_treasury_account_id(client.operator_account_id)
        .set_supply_type(SupplyType.FINITE)
        .set_max_supply(10)
        .freeze_with(client)
    )

    token_tx_id = transaction.execute(client)
    token_receipt = token_tx_id.get_receipt(client)
    new_token_id = token_receipt.tokenId
    print(f"✅ NFT Token Created: {new_token_id}")

    mint_tx = (
        TokenMintTransaction()
        .set_token_id(new_token_id)
        .add_metadata("[SOL-PANEL-001]".encode("utf8"))
        .freeze_with(client)
    )

    mint_tx_id = mint_tx.execute(client)
    mint_receipt = mint_tx_id.get_receipt(client)
    nft_serial = mint_receipt.serials[0]
    print(f"✅ NFT Minted with Serial #: {nft_serial}")

    token_id = new_token_id
    return new_token_id, nft_serial

def distribute_rewards(energy_wh, token_owner_id):
    client = get_client()
    wh_per_hbar = 1000
    reward_amount_hbar = energy_wh / wh_per_hbar

    if reward_amount_hbar <= 0:
        print("No rewards to distribute.")
        return

    print(f"🧾 Distributing {reward_amount_hbar} HBAR for {energy_wh}Wh generated...")

    try:
        transfer_tx = (
            TransferTransaction()
            .add_hbar_transfer(client.operator_account_id, Hbar(-reward_amount_hbar))
            .add_hbar_transfer(AccountId.from_string(token_owner_id), Hbar(reward_amount_hbar))
            .freeze_with(client)
        )
        tx_id = transfer_tx.execute(client)
        receipt = tx_id.get_receipt(client)
        print(f"✅ Reward of {reward_amount_hbar} HBAR sent to {token_owner_id}. TX ID: {tx_id}")
    except Exception as e:
        print(f"❌ Failed to distribute reward: {e}")

def start_sensor_simulation():
    def run_simulation():
        global total_energy_generated
        while True:
            data = simulate_sensor_data("SOL-PANEL-001")
            panel_data['latest'] = data
            total_energy_generated += data['energy_wh']
            time.sleep(10)
    thread = threading.Thread(target=run_simulation, daemon=True)
    thread.start()
    print("📡 Background sensor simulation started...")

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "service": "solirium"})

@app.route('/api/panel-data')
def get_panel_data():
    return jsonify(panel_data.get('latest', {}))

@app.route('/api/mint-nft')
def api_mint_nft():
    global token_id, nft_serial
    if token_id is None:
        token_id, nft_serial = mint_solar_panel_nft()
    return jsonify({
        "status": "success",
        "token_id": str(token_id),
        "nft_serial": nft_serial
    })

@app.route('/api/distribute-rewards')
def api_distribute_rewards():
    owner_id = request.args.get('owner_id', None)
    if not owner_id:
        return jsonify({"error": "Please provide an 'owner_id' parameter"}), 400

    global total_energy_generated
    energy_sent = total_energy_generated
    distribute_rewards(energy_sent, owner_id)
    total_energy_generated = 0.0

    return jsonify({
        "status": "reward_distributed",
        "energy_wh": energy_sent,
        "recipient": owner_id
    })

# Initialize sensor simulation when app starts (for production deployment)
# Using a global flag to ensure initialization happens only once
_initialized = False

def initialize_app():
    global _initialized
    if not _initialized:
        print("⚡ Initializing Solirium Server...")
        start_sensor_simulation()
        _initialized = True

# Initialize immediately when module is imported (for Gunicorn)
initialize_app()

if __name__ == "__main__":
    print("⚡ Starting Solirium Server...")
    initialize_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)