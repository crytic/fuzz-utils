// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/BasicTypes.sol";

contract BasicTypes_Medusa_Test is Test {
    BasicTypes target;

    function setUp() public {
        target = new BasicTypes();
    }
    function test_auto_check_address_0() public { 
        vm.warp(block.timestamp + 592103);
        vm.roll(block.number + 34807);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setAddress(0xE7D62AAD5028B951Baa93783c8405080bdDD746D);
        vm.warp(block.timestamp + 20);
        vm.roll(block.number + 3);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_address();
    }
    
    function test_auto_check_specific_string_1() public { 
        vm.warp(block.timestamp + 565377);
        vm.roll(block.number + 18560);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_specific_string(unicode"\u0000");
    }
    
    function test_auto_check_bytes_2() public { 
        vm.warp(block.timestamp + 461663);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes(bytes(hex"281e5a7ea62236de170107c251ad3e7c9f54bc4db80f0795"));
        vm.warp(block.timestamp + 7);
        vm.roll(block.number + 6);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_bytes();
    }
    
    function test_auto_check_bool_3() public { 
        vm.warp(block.timestamp + 306911);
        vm.roll(block.number + 52752);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBool(true);
        vm.warp(block.timestamp + 360622);
        vm.roll(block.number + 56746);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_bool();
    }
    
    function test_auto_check_int256_4() public { 
        vm.warp(block.timestamp + 2);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setInt256(int256(-57896044618658097711785492504343953926634992332820282019728792003956564819968));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_int256();
    }
    
    function test_auto_check_string_5() public { 
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setString(unicode"\u00ec\u007b\u004b\u0004\u0099\u00d6\u00d4\u0028\u0033\u00fc\u0081\u0012\u00a6\u00ec\u00ca\u00b1\u00e2\u0058\u00d8\u0007\u00fe\u008d\u002e\u00bc\u00e7\u00e1\u004e\u0066\u0059\u008e\u0072\u0025\u0097\u001d\u00b1\u0061\u00f2\u000f\u0084\u007b\u00b7\u0014\u00a9\u0013\u00a8\u00bf\u0005\u00b5\u0007\u009b\u00bf\u0013\u0051\u00d9\u00d2\u00c5\u00d5\u00d7\u0011\u002b\u00d7\u002d\u0084\u00b7\u009c\u00ad\u00e0\u00a7\u00b9\u0057\u00f6\u0056\u00f1");
        vm.warp(block.timestamp + 577918);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_string();
    }
    
    function test_auto_check_uint256_6() public { 
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(uint256(48243198082023998796783739068115029737990636147430484441469391279441722198374));
        vm.warp(block.timestamp + 9289);
        vm.roll(block.number + 2753);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_uint256();
    }
    
    function test_auto_check_combined_input_7() public { 
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.setCombination(true, uint256(53435416342396889816543380556736678711670008167636542535597596197865583522144), int256(-23584384198052993379951759759418486833068931253234756149882793839258141998640), 0x39129d34023aa5337331a35825efdDC3670A6e4b, unicode"\u00b2\u001f\u0097\u00a3\u00a1\u0048\u0038\u00d5\u00a4\u00e0\u009f\u00f7\u001f\u00bd\u003c\u005c\u0004\u00e1\u000f\u001b\u00e4\u00af\u0069\u009f\u004e\u007e\u0017\u0038\u007b\u0029\u0010\u00bd\u007c\u00ab\u00a0\u0055\u00bf\u0034", bytes(hex"a55910b5b6cd490ff632e82a7484c77d7954149e66e51f3dee90a67897c6499c4d39ca4b7f0e5e43438e1b5c34eb674e71020787a639be81c3525335dad4d448269f57bc188920a72fb68a"));
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_combined_input();
    }
    
}

    