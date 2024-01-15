import os
from flask import Flask, render_template
from extensions import db  # Assuming extensions.py exists with db = SQLAlchemy()
from models.shipment import Shipment
from routes.shipment_routes import shipment_bp
from web3 import Web3

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 's3cr3t_k3y_sh1pp1ng_m4n4g3m3nt')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://user:iyam0064@db/shipmentdb')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Initialize web3 instance and smart contract
    app.web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    contract_address = '0xEeF3c56b700fDD4377eD1ea11dA0D5FB64F845cf'  # Replace with your contract address
    contract_abi = [
	{
		"inputs": [
          {
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          },
          {
            "internalType": "address payable",
            "name": "receiver",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "amount",
            "type": "uint256"
          }
        ],
        "name": "createShipment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          }
        ],
        "name": "payShipment",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
      },
      {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
      },
      {
        "anonymous": False,
        "inputs": [
          {
            "indexed": False,
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          },
          {
            "indexed": False,
            "internalType": "address",
            "name": "sender",
            "type": "address"
          },
          {
            "indexed": False,
            "internalType": "address",
            "name": "receiver",
            "type": "address"
          },
          {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount",
            "type": "uint256"
          }
        ],
        "name": "ShipmentCreated",
        "type": "event"
      },
      {
        "anonymous": False,
        "inputs": [
          {
            "indexed": False,
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          },
          {
            "indexed": False,
            "internalType": "uint256",
            "name": "amount",
            "type": "uint256"
          }
        ],
        "name": "ShipmentPaid",
        "type": "event"
      },
      {
        "anonymous": False,
        "inputs": [
          {
            "indexed": False,
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          },
          {
            "indexed": False,
            "internalType": "string",
            "name": "status",
            "type": "string"
          }
        ],
        "name": "ShipmentStatusUpdated",
        "type": "event"
      },
      {
        "inputs": [
          {
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "status",
            "type": "string"
          }
        ],
        "name": "updateShipmentStatus",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          }
        ],
        "name": "getShipmentDetails",
        "outputs": [
          {
            "components": [
              {
                "internalType": "string",
                "name": "trackingNumber",
                "type": "string"
              },
              {
                "internalType": "address payable",
                "name": "sender",
                "type": "address"
              },
              {
                "internalType": "address payable",
                "name": "receiver",
                "type": "address"
              },
              {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
              },
              {
                "internalType": "bool",
                "name": "isPaid",
                "type": "bool"
              },
              {
                "internalType": "string",
                "name": "status",
                "type": "string"
              }
            ],
            "internalType": "struct LogisticsContract.Shipment",
            "name": "",
            "type": "tuple"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [],
        "name": "owner",
        "outputs": [
          {
            "internalType": "address",
            "name": "",
            "type": "address"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "string",
            "name": "",
            "type": "string"
          }
        ],
        "name": "shipments",
        "outputs": [
          {
            "internalType": "string",
            "name": "trackingNumber",
            "type": "string"
          },
          {
            "internalType": "address payable",
            "name": "sender",
            "type": "address"
          },
          {
            "internalType": "address payable",
            "name": "receiver",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "amount",
            "type": "uint256"
          },
          {
            "internalType": "bool",
            "name": "isPaid",
            "type": "bool"
          },
          {
            "internalType": "string",
            "name": "status",
            "type": "string"
          }
        ],
        "stateMutability": "view",
        "type": "function"
      }
    ]

    app.contract = app.web3.eth.contract(address=contract_address, abi=contract_abi)

    with app.app_context():
        db.create_all()  # Create database tables

    app.register_blueprint(shipment_bp, url_prefix='/shipments')
    # Define the root route here
    @app.route('/')
    def index():
        return render_template('index.html')

    # After app initialization
    with app.app_context():
        print(app.url_map)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
