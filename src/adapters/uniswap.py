from typing import Literal

from .rpc_api import RPC_API


class Uniswap(RPC_API):
    
    __swap_v2_topic: str = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"
    __swap_v3_topic: str = "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"

    def __init__(self, rpc_endpoint: str) -> None:
        super().__init__(rpc_endpoint)
    
    async def get_swaps(self, kind: Literal['v2', 'v3'], from_block: str = 'latest', to_block: str = 'latest'):
        if kind == 'v2':
            topic = self.__swap_v2_topic
        elif kind == 'v3':
            topic = self.__swap_v3_topic
        return await self.getLogs(from_block, to_block, topics=[topic])
