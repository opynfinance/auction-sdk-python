#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By: Haythem@Opyn
# Created Date: 08/17/2022
# version ='0.1.0'
# ---------------------------------------------------------------------------
""" Module for wallet utilities """
# ---------------------------------------------------------------------------

from dataclasses import asdict

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import eth_keys
from py_eth_sig_utils.signing import sign_typed_data
from web3 import Web3
from crab_v2_sdk_python.definitions import BidData, ContractConfig, Domain, MessageToSign
from crab_v2_sdk_python.erc20 import ERC20Contract
from crab_v2_sdk_python.crab_v2 import CrabV2Contract

from crab_v2_sdk_python.utils import get_address

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# bytes32 private constant _CRAB_BALANCE_TYPEHASH =
#     keccak256(
#         "Order(uint256 bidId,address trader,uint256 quantity,uint256 price,bool isBuying,uint256 expiry,uint256 nonce)"
#     );
ORDER_TYPES = {
    "EIP712Domain": [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ],
    "Order": [
        {"name": "bidId", "type": "uint256"},
        {"name": "trader", "type": "address"},
        {"name": "quantity", "type": "uint256"},
        {"name": "price", "type": "uint256"},
        {"name": "isBuying", "type": "bool"},
        {"name": "expiry", "type": "uint256"},
        {"name": "nonce", "type": "uint256"},
    ],
}
MIN_ALLOWANCE = 1


# ---------------------------------------------------------------------------
# Wallet Instance
# ---------------------------------------------------------------------------
class Wallet:
    """
    Object to generate bid signature

    Args:
        public_key (str): Public key of the user in hex format with 0x prefix
        private_key (str): Private key of the user in hex format with 0x prefix

    Attributes:
        signer (object): Instance of signer to generate signature
    """

    def __init__(self, public_key: str = None, private_key: str = None):
        if not private_key and not public_key:
            raise ValueError("Can't instanciate a Wallet without a public or private key")

        self.private_key = private_key
        self.public_key = public_key

        if self.private_key:
            self.signer = eth_keys.keys.PrivateKey(bytes.fromhex(self.private_key[2:]))
            if not self.public_key:
                self.public_key = get_address(self.signer.public_key.to_address())

    def sign_bid_data(
        self, domain: Domain, message_to_sign: MessageToSign, types: dict = ORDER_TYPES
    ) -> BidData:
        """Sign a bid using py_eth_sig_utils

        Args:
            domain (dict): Dictionary containing domain parameters including
              name, version, chainId, verifyingContract
            message_to_sign (MessageToSign): Unsigned Order Data

        Raises:
            TypeError: message_to_sign argument is not an instance of MessageToSign class

        Returns:
            signedBid (dict): Bid combined with the generated signature
        """
        if not isinstance(message_to_sign, MessageToSign):
            raise TypeError("Invalid message_to_sign(MessageToSign)")

        if not self.private_key:
            raise ValueError("Unable to sign. Create the Wallet with the private key argument.")

        message_to_sign.trader = get_address(message_to_sign.trader)

        if message_to_sign.trader != self.public_key:
            raise ValueError("Signer wallet address mismatch")

        data = {
            "types": types,
            "domain": asdict(domain),
            "primaryType": "Order",
            "message": asdict(message_to_sign),
        }
        signature = sign_typed_data(data, Web3.toBytes(hexstr=self.private_key))

        return BidData(
            bidId=message_to_sign.bidId,
            trader=message_to_sign.trader,
            quantity=message_to_sign.quantity,
            price=message_to_sign.price,
            isBuying=message_to_sign.isBuying,
            expiry=message_to_sign.expiry,
            nonce=message_to_sign.nonce,
            v=signature[0],
            r=Web3.toHex(signature[1].to_bytes(32, 'big')),
            s=Web3.toHex(signature[2].to_bytes(32, 'big')),
        )

    def verify_allowance(self, crab_config: ContractConfig, token_address: str) -> bool:
        """Verify wallet's allowance for a given token

        Args:
            config (ContractConfig): Configuration to setup the Swap Contract
            token_address (str): Address of token

        Returns:
            verified (bool): True if wallet has sufficient allowance
        """
        token_config = ContractConfig(
            address=token_address,
            rpc_uri=crab_config.rpc_uri,
            chain_id=crab_config.chain_id,
        )
        token = ERC20Contract(token_config)

        allowance = (
            token.get_allowance(self.public_key, crab_config.address) / token.decimals
        )

        return allowance > (MIN_ALLOWANCE * 10**token.decimals)

    def allow_more(self, crab_config: ContractConfig, token_address: str, amount: int):
        """Increase settlement contract allowance

        Args:
            crab_config (ContractConfig): Configuration to setup the Settlement contract
            token_address (str): Address of token to increase allowance of
            amount (str): Amount to increase allowance to
        """
        token_config = ContractConfig(
            address=token_address,
            rpc_uri=crab_config.rpc_uri,
            chain_id=crab_config.chain_id,
        )
        token = ERC20Contract(token_config)

        token.approve(self.public_key, self.private_key, crab_config.address, amount)

    def is_nonce_used(self, crab_config: ContractConfig, nonce: int) -> bool:
        """Check if specific nonce is already used, return false if not
        
        Args:
            crab_config (ContractConfig): Configuration to setup the Settlement contract
            nonce (int): nonce to check
        """
        crab = CrabV2Contract(crab_config)

        return crab.nonces(self.public_key, nonce)

    # def submit_bid(self, )
