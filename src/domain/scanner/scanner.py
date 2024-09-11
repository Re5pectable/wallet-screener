from asyncio import sleep
from collections import defaultdict
from pprint import pprint
from enum import StrEnum

from sqlalchemy import select

from ...adapters.db.engine import Session
from ...adapters.db.models import NetworkOrm, TransactionOrm
from ...adapters.uniswap import Uniswap

transfer_topic = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"


class UniswapV2Router:
    contract: str = '0x7a250d5630b4cf539739df2c5dacb4c659f2488d'
    methods: dict = {
        "0x2f100e4a": "swapETHForExactTokens",
        "0x7ff36ab5": "swapExactETHForTokens",
        "0x18cbafe5": "swapExactTokensForETH",
        "0x4a25d94a": "swapTokensForExactETH",
        "0x8803dbee": "swapTokensForExactTokens",
        "0x38ed1739": "swapExactTokensForTokens",
        "0xb6f9de95": "swapExactETHForTokensSupportingFeeOnTransferTokens",
        "0x791ac947": "swapExactTokensForETHSupportingFeeOnTransferTokens",
        "0x5c11d795": "swapExactTokensForTokensSupportingFeeOnTransferTokens",
    }


class UniswapUniversalRouter:
    contract: str = '0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad'
    methods: dict = {
        "0x3593564c": "executeDeadline",
        "0x24856bc3": "execute",
    }


async def __get_network(name: str) -> NetworkOrm | None:
    async with Session() as session:
        stmt = select(NetworkOrm).where(NetworkOrm.name == name)
        q = await session.execute(stmt)
        return q.scalars().first()


async def __get_block(uniswap: Uniswap):
    data = await uniswap.blockNumber()
    return int(data, 0)


async def __get_logs(uniswap: Uniswap, from_block: int, to_block: int):
    logs = await uniswap.get_swaps("v2", hex(from_block), hex(to_block))
    if not logs:
        return

    txns = {}
    for log in logs:
        if log["transactionHash"] in txns.keys():
            continue
        txns[log["transactionHash"]] = int(log["blockNumber"], 0)

    async with Session() as session:
        objs = [
            TransactionOrm(txn_hash=hash_, block_number=block_number)
            for hash_, block_number in txns.items()
        ]
        session.add_all(objs)
        await session.commit()

    for obj in objs:
        await __get_swap(uniswap, obj.txn_hash)


async def __get_swap(uniswap: Uniswap, txn_hash: str):
    transaction = await uniswap.getTransactionByHash(txn_hash)

    if not transaction:
        return

    sender = transaction["from"]
    to = transaction["to"]
    if to not in [UniswapV2Router.contract, UniswapUniversalRouter.contract]:
        return print("wrong to", to, txn_hash)

    method_id = transaction["input"][:10]

    if method_id in UniswapUniversalRouter.methods.keys():
        print(txn_hash, 'UniswapUniversalRouter', UniswapUniversalRouter.methods[method_id])
    elif method_id in UniswapV2Router.methods.keys():
        print(txn_hash, 'UniswapV2Router', UniswapV2Router.methods[method_id])
    else:
        print(txn_hash, "unkonwn method")
    return

    receipt = await uniswap.getReceipt(txn_hash)
    logs: list[dict] = receipt["logs"]
    sender_sent = {}
    sender_received = {}
    for log in logs:
        if not log["topics"]:
            continue
        if log["topics"][0] != transfer_topic:
            continue
        if sender[2:] in log["topics"][1]:
            sender_sent[log["address"]] = sender_sent.get(log["address"], 0) + int(
                log["data"], 0
            )
        if sender[2:] in log["topics"][2]:
            sender_received[log["address"]] = sender_received.get(
                log["address"], 0
            ) + int(log["data"], 0)

    print(f"Transaction: {txn_hash}")
    print(
        "-----------------------------------------------------------------------------------------"
    )
    print("Sender send:", sender_sent)
    print("Sender received:", sender_received)
    print()


async def main():
    network = await __get_network("Ethereum")
    uniswap = Uniswap(network.endpoint)

    current_block_number = await __get_block(uniswap)

    while True:
        new_block_number = await __get_block(uniswap)
        if new_block_number > current_block_number:
            await __get_logs(uniswap, current_block_number + 1, new_block_number)
            current_block_number = new_block_number

        await sleep(0.5)
