#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn
# Created Date: 08/17/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to store data classes """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from dataclasses import dataclass
from auction_sdk.chains import Chains

# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------
@dataclass
class Domain:
    """
    Domain parameters for signatures
    """

    name: str
    version: str
    chainId: int
    verifyingContract: str


@dataclass
class MessageToSign:
    """Bid message to sign off-chain"""

    bidId: int
    trader: str
    quantity: int
    price: int
    isBuying: bool
    expiry: int
    nonce: int


@dataclass
class BidData:
    """Bid data to send on-chain containing bid information and signature"""

    bidId: int
    trader: str
    quantity: int
    price: int
    isBuying: bool
    expiry: int
    nonce: int  
    v: int
    r: str
    s: str


@dataclass
class ContractConfig:
    """Configuration needed to connect to a Contract"""

    address: str
    rpc_uri: str
    chain_id: Chains = Chains.ETHEREUM


@dataclass
class Signature:
    v: int
    r: str
    s: str