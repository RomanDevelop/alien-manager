# 🚀 ALIEN Presale Bot

**Полнофункциональный бот для управления пресейлом токенов ALIEN на Polygon**

## ✅ **Статус: Пресейл деплоен, протестирован и оптимизирован!**

### **📍 Адреса контрактов:**
- **Пресейл**: `0x2699838c090346Eaf93F96069B56B3637828dFAC`
- **Токен ALIEN**: `0xa8e302849DdF86769C026d9A2405e1cdA01ED992`

### **🔗 Ссылки:**
- **Пресейл**: https://polygonscan.com/address/0x2699838c090346Eaf93F96069B56B3637828dFAC
- **Токен**: https://polygonscan.com/address/0xa8e302849DdF86769C026d9A2405e1cdA01ED992

## 🛠 **Установка и настройка**

### **Требования:**
- Python 3.9+
- web3.py
- python-dotenv
- pandas

### **Установка:**
```bash
pip install web3 python-dotenv pandas
```

### **Настройка .env:**
```env
RPC_URL=https://polygon-rpc.com
PRIVATE_KEY=your_private_key
WALLET_ADDRESS=your_wallet_address
PRESALE_ADDRESS=0x2699838c090346Eaf93F96069B56B3637828dFAC
TOKEN_ADDRESS=0xa8e302849DdF86769C026d9A2405e1cdA01ED992
```

## 🎯 **Использование**

### **Основные команды:**
```bash
# Проверить баланс
python bot.py balance

# Купить токены
python bot.py buy --amount 0.1

# Забрать купленные токены
python bot.py claim

# Информация о пресейле
python bot.py info

# История действий
python bot.py history

# Статистика
python bot.py stats
```

### **Команды владельца:**
```bash
# Приостановить/возобновить пресейл
python bot.py pause

# Забрать собранные средства
python bot.py withdraw

# Обновить цену токена (только владелец)
python update_price.py 0.0001
```

## 📊 **Параметры пресейла (ОБНОВЛЕНО)**

- **Старт**: 1754216280 (через 5 минут после деплоя)
- **Окончание**: 1755943980 (через 20 дней)
- **Hardcap**: 100 MATIC
- **Цена токена**: 0.0001 MATIC (ОБНОВЛЕНО!)
- **Токенов на пресейле**: 400M ALIEN
- **Токенов для продажи**: 1,000,000 ALIEN

## ✅ **Тестирование завершено**

- ✅ **Покупка токенов**: 0.1 MATIC → 200 ALIEN (старая цена)
- ✅ **Обновление цены**: 0.0005 → 0.0001 MATIC (80% снижение)
- ✅ **Автоматический расчет**: Работает корректно
- ✅ **Прогресс пресейла**: 0.1% (0.1/100 MATIC)
- ✅ **Безопасность**: OpenZeppelin + ReentrancyGuard

## 🛡 **Безопасность**

- **OpenZeppelin**: Ownable, Pausable, ReentrancyGuard
- **Проверки**: Валидация параметров, проверки безопасности
- **Модификаторы**: presaleActive, onlyOwner
- **События**: Полное логирование всех операций

## 📁 **Структура проекта**

```
pytoncrypto/
├── bot.py                 # Основной бот
├── config.py              # Конфигурация и ABI
├── presale.py             # Функции пресейла
├── token_v2.py            # Функции токена V2
├── transfer_tokens.py     # Перевод токенов
├── update_price.py        # Обновление цены токена
├── AlienPresale.sol       # Смарт-контракт пресейла
├── ALIEN_V2.sol          # Смарт-контракт токена
├── .env                   # Переменные окружения
└── README.md             # Документация
```

## 🎯 **Готов к запуску!**

Пресейл полностью функционален с оптимизированной ценой и готов к публичному запуску.

---
**Версия**: 2.1 Final (с обновленной ценой)  
**Статус**: ✅ Готов к продакшену
# alien-manager
