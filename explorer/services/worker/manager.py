
import time
import threading
import time

from multiprocessing import Process, Queue

from explorer.utils.misc_helpers import get_sliced_range
from explorer.utils import CustomLogger
from explorer.models import WorkerTask
from explorer.services import Worker


class WorkerManager():
    def __init__(self, callback_func, start_block: int, end_block: int,max_parallel:int=3):

        self._logger = CustomLogger()
        self._max_parallelism = max_parallel
        self._callback_func = callback_func
        self.workers = []

        self.block_start = start_block
        self.block_end = end_block
        
    def __callback_service(self) -> None:
        while True:
            if not self.output_queue._closed:
                if not self.output_queue.empty():
                    data_to_pass = self.output_queue.get()
                    self._callback_func(data_to_pass)
                else:
                    time.sleep(1)
            else:
                break
    
    def __start_callback_thread(self) -> None:
        self._callback_thread = threading.Thread(target=self.__callback_service, args=())
        self._callback_thread.start()

    def __boot_workers(self) -> None:
        for _ in range(self._max_parallelism):
            worker = Worker(input_queue=self.input_queue, output_queue=self.output_queue)
            w_process = Process(target=worker.start, args=())
            self.workers.append(w_process)

        [worker.start() for worker in self.workers]

    def __start(self) -> None:

        if hasattr(self,'input_queue'):
            if self.input_queue and not self.input_queue.empty:
                self._logger.warning(f"WorkerManager:Input Queue not empty! Keeping old queue")
        else:
            self.input_queue = Queue(
                self._max_parallelism*2)
        
        if hasattr(self,'output_queue'):
            if self.output_queue and not self.output_queue.empty:
                self._logger.warning(f"WorkerManager: Output Queue not empty! Keeping old queue")
        else:
            self.output_queue = Queue()
        
        self.__start_callback_thread()

        if len(self.workers):
            self._logger.warning(f"WorkerManager: Found old workers. Overrding")
        
        self.workers.clear()
        self.__boot_workers()

        if not len(self.workers):
            raise Exception("Failed to launch workers")

    def stop(self) -> None:
        # Putting dead pill in queue
        self.input_queue.put(None)

        for worker in self.workers:
            worker.join()
        self._logger.info(f"Job Completed. Exiting...")
        self.input_queue.close()
        
        #This will close callback thread
        self.output_queue.close()

    def start(self) -> None:
        self.__start()

        starting_block = self.block_start

        # Slicing big ranges to smaller chunks of self._max_parallelism size
        for block_range_slice in get_sliced_range(start_block=starting_block, end_block=self.block_end, step=self._max_parallelism):

            # Extend last slice to include last block
            if block_range_slice == self.block_end:
                block_range_slice += 1

            for block_index in range(starting_block, block_range_slice):
                task = WorkerTask(block_number=block_index)
                self.input_queue.put(task)

            starting_block = block_range_slice
        