#!/usr/bin/env python3
"""
Скрипт для паузы и возобновления пресейла ALIEN Token
Это может помочь сбросить ограничения на обновление времени
"""

import os
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def pause_and_resume_presale():
    """Ставит пресейл на паузу и затем возобновляет его"""
    
    print("⏸️  Пауза и возобновление пресейла ALIEN Token")
    print("=" * 60)
    
    # Проверяем наличие приватного ключа
    private_key = os.getenv('PRIVATE_KEY')
    wallet_address = os.getenv('WALLET_ADDRESS')
    
    if not private_key or private_key == 'your_private_key_here':
        print("❌ Приватный ключ не найден в .env файле")
        return False
    
    # Подключение к Polygon
    w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    if not w3.is_connected():
        print("❌ Не удалось подключиться к Polygon RPC")
        return False
    
    # Адрес пресейла
    presale_address = '0x2699838c090346Eaf93F96069B56B3637828dFAC'
    
    # ABI для управления паузой
    pause_abi = [
        {
            'inputs': [],
            'name': 'owner',
            'outputs': [{'name': '', 'type': 'address'}],
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'inputs': [],
            'name': 'paused',
            'outputs': [{'name': '', 'type': 'bool'}],
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'inputs': [{'name': '_status', 'type': 'bool'}],
            'name': 'pausePresale',
            'outputs': [],
            'stateMutability': 'nonpayable',
            'type': 'function'
        }
    ]
    
    try:
        # Создаем контракт
        contract = w3.eth.contract(address=presale_address, abi=pause_abi)
        
        # Проверяем владельца
        contract_owner = contract.functions.owner().call()
        if contract_owner.lower() != wallet_address.lower():
            print(f"❌ Вы не являетесь владельцем контракта")
            print(f"Владелец: {contract_owner}")
            print(f"Ваш адрес: {wallet_address}")
            return False
        
        print(f"✅ Вы являетесь владельцем контракта")
        
        # Проверяем текущий статус паузы
        is_paused = contract.functions.paused().call()
        print(f"\n📊 Текущий статус паузы: {'Да' if is_paused else 'Нет'}")
        
        if is_paused:
            print("🔄 Пресейл уже на паузе. Возобновляем...")
            pause_status = False
        else:
            print("⏸️  Ставим пресейл на паузу...")
            pause_status = True
        
        # Создаем транзакцию для изменения статуса паузы
        transaction = contract.functions.pausePresale(pause_status).build_transaction({
            'from': wallet_address,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(wallet_address),
        })
        
        # Подписываем транзакцию
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
        
        print(f"\n📝 Отправляем транзакцию...")
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"✅ Транзакция отправлена!")
        print(f"🔗 Hash: {tx_hash.hex()}")
        print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
        
        # Ждем подтверждения
        print(f"\n⏳ Ожидаем подтверждения транзакции...")
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        
        if tx_receipt.status == 1:
            print(f"✅ Транзакция подтверждена в блоке {tx_receipt.blockNumber}")
            
            # Проверяем новый статус паузы
            new_pause_status = contract.functions.paused().call()
            print(f"\n🎉 Статус паузы изменен!")
            print(f"📊 Новый статус паузы: {'Да' if new_pause_status else 'Нет'}")
            
            if is_paused:
                print("✅ Пресейл возобновлен!")
            else:
                print("✅ Пресейл поставлен на паузу!")
                
            return True
        else:
            print(f"❌ Транзакция не прошла")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = pause_and_resume_presale()
    if success:
        print(f"\n🎯 Операция с паузой завершена успешно!")
    else:
        print(f"\n❌ Не удалось выполнить операцию с паузой")
        exit(1)
