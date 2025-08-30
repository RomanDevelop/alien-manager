#!/usr/bin/env python3
import json
import os
from datetime import datetime
import time
from web3 import Web3
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from dotenv import load_dotenv

# Load environment early
load_dotenv()

# Try to import RPC config; proceed without RPC if unavailable
USE_RPC = True
try:
    from config import w3
    if not w3.is_connected():
        USE_RPC = False
except Exception:
    w3 = None  # type: ignore[assignment]
    USE_RPC = False


def load_presale_contract(presale_address: str):
    artifact_path = os.path.join(
        "artifacts", "contracts", "AlienPresale.sol", "AlienPresale.json"
    )
    if not os.path.exists(artifact_path):
        raise FileNotFoundError(
            f"Artifact not found at {artifact_path}. Please compile contracts first."
        )

    with open(artifact_path, "r") as f:
        abi = json.load(f)["abi"]
    if not USE_RPC:
        # No RPC: return abi only; caller must use Polygonscan path
        return {"abi": abi}
    return w3.eth.contract(address=Web3.to_checksum_address(presale_address), abi=abi)


def find_block_by_timestamp(target_ts: int, search_window: int = 5_000) -> int:
    """Binary search the block number closest to target_ts (>= target_ts)."""
    if not USE_RPC:
        raise RuntimeError("RPC not available")
    low = 0
    high = w3.eth.block_number

    # Quick narrowing using step jumps if network allows
    while low < high:
        mid = (low + high) // 2
        blk = w3.eth.get_block(mid)
        blk_ts = blk.timestamp
        if blk_ts < target_ts:
            low = mid + 1
        else:
            high = mid
    return low


def main():
    presale_address = os.getenv(
        "PRESALE_ADDRESS", "0x2699838c090346Eaf93F96069B56B3637828dFAC"
    )

    contract = load_presale_contract(presale_address)

    # Determine latest block
    if USE_RPC:
        latest_block = w3.eth.block_number
    else:
        api_key_probe = os.getenv("POLYGONSCAN_API_KEY") or os.getenv("ETHERSCAN_API_KEY")
        base_url = os.getenv("POLYGONSCAN_API", "https://api.polygonscan.com/api")
        if not api_key_probe:
            raise SystemExit("RPC unavailable and POLYGONSCAN_API_KEY not set in .env")
        url = f"{base_url}?{urlencode({'module':'proxy','action':'eth_blockNumber','apikey':api_key_probe})}"
        with urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        latest_block = int(data.get("result", "0x0"), 16)
    # Presale start block can be provided to avoid heavy RPC usage
    env_start_block = os.getenv("PRESALE_START_BLOCK")
    if env_start_block:
        from_block = int(env_start_block)
    else:
        # Try to start from presale start block to minimize range
        if USE_RPC:
            try:
                start_ts = contract.functions.startTime().call()
                approx_start_block = find_block_by_timestamp(int(start_ts))
                from_block = max(0, approx_start_block - 500)
            except Exception:
                default_span = int(os.getenv("FROM_BLOCKS", "2000000"))
                from_block = max(0, latest_block - default_span)
        else:
            # Without RPC, use a conservative 200k-block window by default
            default_span = int(os.getenv("FROM_BLOCKS", "200000"))
            from_block = max(0, latest_block - default_span)
    to_block = latest_block

    # Page through block ranges to avoid RPC "Block range is too large"
    window_size = int(os.getenv("WINDOW_SIZE", "1000"))
    logs_collected = []
    cur_from = from_block
    rpc_failed = False
    retry_limit = 3
    while USE_RPC and cur_from <= to_block:
        cur_to = min(cur_from + window_size, to_block)
        try:
            part = contract.events.TokensPurchased().get_logs(
                from_block=cur_from, to_block=cur_to
            )
            logs_collected.extend(part)
            cur_from = cur_to + 1
        except Exception as e:
            msg = str(e)
            # If provider rate-limited or large range, fallback to Polygonscan later
            if ("Too many requests" in msg) or ("-32090" in msg):
                if retry_limit > 0:
                    retry_limit -= 1
                    time.sleep(15)
                    continue
                rpc_failed = True
                break
            if ("Block range is too large" in msg) or ("-32062" in msg):
                # shrink window and retry
                if window_size > 100:
                    window_size = max(100, window_size // 2)
                    continue
                # as a last resort, scan per-block in this small range
                for b in range(cur_from, cur_to + 1):
                    try:
                        part_b = contract.events.TokensPurchased().get_logs(
                            from_block=b, to_block=b
                        )
                        logs_collected.extend(part_b)
                    except Exception:
                        pass
                cur_from = cur_to + 1
                continue
            # If other error and window can still be reduced, reduce window and retry
            if window_size > 200:
                window_size = max(200, window_size // 2)
                continue
            else:
                raise

    # If RPC failed or returned nothing, try Polygonscan API
    if rpc_failed or not logs_collected or not USE_RPC:
        api_key = os.getenv("POLYGONSCAN_API_KEY") or os.getenv("ETHERSCAN_API_KEY")
        if not api_key:
            raise SystemExit("RPC limited and POLYGONSCAN_API_KEY not set in .env")
        topic0 = Web3.keccak(text="TokensPurchased(address,uint256,uint256)").hex()
        base_url = os.getenv("POLYGONSCAN_API", "https://api.polygonscan.com/api")
        step = int(os.getenv("SCAN_WINDOW", "50000"))
        scan_from = from_block
        while scan_from <= to_block:
            scan_to = min(scan_from + step, to_block)
            q = {
                "module": "logs",
                "action": "getLogs",
                "fromBlock": scan_from,
                "toBlock": scan_to,
                "address": Web3.to_checksum_address(presale_address),
                "topic0": topic0,
                "apikey": api_key,
            }
            url = f"{base_url}?{urlencode(q)}"
            try:
                with urlopen(url, timeout=30) as resp:
                    data = json.loads(resp.read())
                if data.get("status") == "1":
                    for it in data.get("result", []):
                        topics = it.get("topics", [])
                        if len(topics) < 2:
                            continue
                        buyer_hex = topics[1]
                        buyer = "0x" + buyer_hex[-40:]
                        payload = it.get("data", "0x")[2:]
                        if len(payload) < 128:
                            continue
                        amount_wei = int(payload[0:64], 16)
                        tokens = int(payload[64:128], 16)
                        # build a minimal object similar to web3 event
                        logs_collected.append(
                            {
                                "args": {
                                    "buyer": Web3.to_checksum_address(buyer),
                                    "amount": amount_wei,
                                    "tokens": tokens,
                                },
                                "transactionHash": it["transactionHash"],
                                "blockNumber": int(it["blockNumber"], 16),
                            }
                        )
                elif data.get("status") == "0" and data.get("message") == "No records found":
                    pass
                else:
                    # Respect API rate limit: small sleep could be added, but avoid extra deps
                    raise SystemExit(f"Polygonscan error: {data}")
            except (HTTPError, URLError, TimeoutError) as e:
                raise SystemExit(f"Polygonscan request failed: {e}")
            scan_from = scan_to + 1

    print(
        f"Purchases found: {len(logs_collected)} (blocks {from_block}-{to_block}) for presale {presale_address}"
    )

    buyers_to_matic = {}
    total_wei = 0

    for ev in logs_collected:
        args = ev["args"]
        buyer = args["buyer"]
        amount_wei = int(args["amount"])  # MATIC in wei sent
        tokens = int(args["tokens"])  # token amount (18 decimals)
        total_wei += amount_wei
        buyers_to_matic[buyer] = buyers_to_matic.get(buyer, 0) + amount_wei

        if USE_RPC:
            block = w3.eth.get_block(ev["blockNumber"])  # type: ignore[index]
            ts = datetime.fromtimestamp(block.timestamp)
        else:
            # Query timestamp via Polygonscan proxy
            api_key = os.getenv("POLYGONSCAN_API_KEY") or os.getenv("ETHERSCAN_API_KEY")
            base_url = os.getenv("POLYGONSCAN_API", "https://api.polygonscan.com/api")
            blk_hex = hex(ev["blockNumber"])
            url = f"{base_url}?{urlencode({'module':'proxy','action':'eth_getBlockByNumber','tag':blk_hex,'boolean':'false','apikey':api_key})}"
            with urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read())
            ts_hex = data.get("result", {}).get("timestamp", "0x0")
            ts = datetime.fromtimestamp(int(ts_hex, 16))
        print(
            f"- {buyer} | amount: {Web3.from_wei(amount_wei,'ether')} MATIC | tokens: {tokens/10**18:.0f} | tx: {ev['transactionHash'] if isinstance(ev['transactionHash'], str) else ev['transactionHash'].hex()} | time: {ts}"
        )

    print("\nTotals:")
    print(f"- total MATIC: {Web3.from_wei(total_wei,'ether')}")
    print(f"- unique buyers: {len(buyers_to_matic)}")

    if buyers_to_matic:
        print("- buyers:")
        for addr, amt in buyers_to_matic.items():
            print(f"  {addr}: {Web3.from_wei(amt,'ether')} MATIC")


if __name__ == "__main__":
    main()


