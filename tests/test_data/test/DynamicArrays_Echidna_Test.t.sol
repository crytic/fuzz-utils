// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/DynamicArrays.sol";

contract DynamicArrays_Echidna_Test is Test {
    DynamicArrays target;

    function setUp() public {
        target = new DynamicArrays();
    }
    function test_auto_check_bytesArr_0() public { 
        bytes[] memory dynBytesArr_0 = new bytes[](4);
		dynBytesArr_0[0] = bytes(hex"00");
		dynBytesArr_0[1] = bytes(hex"00");
		dynBytesArr_0[2] = bytes(hex"00");
		dynBytesArr_0[3] = bytes(hex"00");

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBytesArr(dynBytesArr_0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytesArr();
    }
    
    function test_auto_check_addressDynArr_1() public { 
        address[] memory dynAddressArr_0 = new address[](8);
		dynAddressArr_0[0] = 0x00000000000000000000000000000000DeaDBeef;
		dynAddressArr_0[1] = 0x00000000000000000000000000000000DeaDBeef;
		dynAddressArr_0[2] = 0x0000000000000000000000000000000000000000;
		dynAddressArr_0[3] = 0x0000000000000000000000000000000000000000;
		dynAddressArr_0[4] = 0x00000000000000000000000000000000DeaDBeef;
		dynAddressArr_0[5] = 0x0000000000000000000000000000000000000000;
		dynAddressArr_0[6] = 0x0000000000000000000000000000000000000000;
		dynAddressArr_0[7] = 0x00000000000000000000000000000000DeaDBeef;

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addAddressArr(dynAddressArr_0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_addressDynArr();
    }
    
    function test_auto_check_boolArr_2() public { 
        bool[] memory dynBoolArr_0 = new bool[](6);
		dynBoolArr_0[0] = true;
		dynBoolArr_0[1] = false;
		dynBoolArr_0[2] = true;
		dynBoolArr_0[3] = false;
		dynBoolArr_0[4] = true;
		dynBoolArr_0[5] = true;

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBoolArr(dynBoolArr_0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_boolArr();
    }
    
    function test_auto_check_intDynArr_3() public { 
        int256[] memory dynIntArr_0 = new int256[](1);
		dynIntArr_0[0] = int256(3);

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addIntArr(dynIntArr_0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_intDynArr();
    }
    
    function test_auto_check_strDynArr_4() public { 
        string[] memory dynStringArr_0 = new string[](4);
		dynStringArr_0[0] = string(hex"00");
		dynStringArr_0[1] = string(hex"00");
		dynStringArr_0[2] = string(hex"00");
		dynStringArr_0[3] = string(hex"00");

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addStrArr(dynStringArr_0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strDynArr();
    }
    
}

    