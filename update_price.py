#!/usr/bin/env python3
"""
Скрипт для обновления цены токена в пресейле
"""

from web3 import Web3
from config import w3, presale_contract, WALLET_ADDRESS, PRIVATE_KEY
import os
from dotenv import load_dotenv

load_dotenv()

def update_token_price(new_price_wei):
    """Обновляет цену токена в пресейле"""
    
    if not presale_contract:
        print("❌ Пресейл контракт не настроен")
        return
    
    try:
        # Проверяем текущую цену
        current_price = presale_contract.functions.tokenPrice().call()
        current_price_matic = current_price / 10**18
        
        print(f"💰 Текущая цена: {current_price_matic} MATIC")
        print(f"📈 Новая цена: {new_price_wei / 10**18} MATIC")
        
        # Получаем nonce
        wallet_address_checksum = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address_checksum)
        
        # Получаем gas price
        gas_price = w3.eth.gas_price
        
        # Строим транзакцию
        transaction = presale_contract.functions.updateTokenPrice(new_price_wei).build_transaction({
            'from': wallet_address_checksum,
            'nonce': nonce,
            'gas': 150000,
            'gasPrice': gas_price
        })
        
        # Подписываем и отправляем
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"⏳ Транзакция отправлена: {tx_hash.hex()}")
        
        # Ждем подтверждения
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print("✅ Цена токена успешно обновлена!")
            print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
            
            # Проверяем новую цену
            new_price = presale_contract.functions.tokenPrice().call()
            new_price_matic = new_price / 10**18
            print(f"💰 Новая цена подтверждена: {new_price_matic} MATIC")
            
        else:
            print("❌ Транзакция не удалась")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Использование: python update_price.py <новая_цена_в_matic>")
        print("Пример: python update_price.py 0.0001")
        sys.exit(1)
    
    try:
        new_price_matic = float(sys.argv[1])
        new_price_wei = int(new_price_matic * 10**18)
        update_token_price(new_price_wei)
    except ValueError:
        print("❌ Неверная цена. Используйте число (например: 0.0001)")
        sys.exit(1) 