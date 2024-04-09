from ..rpc_api import RPC_API

class UniswapPoolV2(RPC_API):
    
    __swap_topic: str = "0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822"

    def __init__(self, rpc_endpoint: str) -> None:
        super().__init__(rpc_endpoint)
    
    async def get_recent_trades(self):
        topics = [self.__swap_topic]
        return await self.getLogs(topics=topics)
        