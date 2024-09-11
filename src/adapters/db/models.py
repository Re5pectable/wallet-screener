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
    address = sa.Column(sa.String(), index=True)
    symbol = sa.Column(sa.String())
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
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    network_id = sa.Column(sa.Integer(), sa.ForeignKey("networks.id"))
    contract = sa.Column(sa.String(), index=True)
    token0_id = sa.Column(sa.Integer(), sa.ForeignKey("tokens.id"))
    token1_id = sa.Column(sa.Integer(), sa.ForeignKey("tokens.id"))
    type = sa.Column(sa.String(32))


class TransactionOrm(Base):
    __tablename__ = "transactions"
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    txn_hash = sa.Column(sa.String(256))
    block_number = sa.Column(sa.Integer())
    

class SwapsOrm(Base):
    __tablename__ = 'swaps'
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    transaction_id = sa.Column(sa.BigInteger(), sa.ForeignKey("transactions.id"), index=True)
    from_token_id = sa.Column(sa.Integer(), sa.ForeignKey("tokens.id"), index=True)
    from_token_amount = sa.Column(sa.Numeric(60, 0))
    to_token_id = sa.Column(sa.Integer(), sa.ForeignKey("tokens.id"), index=True)
    to_token_amount = sa.Column(sa.Numeric(60, 0))


class ErrorOrm(Base):
    __tablename__ = "errors"
    id = sa.Column(sa.BigInteger(), primary_key=True, autoincrement=True)
    created_at = sa.Column(sa.DateTime(), default=func.now(), index=True)
    action = sa.Column(sa.String(32))
    error = sa.Column(sa.String())
    traceback = sa.Column(sa.String())
