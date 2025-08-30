# 🚀 Руководство по деплою ALIEN Token & Presale

Пошаговое руководство по деплою токена ALIEN_V2 и пресейла на Polygon.

## 📋 **Предварительные требования:**

### **1. Настройка окружения:**
```bash
# Установка Node.js и npm
# Установка Hardhat или Remix IDE
# Настройка MetaMask с Polygon сетью
```

### **2. Подготовка кошелька:**
- ✅ MetaMask с Polygon Mainnet
- ✅ Достаточно MATIC для деплоя (минимум 10 MATIC)
- ✅ Приватный ключ для подписи транзакций

## 🪐 **Шаг 1: Деплой токена ALIEN_V2**

### **Параметры деплоя:**
```solidity
// Конструктор ALIEN_V2
constructor(address initialOwner)

// Параметры:
initialOwner = "0xВашАдресКошелька"
```

### **Деплой через Remix:**
1. Откройте [Remix IDE](https://remix.ethereum.org/)
2. Создайте новый файл `ALIEN_V2.sol`
3. Скопируйте код из `ALIEN_V2.sol`
4. Установите компилятор Solidity 0.8.19+
5. Скомпилируйте контракт
6. Перейдите на вкладку "Deploy & Run"
7. Выберите сеть "Polygon Mainnet"
8. Подключите MetaMask
9. Введите адрес владельца в конструктор
10. Нажмите "Deploy"

### **Деплой через Hardhat:**
```javascript
// hardhat.config.js
module.exports = {
  networks: {
    polygon: {
      url: "https://polygon-rpc.com",
      accounts: ["0xВашПриватныйКлюч"]
    }
  }
};

// deploy.js
const ALIEN_V2 = await ethers.getContractFactory("ALIEN_V2");
const alienToken = await ALIEN_V2.deploy("0xВашАдресКошелька");
await alienToken.deployed();
console.log("ALIEN_V2 deployed to:", alienToken.address);
```

## 🚀 **Шаг 2: Деплой пресейла**

### **Параметры деплоя:**
```solidity
// Конструктор AlienPresale
constructor(
    address _token,
    uint256 _startTime,
    uint256 _endTime,
    uint256 _hardCap,
    uint256 _tokenPrice
)

// Пример параметров:
_token = "0xАдресALIEN_V2Токена"
_startTime = 1704067200  // 1 января 2024
_endTime = 1706745600    // 31 января 2024
_hardCap = 1000000000000000000000  // 1000 MATIC в Wei
_tokenPrice = 500000000000000  // 0.0005 MATIC за токен в Wei
```

### **Деплой через Remix:**
1. Создайте файл `AlienPresale.sol`
2. Скопируйте код из `AlienPresale.sol`
3. Скомпилируйте контракт
4. Введите параметры конструктора:
   - `_token`: адрес деплоенного ALIEN_V2
   - `_startTime`: время начала (Unix timestamp)
   - `_endTime`: время окончания (Unix timestamp)
   - `_hardCap`: максимальная сумма в Wei
   - `_tokenPrice`: цена токена в Wei
5. Нажмите "Deploy"

## 🔧 **Шаг 3: Настройка бота**

### **Обновление .env:**
```bash
# .env
RPC_URL=https://polygon-rpc.com
PRIVATE_KEY=ваш_приватный_ключ
WALLET_ADDRESS=0xваш_адрес_кошелька
PRESALE_ADDRESS=0xадрес_деплоенного_пресейла
TOKEN_ADDRESS=0xадрес_деплоенного_ALIEN_V2
```

### **Тестирование подключения:**
```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Проверьте подключение
python bot.py info
```

## 📊 **Шаг 4: Настройка параметров**

### **Параметры токена:**
```solidity
name = "ALIEN Token"
symbol = "ALIEN"
decimals = 18
totalSupply = 1,000,000,000 * 10^18
```

### **Параметры пресейла:**
```solidity
// Пример для 30-дневного пресейла
startTime = 1704067200  // 1 января 2024
endTime = 1706745600    // 31 января 2024
hardCap = 1000 ether    // 1000 MATIC
tokenPrice = 0.0005 ether // 0.0005 MATIC за токен
```

## 🧪 **Шаг 5: Тестирование**

### **Тест токена:**
```bash
# Проверка информации о токене
python bot.py token-info

# Проверка баланса
python bot.py balance

# Тест создания токенов (владелец)
python bot.py mint --address 0x123 --amount 1000
```

### **Тест пресейла:**
```bash
# Проверка информации о пресейле
python bot.py info

# Тест покупки токенов
python bot.py buy --amount 0.1

# Проверка прогресса
python bot.py stats
```

## 🔐 **Шаг 6: Безопасность**

### **Проверки после деплоя:**
- ✅ Контракты верифицированы на Polygonscan
- ✅ Адрес владельца правильный
- ✅ Параметры пресейла корректные
- ✅ Тестовые транзакции прошли успешно

### **Рекомендации:**
- 🔒 Храните приватный ключ в безопасном месте
- 🔒 Используйте мультисиг кошелек для больших сумм
- 🔒 Регулярно проверяйте баланс контрактов
- 🔒 Мониторьте активность через бота

## 📈 **Шаг 7: Запуск пресейла**

### **Подготовка к запуску:**
1. ✅ Токен деплоен и верифицирован
2. ✅ Пресейл деплоен и настроен
3. ✅ Бот подключен и протестирован
4. ✅ Параметры пресейла корректные

### **Команды для управления:**
```bash
# Запуск пресейла (автоматически по времени)
python bot.py info

# Мониторинг активности
python bot.py stats

# Управление паузой (при необходимости)
python bot.py pause --status True
python bot.py pause --status False

# Вывод средств после окончания
python bot.py withdraw --type funds
python bot.py withdraw --type tokens
```

## 🎯 **Полезные команды:**

### **Информация:**
```bash
python bot.py info          # Информация о пресейле
python bot.py token-info    # Информация о токене
python bot.py balance       # Балансы
python bot.py stats         # Статистика
```

### **Управление:**
```bash
python bot.py buy --amount 1.5     # Покупка токенов
python bot.py claim                # Получение токенов
python bot.py withdraw --type funds # Вывод средств
python bot.py pause --status True  # Приостановка
```

### **Владелец токена:**
```bash
python bot.py mint --address 0x123 --amount 1000
python bot.py burn --amount 100
python bot.py pause-token
python bot.py blacklist --address 0x123 --status True
```

## 🚀 **Готово к запуску!**

После выполнения всех шагов у вас будет:
- ✅ Деплоенный токен ALIEN_V2
- ✅ Деплоенный пресейл контракт
- ✅ Настроенный бот для управления
- ✅ Готовый к запуску пресейл

**Удачи с вашим проектом!** 🎉 