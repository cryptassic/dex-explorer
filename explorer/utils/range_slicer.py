
class RangeSlicer:
    @staticmethod
    def get_sliced_range(start_block: int, end_block: int, step: int):
        
        for index, block_index_breakpoint in enumerate(range(start_block, end_block+step, step)):

            if not index:
                continue

            if block_index_breakpoint > end_block:
                yield end_block
            else:
                yield block_index_breakpoint
