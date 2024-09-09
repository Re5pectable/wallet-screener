import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

Base = declarative_base()


class NetworkOrm(Base):
    __tablename__ = "networks"
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), server_default=func.now())
    name = sa.Column(sa.String(32))
    endpoint = sa.Column(sa.String(64))
    

class TokenOrm(Base):
    __tablename__ = 'tokens'
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), server_default=func.now())
    network_id = sa.Column(sa.Integer(), sa.ForeignKey("networks.id"))
    symbol = sa.Column(sa.String())
    address = sa.Column(sa.String())
    decimals = sa.Column(sa.Integer())
    is_stable = sa.Column(sa.Boolean(), default=False)


class TraderOrm(Base):
    __tablename__ = 'traders'
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), server_default=func.now())
    address = sa.Column(sa.String(), unique=True, index=True)


class PoolOrm(Base):
    __tablename__ = "pools"
    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now())
    network_id = sa.Column(sa.Integer(), sa.ForeignKey("networks.id"))
    contract = sa.Column(sa.String(), index=True)
    token0_id = sa.Column(sa.Integer(), sa.ForeignKey("tokens.id"))
    token1_id = sa.Column(sa.Integer(), sa.ForeignKey("tokens.id"))
    type = sa.Column(sa.String(32))


class SwapOrm(Base):
    __tablename__ = "swaps"
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    pool_id = sa.Column(sa.Integer(), sa.ForeignKey("pools.id"))
    trader_id = sa.Column(sa.Integer(), sa.ForeignKey("trader.id"))
    txn_hash = sa.Column(sa.String(256))
    pair_lp_id = sa.Column(sa.Integer, sa.ForeignKey("pair_lps.id"), index=True)
    pool_token0_delta = sa.Column(postgresql.NUMERIC(64, 0))
    pool_token1_delta = sa.Column(postgresql.NUMERIC(64, 0))


class ErrorOrm(Base):
    __tablename__ = "errors"
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    action = sa.Column(sa.String(32))
    error = sa.Column(sa.String())
    traceback = sa.Column(sa.String())
