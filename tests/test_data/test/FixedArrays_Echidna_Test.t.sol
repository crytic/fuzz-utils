// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/FixedArrays.sol";

contract FixedArrays_Echidna_Test is Test {
    FixedArrays target;

    function setUp() public {
        target = new FixedArrays();
    }
    function test_auto_check_boolArr_0() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBoolArr([true,false,true]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_boolArr();
    }
    
    function test_auto_check_strArr_1() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addStrArr([string(hex"00"),string(hex"00")]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strArr();
    }
    
    function test_auto_check_uintArr_2() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addUintArr([uint256(5),uint256(0)]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_uintArr();
    }
    
    function test_auto_check_bytesArr_3() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBytesArr([bytes(hex"00"),bytes(hex"00")]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytesArr();
    }
    
    function test_auto_check_intArr_4() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addIntArr([int256(3),int256(2)]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_intArr();
    }
    
    function test_auto_check_addressArr_5() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addAddressArr([0x00000000000000000000000000000000DeaDBeef,0x0000000000000000000000000000000000000000,0x00000000000000000000000000000000DeaDBeef,0x00000000000000000000000000000000DeaDBeef]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_addressArr();
    }
    
}

    