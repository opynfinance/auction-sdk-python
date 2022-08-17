#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn
# Created Date: 08/17/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import asdict
from crab_v2_sdk_python.definitions import *
from crab_v2_sdk_python.wallet import Wallet

load_dotenv()

rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ROPSTEN
rpc = {Chains.ROPSTEN: os.getenv('RPC_URL')}
rpc_uri = rpc[current_chain] + rpc_token

osqth_token_address = "0xa4222f78d23593e82Aa74742d25D06720DCa4ab7"

crab_contract_address = "0x3B960E47784150F5a63777201ee2B15253D713e8"    #TODO: change to testnet address
crab_config = ContractConfig(crab_contract_address, rpc_uri, current_chain)

domain = Domain("CrabOTC", "2", 3, crab_contract_address)
print(asdict(domain))

maker_public = os.getenv('MAKER_PubKEY')
maker_private = os.getenv('MAKER_PrivKEY')
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
print("signed_maker_order", signed_maker_order)