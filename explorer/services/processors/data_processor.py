
from typing import List
from abc import ABC, abstractmethod
from explorer.models.blockchain_models import BlockV2, TransactionV2
from eth_utils.address import to_checksum_address


class DataProcessor(ABC):
    @staticmethod
    @abstractmethod
    def process(block_data: BlockV2):
        pass

    @staticmethod
    def _filter_relevant_transactions(block: BlockV2, filter_address: str) -> List[TransactionV2]:

        if not block:
            return []

        dex_transactions = []

        for transaction in block.transactions:
            if transaction.to_address and transaction.status:
                to_address = to_checksum_address(transaction.to_address)
                if to_address == filter_address:
                    dex_transactions.append(transaction)

        return dex_transactions
