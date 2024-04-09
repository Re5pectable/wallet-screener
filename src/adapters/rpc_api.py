from httpx import AsyncClient

from ..utils import exclude_none_from_dict


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
            if response.status_code == 200 and response.json().get('result') is not None:
                return response.json()
            raise ValueError("Request failed: %s" % response.content.decode("utf-8"))

    async def getLogs(
        self,
        from_block="latest",
        to_block="latest",
        address: str | list[str] = None,
        topics: list[str] = None,
    ):
        params = exclude_none_from_dict(
            {
                "fromBlock": from_block,
                "toBlock": to_block,
                "topics": topics,
                "address": address,
            }
        )
        response = await self.__request("eth_getLogs", [params])
        return response["result"]
    
    async def blockNumber(self):
        response = await self.__request("eth_blockNumber", [])
        return response["result"]
    
    async def getCode(self, address):
        params = [address, 'latest']
        response = await self.__request("eth_getCode", params)
        return response["result"]