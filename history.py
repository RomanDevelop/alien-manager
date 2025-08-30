import pandas as pd
import os
from datetime import datetime

HISTORY_FILE = 'history.csv'

def log_action(action, tx_hash=None, amount=None, address=None, status="success"):
    """
    Логировать действие в CSV файл
    
    Args:
        action (str): Тип действия (balance, buy, claim)
        tx_hash (str): Хеш транзакции
        amount (float): Сумма (если применимо)
        address (str): Адрес кошелька (если применимо)
        status (str): Статус операции
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Создаем запись
    record = {
        'timestamp': timestamp,
        'action': action,
        'tx_hash': tx_hash or '',
        'amount': amount or '',
        'address': address or '',
        'status': status
    }
    
    # Создаем DataFrame
    df_new = pd.DataFrame([record])
    
    # Проверяем существование файла
    if os.path.exists(HISTORY_FILE):
        # Читаем существующий файл
        df_existing = pd.read_csv(HISTORY_FILE)
        # Объединяем с новой записью
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new
    
    # Сохраняем в CSV
    df_combined.to_csv(HISTORY_FILE, index=False)
    
    print(f"✅ Действие '{action}' записано в {HISTORY_FILE}")

def get_history(limit=None):
    """
    Получить историю действий
    
    Args:
        limit (int): Количество последних записей
    
    Returns:
        pd.DataFrame: История действий
    """
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame()
    
    df = pd.read_csv(HISTORY_FILE)
    
    if limit:
        df = df.tail(limit)
    
    return df

def print_history(limit=10):
    """
    Вывести историю действий в консоль
    
    Args:
        limit (int): Количество последних записей
    """
    df = get_history(limit)
    
    if df.empty:
        print("📝 История действий пуста")
        return
    
    print(f"\n📝 Последние {len(df)} действий:")
    print("-" * 80)
    
    for _, row in df.iterrows():
        timestamp = row['timestamp']
        action = row['action']
        tx_hash = row['tx_hash'] if pd.notna(row['tx_hash']) else ''
        amount = row['amount'] if pd.notna(row['amount']) else ''
        status = row['status']
        
        print(f"🕐 {timestamp} | {action.upper()} | {status}")
        if tx_hash:
            print(f"   📄 TX: {tx_hash}")
        if amount:
            print(f"   💰 Сумма: {amount}")
        print()

def clear_history():
    """
    Очистить историю действий
    """
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("🗑️ История действий очищена")
    else:
        print("📝 История действий уже пуста")

def get_statistics():
    """
    Получить статистику действий
    
    Returns:
        dict: Статистика
    """
    df = get_history()
    
    if df.empty:
        return {"total_actions": 0}
    
    stats = {
        "total_actions": len(df),
        "actions_by_type": df['action'].value_counts().to_dict(),
        "success_rate": len(df[df['status'] == 'success']) / len(df) * 100,
        "last_action": df.iloc[-1]['action'] if not df.empty else None,
        "last_timestamp": df.iloc[-1]['timestamp'] if not df.empty else None
    }
    
    return stats 