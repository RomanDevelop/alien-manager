#!/usr/bin/env python3
"""
Скрипт для проверки баланса токенов ALIEN на основном контракте
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import w3, TOKEN_ADDRESS, TOKEN_V2_ABI
from token_utils import get_token_balance, get_matic_balance
from web3 import Web3

def check_token_contract_balance():
    """Проверяет баланс токенов на основном контракте ALIEN"""
    
    print("🔍 Проверка баланса токенов на основном контракте ALIEN")
    print("=" * 60)
    
    # Адрес основного контракта токена
    token_address = "0xa8e302849DdF86769C026d9A2405e1cdA01ED992"
    
    try:
        # Создаем контракт токена
        token_contract = w3.eth.contract(
            address=Web3.to_checksum_address(token_address),
            abi=TOKEN_V2_ABI
        )
        
        print(f"📍 Адрес контракта токена: {token_address}")
        print(f"🔗 Polygonscan: https://polygonscan.com/address/{token_address}")
        print()
        
        # Получаем общую информацию о токене
        try:
            name = token_contract.functions.name().call()
            symbol = token_contract.functions.symbol().call()
            decimals = token_contract.functions.decimals().call()
            total_supply = token_contract.functions.totalSupply().call()
            
            print(f"📋 Информация о токене:")
            print(f"   Название: {name}")
            print(f"   Символ: {symbol}")
            print(f"   Дробных знаков: {decimals}")
            print(f"   Общее предложение: {total_supply:,} {symbol}")
            print()
            
        except Exception as e:
            print(f"⚠️  Ошибка получения информации о токене: {e}")
            print()
        
        # Проверяем баланс на пресейле
        presale_address = "0x2699838c090346Eaf93F96069B56B3637828dFAC"
        presale_balance = token_contract.functions.balanceOf(
            Web3.to_checksum_address(presale_address)
        ).call()
        
        print(f"💰 Баланс токенов на пресейле:")
        print(f"   Адрес пресейла: {presale_address}")
        print(f"   Баланс: {presale_balance:,} ALIEN")
        print()
        
        # Проверяем баланс у владельца (если есть функция owner)
        try:
            owner = token_contract.functions.owner().call()
            owner_balance = token_contract.functions.balanceOf(owner).call()
            
            print(f"👑 Баланс у владельца:")
            print(f"   Адрес владельца: {owner}")
            print(f"   Баланс: {owner_balance:,} ALIEN")
            print()
            
        except Exception as e:
            print(f"⚠️  Не удалось получить информацию о владельце: {e}")
            print()
        
        # Проверяем баланс у пользователя (если указан в .env)
        try:
            from config import WALLET_ADDRESS
            if WALLET_ADDRESS:
                user_balance = token_contract.functions.balanceOf(
                    Web3.to_checksum_address(WALLET_ADDRESS)
                ).call()
                
                print(f"👤 Баланс у пользователя:")
                print(f"   Адрес: {WALLET_ADDRESS}")
                print(f"   Баланс: {user_balance:,} ALIEN")
                print()
                
        except Exception as e:
            print(f"⚠️  Не удалось получить баланс пользователя: {e}")
            print()
        
        # Проверяем разрешения (allowance) для пресейла
        try:
            if WALLET_ADDRESS:
                allowance = token_contract.functions.allowance(
                    Web3.to_checksum_address(WALLET_ADDRESS),
                    Web3.to_checksum_address(presale_address)
                ).call()
                
                print(f"🔐 Разрешения для пресейла:")
                print(f"   Allowance: {allowance:,} ALIEN")
                print()
                
        except Exception as e:
            print(f"⚠️  Не удалось получить разрешения: {e}")
            print()
        
        # Проверяем статус паузы
        try:
            paused = token_contract.functions.paused().call()
            print(f"⏸️  Статус паузы: {'Да' if paused else 'Нет'}")
            print()
            
        except Exception as e:
            print(f"⚠️  Не удалось получить статус паузы: {e}")
            print()
        
        # Дополнительная информация
        print("📊 Дополнительная информация:")
        print(f"   Сеть: Polygon Mainnet")
        print(f"   RPC: {w3.eth.chain_id}")
        print(f"   Блок: {w3.eth.block_number}")
        print()
        
        print("✅ Проверка завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке баланса: {e}")
        return False
    
    return True

def check_multiple_addresses():
    """Проверяет баланс токенов у нескольких адресов"""
    
    print("🔍 Проверка баланса токенов у нескольких адресов")
    print("=" * 60)
    
    token_address = "0xa8e302849DdF86769C026d9A2405e1cdA01ED992"
    token_contract = w3.eth.contract(
        address=Web3.to_checksum_address(token_address),
        abi=TOKEN_V2_ABI
    )
    
    # Список адресов для проверки
    addresses_to_check = [
        "0x2699838c090346Eaf93F96069B56B3637828dFAC",  # Пресейл
        "0xa8e302849DdF86769C026d9A2405e1cdA01ED992",  # Сам токен
        "0x324EB0E51465d70c3D546BeE1cf18F74A01E9924",  # Владелец
    ]
    
    print("📋 Балансы токенов:")
    print("-" * 40)
    
    for i, address in enumerate(addresses_to_check, 1):
        try:
            balance = token_contract.functions.balanceOf(
                Web3.to_checksum_address(address)
            ).call()
            
            print(f"{i}. {address}")
            print(f"   Баланс: {balance:,} ALIEN")
            print()
            
        except Exception as e:
            print(f"{i}. {address}")
            print(f"   Ошибка: {e}")
            print()

if __name__ == "__main__":
    print("🚀 ALIEN Token Balance Checker")
    print("=" * 40)
    
    # Основная проверка
    success = check_token_contract_balance()
    
    if success:
        print("\n" + "=" * 40)
        # Дополнительная проверка нескольких адресов
        check_multiple_addresses()
    
    print("\n🎯 Проверка завершена!") 