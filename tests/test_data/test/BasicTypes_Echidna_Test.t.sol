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
    
    function test_auto_check_string_1() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setString(string(hex"000000000000000000000000455d40c2824f5c3139325d1bc2a0"));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_string();
    }
    
    function test_auto_check_large_negative_int256_2() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(-57896044618658097711785492504343953926634992332820282019728792003956564819968);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_negative_int256();
    }
    
    function test_auto_check_specific_string_3() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_specific_string(string(hex"00"));
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
    
    function test_auto_check_address_6() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setAddress(0x00000000000000000000000000000000DeaDBeef);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_address();
    }
    
    function test_auto_check_uint256_7() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_uint256();
    }
    
    function test_auto_check_large_uint256_8() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(115792089237316195423570985008687907853269984665640564039457584007913129639935);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_uint256();
    }
    
    function test_auto_check_bytes_9() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes(hex"00000000000000000000000000000000441d032c5c313933");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytes();
    }
    
    function test_auto_check_combined_input_10() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setCombination(true, 73787535259818932473903644254733232752453571753984022104896637448811415645988, -4, 0x00000000000000000000000000000002fFffFffD, string(hex"7665235e5c313837"), hex"3f5fc28070c28bc298c2897f5c313934c28bc2a3c28bc28978290669627d1a6d467e0b7f7e14385c313933761114");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_combined_input();
    }
    
}

    