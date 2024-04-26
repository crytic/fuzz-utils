"""Utility functions to handle Foundry remappings"""
import os
import subprocess
import re
from slither import Slither
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.utils.error_handler import handle_exit

# pylint: disable=too-many-locals
def find_remappings(include_attacks: bool, slither: Slither) -> dict:
    """Finds the remappings used and returns a dict with the values"""
    CryticPrint().print_information("Checking dependencies...")
    openzeppelin = r"(\S+)=lib\/openzeppelin-contracts\/(?!\S*lib\/)(\S*)"
    solmate = r"(\S+)=lib\/solmate\/(?!\S*lib\/)(\S*)"
    properties = r"(\S+)=lib\/properties\/(?!\S*lib\/)(\S*)"

    working_dir = slither.crytic_compile.working_dir
    platform_config = slither.crytic_compile.platform.config(working_dir)

    remappings: str = ""
    if platform_config:
        remappings = "\n".join(platform_config.remappings)
    else:
        output = subprocess.run(["forge", "remappings"], capture_output=True, text=True, check=True)
        forge_remaps = str(output.stdout).split("\n")

        if os.path.exists("remappings.txt"):
            with open("remappings.txt", "r", encoding="utf-8") as file:
                remappings_file = file.read().split("\n")
                # Converting to set to remove duplicates, back to list for joining
                forge_remaps = list(set(forge_remaps + remappings_file))

        remappings = "\n".join(forge_remaps)

    oz_matches = re.findall(openzeppelin, remappings)
    sol_matches = re.findall(solmate, remappings)
    prop_matches = re.findall(properties, remappings)

    if include_attacks and len(oz_matches) == 0 and len(sol_matches) == 0:
        handle_exit(
            "Please make sure that openzeppelin-contracts or solmate are installed if you're using the Attack templates."
        )

    if len(prop_matches) == 0:
        handle_exit(
            "Please make sure crytic/properties is installed before running the template command."
        )

    result = {}
    if len(oz_matches) > 0:
        default = ["contracts/"]
        result["openzeppelin"] = "".join(
            find_difference_between_list_and_tuple(default, oz_matches[0])
        )

    if len(sol_matches) > 0:
        default = ["src/"]
        result["solmate"] = "".join(find_difference_between_list_and_tuple(default, sol_matches[0]))

    if len(prop_matches) > 0:
        default = ["contracts/"]
        result["properties"] = "".join(
            find_difference_between_list_and_tuple(default, prop_matches[0])
        )

    return result


def find_difference_between_list_and_tuple(default: list, my_tuple: tuple) -> list:
    """Used to manage remapping paths based on difference between the remappings and the expected path"""
    return [item for item in my_tuple if item not in default] + [
        item for item in default if item not in my_tuple
    ]
