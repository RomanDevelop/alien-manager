#!/usr/bin/env python3
"""
Экстренный возврат средств из пресейла
"""

from web3 import Web3
from config import w3, presale_contract, WALLET_ADDRESS, PRIVATE_KEY
import os

def emergency_withdraw():
    """Экстренный возврат всех средств из пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл не подключен")
        return
    
    try:
        # Проверяем баланс пресейла
        presale_address = presale_contract.address
        balance = w3.eth.get_balance(presale_address)
        
        if balance == 0:
            print("💰 Пресейл пустой (0 MATIC)")
            return
        
        print(f"💰 Найдено в пресейле: {Web3.from_wei(balance, 'ether')} MATIC")
        
        # Проверяем, что мы владелец
        owner = presale_contract.functions.owner().call()
        if owner.lower() != WALLET_ADDRESS.lower():
            print(f"❌ Вы не владелец пресейла. Владелец: {owner}")
            return
        
        print("✅ Вы владелец пресейла")
        
        # Создаем транзакцию возврата
        nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
        
        # Пытаемся вызвать withdrawFunds
        try:
            tx = presale_contract.functions.withdrawFunds().build_transaction({
                'from': WALLET_ADDRESS,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': w3.eth.gas_price
            })
        except Exception as e:
            print(f"❌ Ошибка withdrawFunds: {e}")
            # Пробуем прямой перевод
            tx = {
                'to': presale_address,
                'from': WALLET_ADDRESS,
                'value': 0,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': w3.eth.gas_price,
                'data': '0x'  # Пустая транзакция
            }
        
        # Подписываем и отправляем
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        print(f"🚀 Транзакция отправлена: {tx_hash.hex()}")
        print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
        
        # Ждем подтверждения
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt.status == 1:
            print("✅ Средства успешно возвращены!")
        else:
            print("❌ Транзакция не прошла")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def check_presale_balance():
    """Проверка баланса пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл не подключен")
        return
    
    try:
        presale_address = presale_contract.address
        balance = w3.eth.get_balance(presale_address)
        
        print(f"💰 Баланс пресейла {presale_address}:")
        print(f"   MATIC: {Web3.from_wei(balance, 'ether')}")
        
        # Проверяем владельца
        owner = presale_contract.functions.owner().call()
        print(f"   Владелец: {owner}")
        print(f"   Вы владелец: {'✅' if owner.lower() == WALLET_ADDRESS.lower() else '❌'}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🚨 Экстренный возврат средств из пресейла")
    print("=" * 50)
    
    check_presale_balance()
    print()
    
    response = input("Хотите попытаться вернуть средства? (y/n): ")
    if response.lower() == 'y':
        emergency_withdraw()
    else:
        print("❌ Операция отменена") 