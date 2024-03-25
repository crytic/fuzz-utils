// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/TupleTypes.sol";

contract TupleTypes_Medusa_Test is Test {
    TupleTypes target;

    function setUp() public {
        target = new TupleTypes();
    }
    function test_auto_check_fixedArrStruct_0() public { 
        vm.warp(block.timestamp + 435575);
        vm.roll(block.number + 22050);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.updateFixedArrStruct(TupleTypes.FixedArrayStruct([uint256(115792089237316195423570985008687907853269984665640564039457584007913129639932),uint256(115792089237316195423570985008687907853269984665640564039457584007913129639932)]));
        vm.warp(block.timestamp + 232844);
        vm.roll(block.number + 23885);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_fixedArrStruct();
    }
    
    function test_auto_check_elementaryStruct_1() public { 
        vm.warp(block.timestamp + 360622);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateElementaryStruct(TupleTypes.ElementaryStruct(uint256(29175316911687380930759309888510656085988173163420460649545775222877352067520),int256(-21164295003209541621101510198590587969858211682339266116935257450669986702085),unicode"\u009c\u001a\u005c\u0018\u0048\u00d4\u005c\u008d\u005f\u0048\u007f\u006e\u0078\u00ee\u0027\u0072\u00a8\u005d\u0074\u0085\u0091\u006a\u002a\u0085\u0088\u0010\u00dd\u0080\u005b\u00e5\u0009\u0083",true));
        
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_elementaryStruct();
    }
    
    function test_auto_check_dynamicArrStruct_2() public { 
        uint256[] memory dynSized = new uint256[](14);
        dynSized[0] = uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935);
        dynSized[1] = uint256(98096370441806817573698871381459818563461079213783045489450206923574524803060);
        dynSized[2] = uint256(34475233473930636343615238476605135949136314161457352577138134971813015459878);
        dynSized[3] = uint256(115792089237316195423570985008687907853269984665640564039457584007913129639931);
        dynSized[4] = uint256(4);
        dynSized[5] = uint256(0);
        dynSized[6] = uint256(88906700865723400882972440601446251484736487935903027986303744825451864998990);
        dynSized[7] = uint256(79981703127755918367152031339994152109035625104646770811349809294242118790585);
        dynSized[8] = uint256(115792089237316195423570985008687907853269984665640564039457584007913129639930);
        dynSized[9] = uint256(4);
        dynSized[10] = uint256(2320438134579692491856204578385100410167928267469489416013210399072552794466);
        dynSized[11] = uint256(8);
        dynSized[12] = uint256(93165821999633309265362504262558661301537129910063335505366683314219877275102);
        dynSized[13] = uint256(77106158076561645837665023102536854447407336996176958576905561195777652011024);
vm.warp(block.timestamp + 360621);
        vm.roll(block.number + 16);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.updateDynArrStruct(TupleTypes.DynamicArrayStruct(dynSized));
        vm.warp(block.timestamp + 360621);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_dynamicArrStruct();
    }
    
    function test_auto_check_enum_3() public { 
        vm.warp(block.timestamp + 158791);
        vm.roll(block.number + 9154);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.updateEnum(TupleTypes.Enumerable(2));
        vm.warp(block.timestamp + 251964);
        vm.roll(block.number + 29516);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_enum();
    }
    
    function test_auto_check_nestedStruct_4() public { 
        vm.warp(block.timestamp + 360620);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.updateNestedStruct(TupleTypes.NestedStruct(TupleTypes.ElementaryStruct(uint256(55959353652089764602757503630713338653008349410459555683429152693228280747164),int256(-14651338095212206656602537797121256820789129745955774861053673794273766718966),unicode"\u00fd\u005f\u0012\u00cb\u0004\u00d4\u00bd\u0097\u0022\u007a\u006d\u0016\u0098\u0064\u0091\u00f7\u00ee\u0070\u00ff\u008f\u0015\u009a\u0080\u004e\u00e4\u003e\u0042\u0093\u00ac\u009d\u00b0\u0080\u001a\u0048\u006f\u00e1\u0043\u00b0\u00bf\u003e\u006c\u0028\u00cd\u004d\u00f8",true),uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        vm.warp(block.timestamp + 497821);
        vm.roll(block.number + 23885);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_nestedStruct();
    }
    
}

    