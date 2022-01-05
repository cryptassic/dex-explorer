import os
from typing import List

from explorer.services.processors.data_processor import DataProcessor
from explorer.models.blockchain_models import BlockV2, TransactionV2, SwapTransaction
from explorer.utils.misc_helpers import load_file
from explorer.utils.logger import CustomLogger

from web3 import Web3
from eth_utils.address import to_checksum_address


class UniswapProcessor(DataProcessor):
    LOGGER = CustomLogger()
    ROUTER_ADDRESS: str = to_checksum_address(
        "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    ROUTER_CONTRACT = Web3().eth.contract(address=ROUTER_ADDRESS,
                                          abi=load_file(r'explorer/services/processors/ABI/uniswap_router2.json'))

    def __init__(self, output_dir: str):
        self._output_dir = output_dir
        self._filepath = None
        for file_index in range(1, 21):
            filepath = os.path.join(output_dir, f'output_{file_index}.csv')
            if not os.path.exists(filepath):
                self._filepath = filepath
                break

        if not filepath:
            self.LOGGER.error(
                "Please make some space for new outputs... Exceeded max output_20.csv")
            raise Exception("Clean up please")

    def process(self, block_data: BlockV2):
        valid_swap_transactions = []

        swap_transactions = UniswapProcessor._filter_relevant_transactions(
            block=block_data, filter_address=UniswapProcessor.ROUTER_ADDRESS)

        for transaction in swap_transactions:
            decoded_transaction = UniswapProcessor.decode_transaction(
                transaction=transaction)
            if decoded_transaction:
                valid_swap_transactions.append(
                    decoded_transaction.to_csv()+"\n")

        if valid_swap_transactions:
            UniswapProcessor.to_csv(
                filepath=self._filepath, data_to_write=valid_swap_transactions)

    @staticmethod
    def to_csv(filepath: str, data_to_write: List[TransactionV2]):
        with open(filepath, 'a') as out_file:
            out_file.writelines(data_to_write)

    @staticmethod
    def decode_transaction(transaction: TransactionV2) -> SwapTransaction:
        try:
            decoded_function, decoded_input_args = UniswapProcessor.ROUTER_CONTRACT.decode_function_input(
                transaction.input)

            function_name = decoded_function.fn_name

            swap_token_path = decoded_input_args['path']

            input_token_amount = decoded_input_args['amountIn'] if 'amountIn' in decoded_input_args else transaction.value
            output_token_amount = decoded_input_args[
                'amountOutMin'] if 'amountOutMin' in decoded_input_args else decoded_input_args['amountOut']

            input_token_address = swap_token_path[0]
            output_token_address = swap_token_path[-1]

            swap_transaction = SwapTransaction(
                exec_function_name=function_name,
                input_token_address=input_token_address,
                input_token_amount=input_token_amount,
                output_token_address=output_token_address,
                output_token_amount=output_token_amount, *transaction)

            return swap_transaction

        except KeyError as kerr:
            UniswapProcessor.LOGGER.warning(
                f"Transaction:{transaction.hash} Ignored:{kerr}")
            return None
        except ValueError:
            """Not a swap function"""
            # UniswapProcessor.LOGGER.warning(
            #     f"Transaction:{transaction.hash} Ignored")
            return None
        except Exception as ex:
            UniswapProcessor.LOGGER.error(
                f"Can't decode transaction:{transaction.hash} Err:{ex}")
            return None
