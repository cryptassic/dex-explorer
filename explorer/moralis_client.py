from typing import NamedTuple, List

from explorer.models.blockchain_models import BlockV2,TransactionV2,Chain
from explorer.utils.misc_helpers import str_datetime_to_timestamp
from explorer.utils import CustomLogger
import traceback
import asyncio
import aiohttp
import traceback
import time

from eth_utils.address import to_checksum_address

import os

API_KEY = os.environ['MORALIS_KEY'] or None
if not API_KEY:
    CustomLogger().error(f"Moralis API key is missing")
    exit()

class MoralisClient:
    def __init__(self, chain: Chain = Chain.ETHEREUM):
        self._session = None
        self._logger = CustomLogger()
        
        self._headers = {"accept": "application/json", "X-API-Key": API_KEY}
        self._url = "https://deep-index.moralis.io/api/v2/"

        self._chain = chain.value

    async def get_latest_block(self) -> int:
        latest_block_number = None
        request_url = f"{self._url}dateToBlock?chain={self._chain}&date={time.time()}"
        request_result = await self._get_async(request_url=request_url)
        
        if request_result:
            latest_block_number = request_result['block']
        else:
            self._logger.error(
                f"get_latest_block failed")

        return latest_block_number

    async def get_block(self, block_number: int):
        block = None

        request_url = f"{self._url}block/{block_number}?chain={self._chain}"
        
        start_time = time.perf_counter()
        
        request_result = await self._get_async(request_url=request_url)

        get_data_time = time.perf_counter() - start_time
        
        if request_result:
            start_time = time.perf_counter()
            block = await self._process_response(response_data_json=request_result)
            process_data_time = time.perf_counter() - start_time
            self._logger.info(
                    f"Get:{block_number} Size:{block.size} Tx_Count:{len(block.transactions)} Time -> Get:{get_data_time:.4f} Process:{process_data_time:.4f}")

        else:
            self._logger.error(
                f"get_block with param:block_number{block_number} failed")

        
        return block

    async def _process_response(self, response_data_json: dict) -> BlockV2:

        typed_block = None

        try:

            datetime_in_str = response_data_json['timestamp']

            block_ctor_kwargs = {
                "timestamp": str_datetime_to_timestamp(datetime_in_str),
                "number": int(response_data_json['number']),
                "hash": response_data_json['hash'],
                "size": int(response_data_json['size']),
                "transaction_count": int(response_data_json['transaction_count']),
                "transactions": []
            }

            for transaction in response_data_json['transactions']:
                
                if not transaction['to_address']:
                    to_address = transaction['receipt_contract_address']
                else:
                    to_address = transaction['to_address']
                    
                transaction_ctor_kwargs = {
                    "block_hash": transaction['block_hash'],
                    "block_number": int(transaction['block_number']),
                    "hash": transaction['hash'],
                    "input": transaction['input'],
                    "nonce": int(transaction['nonce']),
                    "index_at_block": int(transaction['transaction_index']),
                    "from_address": to_checksum_address(transaction['from_address']),
                    "to_address": to_checksum_address(to_address),
                    "value": int(transaction['value']),
                    "gas": int(transaction['gas']),
                    "gas_price": int(transaction['gas_price']),
                    "gas_used": int(transaction['receipt_cumulative_gas_used']),
                    "status": int(transaction['receipt_status'])
                }

                typed_transaction = TransactionV2(**transaction_ctor_kwargs)
                block_ctor_kwargs['transactions'].append(typed_transaction)

            typed_block = BlockV2(**block_ctor_kwargs)

        except Exception as ex:
            self._logger.error(f"Can't parse block. {ex}")
            traceback.print_exc()

        return typed_block

    async def _handler(self, response: aiohttp.ClientResponse) -> dict:
        response_data_json = None
        if response.status == 200:
            try:
                response_data_json = await response.json()

            except Exception as ex:
                self._logger.error(f"{ex}")
                traceback.print_exc()
        else:
            self._logger.error(
                f"Request failed {response.status}:{response.reason}")
        return response_data_json

    async def _get_async(self, request_url: str) -> dict:

        response_data_json = None

        try:
            if self._session:
                async with self._session.get(url=request_url, timeout=10) as response:
                    response_data_json = await self._handler(response=response)
            else:
                async with aiohttp.ClientSession(headers=self._headers) as session:
                    async with session.get(url=request_url, timeout=10) as response:
                        response_data_json = await self._handler(response=response)

        except Exception as ex:
            self._logger.error(f"{ex}")
            traceback.print_exc()

        return response_data_json


if __name__ == "__main__":
    mc = MoralisClient()
    b_n = asyncio.run(mc.get_latest_block())
    print()
