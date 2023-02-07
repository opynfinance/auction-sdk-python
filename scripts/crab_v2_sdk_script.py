#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn
# Created Date: 08/17/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------

import requests
import os
import time
from dotenv import load_dotenv
from datetime import datetime
from dataclasses import asdict
from auction_sdk.definitions import *
from auction_sdk.wallet.wallet import Wallet

load_dotenv()

@dataclass
class Auction:
    currentAuctionId: int
    nextAuctionId: int
    oSqthAmount: str
    price: str
    auctionEnd: int
    isSelling: bool
    minSize: int

auction_endpoint = 'http://localhost:3000/'
rpc_token = os.getenv('RPC_TOKEN')
current_chain = Chains.ETHEREUM
rpc = {Chains.ETHEREUM: os.getenv('RPC_URL')}
rpc_uri = rpc[current_chain] + rpc_token

osqth_token_address = "0xf1B99e3E573A1a9C5E6B2Ce818b617F0E664E86B"

crab_contract_address = "0x3b960e47784150f5a63777201ee2b15253d713e8"    #TODO: change to testnet address
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

is_nonce_used = maker_wallet.is_nonce_used(crab_config, 1)
print("is_nonce_used", is_nonce_used)


# create new auction 
print("#### Crating new auction ####")
print("round(time.time()", round(time.time()))
print("int(round(time.time() + 3600 * 60)) * 1000", int((round(time.time()) + 3600) * 1000))
auction_to_create : Auction = Auction(1, 2, 100, 1, int((round(time.time()) + 3600) * 1000), True, 0)
req = requests.post(auction_endpoint + 'api/auction/createOrEditAuction',
                    json={"signature": "", "auction": auction_to_create.__dict__})

created_auction = (requests.get(auction_endpoint + 'api/auction/getLatestAuction')).json()
print("created_auction", created_auction)

print("### Submiting bid ###")
maker_wallet.submit_bid(
    Domain("CrabOTC", "2", 3, crab_contract_address),
    1,
    1,    # 1 oSQTH
    2,     # .2 WETH
    True, 
    60 * 1000, 
    int(round(time.time() * 1000))  # some random number that's not used before
)