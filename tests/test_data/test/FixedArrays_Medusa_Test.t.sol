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
        target.addBytesArr([bytes(hex"511ccf9054fa36879bbc34df67310e609a4e370b72d13d097dfebb8d6d366a016aebb12fddcfbd34a30ac40e8b7d5e536edabf125628d96fdda3ab"),bytes(hex"8300dbcf739f5ba178f7d783d412d44b0bb0c42f3954b351f11a65cea4505539d3a44e7f9decfcf1e56396ce336ebbab452cb1015708f30965322011bb8c535015ee06179175f6162c")]);
        vm.warp(block.timestamp + 529389);
        vm.roll(block.number + 57396);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_bytesArr();
    }
    
    function test_auto_check_strArr_2() public { 
        vm.warp(block.timestamp + 345212);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addStrArr([unicode"\u00b4\u0039\u009b\u00b4\u0093\u00f1\u0003\u00ee\u0006\u00d2\u0066\u007e\u0087\u0041\u006f",unicode"\u00f4\u0024\u00c7\u0096\u0061\u0054\u00ae\u0028\u00ca\u00ff\u00b1\u00f5\u0033\u0058\u0035\u0042\u0032\u0002\u00aa\u00af\u00f4\u0085\u00f7\u00de\u0072\u00d0\u002e\u0097\u0039\u000d\u0035\u001d\u00b9\u00eb\u0009\u0030\u00d1\u0037\u0067"]);
        vm.warp(block.timestamp + 47791);
        vm.roll(block.number + 2625);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strArr();
    }
    
    function test_auto_check_strArr_3() public { 
        vm.warp(block.timestamp + 4);
        vm.roll(block.number + 3);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.addStrArr([unicode"\u0012\u0036\u00c5\u0090\u00ac\u0090\u0082\u0079\u006e\u0021\u000b\u00fc\u000d\u00dd\u0029\u00b6\u0006\u00fa\u00c9\u0098\u00ba\u005e\u0096\u00ac\u008b\u00a2\u0093\u0061\u004b\u00db\u0034\u0073\u0073\u00f2\u00b3\u00d2\u000e\u0062\u0099\u00ad\u005d\u0077\u0073\u00c1\u006c\u0058\u0007\u00e5\u00b0\u009c\u009b\u0028\u0033\u00a7\u0075\u008d\u00d4\u00d8\u00c5\u0043\u00a9\u0095\u007d\u003a\u0027\u0055\u0032\u003a\u0059\u0077\u0013\u0039\u0018\u00de",unicode"\u006a\u003b\u00c2\u0045\u004d\u00d9\u00a8\u0054\u005f\u0020\u00bb\u00a2\u0091\u00d5\u005c\u002c\u0014\u0084\u00b9\u0087\u0093\u009b\u005a\u0091\u004b\u00d7\u00d2\u00e7\u00c3\u0086\u0076\u0053\u00ae\u00d7\u00cd\u001b\u005c\u00e0\u005c\u0038\u008c\u00dc\u00af\u0066\u0026\u00ca"]);
        vm.warp(block.timestamp + 101506);
        vm.roll(block.number + 59400);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_strArr();
    }
    
    function test_auto_check_strArr_4() public { 
        vm.warp(block.timestamp + 244884);
        vm.roll(block.number + 11399);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addStrArr([unicode"\u00e3\u00bd\u0057\u0079\u00b2\u006e\u0045\u00fb\u007d\u0044\u005b\u0004\u00ef\u00a0\u005b\u00e1\u00dc\u0097\u00d7\u0076\u00a7\u00f6\u00c5\u00ee\u00a5\u00dd\u0000\u00f6\u00bd\u0087\u00d7\u00b5\u0054\u00ac\u00f9\u0079\u0042\u0033\u003d\u00bf\u0081\u0099\u00bc\u00e0\u00d1\u0020\u005d\u0044\u00d6\u0005\u0069\u0052",unicode"\u0071\u0050\u007c\u00f1\u0056\u0097\u00e9\u000b\u0033\u007a"]);
        vm.warp(block.timestamp + 9);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_strArr();
    }
    
    function test_auto_check_bytesArr_5() public { 
        vm.warp(block.timestamp + 262160);
        vm.roll(block.number + 28567);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.addBytesArr([bytes(hex"511ccf9054fa36879bbc34df67310e609a4e370b72d13d097dfebb8d6d366a016aebb12fddcfbd34a30ac40e8b7d5e536edabf125628d96fdda3ab"),bytes(hex"8300dbcf739f5ba178f7d783d412d44b0bb0c42f3954b351f11a65cea4505539d3a44e7f9decfcf1e56396ce336ebbab452cb1015708f30965322011bb8c535015ee06179175f6162c")]);
        vm.warp(block.timestamp + 488544);
        vm.roll(block.number + 4);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_bytesArr();
    }
    
    function test_auto_check_addressArr_6() public { 
        vm.warp(block.timestamp + 360620);
        vm.roll(block.number + 13737);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addAddressArr([0x0000000000000000000000000000000000000003,0x0000000000000000000000000000000000000000,0xfFeaeFc0E9cD2A512CDc451671DC7537A748DD4A,0x0000000000000000000000000000000000010000]);
        vm.warp(block.timestamp + 42402);
        vm.roll(block.number + 23884);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_addressArr();
    }
    
    function test_auto_check_addressArr_7() public { 
        vm.warp(block.timestamp + 117639);
        vm.roll(block.number + 40006);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.addAddressArr([0x0000000000000000000000000000000000000003,0x0000000000000000000000000000000000000000,0xaC3B269c1092309beCEF58D80C3AE9b500E56234,0x3D3ECe12cc8e9b93bf941dc9D44238De2DdE39e9]);
        vm.warp(block.timestamp + 543755);
        vm.roll(block.number + 24914);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_addressArr();
    }
    
    function test_auto_check_bytesArr_8() public { 
        vm.warp(block.timestamp + 139299);
        vm.roll(block.number + 23884);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.addBytesArr([bytes(hex"c9707fd734b040b6f83e9275f993c370ac9c843d84e4253d82b2c9947aa6b5c84ae107a8fb60824db1c388cbb23fcf46f0551461866c373c00bc46c00af0d1e8ae7e856558aafaa2278b95a53d473cbb87d923dbfcbf2a92cbfecb"),bytes(hex"ac8c138f86ad886466c911b05b961d71cc55d66450eb3f8bae36a7868ef94c00907202b56ba6b2be34d9f897e8aaf72aded12552a63823b89a995c017d6924a6bbbfa460c1d2")]);
        vm.warp(block.timestamp + 537529);
        vm.roll(block.number + 23881);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_bytesArr();
    }
    
    function test_auto_check_boolArr_9() public { 
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

    