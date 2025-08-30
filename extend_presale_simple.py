#!/usr/bin/env python3
"""
Простой скрипт для продления пресейла ALIEN Token на 20 дней
Использует существующие функции из update_presale_params.py
"""

import time
from datetime import datetime, timedelta
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def extend_presale_simple():
    """Продлевает пресейл на 20 дней используя простой подход"""
    
    print("🚀 Продление пресейла ALIEN Token на 20 дней")
    print("=" * 60)
    
    # Проверяем наличие приватного ключа
    private_key = os.getenv('PRIVATE_KEY')
    wallet_address = os.getenv('WALLET_ADDRESS')
    
    if not private_key or private_key == 'your_private_key_here':
        print("❌ Приватный ключ не найден в .env файле")
        print("\n📝 Создайте .env файл со следующими параметрами:")
        print("PRIVATE_KEY=ваш_приватный_ключ_без_0x")
        print("WALLET_ADDRESS=0x324EB0E51465d70c3D546BeE1cf18F74A01E9924")
        return False
    
    # Подключение к Polygon
    w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    if not w3.is_connected():
        print("❌ Не удалось подключиться к Polygon RPC")
        return False
    
    # Адрес пресейла
    presale_address = '0x2699838c090346Eaf93F96069B56B3637828dFAC'
    
    # ABI для обновления времени
    update_abi = [
        {
            'inputs': [
                {'name': '_startTime', 'type': 'uint256'},
                {'name': '_endTime', 'type': 'uint256'}
            ],
            'name': 'updatePresaleTimes',
            'outputs': [],
            'stateMutability': 'nonpayable',
            'type': 'function'
        },
        {
            'inputs': [],
            'name': 'owner',
            'outputs': [{'name': '', 'type': 'address'}],
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'inputs': [],
            'name': 'startTime',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'stateMutability': 'view',
            'type': 'function'
        },
        {
            'inputs': [],
            'name': 'endTime',
            'outputs': [{'name': '', 'type': 'uint256'}],
            'stateMutability': 'view',
            'type': 'function'
        }
    ]
    
    try:
        # Создаем контракт
        contract = w3.eth.contract(address=presale_address, abi=update_abi)
        
        # Проверяем владельца
        contract_owner = contract.functions.owner().call()
        if contract_owner.lower() != wallet_address.lower():
            print(f"❌ Вы не являетесь владельцем контракта")
            print(f"Владелец: {contract_owner}")
            print(f"Ваш адрес: {wallet_address}")
            return False
        
        print(f"✅ Вы являетесь владельцем контракта")
        
        # Текущие параметры
        current_start = contract.functions.startTime().call()
        current_end = contract.functions.endTime().call()
        
        start_dt = datetime.fromtimestamp(current_start)
        end_dt = datetime.fromtimestamp(current_end)
        
        print(f"\n📊 Текущие параметры:")
        print(f"🚀 Время старта: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏹ Время окончания: {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Рассчитываем новое время окончания (20 дней от текущего момента)
        now = datetime.now()
        new_end = now + timedelta(days=20)
        new_end_timestamp = int(new_end.timestamp())
        
        print(f"\n📅 Новые параметры:")
        print(f"🚀 Время старта: {start_dt.strftime('%Y-%m-%d %H:%M:%S')} (остается)")
        print(f"⏹ Время окончания: {new_end.strftime('%Y-%m-%d %H:%M:%S')} (+20 дней)")
        
        # Подтверждение
        print(f"\n⚠️  ВНИМАНИЕ: Пресейл будет продлен до {new_end.strftime('%Y-%m-%d %H:%M:%S')}")
        confirm = input("Продолжить? (y/N): ")
        
        if confirm.lower() != 'y':
            print("❌ Операция отменена")
            return False
        
        # Создаем транзакцию
        transaction = contract.functions.updatePresaleTimes(
            current_start,  # Оставляем текущее время старта
            new_end_timestamp  # Обновляем время окончания
        ).build_transaction({
            'from': wallet_address,
            'gas': 300000,  # Увеличиваем газ
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
            
            # Проверяем обновленные параметры
            new_end_time = contract.functions.endTime().call()
            new_end_dt = datetime.fromtimestamp(new_end_time)
            
            print(f"\n🎉 Пресейл успешно продлен!")
            print(f"📅 Новое время окончания: {new_end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Рассчитываем оставшееся время
            time_left = new_end_timestamp - int(datetime.now().timestamp())
            days = time_left // 86400
            hours = (time_left % 86400) // 3600
            
            print(f"⏳ До окончания: {days} дней, {hours} часов")
            
            return True
        else:
            print(f"❌ Транзакция не прошла")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    import os
    success = extend_presale_simple()
    if success:
        print(f"\n🎯 Пресейл успешно продлен на 20 дней!")
    else:
        print(f"\n❌ Не удалось продлить пресейл")
        exit(1)
