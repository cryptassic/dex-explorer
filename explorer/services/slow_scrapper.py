import asyncio

from explorer.services import WorkerManager
from explorer.services.processors import UniswapProcessor

from explorer.moralis_client import MoralisClient

class SlowScrapper(MoralisClient):
    def __init__(self, config):
        super(SlowScrapper, self).__init__()
        self._config = config

    def start(self) -> None:

        latest_block_number = asyncio.run(self.get_latest_block())
        if not latest_block_number:
            self._logger.error("Can't get lastest_block_number. Exiting...")
            exit()

        start_block = self._config.start_block
        end_block = self._config.end_block

        if not start_block:
            start_block = 1
            self._logger.warning(
                f"start_block is not set. Scraping from: 1 block")

        if not end_block:
            end_block = latest_block_number
            self._logger.warning(
                f"end_block is not set. Scrapping till: {latest_block_number} block")

        elif end_block > latest_block_number:
            end_block = latest_block_number
            self._logger.warning(
                f"end_block is higher than current available block. Scrapping till: {latest_block_number} block")

        total_blocks_to_scrap = end_block-start_block+1

        self._logger.info(
            f"start_block:{start_block} end_block:{end_block} total_blocks:{total_blocks_to_scrap} workers:{self._config.workers}")

        
        self.w_manager = WorkerManager(
            callback_func=UniswapProcessor(output_dir=self._config.out_dir).process, 
            start_block=start_block,
            end_block=end_block, 
            max_parallel=self._config.workers)

        self.w_manager.start()

    def stop(self) -> None:
        self.w_manager.stop()


def main(config):
    sloth = SlowScrapper(config=config)
    sloth.start()
    sloth.stop()