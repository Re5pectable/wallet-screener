import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

Base = declarative_base()

class NetworkOrm(Base):
    __tablename__ = 'networks'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now())
    title = sa.Column(sa.String(32))
    endpoint = sa.Column(sa.String(64))


class PairLPOrm(Base):
    __tablename__ = 'pair_lps'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now())
    contract = sa.Column(sa.String(64), index=True)
    type = sa.Column(sa.String(32))
    

class SwapOrm(Base):
    __tablename__ = 'trades'
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    txn_hash = sa.Column(sa.String(256))
    wallet = sa.Column(sa.String(128), index=True)
    pair_lp_id = sa.Column(sa.Integer, sa.ForeignKey('pair_lps.id'), index=True)
    pool_token0_delta = sa.Column(postgresql.NUMERIC(64, 0))
    pool_token1_delta = sa.Column(postgresql.NUMERIC(64, 0))
    

class ErrorOrm(Base):
    __tablename__ = 'errors'
    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    action = sa.Column(sa.String(32))
    type = sa.Column(sa.String(32))
    traceback = sa.Column(sa.String())