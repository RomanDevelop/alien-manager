from web3 import Web3
from config import w3, presale_contract, PRIVATE_KEY, WALLET_ADDRESS

def get_presale_status():
    """
    Получить детальный статус пресейла
    
    Returns:
        dict: Статус пресейла
    """
    if not presale_contract:
        return {"error": "Пресейл контракт не настроен"}
    
    try:
        # Получаем текущее время
        current_time = w3.eth.get_block('latest').timestamp
        
        # Получаем параметры пресейла
        start_time = presale_contract.functions.startTime().call()
        end_time = presale_contract.functions.endTime().call()
        hard_cap = presale_contract.functions.hardCap().call()
        total_raised = presale_contract.functions.totalRaised().call()
        paused = presale_contract.functions.paused().call()
        token_price = presale_contract.functions.tokenPrice().call()
        
        # Проверяем статус
        is_active = current_time >= start_time and current_time <= end_time and not paused
        is_before_start = current_time < start_time
        is_after_end = current_time > end_time
        is_paused = paused
        is_hardcap_reached = total_raised >= hard_cap
        
        # Конвертируем в читаемый формат
        start_time_readable = w3.from_wei(start_time, 'ether') if start_time > 0 else 0
        end_time_readable = w3.from_wei(end_time, 'ether') if end_time > 0 else 0
        hard_cap_matic = w3.from_wei(hard_cap, 'ether')
        total_raised_matic = w3.from_wei(total_raised, 'ether')
        token_price_matic = w3.from_wei(token_price, 'ether')
        
        return {
            "status": "Пресейл контракт подключен",
            "address": presale_contract.address,
            "current_time": current_time,
            "start_time": start_time,
            "end_time": end_time,
            "hard_cap": hard_cap,
            "total_raised": total_raised,
            "paused": paused,
            "token_price": token_price,
            "is_active": is_active,
            "is_before_start": is_before_start,
            "is_after_end": is_after_end,
            "is_paused": is_paused,
            "is_hardcap_reached": is_hardcap_reached,
            "remaining_cap": hard_cap - total_raised,
            "progress_percent": (total_raised / hard_cap * 100) if hard_cap > 0 else 0
        }
        
    except Exception as e:
        return {"error": f"Ошибка получения статуса: {str(e)}"}

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
    
    try:
        # Проверяем статус пресейла
        status = get_presale_status()
        if "error" in status:
            raise ValueError(f"Ошибка проверки статуса: {status['error']}")
        
        if not status.get("is_active", False):
            if status.get("is_before_start", False):
                raise ValueError("Пресейл еще не начался")
            elif status.get("is_after_end", False):
                raise ValueError("Пресейл уже закончился")
            elif status.get("is_paused", False):
                raise ValueError("Пресейл приостановлен")
            else:
                raise ValueError("Пресейл не активен")
        
        if status.get("is_hardcap_reached", False):
            raise ValueError("Hardcap достигнут")
        
        # Конвертируем MATIC в Wei
        amount_wei = w3.to_wei(amount_matic, 'ether')
        
        # Проверяем, не превышает ли сумма оставшийся hardcap
        remaining_cap = status.get("remaining_cap", 0)
        if amount_wei > remaining_cap:
            raise ValueError(f"Сумма превышает оставшийся hardcap. Максимум: {w3.from_wei(remaining_cap, 'ether')} MATIC")
        
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
        
    except Exception as e:
        print(f"❌ Ошибка при покупке: {str(e)}")
        print(f"🔍 Детали: {type(e).__name__}")
        raise e

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
    
    try:
        # Проверяем, есть ли токены для забора
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        claimable_tokens = presale_contract.functions.claimableTokens(wallet_address).call()
        
        if claimable_tokens == 0:
            raise ValueError("Нет токенов для забора")
        
        # Получаем nonce
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
        
    except Exception as e:
        print(f"❌ Ошибка при заборе токенов: {str(e)}")
        print(f"🔍 Детали: {type(e).__name__}")
        raise e

def withdraw_funds():
    """
    Забрать собранные MATIC (только для владельца)
    
    Returns:
        str: Хеш транзакции
    """
    if not presale_contract:
        raise ValueError("Пресейл контракт не настроен в .env")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = presale_contract.functions.withdrawFunds().build_transaction({
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
        print(f"❌ Ошибка при заборе средств: {str(e)}")
        print(f"🔍 Детали: {type(e).__name__}")
        raise e

def withdraw_unsold_tokens():
    """
    Забрать нераспроданные токены (только для владельца)
    
    Returns:
        str: Хеш транзакции
    """
    if not presale_contract:
        raise ValueError("Пресейл контракт не настроен в .env")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = presale_contract.functions.withdrawUnsoldTokens().build_transaction({
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
        print(f"❌ Ошибка при заборе нераспроданных токенов: {str(e)}")
        print(f"🔍 Детали: {type(e).__name__}")
        raise e

def pause_presale(status):
    """
    Приостановить/возобновить пресейл (только для владельца)
    
    Args:
        status (bool): True - приостановить, False - возобновить
    
    Returns:
        str: Хеш транзакции
    """
    if not presale_contract:
        raise ValueError("Пресейл контракт не настроен в .env")
    
    if not PRIVATE_KEY or PRIVATE_KEY == 'your_private_key':
        raise ValueError("Приватный ключ не настроен в .env")
    
    try:
        # Получаем nonce
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        nonce = w3.eth.get_transaction_count(wallet_address)
        
        # Строим транзакцию
        transaction = presale_contract.functions.pausePresale(status).build_transaction({
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
        print(f"❌ Ошибка при изменении статуса паузы: {str(e)}")
        print(f"🔍 Детали: {type(e).__name__}")
        raise e

def get_presale_info():
    """
    Получить информацию о пресейле
    
    Returns:
        dict: Информация о пресейле
    """
    if not presale_contract:
        return {"error": "Пресейл контракт не настроен"}
    
    try:
        # Получаем детальный статус
        status = get_presale_status()
        
        if "error" in status:
            return status
        
        # Добавляем информацию о пользователе
        wallet_address = Web3.to_checksum_address(WALLET_ADDRESS)
        user_contribution = presale_contract.functions.contributions(wallet_address).call()
        user_claimable = presale_contract.functions.claimableTokens(wallet_address).call()
        
        status["user_contribution"] = w3.from_wei(user_contribution, 'ether')
        status["user_claimable_tokens"] = w3.from_wei(user_claimable, 'ether')
        
        return status
        
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
        
        if receipt.status == 0:
            # Транзакция провалилась, получаем детали ошибки
            try:
                tx = w3.eth.get_transaction(tx_hash)
                # Пытаемся декодировать ошибку
                error_msg = "Транзакция провалилась"
                if hasattr(receipt, 'logs') and receipt.logs:
                    error_msg = f"Ошибка: {receipt.logs}"
            except:
                error_msg = "Транзакция провалилась (не удалось получить детали)"
            
            return {
                "success": False,
                "error": error_msg,
                "gas_used": receipt.gasUsed,
                "block_number": receipt.blockNumber
            }
        else:
            return {
                "success": True,
                "gas_used": receipt.gasUsed,
                "block_number": receipt.blockNumber
            }
            
    except Exception as e:
        return {"error": f"Ошибка ожидания транзакции: {str(e)}"} 