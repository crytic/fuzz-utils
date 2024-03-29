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
import "src/TestERC20.sol";
contract ActorDefault is PropertiesAsserts {
    TestERC20 testerc20;
    constructor(address _testerc20){
       testerc20 = TestERC20(_testerc20);
    }

    // -------------------------------------
    // ERC20 functions
    // lib/solmate/src/tokens/ERC20.sol
    // -------------------------------------

    function approve(address payable spender, uint256 amount) public returns (bool) {
        testerc20.approve(spender, amount);
    }

    function transfer(address payable to, uint256 amount) public returns (bool) {
        testerc20.transfer(to, amount);
    }

    function transferFrom(address payable from, address payable to, uint256 amount) public returns (bool) {
        testerc20.transferFrom(from, to, amount);
    }

    function permit(address payable owner, address payable spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) public {
        testerc20.permit(owner, spender, value, deadline, v, r, s);
    }
}