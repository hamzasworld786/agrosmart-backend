import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

class BlockchainService:
    def __init__(self):
        # Connect to Sepolia testnet via Infura or public RPC
        self.infura_url = os.getenv('INFURA_URL', 'https://rpc.sepolia.org')
        self.w3 = Web3(Web3.HTTPProvider(self.infura_url))
        
        # Account private key (keep secret!)
        self.private_key = os.getenv('PRIVATE_KEY')
        self.account_address = os.getenv('ACCOUNT_ADDRESS')
        
        # Contract address after deployment
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        
        # ABI (Application Binary Interface) - from smart contract
        self.contract_abi = [
            {
                "inputs": [
                    {"internalType": "string", "name": "type", "type": "string"},
                    {"internalType": "string", "name": "recommendation", "type": "string"},
                    {"internalType": "string", "name": "inputData", "type": "string"}
                ],
                "name": "logRecommendation",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getTotalLogs",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "getAllLogs",
                "outputs": [{"internalType": "string[]", "name": "", "type": "string[]"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "uint256", "name": "index", "type": "uint256"}],
                "name": "getLog",
                "outputs": [{"internalType": "string", "name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        self.is_connected = False
        self.contract = None
        
        if self.w3.is_connected():
            self.is_connected = True
            print("✅ Connected to Ethereum Sepolia")
            if self.contract_address and self.contract_abi:
                self.contract = self.w3.eth.contract(
                    address=Web3.to_checksum_address(self.contract_address),
                    abi=self.contract_abi
                )
                print("✅ Smart contract loaded")
        else:
            print("⚠️ Could not connect to Ethereum network")
    
    def log_recommendation(self, type_name, recommendation, input_data):
        """
        Log a recommendation to the blockchain
        Returns transaction hash if successful, None if failed
        """
        if not self.is_connected:
            print("⚠️ Blockchain not connected, skipping")
            return None
        
        if not self.private_key or not self.account_address or not self.contract:
            print("⚠️ Blockchain credentials missing, skipping")
            return None
        
        try:
            # Prepare transaction
            transaction = self.contract.functions.logRecommendation(
                type_name,
                recommendation,
                input_data
            ).build_transaction({
                'from': self.account_address,
                'nonce': self.w3.eth.get_transaction_count(self.account_address),
                'gas': 500000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction, 
                self.private_key
            )
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f"✅ Blockchain transaction sent: {tx_hash.hex()}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Blockchain error: {e}")
            return None
    
    def get_total_logs(self):
        """Get total number of logs stored on blockchain"""
        if not self.contract:
            return 0
        try:
            return self.contract.functions.getTotalLogs().call()
        except Exception as e:
            print(f"Error getting total logs: {e}")
            return 0

# Create singleton instance
blockchain_service = BlockchainService()