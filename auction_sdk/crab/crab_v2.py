#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn
# Created Date: 08/17/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module to interact with Crab V2 contracts """
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from auction_sdk.common.contract import ContractConnection
from auction_sdk.common.definitions import ContractConfig
from auction_sdk.common.utils import get_address

# ---------------------------------------------------------------------------
# Crab V2 Contract
# ---------------------------------------------------------------------------
class CrabV2Contract(ContractConnection):
    """
    Object to create connection to the Crab V2 contract

    Args:
        config (ContractConfig): Configuration to setup the Contract
    """

    abi_location = "abis/CrabV2.json"

    def __init__(self, config: ContractConfig):
        super().__init__(config)

    def nonces(self, owner: str, nonce: int) -> bool:
        """
        Method to check if nonce for specific address is already used

        Args:
            owner (str): Address of owner's address e.g. user wallet address

        Raises:
            ValueError: Address of wallet is invalid

        Returns:
            is_used (bool): true if nonce is already used, otherwise false
        """
        owner_address = get_address(owner)

        is_used = self.contract.functions.nonces(owner_address, nonce).call()

        return is_used