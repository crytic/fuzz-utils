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
        target.check_specific_string(string(hex""));
    }
    
    function test_auto_check_bytes_2() public { 
        vm.warp(block.timestamp + 461663);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes(bytes(hex"007e223600ad009f00000f00"));
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
        target.setInt256(3618502788666131106986593281521497120414687020801267626233049500247285301230);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_int256();
    }
    
    function test_auto_check_string_5() public { 
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setString(string(hex"7b4b0400efbfbdefbfbdefbfbd2833efbfbdefbfbdefbfbd12efbfbdefbfbdefbfbdcab1efbfbd58efbfbd07efbfbdefbfbd2eefbfbd00efbfbd4e0059efbfbd0025001defbfbdefbfbd0fefbfbd7befbfbd14efbfbdefbfbdefbfbd05efbfbd07efbfbdefbfbd1351efbfbdefbfbd00efbfbdefbfbd112befbfbd2defbfbd00efbfbdefbfbde0a7b957efbfbd56efbfbd"));
        vm.warp(block.timestamp + 577918);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_string();
    }
    
    function test_auto_check_uint256_6() public { 
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(188449992507906245299936480734824334914025922450900329849489809685319227362);
        vm.warp(block.timestamp + 9289);
        vm.roll(block.number + 2753);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_uint256();
    }
    
    function test_auto_check_combined_input_7() public { 
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.setCombination(true, 3261438985741997669466759067183635175272827646950472566869970471061131803, -43445065089186984410186728518648022561024163127792198581349213918826074144270, 0x39129d34023aa5337331a35825efdDC3670A6e4b, string(hex"efbfbdefbfbd1f00efbfbdefbfbdefbfbd4838efbfbdefbfbdefbfbd00efbfbd001f003c5c04efbfbd0f00efbfbdefbfbdefbfbdefbfbdefbfbd00efbfbdefbfbd4e7e002910efbfbd7cefbfbdefbfbdefbfbdefbfbd550034"), bytes(hex"a55910b5b6cd490ff6320000c77d7900149e66e500ee907897c6009c394b7f0e0043008e005ceb6700020087a600be81c3525335dad4d448269f57bc89202f8a"));
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_combined_input();
    }
    
}

    