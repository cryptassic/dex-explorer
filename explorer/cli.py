import os
import argparse
from explorer.services import slow_scrapper



def run(config):
    slow_scrapper.main(config)

def validate_config(config):
    if config.start_block and config.end_block:
        if config.start_block > config.end_block:
            raise argparse.ArgumentTypeError(f"start_block has to be lower than end_block")

def check_positive(value):
    try:
        value = int(value)
        if value < 1:
            raise argparse.ArgumentTypeError(f"value has to be greater than 0")
    except ValueError:
        raise Exception(f"Value is not integer: {value}")
    return value

def check_dir_exists(value):
    if not os.path.isdir(value):
        raise argparse.ArgumentTypeError(f"{value} path does not exists")
    
    return value

def main():
    parser = argparse.ArgumentParser(description="Ethereum Blockchain Scrapper")
    
    parser.add_argument('-s','--start_block',type=check_positive)
    parser.add_argument('-e','--end_block',type=check_positive)
    parser.add_argument('-w','--workers',type=check_positive,default=10)
    parser.add_argument('-o','--out_dir',type=check_dir_exists,default='./')

    config = parser.parse_args()
    validate_config(config)
    run(config)

if __name__ == "__main__":
    main()