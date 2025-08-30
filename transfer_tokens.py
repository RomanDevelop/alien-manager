#!/usr/bin/env python3
"""
Скрипт для перевода токенов на пресейл контракт
"""

from web3 import Web3
from config import w3, token_contract, WALLET_ADDRESS, PRIVATE_KEY, PRESALE_ADDRESS
import os
from dotenv import load_dotenv

load_dotenv()

def transfer_tokens_to_presale(amount):
    """Переводит токены на пресейл контракт"""
    
    if not token_contract:
        print("❌ Токен контракт не настроен")
        return
    
    if not PRESALE_ADDRESS:
        print("❌ Адрес пресейла не настроен")
        return
    
    try:
        # Проверяем баланс
        wallet_address_checksum = Web3.to_checksum_address(WALLET_ADDRESS)
        balance = token_contract.functions.balanceOf(wallet_address_checksum).call()
        balance_human = balance / 10**18
        
        print(f"💰 Текущий баланс: {balance_human:,.0f} ALIEN")
        print(f"📤 Переводим: {amount:,.0f} ALIEN")
        print(f"📍 На пресейл: {PRESALE_ADDRESS}")
        
        # Конвертируем в wei
        amount_wei = amount * 10**18
        
        if amount_wei > balance:
            print(f"❌ Недостаточно токенов. Доступно: {balance_human:,.0f}")
            return
        
        # Строим транзакцию
        nonce = w3.eth.get_transaction_count(wallet_address_checksum)
        
        # Получаем gas price
        gas_price = w3.eth.gas_price
        
        # Строим транзакцию
        transaction = token_contract.functions.transfer(
            Web3.to_checksum_address(PRESALE_ADDRESS),
            amount_wei
        ).build_transaction({
            'from': Web3.to_checksum_address(WALLET_ADDRESS),
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
            print("✅ Токены успешно переведены на пресейл!")
            print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
            
            # Проверяем новый баланс
            new_balance = token_contract.functions.balanceOf(wallet_address_checksum).call()
            new_balance_human = new_balance / 10**18
            print(f"💰 Новый баланс: {new_balance_human:,.0f} ALIEN")
            
            # Проверяем баланс пресейла
            presale_balance = token_contract.functions.balanceOf(PRESALE_ADDRESS).call()
            presale_balance_human = presale_balance / 10**18
            print(f"🏦 Баланс пресейла: {presale_balance_human:,.0f} ALIEN")
            
        else:
            print("❌ Транзакция не удалась")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Использование: python transfer_tokens.py <количество_токенов>")
        print("Пример: python transfer_tokens.py 400000000")
        sys.exit(1)
    
    try:
        amount = int(sys.argv[1])
        transfer_tokens_to_presale(amount)
    except ValueError:
        print("❌ Неверное количество токенов. Используйте число.")
        sys.exit(1) 