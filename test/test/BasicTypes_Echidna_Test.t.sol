// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/BasicTypes.sol";

contract BasicTypes_Echidna_Test is Test {
    BasicTypes target;

    function setUp() public {
        target = new BasicTypes();
    }
    function test_auto_check_large_positive_int256_0() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(57896044618658097711785492504343953926634992332820282019728792003956564819967);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_positive_int256();
    }
    
    function test_auto_check_large_negative_int256_1() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(-57896044618658097711785492504343953926634992332820282019728792003956564819968);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_negative_int256();
    }
    
    function test_auto_check_string_2() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setString(string(hex"0000000000000000000000000000007b5b3137315d5b39315d5b3134365d5b3136385d5e"));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_string();
    }
    
    function test_auto_check_combined_input_3() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setCombination(true, 97050253085751362382831783309837709962118062772644684258071387590153646953544, -2158778574, 0x00000000000000000000000000000000FFFFfFFF, string(hex"5c745c43414e5b3132355d7b"), hex"5a45524f5f41444452455353");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_combined_input();
    }
    
    function test_auto_check_bool_4() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBool(true);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bool();
    }
    
    function test_auto_check_int256_5() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_int256();
    }
    
    function test_auto_check_bytes32_6() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes32(hex"000000000000000000000000000000000000000000000000000000000000005b3130355d");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytes32();
    }
    
    function test_auto_check_address_7() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setAddress(0x00000000000000000000000000000000DeaDBeef);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_address();
    }
    
    function test_auto_check_uint256_8() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_uint256();
    }
    
    function test_auto_check_bytes_9() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes(hex"000000000000000000000000000000000000000000");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytes();
    }
    
    function test_auto_check_large_uint256_10() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(115792089237316195423570985008687907853269984665640564039457584007913129639935);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_uint256();
    }
    
}

    