# 🪐 ALIEN Token V2 - Улучшенная версия

Улучшенная версия токена ALIEN с дополнительными функциями безопасности и управления.

## 🚀 **Улучшения по сравнению с V1:**

### ✅ **Новые функции безопасности:**
- **Pausable** — возможность приостановки переводов
- **Blacklist** — черный список адресов
- **ReentrancyGuard** — защита от повторного входа
- **Ownable** — управление владельцем

### ✅ **Новые функции управления:**
- **mint()** — создание новых токенов (владелец)
- **burn()** — сжигание токенов (пользователи)
- **burnFrom()** — принудительное сжигание (владелец)
- **pause()/unpause()** — приостановка переводов
- **setBlacklist()** — управление черным списком

## 📋 **Структура контракта:**

### **Основные параметры:**
```solidity
name = "ALIEN Token"
symbol = "ALIEN"
decimals = 18
totalSupply = 1,000,000,000 * 10^18
```

### **События:**
```solidity
event Transfer(address indexed from, address indexed to, uint256 value);
event Approval(address indexed owner, address indexed spender, uint256 value);
event TokensMinted(address indexed to, uint256 amount);
event TokensBurned(address indexed from, uint256 amount);
event AddressBlacklisted(address indexed account, bool status);
```

## 🔧 **Функции токена:**

### **ERC-20 функции:**
- `transfer(address _to, uint256 _value)` — перевод токенов
- `approve(address _spender, uint256 _value)` — разрешение тратить
- `transferFrom(address _from, address _to, uint256 _value)` — перевод от имени

### **Функции владельца:**
- `mint(address _to, uint256 _amount)` — создать токены
- `burnFrom(address _from, uint256 _amount)` — сжечь токены с адреса
- `pause()` — приостановить переводы
- `unpause()` — возобновить переводы
- `setBlacklist(address _address, bool _status)` — черный список

### **Функции пользователей:**
- `burn(uint256 _amount)` — сжечь свои токены

### **Информационные функции:**
- `getContractInfo()` — информация о контракте
- `getBlacklistStatus(address _address)` — статус в черном списке

## 🛡️ **Безопасность:**

### **Проверки:**
- ✅ Проверка на нулевой адрес
- ✅ Проверка баланса
- ✅ Проверка разрешений
- ✅ Проверка черного списка
- ✅ Защита от переполнения (Solidity 0.8+)

### **Модификаторы:**
- `onlyOwner` — только владелец
- `whenNotPaused` — когда не приостановлено
- `nonReentrant` — защита от повторного входа

## 🚀 **Использование с ботом:**

### **Команды для токена V2:**
```bash
# Информация о токене
python bot.py token-info

# Создание токенов (владелец)
python bot.py mint --address 0x123 --amount 1000

# Сжигание токенов
python bot.py burn --amount 100

# Принудительное сжигание (владелец)
python bot.py burn-from --address 0x123 --amount 100

# Приостановка переводов (владелец)
python bot.py pause-token

# Возобновление переводов (владелец)
python bot.py unpause-token

# Черный список (владелец)
python bot.py blacklist --address 0x123 --status True
```

## 📊 **Сравнение версий:**

| Функция | ALIEN V1 | ALIEN V2 |
|---------|----------|----------|
| **ERC-20 стандарт** | ✅ | ✅ |
| **Базовые переводы** | ✅ | ✅ |
| **Mint функция** | ❌ | ✅ |
| **Burn функция** | ❌ | ✅ |
| **Pause функция** | ❌ | ✅ |
| **Blacklist** | ❌ | ✅ |
| **ReentrancyGuard** | ❌ | ✅ |
| **Ownable** | ❌ | ✅ |
| **События** | Базовые | Расширенные |

## 🔧 **Деплой:**

### **Требования:**
- Solidity 0.8.19+
- OpenZeppelin контракты
- Polygon сеть

### **Конструктор:**
```solidity
constructor(address initialOwner) Ownable(initialOwner)
```

### **Параметры деплоя:**
- **initialOwner** — адрес владельца контракта
- **totalSupply** — 1 миллиард токенов
- **decimals** — 18

## 📈 **Преимущества V2:**

### **Для владельца:**
- ✅ Полный контроль над токеном
- ✅ Возможность создания новых токенов
- ✅ Приостановка при аварийных ситуациях
- ✅ Управление черным списком

### **Для пользователей:**
- ✅ Безопасные переводы
- ✅ Возможность сжигания токенов
- ✅ Прозрачность операций
- ✅ Защита от мошенничества

### **Для экосистемы:**
- ✅ Совместимость с пресейлом
- ✅ Совместимость с биржами
- ✅ Стандартные ERC-20 функции
- ✅ Расширенные возможности

## 🎯 **Заключение:**

**ALIEN Token V2** — это улучшенная версия с полным набором функций безопасности и управления, готовая для серьезных проектов и интеграции с биржами.

---

🔥 **Готов к использованию!** 