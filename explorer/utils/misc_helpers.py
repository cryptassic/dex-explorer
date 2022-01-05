import ciso8601
import calendar
from json import load

def str_datetime_to_timestamp(date_in_str:str) -> int:
    ts = ciso8601.parse_datetime(date_in_str)
    return int(calendar.timegm(ts.timetuple()))

def load_file(filepath:str):
    with open(filepath,'r') as abi_file:
        file_content = load(abi_file)
    
    return file_content

def get_sliced_range(start_block: int, end_block: int, step: int):
        
        for index, block_index_breakpoint in enumerate(range(start_block, end_block+step, step)):

            if not index:
                continue

            if block_index_breakpoint > end_block:
                yield end_block
            else:
                yield block_index_breakpoint
   