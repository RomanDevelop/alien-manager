#!/usr/bin/env python3
"""
Возврат средств и удаление пресейла
"""

from web3 import Web3
from config import w3, presale_contract, WALLET_ADDRESS, PRIVATE_KEY
import os

def withdraw_and_destroy():
    """Возврат средств и удаление пресейла"""
    
    if not presale_contract:
        print("❌ Пресейл не подключен")
        return
    
    try:
        presale_address = presale_contract.address
        print(f"🎯 Адрес пресейла: {presale_address}")
        
        # Проверяем баланс пресейла
        balance = w3.eth.get_balance(presale_address)
        print(f"💰 Баланс пресейла: {Web3.from_wei(balance, 'ether')} MATIC")
        
        # Проверяем владельца
        try:
            owner = presale_contract.functions.owner().call()
            print(f"👑 Владелец: {owner}")
            print(f"🔑 Вы владелец: {'✅' if owner.lower() == WALLET_ADDRESS.lower() else '❌'}")
        except Exception as e:
            print(f"⚠️ Не удалось проверить владельца: {e}")
            owner = WALLET_ADDRESS  # Предполагаем, что вы владелец
        
        if owner.lower() != WALLET_ADDRESS.lower():
            print("❌ Вы не владелец пресейла. Невозможно удалить.")
            return
        
        # Проверяем ваши токены
        try:
            user_info = presale_contract.functions.getUserInfo(WALLET_ADDRESS).call()
            contribution = Web3.from_wei(user_info[0], 'ether')
            claimable_tokens = user_info[1]
            print(f"💎 Ваш вклад: {contribution} MATIC")
            print(f"🎁 Claimable токены: {claimable_tokens} ALIEN")
        except Exception as e:
            print(f"⚠️ Не удалось проверить ваш вклад: {e}")
        
        # Возвращаем средства (если пресейл еще не закончился)
        if balance > 0:
            print("\n🔄 Возврат средств...")
            
            nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
            
            # Пытаемся вызвать withdrawFunds
            try:
                tx = presale_contract.functions.withdrawFunds().build_transaction({
                    'from': WALLET_ADDRESS,
                    'nonce': nonce,
                    'gas': 200000,
                    'gasPrice': w3.eth.gas_price
                })
                
                signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                
                print(f"🚀 Транзакция возврата отправлена: {tx_hash.hex()}")
                print(f"🔗 Polygonscan: https://polygonscan.com/tx/{tx_hash.hex()}")
                
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                
                if receipt.status == 1:
                    print("✅ Средства успешно возвращены!")
                else:
                    print("❌ Транзакция возврата не прошла")
                    
            except Exception as e:
                print(f"❌ Ошибка возврата средств: {e}")
                print("💡 Возможно, пресейл еще не закончился")
        
        print("\n🗑️ Пресейл готов к удалению!")
        print("📝 Для полного удаления нужно:")
        print("1. Дождаться окончания пресейла")
        print("2. Забрать все средства через withdrawFunds")
        print("3. Забрать нераспроданные токены через withdrawUnsoldTokens")
        print("4. Удалить контракт (требует selfdestruct в коде)")
        
        print(f"\n📍 Адрес для удаления: {presale_address}")
        print("🔗 Polygonscan: https://polygonscan.com/address/" + presale_address)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🗑️ Подготовка к удалению пресейла")
    print("=" * 50)
    
    withdraw_and_destroy() 