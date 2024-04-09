from .models import SwapperOrm, NetworkOrm, SwapOrm, ErrorOrm
from .engine import Session
from sqlalchemy import select

class Repository:
    
    @classmethod
    async def get_swapper(cls, **kwargs) -> SwapperOrm | None:
        async with Session() as session:
            stmt = select(SwapperOrm).filter_by(**kwargs).limit(1)
            q = await session.execute(stmt)
            return q.scalars().first()
        
    @classmethod
    async def get_network(cls, **kwargs) -> NetworkOrm | None:
        async with Session() as session:
            stmt = select(NetworkOrm).filter_by(**kwargs).limit(1)
            q = await session.execute(stmt)
            return q.scalars().first()
        
    @classmethod
    async def save_swaps(cls, swapper_id: int, data: list[dict]):
        objs = [SwapOrm(swapper_id=swapper_id, **swap_log) for swap_log in data]
        async with Session() as session:
            session.add_all(objs)
            await session.commit()
            
    @classmethod
    async def save_error(cls, action, type, traceback):
        async with Session() as session:
            obj = ErrorOrm(action=action, type=type, traceback=traceback)
            session.add(obj)
            await session.commit()