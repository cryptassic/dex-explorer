
# Decentralized Exchange Explorer

Simple tool for Uniswap data extraction. With this tool you can easily get transactions data in CSV format for further data analysis.

**Output CSV format**

    0. Block_Number - block index number
    1. Hash - unique transaction identifier 
    2. Nonce - number of transactions sent from this address
    3. Index_At_Block - positional transaction index at block
    4. From_Address - sender wallet address
    5. To_Address - receiver (UniswapV2Router) address
    6. Value - transaction value in ether
    7. Gas - maximum allowed gas spending
    8. Gas_Price - used for calculating total transaction price
    9. Gas_Used - actual gas used
    10. Executed_Function - function that was executed on UniswapV2Router contract
    11. Input_Token_Address
    12. Input_Token_Amount
    13. Output_Token_Address
    14. Output_Token_Amount


## Installation

### Requirements

- Python >= 3.6


```bash
  sudo apt update
  sudo apt install python3 -y
```

Clone this repository

```bash
  git clone https://github.com/cryptassic/dex-explorer.git
  cd dex-explorer/
```
To keep everything clean - create a virtual environment (Optional)
```bash
  python3 -m venv ./env
  source ./env/bin/activate
```


Finally install the package
```bash
  python3 setup.py install
```



## Environment Variables

To run this project, you will need to add the following environment variables.

`MORALIS_KEY`

This is crucial, because without this key our explorer can't get any data from blockchain. 
You can get one for free at - https://admin.moralis.io/register. After registration simply navigate to Web3API and press Copy API key.

```bash
  export MORALIS_KEY=<API_KEY>
```



## Usage/Examples

Default - will run from **10000835** block till latest mined block
```bash
    python3 ./bin/blockchain_scrapper
```

You can specify start_block:

```bash
    python3 ./bin/blockchain_scrapper --start_block 13960000
```


Or even combine it with end_block:

```bash
    python3 ./bin/blockchain_scrapper --start_block 13960000 --end_block 13963800
```

