#!/usr/bin/env python3
"""
Скрипт для обновления параметров пресейла
"""

from web3 import Web3
from config import w3, presale_contract, WALLET_ADDRESS, PRIVATE_KEY
import os
from dotenv import load_dotenv
import time

load_dotenv()

def update_token_price(new_price_wei):
    """Обновляет цену токена в пресейле"""
    
    if not presale_contract:
        print("❌ Пресейл контракт не настроен")
        return False
    
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
            return True
            
        else:
            print("❌ Транзакция не удалась")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def update_hard_cap(new_hard_cap_wei):
    """Обновляет hardcap пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл контракт не настроен")
        return False
    
    try:
        # Проверяем текущий hardcap
        current_hard_cap = presale_contract.functions.hardCap().call()
        current_hard_cap_matic = current_hard_cap / 10**18
        
        print(f"💰 Текущий hardcap: {current_hard_cap_matic} MATIC")
        print(f"📈 Новый hardcap: {new_hard_cap_wei / 10**18} MATIC")
        
        # Получаем nonce
        wallet_address_checksum = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address_checksum)
        
        # Получаем gas price
        gas_price = w3.eth.gas_price
        
        # Строим транзакцию
        transaction = presale_contract.functions.updateHardCap(new_hard_cap_wei).build_transaction({
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
            print("✅ Hardcap успешно обновлен!")
            print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
            
            # Проверяем новый hardcap
            new_hard_cap = presale_contract.functions.hardCap().call()
            new_hard_cap_matic = new_hard_cap / 10**18
            print(f"💰 Новый hardcap подтвержден: {new_hard_cap_matic} MATIC")
            return True
            
        else:
            print("❌ Транзакция не удалась")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def update_presale_times(new_start_time, new_end_time):
    """Обновляет время начала и окончания пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл контракт не настроен")
        return False
    
    try:
        # Проверяем текущие времена
        current_start_time = presale_contract.functions.startTime().call()
        current_end_time = presale_contract.functions.endTime().call()
        
        print(f"⏰ Текущее время начала: {time.ctime(current_start_time)}")
        print(f"⏰ Текущее время окончания: {time.ctime(current_end_time)}")
        print(f"📅 Новое время начала: {time.ctime(new_start_time)}")
        print(f"📅 Новое время окончания: {time.ctime(new_end_time)}")
        
        # Получаем nonce
        wallet_address_checksum = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address_checksum)
        
        # Получаем gas price
        gas_price = w3.eth.gas_price
        
        # Строим транзакцию
        transaction = presale_contract.functions.updatePresaleTimes(new_start_time, new_end_time).build_transaction({
            'from': wallet_address_checksum,
            'nonce': nonce,
            'gas': 200000,
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
            print("✅ Время пресейла успешно обновлено!")
            print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
            return True
            
        else:
            print("❌ Транзакция не удалась")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def show_current_params():
    """Показывает текущие параметры пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл контракт не настроен")
        return
    
    try:
        # Получаем параметры
        start_time = presale_contract.functions.startTime().call()
        end_time = presale_contract.functions.endTime().call()
        hard_cap = presale_contract.functions.hardCap().call()
        token_price = presale_contract.functions.tokenPrice().call()
        total_raised = presale_contract.functions.totalRaised().call()
        paused = presale_contract.functions.paused().call()
        
        print("📊 Текущие параметры пресейла:")
        print("=" * 50)
        print(f"⏰ Время начала: {time.ctime(start_time)}")
        print(f"⏰ Время окончания: {time.ctime(end_time)}")
        print(f"💰 Hardcap: {hard_cap / 10**18} MATIC")
        print(f"💎 Цена токена: {token_price / 10**18} MATIC")
        print(f"📈 Собрано: {total_raised / 10**18} MATIC")
        print(f"⏸️  Пауза: {'Да' if paused else 'Нет'}")
        print(f"📊 Прогресс: {(total_raised / hard_cap * 100):.2f}%")
        print()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def update_to_optimal_params():
    """Обновляет параметры до оптимальных значений"""
    
    print("🚀 Обновление параметров до оптимальных значений")
    print("=" * 60)
    
    # Оптимальные параметры
    optimal_price = 0.0001  # 0.0001 MATIC
    optimal_hardcap = 500   # 500 MATIC
    optimal_duration_days = 30  # 30 дней
    
    # Рассчитываем новые времена
    current_time = int(time.time())
    new_start_time = current_time + 300  # Начинаем через 5 минут
    new_end_time = new_start_time + (optimal_duration_days * 24 * 60 * 60)  # 30 дней
    
    print(f"💰 Новая цена: {optimal_price} MATIC")
    print(f"📈 Новый hardcap: {optimal_hardcap} MATIC")
    print(f"⏰ Новое время начала: {time.ctime(new_start_time)}")
    print(f"⏰ Новое время окончания: {time.ctime(new_end_time)}")
    print()
    
    # Обновляем параметры
    success = True
    
    # 1. Обновляем цену
    print("1️⃣ Обновление цены токена...")
    if not update_token_price(int(optimal_price * 10**18)):
        success = False
    print()
    
    # 2. Обновляем hardcap
    print("2️⃣ Обновление hardcap...")
    if not update_hard_cap(int(optimal_hardcap * 10**18)):
        success = False
    print()
    
    # 3. Обновляем время
    print("3️⃣ Обновление времени пресейла...")
    if not update_presale_times(new_start_time, new_end_time):
        success = False
    print()
    
    if success:
        print("✅ Все параметры успешно обновлены!")
        print("📊 Новые параметры:")
        show_current_params()
    else:
        print("❌ Некоторые параметры не удалось обновить")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python update_presale_params.py show                    - показать текущие параметры")
        print("  python update_presale_params.py price <цена>            - обновить цену")
        print("  python update_presale_params.py hardcap <hardcap>       - обновить hardcap")
        print("  python update_presale_params.py time <start> <end>      - обновить время")
        print("  python update_presale_params.py optimal                 - обновить до оптимальных значений")
        print()
        print("Примеры:")
        print("  python update_presale_params.py price 0.0001")
        print("  python update_presale_params.py hardcap 500")
        print("  python update_presale_params.py optimal")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "show":
        show_current_params()
    
    elif command == "price":
        if len(sys.argv) != 3:
            print("❌ Укажите новую цену")
            sys.exit(1)
        try:
            new_price = float(sys.argv[2])
            update_token_price(int(new_price * 10**18))
        except ValueError:
            print("❌ Неверная цена")
    
    elif command == "hardcap":
        if len(sys.argv) != 3:
            print("❌ Укажите новый hardcap")
            sys.exit(1)
        try:
            new_hardcap = float(sys.argv[2])
            update_hard_cap(int(new_hardcap * 10**18))
        except ValueError:
            print("❌ Неверный hardcap")
    
    elif command == "time":
        if len(sys.argv) != 4:
            print("❌ Укажите время начала и окончания")
            sys.exit(1)
        try:
            start_time = int(sys.argv[2])
            end_time = int(sys.argv[3])
            update_presale_times(start_time, end_time)
        except ValueError:
            print("❌ Неверное время")
    
    elif command == "optimal":
        update_to_optimal_params()
    
    else:
        print(f"❌ Неизвестная команда: {command}")
        sys.exit(1) 