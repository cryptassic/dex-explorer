

from multiprocessing import Queue
from aiohttp import ClientSession
from asyncio import sleep, run

from explorer.models import WorkerTask
from explorer.models.blockchain_models import BlockV2
from explorer.moralis_client import MoralisClient


class Worker(MoralisClient):
    def __init__(self, input_queue: "Queue[WorkerTask]", output_queue: "Queue[BlockV2]"):
        super(Worker, self).__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue

    async def run(self):

        async with ClientSession(headers=self._headers) as worker_session:

            self._session = worker_session

            while True:
                if not self.input_queue.empty():

                    task = self.input_queue.get()
                    if not task:
                        #Propagating dead pill to other workers
                        self.input_queue.put(None)
                        break
                    
                    scraped_block = await self.get_block(block_number=task.block_number)

                    if scraped_block:
                        self.output_queue.put(scraped_block)
                    else:
                        # Failed to execute task, putting back to queue for retry
                        self.input_queue.put(task)

                else:
                    await sleep(1)
            
    def start(self):
        run(self.run())

