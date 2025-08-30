# 🚀 ALIEN Presale - Контракт для продажи токенов

Улучшенный контракт пресейла для токена ALIEN с полным набором функций безопасности и управления.

## 🎯 **Основные функции:**

### ✅ **Для покупателей:**
- **buyTokens()** — покупка токенов за MATIC
- **claimTokens()** — получение купленных токенов после окончания

### ✅ **Для владельца:**
- **withdrawFunds()** — вывод собранных средств
- **withdrawUnsoldTokens()** — вывод непроданных токенов
- **pausePresale()** — приостановка/возобновление пресейла
- **updatePresaleTimes()** — обновление времени начала/окончания
- **updateHardCap()** — обновление максимальной суммы
- **updateTokenPrice()** — обновление цены токена

## 📋 **Структура контракта:**

### **Основные параметры:**
```solidity
IERC20 public token;           // Адрес токена ALIEN
uint256 public startTime;      // Время начала пресейла
uint256 public endTime;        // Время окончания пресейла
uint256 public hardCap;        // Максимальная сумма сбора
uint256 public totalRaised;    // Собранная сумма
uint256 public tokenPrice;     // Цена токена в Wei
```

### **События:**
```solidity
event TokensPurchased(address indexed buyer, uint256 amount, uint256 tokens);
event TokensClaimed(address indexed buyer, uint256 tokens);
event FundsWithdrawn(address indexed owner, uint256 amount);
event UnsoldTokensWithdrawn(address indexed owner, uint256 tokens);
event PresalePaused(address indexed owner, bool status);
```

## 🔧 **Функции контракта:**

### **Основные функции:**
- `buyTokens()` — покупка токенов (payable)
- `claimTokens()` — получение токенов после пресейла
- `getPresaleInfo()` — информация о пресейле
- `getUserInfo(address _user)` — информация о пользователе
- `getPresaleProgress()` — прогресс пресейла

### **Функции владельца:**
- `withdrawFunds()` — вывод собранных средств
- `withdrawUnsoldTokens()` — вывод непроданных токенов
- `pausePresale(bool _status)` — приостановка/возобновление
- `updatePresaleTimes(uint256 _startTime, uint256 _endTime)` — обновление времени
- `updateHardCap(uint256 _hardCap)` — обновление hardcap
- `updateTokenPrice(uint256 _tokenPrice)` — обновление цены

## 🛡️ **Безопасность:**

### **Проверки:**
- ✅ Проверка времени начала/окончания
- ✅ Проверка hardcap
- ✅ Проверка паузы
- ✅ Защита от повторного входа
- ✅ Проверка владельца для админ функций

### **Модификаторы:**
- `onlyOwner` — только владелец
- `presaleActive` — пресейл активен
- `nonReentrant` — защита от повторного входа

## 🚀 **Использование с ботом:**

### **Команды для пресейла:**
```bash
# Информация о пресейле
python bot.py info

# Покупка токенов
python bot.py buy --amount 1.5

# Получение токенов
python bot.py claim

# Вывод средств (владелец)
python bot.py withdraw --type funds

# Вывод непроданных токенов (владелец)
python bot.py withdraw --type tokens

# Приостановка пресейла (владелец)
python bot.py pause --status True
```

## 📊 **Примеры параметров деплоя:**

### **Для тестирования:**
```solidity
_token = "0xАдресТокенаALIEN"
_startTime = block.timestamp + 3600  // Через 1 час
_endTime = block.timestamp + 86400    // Через 24 часа
_hardCap = 100 ether                 // 100 MATIC
_tokenPrice = 0.001 ether            // 0.001 MATIC за токен
```

### **Для продакшена:**
```solidity
_token = "0xАдресТокенаALIEN"
_startTime = 1704067200              // 1 января 2024
_endTime = 1706745600                // 31 января 2024
_hardCap = 1000 ether                // 1000 MATIC
_tokenPrice = 0.0005 ether           // 0.0005 MATIC за токен
```

## 🔧 **Деплой:**

### **Требования:**
- Solidity 0.8.19+
- OpenZeppelin контракты
- Polygon сеть
- Деплой токена ALIEN

### **Конструктор:**
```solidity
constructor(
    address _token,
    uint256 _startTime,
    uint256 _endTime,
    uint256 _hardCap,
    uint256 _tokenPrice
)
```

### **Параметры деплоя:**
- **_token** — адрес токена ALIEN
- **_startTime** — время начала (Unix timestamp)
- **_endTime** — время окончания (Unix timestamp)
- **_hardCap** — максимальная сумма сбора (в Wei)
- **_tokenPrice** — цена токена (в Wei)

## 📈 **Преимущества:**

### **Для покупателей:**
- ✅ Прозрачная покупка токенов
- ✅ Автоматический расчет количества токенов
- ✅ Безопасное получение токенов после пресейла
- ✅ Защита от мошенничества

### **Для владельца:**
- ✅ Полный контроль над пресейлом
- ✅ Возможность обновления параметров
- ✅ Безопасный вывод средств
- ✅ Управление паузой

### **Для экосистемы:**
- ✅ Совместимость с любым ERC-20 токеном
- ✅ Стандартные функции пресейла
- ✅ Расширенные возможности управления
- ✅ Безопасность на уровне контракта

## 🎯 **Интеграция с ALIEN_V2:**

### **Совместимость:**
- ✅ Работает с любым ERC-20 токеном
- ✅ Полная совместимость с ALIEN_V2
- ✅ Поддержка всех функций токена

### **Рекомендуемая последовательность:**
1. Деплой токена ALIEN_V2
2. Деплой пресейла с адресом токена
3. Настройка параметров пресейла
4. Запуск пресейла
5. Управление через бота

## 🚀 **Заключение:**

**AlienPresale** — это профессиональный контракт пресейла с полным набором функций безопасности и управления, готовый для серьезных проектов.

---

🔥 **Готов к деплою и использованию!** 