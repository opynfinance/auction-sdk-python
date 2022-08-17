# OPYN SDK

## Install

It's possible to install the package via `pip`,
having also `git` installed.

```bash
# Latest version
python3 -m pip install \
    "git+https://github.com/opynfinance/crab-v2-sdk-python.git#egg=crab_v2_sdk_python&subdirectory=crab_v2_sdk_python"
```

## Usage

There are different things you are able to do with this package.

### Define domain 

```python
from crab_v2_sdk_python.definitions import Chains, ContractConfig, Domain
from crab_v2_sdk_python.settlement import SettlementContract, asdict

# Define the following variables:
crab_contract_address = "0x..."
domain = Domain("CrabOTC", "2", 3, crab_contract_address)
print(asdict(domain))
```

This will output something similar to:
```python
{'name': 'CrabOTC', 'version': '2', 'chainId': 3, 'verifyingContract': '0x3B960E47784150F5a63777201ee2B15253D713e8'}
```

### Signing bid order

```python
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import asdict
from crab_v2_sdk_python.definitions import *
from crab_v2_sdk_python.wallet import Wallet

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"

maker_public = 0x0...
maker_private = 0x012...
maker_wallet = Wallet(maker_public, maker_private)

maker_message = MessageToSign(
    bidId=1,
    trader=maker_wallet.public_key,
    quantity=int(10**18),
    price=int(0.5 * 10**18),
    isBuying=True,
    expiry=int(datetime.timestamp(datetime.now()) + 3600),
    nonce=1,
)
signed_maker_order = maker_wallet.sign_bid_data(domain, maker_message)
```

This will output something similar to:
```python
signed_maker_order BidData(bidId=1, trader='0x5599b4EAdDd319e2F462b27fC8378B0BFaD309CA', quantity=1000000000000000000, price=500000000000000000, isBuying=True, expiry=1660738176, nonce=1, v=27, r='0x818976080a8f886be93277d70c8e7b141d6ec65266ff837dde3d6bca31e6dfb5', s='0x52b4c51d59cea64a3e11c1c0440010638bae899fcbcbeadd5214f8856151262a')
```

### Validate wallets

```python
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import asdict
from crab_v2_sdk_python.definitions import *
from crab_v2_sdk_python.wallet import Wallet

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"
crab_contract_address = "0x3B960E47784150F5a63777201ee2B15253D713e8"
crab_config = ContractConfig(crab_contract_address, rpc_uri, current_chain)
token_address = "0x..." #token address to check allowance for

maker_public = 0x0...
maker_private = 0x012...
maker_wallet = Wallet(maker_public, maker_private)

check = wallet.verify_allowance(crab_config, token_address)
print(check)

# True
```

## Local development

- Make sure to have [poetry installed](https://python-poetry.org/docs/#installation)
- Install dependencies using poetry by running `poetry install`

### How to run script file

- Make sure to have the following environment variables in `.env` file:
```
RPC_TOKEN=
RPC_URL=
MAKER_PubKEY=
MAKER_PrivKEY=
```
- Build the crab_v2_sdk_python package by running `poetry build`
- Run `pip3 install -I dist/crab_v2_sdk_python-0.1.0-py3-none-any.whl`
- Run python3 scripts/crab_v2_sdk_script.py

## Crab V2 Contract Addresses

- Mainnet: 0x3B960E47784150F5a63777201ee2B15253D713e8
- Ropsten: 
