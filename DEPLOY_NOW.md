# 🚀 Деплой пресейла СЕЙЧАС на 20 дней

## 📋 **Параметры для немедленного деплоя:**

### **Основные параметры:**
```solidity
_token = "0xa8e302849DdF86769C026d9A2405e1cdA01ED992"
_startTime = block.timestamp + 300     // Через 5 минут
_endTime = block.timestamp + 1728000   // Через 20 дней (1,728,000 секунд)
_hardCap = 100 ether                   // 100 MATIC
_tokenPrice = 0.0005 ether             // 0.0005 MATIC за токен
```

### **В Wei (для Remix):**
```solidity
_token = "0xa8e302849DdF86769C026d9A2405e1cdA01ED992"
_startTime = block.timestamp + 300
_endTime = block.timestamp + 1728000
_hardCap = 100000000000000000000      // 100 MATIC в Wei
_tokenPrice = 500000000000000          // 0.0005 MATIC в Wei
```

## 📊 **Расчеты:**

### **Время:**
- **Начало:** Через 5 минут после деплоя
- **Окончание:** Через 20 дней после деплоя
- **Длительность:** 20 дней

### **Финансы:**
- **Hardcap:** 100 MATIC
- **Цена токена:** 0.0005 MATIC за токен
- **Токенов для продажи:** 200,000,000 ALIEN (20% от supply)

### **Расчет токенов:**
```
Токены = 100 MATIC / 0.0005 MATIC * 10^18 = 200,000,000 ALIEN
Процент от supply = 200,000,000 / 1,000,000,000 * 100 = 20%
```

## 🔧 **Инструкции по деплою:**

### **Через Remix IDE:**
1. Откройте [Remix IDE](https://remix.ethereum.org/)
2. Создайте файл `AlienPresale.sol`
3. Скопируйте код из `AlienPresale.sol`
4. Скомпилируйте с Solidity 0.8.19+
5. Перейдите на "Deploy & Run"
6. Выберите сеть "Polygon Mainnet"
7. Подключите MetaMask
8. Введите параметры:
   - `_token`: `0xa8e302849DdF86769C026d9A2405e1cdA01ED992`
   - `_startTime`: `block.timestamp + 300`
   - `_endTime`: `block.timestamp + 1728000`
   - `_hardCap`: `100000000000000000000`
   - `_tokenPrice`: `500000000000000`
9. Нажмите "Deploy"

### **Через Hardhat:**
```javascript
const AlienPresale = await ethers.getContractFactory("AlienPresale");
const presale = await AlienPresale.deploy(
    "0xa8e302849DdF86769C026d9A2405e1cdA01ED992", // токен
    Math.floor(Date.now() / 1000) + 300,           // startTime (через 5 минут)
    Math.floor(Date.now() / 1000) + 1728000,       // endTime (через 20 дней)
    ethers.utils.parseEther("100"),                 // hardCap
    ethers.utils.parseEther("0.0005")              // tokenPrice
);
await presale.deployed();
console.log("Presale deployed to:", presale.address);
```

## 🎯 **После деплоя:**

### **1. Верификация:**
- Скопируйте адрес деплоенного контракта
- Верифицируйте на [Polygonscan](https://polygonscan.com/)
- Используйте код из `AlienPresale.sol`

### **2. Настройка бота:**
```bash
# Обновите .env файл
PRESALE_ADDRESS=0xНовыйАдресПресейла

# Протестируйте подключение
python bot.py info
```

### **3. Тестирование:**
```bash
# Проверка информации о пресейле
python bot.py info

# Тест покупки (если нужно)
python bot.py buy --amount 0.1

# Проверка прогресса
python bot.py stats
```

## 📈 **Ожидаемые результаты:**

### **Параметры пресейла:**
- **Длительность:** 20 дней
- **Цель:** 100 MATIC
- **Цена:** 0.0005 MATIC за токен
- **Токены:** 200,000,000 ALIEN (20% от supply)

### **Преимущества:**
- ✅ Достаточно времени для маркетинга
- ✅ Реалистичная цена токена
- ✅ Умеренный hardcap
- ✅ Хороший процент токенов для продажи

## 🚀 **Готово к деплою!**

**Все параметры настроены для немедленного деплоя пресейла на 20 дней!**

---

**Удачи с пресейлом!** 🎉 