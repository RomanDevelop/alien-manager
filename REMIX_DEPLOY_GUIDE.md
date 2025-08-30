# 🚀 Деплой пресейла ALIEN через Remix

## ✅ **Статус:**
- ✅ Старый пресейл удален из конфигурации
- ✅ Ваши токены в безопасности (800M ALIEN)
- ✅ Готов к новому деплою через Remix

## 📋 **Инструкции для деплоя через Remix:**

### **1. Откройте Remix IDE:**
https://remix.ethereum.org/

### **2. Создайте новый файл:**
- Нажмите "+" в файловом менеджере
- Назовите файл `AlienPresale.sol`

### **3. Вставьте код пресейла:**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AlienPresale is Ownable, Pausable, ReentrancyGuard {
    IERC20 public token;

    uint256 public startTime;
    uint256 public endTime;
    uint256 public hardCap;
    uint256 public totalRaised;
    uint256 public tokenPrice;

    mapping(address => uint256) public contributions;
    mapping(address => uint256) public claimableTokens;

    event TokensPurchased(
        address indexed buyer,
        uint256 amount,
        uint256 tokens
    );
    event TokensClaimed(address indexed buyer, uint256 tokens);
    event FundsWithdrawn(address indexed owner, uint256 amount);
    event UnsoldTokensWithdrawn(address indexed owner, uint256 tokens);
    event PresalePaused(address indexed owner, bool status);

    constructor(
        address _token,
        uint256 _startTime,
        uint256 _endTime,
        uint256 _hardCap,
        uint256 _tokenPrice
    ) {
        require(_token != address(0), "Invalid token address");
        require(_startTime > block.timestamp, "Start time must be in future");
        require(_endTime > _startTime, "End time must be after start time");
        require(_hardCap > 0, "Hard cap must be greater than 0");
        require(_tokenPrice > 0, "Token price must be greater than 0");

        token = IERC20(_token);
        startTime = _startTime;
        endTime = _endTime;
        hardCap = _hardCap;
        tokenPrice = _tokenPrice;
    }

    modifier presaleActive() {
        require(block.timestamp >= startTime, "Presale not started");
        require(block.timestamp <= endTime, "Presale ended");
        require(!paused(), "Presale paused");
        require(totalRaised < hardCap, "Hard cap reached");
        _;
    }

    function buyTokens() public payable presaleActive nonReentrant {
        require(msg.value > 0, "Amount must be greater than 0");
        require(totalRaised + msg.value <= hardCap, "Exceeds hard cap");

        uint256 tokensToReceive = (msg.value * 10 ** 18) / tokenPrice;
        require(tokensToReceive > 0, "No tokens to receive");

        contributions[msg.sender] += msg.value;
        claimableTokens[msg.sender] += tokensToReceive;
        totalRaised += msg.value;

        emit TokensPurchased(msg.sender, msg.value, tokensToReceive);
    }

    function claimTokens() external nonReentrant {
        require(block.timestamp > endTime, "Presale not ended");
        require(claimableTokens[msg.sender] > 0, "No tokens to claim");

        uint256 tokensToClaim = claimableTokens[msg.sender];
        claimableTokens[msg.sender] = 0;

        require(
            token.transfer(msg.sender, tokensToClaim),
            "Token transfer failed"
        );

        emit TokensClaimed(msg.sender, tokensToClaim);
    }

    function withdrawFunds() external onlyOwner {
        require(block.timestamp > endTime, "Presale not ended");
        require(totalRaised > 0, "No funds to withdraw");

        uint256 amount = totalRaised;
        totalRaised = 0;

        (bool success, ) = payable(owner()).call{value: amount}("");
        require(success, "Transfer failed");

        emit FundsWithdrawn(owner(), amount);
    }

    function withdrawUnsoldTokens() external onlyOwner {
        require(block.timestamp > endTime, "Presale not ended");

        uint256 contractBalance = token.balanceOf(address(this));
        require(contractBalance > 0, "No unsold tokens");

        require(
            token.transfer(owner(), contractBalance),
            "Token transfer failed"
        );

        emit UnsoldTokensWithdrawn(owner(), contractBalance);
    }

    function pausePresale(bool _status) external onlyOwner {
        if (_status) {
            _pause();
        } else {
            _unpause();
        }

        emit PresalePaused(owner(), _status);
    }

    function updatePresaleTimes(
        uint256 _startTime,
        uint256 _endTime
    ) external onlyOwner {
        require(_startTime > block.timestamp, "Start time must be in future");
        require(_endTime > _startTime, "End time must be after start time");

        startTime = _startTime;
        endTime = _endTime;
    }

    function updateHardCap(uint256 _hardCap) external onlyOwner {
        require(
            _hardCap > totalRaised,
            "Hard cap must be greater than total raised"
        );
        hardCap = _hardCap;
    }

    function updateTokenPrice(uint256 _tokenPrice) external onlyOwner {
        require(_tokenPrice > 0, "Token price must be greater than 0");
        tokenPrice = _tokenPrice;
    }

    function getPresaleInfo()
        external
        view
        returns (
            uint256 _startTime,
            uint256 _endTime,
            uint256 _hardCap,
            uint256 _totalRaised,
            uint256 _tokenPrice,
            bool _paused,
            bool _isActive
        )
    {
        bool isActive = block.timestamp >= startTime &&
            block.timestamp <= endTime &&
            !paused() &&
            totalRaised < hardCap;

        return (
            startTime,
            endTime,
            hardCap,
            totalRaised,
            tokenPrice,
            paused(),
            isActive
        );
    }

    function getUserInfo(
        address _user
    ) external view returns (uint256 _contribution, uint256 _claimableTokens) {
        return (contributions[_user], claimableTokens[_user]);
    }

    function getPresaleProgress()
        external
        view
        returns (
            uint256 _totalRaised,
            uint256 _hardCap,
            uint256 _remaining,
            uint256 _progressPercent
        )
    {
        uint256 remaining = hardCap > totalRaised ? hardCap - totalRaised : 0;
        uint256 progressPercent = hardCap > 0
            ? (totalRaised * 100) / hardCap
            : 0;

        return (totalRaised, hardCap, remaining, progressPercent);
    }

    receive() external payable {
        buyTokens();
    }

    fallback() external payable {
        buyTokens();
    }
}
```

### **4. Настройте компиляцию:**
- Перейдите в "Solidity Compiler"
- **Compiler:** 0.8.19
- **Optimization:** Enabled
- **Runs:** 200

### **5. Скомпилируйте контракт**

### **6. Деплой:**
- Перейдите в "Deploy & Run Transactions"
- **Environment:** Injected Provider - MetaMask
- **Network:** Polygon
- **Contract:** AlienPresale
- **Constructor Parameters:**
  ```
  _token: 0xa8e302849DdF86769C026d9A2405e1cdA01ED992
  _startTime: [текущее время + 5 минут в секундах]
  _endTime: [текущее время + 20 дней в секундах]
  _hardCap: 100000000000000000000 (100 MATIC в wei)
  _tokenPrice: 500000000000000 (0.0005 MATIC в wei)
  ```

### **7. После деплоя:**
1. Скопируйте адрес нового пресейла
2. Обновите .env файл:
   ```bash
   echo "PRESALE_ADDRESS=[НОВЫЙ_АДРЕС]" >> .env
   ```
3. Протестируйте бота:
   ```bash
   python bot.py info
   ```

## 🎯 **Преимущества деплоя через Remix:**
- ✅ Простая верификация на Polygonscan
- ✅ Стандартные параметры компиляции
- ✅ Автоматическое копирование кода для верификации
- ✅ Прозрачность и доверие

## 📊 **Текущие активы:**
- 💰 **MATIC:** 24.22 MATIC
- 🎁 **ALIEN:** 800M ALIEN токенов
- 🔧 **Готовность:** 100% для нового деплоя

**Готовы к деплою через Remix!** 🚀 