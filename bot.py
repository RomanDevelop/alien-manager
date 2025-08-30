#!/usr/bin/env python3
"""
ALIEN Presale Bot - CLI интерфейс
"""

import argparse
import sys
from web3 import Web3

from config import w3, WALLET_ADDRESS
from token_utils import get_matic_balance, get_token_balance, format_balance
from presale import buy_tokens, claim_tokens, get_presale_info, wait_for_transaction, withdraw_funds, withdraw_unsold_tokens, pause_presale
from history import log_action, print_history, get_statistics

def check_balance(address=None):
    """
    Проверить балансы MATIC и ALIEN токенов
    
    Args:
        address (str): Адрес для проверки (опционально)
    """
    try:
        # Получаем балансы
        matic_balance = get_matic_balance(address)
        token_balance = get_token_balance(address)
        
        # Выводим результаты
        print(f"\n💰 Балансы для адреса: {address or WALLET_ADDRESS}")
        print("-" * 50)
        print(f"🟣 MATIC: {matic_balance:.4f}")
        print(f"👽 ALIEN: {format_balance(token_balance)}")
        print("-" * 50)
        
        # Логируем действие
        log_action("balance", address=address or WALLET_ADDRESS)
        
    except Exception as e:
        print(f"❌ Ошибка при проверке баланса: {str(e)}")
        log_action("balance", address=address or WALLET_ADDRESS, status="error")

def buy_tokens_cli(amount):
    """
    Купить токены ALIEN
    
    Args:
        amount (float): Количество MATIC для покупки
    """
    try:
        print(f"\n🛒 Покупка токенов ALIEN за {amount} MATIC...")
        
        # Проверяем баланс MATIC
        matic_balance = get_matic_balance()
        if matic_balance < amount:
            print(f"❌ Недостаточно MATIC. Доступно: {matic_balance:.4f}, нужно: {amount}")
            return
        
        # Выполняем покупку
        tx_hash = buy_tokens(amount)
        print(f"✅ Транзакция отправлена: {tx_hash}")
        
        # Ждем подтверждения
        print("⏳ Ожидание подтверждения транзакции...")
        result = wait_for_transaction(tx_hash)
        
        if result.get("success"):
            print(f"✅ Транзакция подтверждена! Блок: {result['block_number']}")
            log_action("buy", tx_hash=tx_hash, amount=amount, status="success")
        else:
            print(f"❌ Ошибка транзакции: {result.get('error', 'Неизвестная ошибка')}")
            log_action("buy", tx_hash=tx_hash, amount=amount, status="error")
            
    except Exception as e:
        print(f"❌ Ошибка при покупке токенов: {str(e)}")
        log_action("buy", amount=amount, status="error")

def claim_tokens_cli():
    """
    Забрать купленные токены
    """
    try:
        print("\n🎁 Забираем купленные токены...")
        
        # Выполняем claim
        tx_hash = claim_tokens()
        print(f"✅ Транзакция отправлена: {tx_hash}")
        
        # Ждем подтверждения
        print("⏳ Ожидание подтверждения транзакции...")
        result = wait_for_transaction(tx_hash)
        
        if result.get("success"):
            print(f"✅ Токены успешно забраны! Блок: {result['block_number']}")
            log_action("claim", tx_hash=tx_hash, status="success")
        else:
            print(f"❌ Ошибка транзакции: {result.get('error', 'Неизвестная ошибка')}")
            log_action("claim", tx_hash=tx_hash, status="error")
            
    except Exception as e:
        print(f"❌ Ошибка при заборе токенов: {str(e)}")
        log_action("claim", status="error")

def show_history(limit=10):
    """
    Показать историю действий
    
    Args:
        limit (int): Количество последних записей
    """
    print_history(limit)

def show_stats():
    """
    Показать статистику
    """
    stats = get_statistics()
    
    print("\n📊 Статистика действий:")
    print("-" * 30)
    print(f"Всего действий: {stats['total_actions']}")
    
    if stats['total_actions'] > 0:
        print(f"Успешность: {stats['success_rate']:.1f}%")
        print(f"Последнее действие: {stats['last_action']}")
        print(f"Последний раз: {stats['last_timestamp']}")
        
        if stats['actions_by_type']:
            print("\nПо типам действий:")
            for action, count in stats['actions_by_type'].items():
                print(f"  {action}: {count}")

def main():
    """
    Главная функция CLI
    """
    parser = argparse.ArgumentParser(
        description="ALIEN Presale Bot - CLI для работы с токенами ALIEN",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python bot.py balance                    # Проверить баланс
  python bot.py balance --address 0x123   # Проверить баланс другого адреса
  python bot.py buy --amount 1            # Купить токены за 1 MATIC
  python bot.py claim                     # Забрать купленные токены
  python bot.py history                   # Показать историю
  python bot.py stats                     # Показать статистику
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда balance
    balance_parser = subparsers.add_parser('balance', help='Проверить баланс')
    balance_parser.add_argument('--address', help='Адрес для проверки (по умолчанию используется WALLET_ADDRESS)')
    
    # Команда buy
    buy_parser = subparsers.add_parser('buy', help='Купить токены ALIEN')
    buy_parser.add_argument('--amount', type=float, required=True, help='Количество MATIC для покупки')
    
    # Команда claim
    subparsers.add_parser('claim', help='Забрать купленные токены')
    
    # Команда history
    history_parser = subparsers.add_parser('history', help='Показать историю действий')
    history_parser.add_argument('--limit', type=int, default=10, help='Количество последних записей')
    
    # Команда stats
    subparsers.add_parser('stats', help='Показать статистику')
    
    # Команда info
    subparsers.add_parser('info', help='Информация о пресейле')
    
    # Команды владельца
    withdraw_parser = subparsers.add_parser('withdraw', help='Забрать средства (только для владельца)')
    withdraw_parser.add_argument('--type', choices=['funds', 'tokens'], required=True, help='Тип вывода: funds (MATIC) или tokens (ALIEN)')
    
    pause_parser = subparsers.add_parser('pause', help='Приостановить/возобновить пресейл (только для владельца)')
    pause_parser.add_argument('--status', type=bool, required=True, help='True - приостановить, False - возобновить')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Проверяем подключение к сети
        if not w3.is_connected():
            print("❌ Не удалось подключиться к Polygon RPC")
            sys.exit(1)
        
        # Выполняем команды
        if args.command == 'balance':
            check_balance(args.address)
        elif args.command == 'buy':
            buy_tokens_cli(args.amount)
        elif args.command == 'claim':
            claim_tokens_cli()
        elif args.command == 'history':
            show_history(args.limit)
        elif args.command == 'stats':
            show_stats()
        elif args.command == 'info':
            info = get_presale_info()
            print(f"\n📋 Информация о пресейле:")
            print("-" * 30)
            for key, value in info.items():
                print(f"{key}: {value}")
        elif args.command == 'withdraw':
            if args.type == 'funds':
                print("\n💰 Забираем собранные MATIC...")
                tx_hash = withdraw_funds()
                print(f"✅ Транзакция отправлена: {tx_hash}")
                
                result = wait_for_transaction(tx_hash)
                if result.get("success"):
                    print(f"✅ Средства успешно забраны! Блок: {result['block_number']}")
                    log_action("withdraw_funds", tx_hash=tx_hash, status="success")
                else:
                    print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
                    log_action("withdraw_funds", tx_hash=tx_hash, status="error")
            else:  # tokens
                print("\n🎁 Забираем нераспроданные токены...")
                tx_hash = withdraw_unsold_tokens()
                print(f"✅ Транзакция отправлена: {tx_hash}")
                
                result = wait_for_transaction(tx_hash)
                if result.get("success"):
                    print(f"✅ Токены успешно забраны! Блок: {result['block_number']}")
                    log_action("withdraw_tokens", tx_hash=tx_hash, status="success")
                else:
                    print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
                    log_action("withdraw_tokens", tx_hash=tx_hash, status="error")
        elif args.command == 'pause':
            status_text = "приостановлен" if args.status else "возобновлен"
            print(f"\n⏸️ Пресейл {status_text}...")
            tx_hash = pause_presale(args.status)
            print(f"✅ Транзакция отправлена: {tx_hash}")
            
            result = wait_for_transaction(tx_hash)
            if result.get("success"):
                print(f"✅ Пресейл {status_text}! Блок: {result['block_number']}")
                log_action("pause_presale", tx_hash=tx_hash, status="success")
            else:
                print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
                log_action("pause_presale", tx_hash=tx_hash, status="error")
    
    except KeyboardInterrupt:
        print("\n⏹️ Операция прервана пользователем")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 