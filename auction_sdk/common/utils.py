#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn
# Created Date: 08/17/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Utility functions for encode.py """
# ---------------------------------------------------------------------------

import re

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from web3 import Web3

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PADDING = bytearray([0] * 32)
ADDRESS_ZERO = "0x0000000000000000000000000000000000000000"

# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def id(text: str) -> str:
    """
    Generate the keccak256 of a string

    Args:
        text (str): String to hash

    Returns:
        hash (str): Resulting hash
    """
    return Web3.keccak(text=text).hex()


def get_address(address: str) -> str:
    """
    Validate address validity and return the checksum address

    Args:
        address (str): Address with 0x prefix

    Returns:
        address (str): Returns address if valid
    """
    try:
        return Web3.toChecksumAddress(address)
    except ValueError:
        raise ValueError(f'Invalid address: {address}')
