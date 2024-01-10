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
    function test_auto_check_bytes32_0() public { 
        vm.warp(block.timestamp + 308317);
        vm.roll(block.number + 26578);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setBytes32(bytes32(hex"8f8cdfb94685a0285f6884a3c83f688921ef5bb1efcd4ddc01a2395bbb3ef3eb"));
        vm.warp(block.timestamp + 597510);
        vm.roll(block.number + 34347);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_bytes32();
    }
    
    function test_auto_check_combined_input_1() public { 
        vm.warp(block.timestamp + 35011);
        vm.roll(block.number + 20);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setCombination(true, 53199546330680883866342098722173342841888747871862441478556530424043963376, 113078212145816597093331040047546785012958969400039613319782796882727665663, 0xdbbE0d97c0f911bBbff4D66B4d2f5b992F58aFDc, string(hex"275c783030efbfbdefbfbd5c7837665c783030efbfbdefbfbd5c783030efbfbdefbfbdefbfbdefbfbd5c78303065efbfbd2e49efbfbdefbfbdefbfbd5c783766d2bc2635efbfbd5c7830305c7830305c7830305c783133efbfbd75efbfbd3e5c7830305c7830305c78303027"), bytes(hex"b360008f0000da00b3c0dc0027"));
        vm.warp(block.timestamp + 421002);
        vm.roll(block.number + 5);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_combined_input();
    }
    
    function test_auto_check_address_2() public { 
        vm.warp(block.timestamp + 592103);
        vm.roll(block.number + 34807);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setAddress(0xE7D62AAD5028B951Baa93783c8405080bdDD746D);
        vm.warp(block.timestamp + 20);
        vm.roll(block.number + 3);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_address();
    }
    
    function test_auto_check_specific_string_3() public { 
        vm.warp(block.timestamp + 565377);
        vm.roll(block.number + 18560);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_specific_string(string(hex"2727"), string(hex"27efbfbd6aefbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbd4034efbfbd6eefbfbdefbfbdefbfbd5c783030efbfbd5c783030efbfbdefbfbd2644efbfbd5c7830305c72efbfbd37efbfbd5c7830305eefbfbd5c783062606a7c5c783063efbfbdefbfbd4cefbfbd5c74efbfbd48efbfbdefbfbdefbfbd265c783165efbfbd415c783135efbfbd465c7831325c7837665c7830305c783030efbfbdefbfbdefbfbdefbfbd5c783030efbfbd5c78303066efbfbd2cefbfbd5c7837666cefbfbdefbfbd56efbfbd5c7830355c783030efbfbd5c7831655c783030efbfbd2cefbfbdefbfbdefbfbd5c7830305c7830305c78313627"));
    }
    
    function test_auto_check_bytes_4() public { 
        vm.warp(block.timestamp + 461663);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBytes(bytes(hex"007e223600ad009f00000f00"));
        vm.warp(block.timestamp + 7);
        vm.roll(block.number + 6);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_bytes();
    }
    
    function test_auto_check_bool_5() public { 
        vm.warp(block.timestamp + 306911);
        vm.roll(block.number + 52752);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setBool(true);
        vm.warp(block.timestamp + 360622);
        vm.roll(block.number + 56746);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_bool();
    }
    
    function test_auto_check_large_positive_int256_6() public { 
        vm.warp(block.timestamp + 245673);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setInt256(-226156424291633194186662080095093570025917938800079226639565593765455331330);
        
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_large_positive_int256();
    }
    
    function test_auto_check_int256_7() public { 
        vm.warp(block.timestamp + 2);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setInt256(3618502788666131106986593281521497120414687020801267626233049500247285301230);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_int256();
    }
    
    function test_auto_check_bytes32_8() public { 
        vm.warp(block.timestamp + 326989);
        vm.roll(block.number + 44966);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.setBytes32(bytes32(hex"95d7557a949887ee470173b38eecbabfbf4912608b76d8b59c4aa0e60ed4c70d"));
        vm.warp(block.timestamp + 1);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_bytes32();
    }
    
    function test_auto_check_string_9() public { 
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setString(string(hex"277b4b5c7830345c783030efbfbdefbfbdefbfbd2833efbfbdefbfbdefbfbd5c783132efbfbdefbfbdefbfbdcab1efbfbd58efbfbd5c783037efbfbdefbfbd2eefbfbd5c783030efbfbd4e5c78303059efbfbd5c783030255c7830305c783164efbfbdefbfbd5c783066efbfbd7befbfbd5c783134efbfbdefbfbdefbfbd5c783035efbfbd5c783037efbfbdefbfbd5c78313351efbfbdefbfbd5c783030efbfbdefbfbd5c7831312befbfbd2defbfbd5c783030efbfbdefbfbde0a7b957efbfbd56efbfbd27"));
        vm.warp(block.timestamp + 577918);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_string();
    }
    
    function test_auto_check_uint256_10() public { 
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(188449992507906245299936480734824334914025922450900329849489809685319227362);
        vm.warp(block.timestamp + 9289);
        vm.roll(block.number + 2753);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_uint256();
    }
    
    function test_auto_check_large_negative_int256_11() public { 
        vm.warp(block.timestamp + 285739);
        vm.roll(block.number + 44041);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setInt256(-28269553036454149273332760011886696253239742350009903329945699220681916417);
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_large_negative_int256();
    }
    
    function test_auto_check_bytes32_12() public { 
        vm.warp(block.timestamp + 360623);
        vm.roll(block.number + 40603);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.setBytes32(bytes32(hex"7e8ce7efb5e7dc7e92e90ce4f6d12f2e595207cb6a0713328831c8dd5ffd1ec4"));
        vm.warp(block.timestamp + 360623);
        vm.roll(block.number + 23866);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytes32();
    }
    
    function test_auto_check_large_uint256_13() public { 
        vm.warp(block.timestamp + 360621);
        vm.roll(block.number + 25870);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.setUint256(0);
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_large_uint256();
    }
    
    function test_auto_check_combined_input_14() public { 
        vm.warp(block.timestamp + 3);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.setCombination(true, 3261438985741997669466759067183635175272827646950472566869970471061131803, -43445065089186984410186728518648022561024163127792198581349213918826074144270, 0x39129d34023aa5337331a35825efdDC3670A6e4b, string(hex"27efbfbdefbfbd5c7831665c783030efbfbdefbfbdefbfbd4838efbfbdefbfbdefbfbd5c783030efbfbd5c7830305c7831665c7830303c5c5c5c783034efbfbd5c7830665c783030efbfbdefbfbdefbfbdefbfbdefbfbd5c783030efbfbdefbfbd4e7e5c783030295c783130efbfbd7cefbfbdefbfbdefbfbdefbfbd555c7830303427"), bytes(hex"a55910b5b6cd490ff6320000c77d7900149e66e500ee907897c6009c394b7f0e0043008e005ceb6700020087a600be81c3525335dad4d448269f57bc89202f8a"));
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_combined_input();
    }
    
    function test_auto_check_large_uint256_15() public { 
        vm.warp(block.timestamp + 455042);
        vm.roll(block.number + 50771);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.setUint256(56539106072908298546665520023773392506479484700019806659891398441363832852);
        vm.warp(block.timestamp + 2);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_large_uint256();
    }
    
}

    