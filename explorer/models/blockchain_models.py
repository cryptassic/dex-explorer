from typing import NamedTuple, List
from enum import Enum


class Chain(Enum):
    ETHEREUM: str = "eth"
    BINANCE_SMART_CHAIN: str = "bsc"


class TransactionV2(NamedTuple):
    block_hash: str
    hash: str
    block_number: int
    input: str
    nonce: int
    index_at_block: int
    from_address: str
    to_address: str
    value: int
    gas: int
    gas_price: int
    gas_used: int
    status: int

    def to_csv(self):
        return f"{self.block_number},{self.hash},{self.nonce},{self.index_at_block},{self.from_address},{self.to_address},{self.value},{self.gas},{self.gas_price},{self.gas_used}"

class BlockV2(NamedTuple):
    timestamp: int
    number: int
    hash: str
    size: int
    transaction_count: int
    transactions: List[TransactionV2]

class SwapTransaction(TransactionV2):
    exec_function_name: str
    input_token_address: str
    output_token_address: str
    input_token_amount: int
    output_token_amount: int

    def __new__(cls, *args, **kwargs):
        new_class = super(SwapTransaction, cls).__new__(cls, *args)
        new_class.__dict__.update(**kwargs)
        return new_class

    def __repr__(self) -> str:
        return f"{self.exec_function_name}"
    
    def to_csv(self) -> str:
        parent_csv = super(SwapTransaction,self).to_csv()
        extended_csv = parent_csv+f",{self.exec_function_name},{self.input_token_address},{self.input_token_amount},{self.output_token_address},{self.output_token_amount}"
        return extended_csv
