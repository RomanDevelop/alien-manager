from web3 import Web3
from config import w3, token_v2_contract, WALLET_ADDRESS, PRIVATE_KEY

def mint_tokens(to_address, amount):
    """
    Создать новые токены (только для владельца)
    
    Args:
        to_address (str): Адрес получателя
        amount (float): Количество токенов
    
    Returns:
        str: Хеш транзакции
    """
    if not token_v2_contract:
        raise ValueError("Улучшенный токен не настроен")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Конвертируем в Wei
        amount_wei = w3.to_wei(amount, 'ether')
        
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = token_v2_contract.functions.mint(to_address, amount_wei).build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 150000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Подписываем транзакцию
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Ошибка при создании токенов: {str(e)}")
        raise e

def burn_tokens(amount):
    """
    Сжечь токены
    
    Args:
        amount (float): Количество токенов для сжигания
    
    Returns:
        str: Хеш транзакции
    """
    if not token_v2_contract:
        raise ValueError("Улучшенный токен не настроен")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Конвертируем в Wei
        amount_wei = w3.to_wei(amount, 'ether')
        
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = token_v2_contract.functions.burn(amount_wei).build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Подписываем транзакцию
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Ошибка при сжигании токенов: {str(e)}")
        raise e

def burn_from_tokens(from_address, amount):
    """
    Сжечь токены с другого адреса (только для владельца)
    
    Args:
        from_address (str): Адрес, с которого сжигать
        amount (float): Количество токенов
    
    Returns:
        str: Хеш транзакции
    """
    if not token_v2_contract:
        raise ValueError("Улучшенный токен не настроен")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Конвертируем в Wei
        amount_wei = w3.to_wei(amount, 'ether')
        
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = token_v2_contract.functions.burnFrom(from_address, amount_wei).build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Подписываем транзакцию
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Ошибка при сжигании токенов: {str(e)}")
        raise e

def pause_token():
    """
    Приостановить переводы токенов (только для владельца)
    
    Returns:
        str: Хеш транзакции
    """
    if not token_v2_contract:
        raise ValueError("Улучшенный токен не настроен")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = token_v2_contract.functions.pause().build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Подписываем транзакцию
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Ошибка при приостановке токена: {str(e)}")
        raise e

def unpause_token():
    """
    Возобновить переводы токенов (только для владельца)
    
    Returns:
        str: Хеш транзакции
    """
    if not token_v2_contract:
        raise ValueError("Улучшенный токен не настроен")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = token_v2_contract.functions.unpause().build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Подписываем транзакцию
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Ошибка при возобновлении токена: {str(e)}")
        raise e

def set_blacklist(address, status):
    """
    Добавить/удалить адрес из черного списка (только для владельца)
    
    Args:
        address (str): Адрес для изменения статуса
        status (bool): True - добавить в черный список, False - убрать
    
    Returns:
        str: Хеш транзакции
    """
    if not token_v2_contract:
        raise ValueError("Улучшенный токен не настроен")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = token_v2_contract.functions.setBlacklist(address, status).build_transaction({
            'from': wallet_address,
            'nonce': nonce,
            'gas': 100000,
            'gasPrice': w3.eth.gas_price
        })
        
        # Подписываем транзакцию
        private_key_with_0x = f"0x{PRIVATE_KEY}" if not PRIVATE_KEY.startswith('0x') else PRIVATE_KEY
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key_with_0x)
        
        # Отправляем транзакцию
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        return tx_hash.hex()
        
    except Exception as e:
        print(f"❌ Ошибка при изменении черного списка: {str(e)}")
        raise e

def get_token_info():
    """
    Получить информацию о токене
    
    Returns:
        dict: Информация о токене
    """
    if not token_v2_contract:
        return {"error": "Улучшенный токен не настроен"}
    
    try:
        info = token_v2_contract.functions.getContractInfo().call()
        
        return {
            "name": info[0],
            "symbol": info[1],
            "decimals": info[2],
            "total_supply": w3.from_wei(info[3], 'ether'),
            "is_paused": info[4],
            "owner": info[5]
        }
        
    except Exception as e:
        return {"error": f"Ошибка получения информации: {str(e)}"}

def get_blacklist_status(address):
    """
    Проверить статус адреса в черном списке
    
    Args:
        address (str): Адрес для проверки
    
    Returns:
        bool: True если в черном списке
    """
    if not token_v2_contract:
        return None
    
    try:
        return token_v2_contract.functions.getBlacklistStatus(address).call()
    except:
        return None 