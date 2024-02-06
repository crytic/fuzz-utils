// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/ValueTransfer.sol";

contract ValueTransfer_Echidna_Test is Test {
    ValueTransfer target;

    function setUp() public {
        target = new ValueTransfer();
    }
    function test_auto_check_balance_0() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        (bool success, ) = payable(address(target)).call{value: 1}("");
        require(success, "Low level call failed.");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_balance();
    }
    
}

    