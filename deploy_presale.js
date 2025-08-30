const { ethers } = require("ethers");

async function main() {
    console.log("🚀 Начинаем деплой пресейла ALIEN...");
    
    // Параметры для деплоя
    const tokenAddress = "0xa8e302849DdF86769C026d9A2405e1cdA01ED992";
    const startTime = Math.floor(Date.now() / 1000) + 300; // Через 5 минут
    const endTime = Math.floor(Date.now() / 1000) + 1728000; // Через 20 дней
    const hardCap = ethers.parseEther("100"); // 100 MATIC
    const tokenPrice = ethers.parseEther("0.0005"); // 0.0005 MATIC за токен
    
    console.log("📋 Параметры деплоя:");
    console.log(`Токен: ${tokenAddress}`);
    console.log(`Начало: ${new Date(startTime * 1000).toLocaleString()}`);
    console.log(`Окончание: ${new Date(endTime * 1000).toLocaleString()}`);
    console.log(`Hardcap: ${ethers.formatEther(hardCap)} MATIC`);
    console.log(`Цена токена: ${ethers.formatEther(tokenPrice)} MATIC`);
    
    // Получаем Hardhat ethers для деплоя
    const hre = require("hardhat");
    const hardhatEthers = hre.ethers;
    
    // Деплой контракта
    const AlienPresale = await hardhatEthers.getContractFactory("AlienPresale");
    const presale = await AlienPresale.deploy(
        tokenAddress,
        startTime,
        endTime,
        hardCap,
        tokenPrice
    );
    
    console.log("⏳ Ожидаем деплой...");
    await presale.waitForDeployment();
    
    const presaleAddress = await presale.getAddress();
    console.log("✅ Пресейл успешно деплоен!");
    console.log(`📍 Адрес: ${presaleAddress}`);
    console.log(`🔗 Polygonscan: https://polygonscan.com/address/${presaleAddress}`);
    
    // Проверяем параметры
    console.log("\n📊 Проверка параметров:");
    const deployedStartTime = await presale.startTime();
    const deployedEndTime = await presale.endTime();
    const deployedHardCap = await presale.hardCap();
    const deployedTokenPrice = await presale.tokenPrice();
    
    console.log(`Начало: ${new Date(Number(deployedStartTime) * 1000).toLocaleString()}`);
    console.log(`Окончание: ${new Date(Number(deployedEndTime) * 1000).toLocaleString()}`);
    console.log(`Hardcap: ${ethers.formatEther(deployedHardCap)} MATIC`);
    console.log(`Цена токена: ${ethers.formatEther(deployedTokenPrice)} MATIC`);
    
    console.log("\n🎯 Следующие шаги:");
    console.log("1. Верифицируйте контракт на Polygonscan");
    console.log("2. Обновите PRESALE_ADDRESS в .env файле");
    console.log("3. Протестируйте через бота: python bot.py info");
    
    return presaleAddress;
}

main()
    .then((address) => {
        console.log(`\n🚀 Деплой завершен! Адрес: ${address}`);
        process.exit(0);
    })
    .catch((error) => {
        console.error("❌ Ошибка деплоя:", error);
        process.exit(1);
    }); 