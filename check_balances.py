from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com'))

token_address = Web3.to_checksum_address('0xfb9da3c7d6500db33062eeb805863f80f4965e90')
sender = Web3.to_checksum_address('0x324eb0e51465d70c3d546bee1cf18f74a01e9924')
receiver = Web3.to_checksum_address('0xc55dc7dc4d6ddb16dc7e6a7ca74aca8293152126')

# Пример ABI функции balanceOf (сокращённый)
abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]

token_contract = w3.eth.contract(address=token_address, abi=abi)

def get_balance(addr):
    addr = Web3.to_checksum_address(addr)  # ещё раз на всякий случай
    return token_contract.functions.balanceOf(addr).call() / 1e18

print(f"Sender balance: {get_balance(sender)} ALIEN")
print(f"Receiver balance: {get_balance(receiver)} ALIEN")
