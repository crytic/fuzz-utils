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
    
/*     function test_auto_check_bytes32_1() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes32(bytes32(hex"000000000000000000000000000000000000000000000000000000000000005c313835"));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytes32();
    } */
    
    function test_auto_check_combined_input_2() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setCombination(true, 57128289344427898022897251869689318228644666479777574762312788645080208847162, -21, 0x0000000000000000000000000000000000010000, string(hex"c281766f775c313932c28024c2abc2844b57067368766214605c14381172"), hex"5065726d69742861646472657373206f776e65722c61646472657373207370656e6465722c75696e743235362076616c75652c75696e74323536206e6f6e63652c75696e74323536646561646c696e6529");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_combined_input();
    }
    
    function test_auto_check_large_negative_int256_3() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(-57896044618658097711785492504343953926634992332820282019728792003956564819968);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_negative_int256();
    }
    
    function test_auto_check_string_4() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setString(string(hex"000000000000000000000000000000000000005238"));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_string();
    }
    
    function test_auto_check_specific_string_5() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_specific_string(string(hex"00"), string(hex"00"));
    }
    
    function test_auto_check_bytes_6() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes(hex"00000000000000000000000000000000005c3138371b5c31383715");
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytes();
    }
    
    function test_auto_check_bool_7() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBool(true);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bool();
    }
    
    function test_auto_check_int256_8() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_int256();
    }
    
    function test_auto_check_address_9() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setAddress(0x00000000000000000000000000000000DeaDBeef);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_address();
    }
    
    function test_auto_check_uint256_10() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(0);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_uint256();
    }
    
    function test_auto_check_large_uint256_11() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(115792089237316195423570985008687907853269984665640564039457584007913129639935);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_uint256();
    }
    
}

    