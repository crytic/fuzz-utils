// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/ValueTransfer.sol";

contract ValueTransfer_Medusa_Test is Test {
    ValueTransfer target;

    function setUp() public {
        target = new ValueTransfer();
    }
}

    