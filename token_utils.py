from web3 import Web3
from config import w3, token_contract, WALLET_ADDRESS

def get_matic_balance(address=None):
    """
    Получить баланс MATIC в читаемом формате
    
    Args:
        address (str): Адрес кошелька. Если None, используется WALLET_ADDRESS из .env
    
    Returns:
        float: Баланс MATIC в ETH формате
    """
    if address is None:
        address = WALLET_ADDRESS
    
    if not address:
        raise ValueError("Адрес не указан и WALLET_ADDRESS не настроен в .env")
    
    address = Web3.to_checksum_address(address)
    balance_wei = w3.eth.get_balance(address)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    
    return float(balance_eth)

def get_token_balance(address=None):
    """
    Получить баланс токена ALIEN, используя существующую логику из check_balances.py
    
    Args:
        address (str): Адрес кошелька. Если None, используется WALLET_ADDRESS из .env
    
    Returns:
        float: Баланс токенов ALIEN
    """
    if address is None:
        address = WALLET_ADDRESS
    
    if not address:
        raise ValueError("Адрес не указан и WALLET_ADDRESS не настроен в .env")
    
    address = Web3.to_checksum_address(address)
    
    # Используем существующую логику из check_balances.py
    balance_wei = token_contract.functions.balanceOf(address).call()
    balance_tokens = balance_wei / 1e18
    
    return float(balance_tokens)

def get_allowance(owner, spender):
    """
    Получить разрешение (allowance) токенов
    
    Args:
        owner (str): Адрес владельца токенов
        spender (str): Адрес, которому разрешено тратить токены
    
    Returns:
        float: Размер разрешения в токенах
    """
    owner = Web3.to_checksum_address(owner)
    spender = Web3.to_checksum_address(spender)
    
    allowance_wei = token_contract.functions.allowance(owner, spender).call()
    allowance_tokens = allowance_wei / 1e18
    
    return float(allowance_tokens)

def format_balance(balance, token_name="ALIEN"):
    """
    Форматировать баланс для вывода
    
    Args:
        balance (float): Баланс токенов
        token_name (str): Название токена
    
    Returns:
        str: Отформатированный баланс
    """
    if balance >= 1_000_000:
        return f"{balance/1_000_000:.2f}M {token_name}"
    elif balance >= 1_000:
        return f"{balance/1_000:.2f}K {token_name}"
    else:
        return f"{balance:.2f} {token_name}" 