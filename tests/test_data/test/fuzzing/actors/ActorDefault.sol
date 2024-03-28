// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

/// --------------------------------------------------------------------
/// @notice This file was automatically generated using fuzz-utils 
///
/// -- [ Prerequisites ]
/// 1. The generated contracts depend on crytic/properties utilities
///    which need to be installed, this can be done by running:
///    `forge install crytic/properties`
/// 2. Absolute paths are used for contract inheritance, requiring
///    the main directory that contains the contracts to be added to
///    the Foundry remappings. This can be done by adding:
///    `directoryName/=directoryName/` to foundry.toml or remappings.txt

import "properties/util/PropertiesHelper.sol";
import "src/BasicTypes.sol";
contract ActorDefault is PropertiesAsserts {
    BasicTypes basictypes;
    constructor(address _basictypes){
       basictypes = BasicTypes(_basictypes);
    }

    // -------------------------------------
    // BasicTypes functions
    // src/BasicTypes.sol
    // -------------------------------------

    function setBool(bool set) public {
        basictypes.setBool(set);
    }

    function check_bool() public {
        basictypes.check_bool();
    }

    function setUint256(uint256 input) public {
        basictypes.setUint256(input);
    }

    function check_uint256() public {
        basictypes.check_uint256();
    }

    function check_large_uint256() public {
        basictypes.check_large_uint256();
    }

    function setInt256(int256 input) public {
        basictypes.setInt256(input);
    }

    function check_int256() public {
        basictypes.check_int256();
    }

    function check_large_positive_int256() public {
        basictypes.check_large_positive_int256();
    }

    function check_large_negative_int256() public {
        basictypes.check_large_negative_int256();
    }

    function setAddress(address payable input) public {
        basictypes.setAddress(input);
    }

    function check_address() public {
        basictypes.check_address();
    }

    function setString(string memory input) public {
        basictypes.setString(input);
    }

    function check_string() public {
        basictypes.check_string();
    }

    function check_specific_string(string memory provided) public {
        basictypes.check_specific_string(provided);
    }

    function setBytes(bytes memory input) public {
        basictypes.setBytes(input);
    }

    function check_bytes() public {
        basictypes.check_bytes();
    }

    function setCombination(bool bool_input, uint256 unsigned_input, int256 signed_input, address payable address_input, string memory str_input, bytes memory bytes_input) public {
        basictypes.setCombination(bool_input, unsigned_input, signed_input, address_input, str_input, bytes_input);
    }

    function check_combined_input() public {
        basictypes.check_combined_input();
    }
}