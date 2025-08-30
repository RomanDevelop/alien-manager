#!/usr/bin/env python3
import os
import json
from decimal import Decimal, getcontext
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from dotenv import load_dotenv

getcontext().prec = 50

load_dotenv()

TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS", "0xa8e302849DdF86769C026d9A2405e1cdA01ED992")
API_KEY = os.getenv("POLYGONSCAN_API_KEY") or os.getenv("ETHERSCAN_API_KEY")
API_BASE = os.getenv("POLYGONSCAN_API", "https://api.polygonscan.com/api")
TOP_N = int(os.getenv("TOP_N", "20"))
DECIMALS = int(os.getenv("TOKEN_DECIMALS", "18"))


def api_get(params: dict):
    if not API_KEY:
        raise SystemExit("POLYGONSCAN_API_KEY not set in .env")
    params = {**params, "apikey": API_KEY}
    url = f"{API_BASE}?{urlencode(params)}"
    with urlopen(url, timeout=30) as resp:
        return json.loads(resp.read())


def try_tokenholderlist(contract: str):
    # Not all providers expose this endpoint; try and fall back if needed
    try:
        data = api_get(
            {
                "module": "token",
                "action": "tokenholderlist",
                "contractaddress": contract,
                "page": 1,
                "offset": 200,  # top 200
            }
        )
        if data.get("status") == "1":
            return data.get("result", [])
        return None
    except Exception:
        return None


def get_total_supply(contract: str) -> Decimal:
    data = api_get({"module": "stats", "action": "tokensupply", "contractaddress": contract})
    if data.get("status") == "1":
        return Decimal(data["result"]) / (Decimal(10) ** DECIMALS)
    # Fallback zero if not provided
    return Decimal(0)


def build_balances_from_transfers(contract: str):
    balances: dict[str, Decimal] = {}
    page = 1
    offset = int(os.getenv("TX_OFFSET", "10000"))
    while True:
        data = api_get(
            {
                "module": "account",
                "action": "tokentx",
                "contractaddress": contract,
                "page": page,
                "offset": offset,
                "sort": "asc",
            }
        )
        if data.get("status") != "1":
            # no more records
            break
        txs = data.get("result", [])
        if not txs:
            break
        for tx in txs:
            frm = tx["from"].lower()
            to = tx["to"].lower()
            value = Decimal(tx["value"]) / (Decimal(10) ** DECIMALS)
            if value == 0:
                continue
            if frm != "0x0000000000000000000000000000000000000000":
                balances[frm] = balances.get(frm, Decimal(0)) - value
            balances[to] = balances.get(to, Decimal(0)) + value
        if len(txs) < offset:
            break
        page += 1
    # Clean near-zero
    balances = {a: b for a, b in balances.items() if b > Decimal(0)}
    return balances


def main():
    contract = TOKEN_ADDRESS
    print(f"Token: {contract}")

    total_supply = get_total_supply(contract)

    holders = try_tokenholderlist(contract)
    if holders:
        rows = []
        for h in holders:
            addr = h.get("HolderAddress") or h.get("address")
            bal_raw = h.get("TokenHolderQuantity") or h.get("balance")
            try:
                bal = Decimal(bal_raw) / (Decimal(10) ** DECIMALS)
            except Exception:
                bal = Decimal(0)
            rows.append((addr, bal))
    else:
        print("tokenholderlist unavailable; building from transfers (tokentx)...")
        balances = build_balances_from_transfers(contract)
        rows = list(balances.items())

    rows.sort(key=lambda x: x[1], reverse=True)
    top = rows[:TOP_N]

    total_known = sum(b for _, b in rows)
    print(f"Total supply (reported): {total_supply:,.0f}")
    print(f"Holders discovered: {len(rows)} | Sum balances: {total_known:,.0f}")
    print(f"Top {len(top)} holders:")
    for i, (addr, bal) in enumerate(top, 1):
        pct = (bal / total_supply * 100) if total_supply > 0 else Decimal(0)
        print(f"{i:>2}. {addr} | {bal:,.0f} ALIEN | {pct:.2f}%")


if __name__ == "__main__":
    main()


