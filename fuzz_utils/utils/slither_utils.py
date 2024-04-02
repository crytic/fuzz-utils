"""Common utilities for Slither"""
from slither import Slither
from slither.core.declarations.contract import Contract
from fuzz_utils.utils.error_handler import handle_exit


def get_target_contract(slither: Slither, target_name: str) -> Contract:
    """Gets the Slither Contract object for the specified contract file"""
    contracts = slither.get_contract_from_name(target_name)
    # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
    for contract in contracts:
        if contract.name == target_name:
            return contract

    handle_exit(f"\n* Slither could not find the specified contract `{target_name}`.")
