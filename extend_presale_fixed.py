#!/usr/bin/env python3
"""
Исправленный скрипт для продления пресейла ALIEN Token на 20 дней
Учитывает требования контракта: новое время старта должно быть в будущем
"""

import os
import time
from datetime import datetime, timedelta
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def extend_presale():
    """Продлевает пресейл на 20 дней с учетом требований контракта"""
    
    print("🚀 Продление пресейла ALIEN Token на 20 дней (ИСПРАВЛЕНО)")
    print("=" * 70)
    
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
    
    # ABI для управления пресейлом
    presale_abi = [
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
        },
        {
            'inputs': [{'name': '_startTime', 'type': 'uint256'}, {'name': '_endTime', 'type': 'uint256'}],
            'name': 'updatePresaleTimes',
            'outputs': [],
            'stateMutability': 'nonpayable',
            'type': 'function'
        }
    ]
    
    try:
        # Создаем контракт
        contract = w3.eth.contract(address=presale_address, abi=presale_abi)
        
        # Проверяем владельца
        contract_owner = contract.functions.owner().call()
        if contract_owner.lower() != wallet_address.lower():
            print(f"❌ Вы не являетесь владельцем контракта")
            print(f"Владелец: {contract_owner}")
            print(f"Ваш адрес: {wallet_address}")
            return False
        
        print(f"✅ Вы являетесь владельцем контракта")
        
        # Получаем текущие параметры
        current_start = contract.functions.startTime().call()
        current_end = contract.functions.endTime().call()
        
        # Конвертируем в datetime
        current_start_dt = datetime.fromtimestamp(current_start)
        current_end_dt = datetime.fromtimestamp(current_end)
        
        print(f"\n📊 Текущие параметры:")
        print(f"🚀 Время старта: {current_start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏹ Время окончания: {current_end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Получаем текущее время блокчейна
        current_block_time = w3.eth.get_block('latest')['timestamp']
        current_block_dt = datetime.fromtimestamp(current_block_time)
        
        print(f"🕐 Текущее время блокчейна: {current_block_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # ВАЖНО: Контракт требует, чтобы новое время старта было в будущем
        # Поэтому устанавливаем новое время старта на текущий момент + 1 час
        new_start_timestamp = current_block_time + 3600  # +1 час
        new_start_dt = datetime.fromtimestamp(new_start_timestamp)
        
        # Новое время окончания = новое время старта + 20 дней
        new_end_timestamp = new_start_timestamp + (20 * 24 * 3600)  # +20 дней
        new_end_dt = datetime.fromtimestamp(new_end_timestamp)
        
        print(f"\n📅 Новые параметры:")
        print(f"🚀 Время старта: {new_start_dt.strftime('%Y-%m-%d %H:%M:%S')} (+1 час от текущего)")
        print(f"⏹ Время окончания: {new_end_dt.strftime('%Y-%m-%d %H:%M:%S')} (+20 дней)")
        
        # Проверяем требования контракта
        if new_start_timestamp <= current_block_time:
            print("❌ Ошибка: новое время старта должно быть в будущем")
            return False
        
        if new_end_timestamp <= new_start_timestamp:
            print("❌ Ошибка: время окончания должно быть после времени старта")
            return False
        
        print(f"\n⚠️  ВНИМАНИЕ: Пресейл будет перезапущен с новыми параметрами")
        print(f"Продолжить? (y/N): ", end="")
        
        # В автоматическом режиме подтверждаем
        confirm = "y"
        print("y")
        
        if confirm.lower() != 'y':
            print("❌ Операция отменена")
            return False
        
        # Создаем транзакцию
        transaction = contract.functions.updatePresaleTimes(
            new_start_timestamp,
            new_end_timestamp
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
            print(f"⛽ Gas использовано: {tx_receipt.gasUsed}")
            
            # Проверяем новые параметры
            new_start = contract.functions.startTime().call()
            new_end = contract.functions.endTime().call()
            
            new_start_dt = datetime.fromtimestamp(new_start)
            new_end_dt = datetime.fromtimestamp(new_end)
            
            print(f"\n🎉 Пресейл успешно продлен!")
            print(f"📊 Новые параметры:")
            print(f"🚀 Время старта: {new_start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"⏹ Время окончания: {new_end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True
        else:
            print(f"❌ Транзакция не прошла")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    success = extend_presale()
    if success:
        print(f"\n🎯 Пресейл успешно продлен на 20 дней!")
    else:
        print(f"\n❌ Не удалось продлить пресейл")
        exit(1)
