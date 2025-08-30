#!/usr/bin/env python3
"""
Детальная проверка всех условий пресейла
"""

from web3 import Web3
from config import w3, presale_contract, WALLET_ADDRESS
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def check_presale_conditions():
    """Проверяет все условия пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл контракт не настроен")
        return
    
    try:
        print("🔍 Детальная проверка условий пресейла ALIEN")
        print("=" * 50)
        
        # Основные параметры
        print("\n📊 ОСНОВНЫЕ ПАРАМЕТРЫ:")
        print("-" * 30)
        
        # Адрес пресейла
        presale_address = presale_contract.address
        print(f"📍 Адрес пресейла: {presale_address}")
        
        # Адрес токена
        token_address = presale_contract.functions.token().call()
        print(f"👽 Адрес токена: {token_address}")
        
        # Цена токена
        token_price_wei = presale_contract.functions.tokenPrice().call()
        token_price_matic = token_price_wei / 10**18
        print(f"💰 Цена токена: {token_price_matic} MATIC (${token_price_matic * 0.9:.6f})")
        
        # Hardcap
        hardcap_wei = presale_contract.functions.hardCap().call()
        hardcap_matic = hardcap_wei / 10**18
        print(f"🎯 Hardcap: {hardcap_matic} MATIC (${hardcap_matic * 0.9:.2f})")
        
        # Временные рамки
        print("\n⏰ ВРЕМЕННЫЕ РАМКИ:")
        print("-" * 30)
        
        current_time = presale_contract.functions.getPresaleInfo().call()[0]  # Используем startTime как базовое время
        start_time = presale_contract.functions.startTime().call()
        end_time = presale_contract.functions.endTime().call()
        
        current_dt = datetime.fromtimestamp(current_time)
        start_dt = datetime.fromtimestamp(start_time)
        end_dt = datetime.fromtimestamp(end_time)
        
        print(f"🕐 Текущее время: {current_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🚀 Время старта: {start_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏹ Время окончания: {end_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Статус пресейла
        print("\n📈 СТАТУС ПРЕСЕЙЛА:")
        print("-" * 30)
        
        total_raised_wei = presale_contract.functions.totalRaised().call()
        total_raised_matic = total_raised_wei / 10**18
        print(f"💰 Собрано: {total_raised_matic} MATIC")
        
        remaining_cap_wei = hardcap_wei - total_raised_wei
        remaining_cap_matic = remaining_cap_wei / 10**18
        print(f"🎯 Осталось: {remaining_cap_matic} MATIC")
        
        progress_percent = (total_raised_matic / hardcap_matic) * 100
        print(f"📊 Прогресс: {progress_percent:.2f}%")
        
        # Статус активности
        is_paused = presale_contract.functions.paused().call()
        is_active = presale_contract.functions.getPresaleInfo().call()[6]  # _isActive
        
        print(f"⏸ Пауза: {'Да' if is_paused else 'Нет'}")
        print(f"✅ Активен: {'Да' if is_active else 'Нет'}")
        
        # Расчеты токенов
        print("\n🧮 РАСЧЕТЫ ТОКЕНОВ:")
        print("-" * 30)
        
        tokens_for_sale = hardcap_matic / token_price_matic
        print(f"🎯 Токенов для продажи: {tokens_for_sale:,.0f} ALIEN")
        
        tokens_sold = total_raised_matic / token_price_matic
        print(f"💰 Продано токенов: {tokens_sold:,.0f} ALIEN")
        
        tokens_remaining = tokens_for_sale - tokens_sold
        print(f"📦 Осталось токенов: {tokens_remaining:,.0f} ALIEN")
        
        # Примеры покупок
        print("\n💡 ПРИМЕРЫ ПОКУПОК:")
        print("-" * 30)
        
        examples = [0.01, 0.1, 1, 10]
        for amount in examples:
            tokens = amount / token_price_matic
            usd_cost = amount * 0.9
            print(f"💸 {amount} MATIC → {tokens:,.0f} ALIEN (${usd_cost:.2f})")
        
        # Информация о владельце
        print("\n👑 ИНФОРМАЦИЯ О ВЛАДЕЛЬЦЕ:")
        print("-" * 30)
        
        owner = presale_contract.functions.owner().call()
        print(f"👤 Владелец: {owner}")
        
        # Проверяем, является ли текущий пользователь владельцем
        if WALLET_ADDRESS:
            wallet_checksum = Web3.to_checksum_address(WALLET_ADDRESS)
            is_owner = owner.lower() == wallet_checksum.lower()
            print(f"🔑 Вы владелец: {'Да' if is_owner else 'Нет'}")
        
        # Баланс токенов на пресейле
        print("\n🏦 БАЛАНСЫ:")
        print("-" * 30)
        
        # Импортируем токен контракт для проверки баланса
        from config import token_contract
        if token_contract:
            presale_token_balance = token_contract.functions.balanceOf(presale_address).call()
            presale_token_balance_human = presale_token_balance / 10**18
            print(f"👽 Токенов на пресейле: {presale_token_balance_human:,.0f} ALIEN")
        
        # Ссылки
        print("\n🔗 ПОЛЕЗНЫЕ ССЫЛКИ:")
        print("-" * 30)
        print(f"📊 Пресейл: https://polygonscan.com/address/{presale_address}")
        print(f"👽 Токен: https://polygonscan.com/address/{token_address}")
        
        print("\n✅ Проверка завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке: {e}")

if __name__ == "__main__":
    check_presale_conditions() 