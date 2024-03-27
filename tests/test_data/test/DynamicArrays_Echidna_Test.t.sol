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
    // Reproduced from: echidna-corpora/corpus-dyn-arr/reproducers/-533708655584678499.json
    function test_auto_check_bytesArr_0() public { 
        bytes[] memory dynbytesArr_0 = new bytes[](4);
		dynbytesArr_0[0] = bytes(hex"00");
		dynbytesArr_0[1] = bytes(hex"00");
		dynbytesArr_0[2] = bytes(hex"00");
		dynbytesArr_0[3] = bytes(hex"00");

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBytesArr(dynbytesArr_0);
        
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytesArr();
        
    }
    
    // Reproduced from: echidna-corpora/corpus-dyn-arr/reproducers/-7647997810271354783.json
    function test_auto_check_addressDynArr_1() public { 
        address[] memory dynaddressArr_0 = new address[](8);
		dynaddressArr_0[0] = 0x00000000000000000000000000000000DeaDBeef;
		dynaddressArr_0[1] = 0x00000000000000000000000000000000DeaDBeef;
		dynaddressArr_0[2] = 0x0000000000000000000000000000000000000000;
		dynaddressArr_0[3] = 0x0000000000000000000000000000000000000000;
		dynaddressArr_0[4] = 0x00000000000000000000000000000000DeaDBeef;
		dynaddressArr_0[5] = 0x0000000000000000000000000000000000000000;
		dynaddressArr_0[6] = 0x0000000000000000000000000000000000000000;
		dynaddressArr_0[7] = 0x00000000000000000000000000000000DeaDBeef;

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addAddressArr(dynaddressArr_0);
        
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_addressDynArr();
        
    }
    
    // Reproduced from: echidna-corpora/corpus-dyn-arr/reproducers/959716005390025023.json
    function test_auto_check_boolArr_2() public { 
        bool[] memory dynboolArr_0 = new bool[](6);
		dynboolArr_0[0] = true;
		dynboolArr_0[1] = false;
		dynboolArr_0[2] = true;
		dynboolArr_0[3] = false;
		dynboolArr_0[4] = true;
		dynboolArr_0[5] = true;

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBoolArr(dynboolArr_0);
        
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_boolArr();
        
    }
    
    // Reproduced from: echidna-corpora/corpus-dyn-arr/reproducers/5551649382488529349.json
    function test_auto_check_intDynArr_3() public { 
        int256[] memory dynint256Arr_0 = new int256[](1);
		dynint256Arr_0[0] = int256(3);

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addIntArr(dynint256Arr_0);
        
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_intDynArr();
        
    }
    
    // Reproduced from: echidna-corpora/corpus-dyn-arr/reproducers/1997449955301376751.json
    function test_auto_check_strDynArr_4() public { 
        string[] memory dynstringArr_0 = new string[](4);
		dynstringArr_0[0] = string(hex"00");
		dynstringArr_0[1] = string(hex"00");
		dynstringArr_0[2] = string(hex"00");
		dynstringArr_0[3] = string(hex"00");

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addStrArr(dynstringArr_0);
        
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strDynArr();
        
    }
    
    // Reproduced from: echidna-corpora/corpus-dyn-arr/reproducers/dyn_array_variable_definition.json
    function test_auto_check_intDynArr_5() public { 
        int256[] memory dynint256Arr_0 = new int256[](1);
		dynint256Arr_0[0] = int256(3);

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addIntArr(dynint256Arr_0);
        
        dynint256Arr_0 = new int256[](1);
		dynint256Arr_0[0] = int256(3);

        vm.prank(0x0000000000000000000000000000000000010000);
        target.addIntArr(dynint256Arr_0);
        
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_intDynArr();
        
    }
    
}

    