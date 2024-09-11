from httpx import AsyncClient


class EVMError(Exception):
    pass

class RPC_API:

    __endpoint: str

    def __init__(self, rpc_endpoint: str) -> None:
        self.__endpoint = rpc_endpoint

    async def __request(self, method: str, params: list[dict]):
        headers = {"Content-Type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1,
        }
        async with AsyncClient() as c:
            response = await c.post(self.__endpoint, headers=headers, json=payload)
            data: dict = response.json()
            if 'result' in data.keys():
                return data['result']    
            raise ValueError(data['error'])

    async def getLogs(
        self,
        from_block="latest",
        to_block="latest",
        address: str | list[str] = None,
        topics: list[str] = None,
    ):
        params = [{
            "fromBlock": from_block,
            "toBlock": to_block,
            "topics": topics,
            "address": address,
        }]
        return await self.__request("eth_getLogs", params)
    
    async def getReceipt(self, txn_hash: str):
        params = [txn_hash]
        return await self.__request("eth_getTransactionReceipt", params)
    
    async def getTransactionByHash(self, txn_hash: str):
        params = [txn_hash]
        return await self.__request("eth_getTransactionByHash", params)
    
    async def blockNumber(self):
        return await self.__request("eth_blockNumber", [])
    
    async def getCode(self, address):
        params = [address, 'latest']
        return await self.__request("eth_getCode", params)