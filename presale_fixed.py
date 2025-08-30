from web3 import Web3
from config import w3, presale_contract, PRIVATE_KEY, WALLET_ADDRESS

def buy_tokens(amount_matic):
    """
    Купить токены ALIEN за MATIC
    
    Args:
        amount_matic (float): Количество MATIC для покупки
    
    Returns:
        str: Хеш транзакции
    """
    if not presale_contract:
        raise ValueError("Пресейл контракт не настроен в .env")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    # Конвертируем MATIC в Wei
    amount_wei = w3.to_wei(amount_matic, 'ether')
    
    # Получаем nonce
    wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
    nonce = w3.eth.get_transaction_count(wallet_address)
    
    # Строим транзакцию
    transaction = presale_contract.functions.buyTokens().build_transaction({
        'from': wallet_address,
        'value': amount_wei,
        'nonce': nonce,
        'gas': 200000,  # Можно оптимизировать
        'gasPrice': w3.eth.gas_price
    })
    
    # Подписываем транзакцию
    private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
    
    # Отправляем транзакцию
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    return tx_hash.hex()

def claim_tokens():
    """
    Забрать купленные токены
    
    Returns:
        str: Хеш транзакции
    """
    if not presale_contract:
        raise ValueError("Пресейл контракт не настроен в .env")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    # Получаем nonce
    wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
    nonce = w3.eth.get_transaction_count(wallet_address)
    
    # Строим транзакцию
    transaction = presale_contract.functions.claimTokens().build_transaction({
        'from': wallet_address,
        'nonce': nonce,
        'gas': 150000,  # Можно оптимизировать
        'gasPrice': w3.eth.gas_price
    })
    
    # Подписываем транзакцию
    private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
    
    # Отправляем транзакцию
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    
    return tx_hash.hex()

def get_presale_info():
    """
    Получить информацию о пресейле
    
    Returns:
        dict: Информация о пресейле
    """
    if not presale_contract:
        return {"error": "Пресейл контракт не настроен"}
    
    try:
        # Здесь можно добавить вызовы методов пресейл контракта
        # для получения информации о статусе, ценах и т.д.
        return {
            "status": "Пресейл контракт подключен",
            "address": presale_contract.address
        }
    except Exception as e:
        return {"error": f"Ошибка получения информации: {str(e)}"}

def wait_for_transaction(tx_hash, timeout=300):
    """
    Ожидать подтверждения транзакции
    
    Args:
        tx_hash (str): Хеш транзакции
        timeout (int): Таймаут в секундах
    
    Returns:
        dict: Результат транзакции
    """
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        return {
            "success": receipt.status == 1,
            "gas_used": receipt.gasUsed,
            "block_number": receipt.blockNumber
        }
    except Exception as e:
        return {"error": f"Ошибка ожидания транзакции: {str(e)}"} 