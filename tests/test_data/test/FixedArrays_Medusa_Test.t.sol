// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/FixedArrays.sol";

contract FixedArrays_Medusa_Test is Test {
    FixedArrays target;

    function setUp() public {
        target = new FixedArrays();
    }
    function test_auto_check_addressArr_0() public { 
        vm.warp(block.timestamp + 360624);
        vm.roll(block.number + 8683);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.addAddressArr([0xA647ff3c36cFab592509E13860ab8c4F28781a66,0x0000000000000000000000000000000000000000,0xfaa2110aaB3b88abab6bE68A1690869AA2eE3cBa,0x0000000000000000000000000000000000000004]);
        vm.warp(block.timestamp + 360621);
        vm.roll(block.number + 23881);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_addressArr();
    }
    
    function test_auto_check_bytesArr_1() public { 
        vm.warp(block.timestamp + 262160);
        vm.roll(block.number + 28567);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBytesArr([bytes(hex"511ccf0054fa36879bbc3400310e609a4e000b72d13d097dfebb8d6d366a016aebb12fcfbd34a300c4005e0000bf125628d9dd00ab"),bytes(hex"0000dbcf739f5ba178f70083d412d44b0bb0c42f3954b351f11a65ce000039d3a44e7fecfcf16396ce336e0000002cb10108f365322011bb8c535015ee0617917500162c")]);
        vm.warp(block.timestamp + 529389);
        vm.roll(block.number + 57396);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_bytesArr();
    }
    
    function test_auto_check_strArr_2() public { 
        vm.warp(block.timestamp + 345212);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addStrArr([string(hex"0000efbfbdefbfbfefbfbd00efbfbd00efbfbd06efbfbd66efbfbdefbfbd0000"),string(hex"0024c7966154efbfbd28efbfbdefbfbdefbfbdefbfbd335835423200efbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbd00002eefbfbd393500efbfbdefbfbdefbfbd0930efbfbdefbfbd3767")]);
        vm.warp(block.timestamp + 47791);
        vm.roll(block.number + 2625);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strArr();
    }
    
    function test_auto_check_strArr_3() public { 
        vm.warp(block.timestamp + 4);
        vm.roll(block.number + 3);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.addStrArr([string(hex"123600efbfbdefbfbd00efbfbd79210befbfbd0defbfbdefbfbd29efbfbd06efbfbd00efbfbd5eefbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbd4befbfbd347373efbfbdefbfbdefbfbd0e62efbfbdefbfbdefbfbdefbfbd5d7773efbfbdefbfbd5807e5b09cefbfbd2833efbfbdefbfbd75efbfbdefbfbdefbfbdefbfbdefbfbd43efbfbdefbfbdefbfbd7d3a2755003a5900133918efbfbd"),string(hex"6a3befbfbd454defbfbd545f200000efbfbdefbfbd5c2c00efbfbdefbfbdefbfbdefbfbdefbfbdefbfbd0000004befbfbdefbfbd0000c386760000efbfbdefbfbdefbfbd1befbfbd5c38efbfbd006600efbfbdefbfbd")]);
        vm.warp(block.timestamp + 101506);
        vm.roll(block.number + 59400);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strArr();
    }
    
    function test_auto_check_uintArr_4() public { 
        vm.warp(block.timestamp + 360624);
        vm.roll(block.number + 45290);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addUintArr([uint256(3618502788666131106986593281521497120414687020801267626233049500247285301247),uint256(0)]);
        
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_uintArr();
    }
    
    function test_auto_check_strArr_5() public { 
        vm.warp(block.timestamp + 244884);
        vm.roll(block.number + 11399);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addStrArr([string(hex"00efbfbdefbfbdefbfbd5779efbfbd6eefbfbdefbfbd00445b04efbfbd005befbfbddc97efbfbdefbfbd76efbfbdefbfbd00efbfbdefbfbdefbfbd0000efbfbdefbfbdefbfbdd7b554efbfbdefbfbdefbfbdefbfbd7900333defbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbd200044efbfbd056952"),string(hex"717cefbfbdefbfbdefbfbdefbfbd00000000")]);
        vm.warp(block.timestamp + 9);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_strArr();
    }
    
    function test_auto_check_bytesArr_6() public { 
        vm.warp(block.timestamp + 262160);
        vm.roll(block.number + 28567);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBytesArr([bytes(hex"001ccf9054fa36879bbc34df310e009a4e3772d13d007dfe008d6d366a016aeb2f00cfbd34000ac40e8b7d5e5300dabf125600d96f0000"),bytes(hex"00db00739f5ba178f70083d412d44b0b2f3951f11a65ce00505539d3a44eecfcf1e563ce0000bbab002cb10008f309653200bb53501506179100f6162c")]);
        vm.warp(block.timestamp + 488544);
        vm.roll(block.number + 4);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytesArr();
    }
    
    function test_auto_check_addressArr_7() public { 
        vm.warp(block.timestamp + 360620);
        vm.roll(block.number + 13737);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addAddressArr([0x0000000000000000000000000000000000000003,0x0000000000000000000000000000000000000000,0xfFeaeFc0E9cD2A512CDc451671DC7537A748DD4A,0x0000000000000000000000000000000000010000]);
        vm.warp(block.timestamp + 42402);
        vm.roll(block.number + 23884);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_addressArr();
    }
    
    function test_auto_check_addressArr_8() public { 
        vm.warp(block.timestamp + 117639);
        vm.roll(block.number + 40006);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.addAddressArr([0x0000000000000000000000000000000000000003,0x0000000000000000000000000000000000000000,0xaC3B269c1092309beCEF58D80C3AE9b500E56234,0x3D3ECe12cc8e9b93bf941dc9D44238De2DdE39e9]);
        vm.warp(block.timestamp + 543755);
        vm.roll(block.number + 24914);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_addressArr();
    }
    
    function test_auto_check_intArr_9() public { 
        vm.warp(block.timestamp + 360619);
        vm.roll(block.number + 23883);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addIntArr([int256(0),int256(0)]);
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_intArr();
    }
    
    function test_auto_check_bytesArr_10() public { 
        vm.warp(block.timestamp + 139299);
        vm.roll(block.number + 23884);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addBytesArr([bytes(hex"c970d734b040b6f83e9275f99300ac843d84e4253d82b2c9947aa6c84a00a8fb60824db10088cb003fcf005561866c373c0000460af0d1e8ae7e856500aa95a53d470087d92300bf2a9200"),bytes(hex"ac8c138f00886466c911005b961d71ccd664003f8bae00868ef94c007202b56b00b234d90097aa0000d12552a623b89a005c017d00a6bfa460c1")]);
        vm.warp(block.timestamp + 537529);
        vm.roll(block.number + 23881);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_bytesArr();
    }
    
    function test_auto_check_boolArr_11() public { 
        vm.warp(block.timestamp + 439109);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBoolArr([true,false,true]);
        vm.warp(block.timestamp + 134596);
        vm.roll(block.number + 28635);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_boolArr();
    }
    
}

    