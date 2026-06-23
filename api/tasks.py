import json
from celery import shared_task
from .blockchain_service import blockchain_service

@shared_task
def log_recommendation_task(type_name, recommendation, input_data_json):
    """
    Celery background task to log a recommendation to the blockchain.
    """
    print(f"[Celery Worker] Starting blockchain log task for type: {type_name}")
    try:
        tx_hash = blockchain_service.log_recommendation(
            type_name=type_name,
            recommendation=recommendation,
            input_data=input_data_json
        )
        if tx_hash:
            print(f"[Celery Worker] Blockchain transaction successfully logged: {tx_hash}")
            return tx_hash
        else:
            print("[Celery Worker] Blockchain transaction failed.")
            return None
    except Exception as e:
        print(f"[Celery Worker] Blockchain task execution error: {e}")
        return None
