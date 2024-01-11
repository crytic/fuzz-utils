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
        target.updateFixedArrStruct(TupleTypes.FixedArrayStruct([uint256(1809251394333065553493296640760748560207343510400633813116524750123642650628),uint256(3533694129556768659166595001485837031654967793751237916243212402585239544)]));
        vm.warp(block.timestamp + 232844);
        vm.roll(block.number + 23885);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_fixedArrStruct();
    }
    
    function test_auto_check_elementaryStruct_1() public { 
        vm.warp(block.timestamp + 360622);
        vm.roll(block.number + 0);
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateElementaryStruct(TupleTypes.ElementaryStruct(uint256(1780720026348106746262164910187417973998301584681424600192002882255697759),int256(-21876362786709361185834415237555471691002639403575881273936853700317071078615),string(hex"001a5c0000efbfbdefbfbd00efbfbd487f6e78000072efbfbdefbfbdefbfbdefbfbd74efbfbdefbfbd002aefbfbdefbfbd00efbfbdefbfbdefbfbdefbfbd10005befbfbdefbfbd00"),true));
        
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_elementaryStruct();
    }
    
    function test_auto_check_dynamicArrStruct_2() public { 
        uint256[] memory dynuint256Arr_0 = new uint256[](14);
		dynuint256Arr_0[0] = uint256(3618502788666131106986593281521497120414687020801267626233049500247285301246);
		dynuint256Arr_0[1] = uint256(766377894076615762294522432667654832527039681357680042886329741590425975023);
		dynuint256Arr_0[2] = uint256(16833610094692693527155878162404851537664215899149097938055729966705573958);
		dynuint256Arr_0[3] = uint256(113078212145816597093331040047546785012958969400039613319782796882727665665);
		dynuint256Arr_0[4] = uint256(3618502788666131106986593281521497120414687020801267626233049500247285301250);
		dynuint256Arr_0[5] = uint256(0);
		dynuint256Arr_0[6] = uint256(2713217189505719021086805438276557967673843015622040648996085962690791773);
		dynuint256Arr_0[7] = uint256(156214263921398278060843811210926078337960205282513224240917596277816638263);
		dynuint256Arr_0[8] = uint256(0);
		dynuint256Arr_0[9] = uint256(0);
		dynuint256Arr_0[10] = uint256(4532105731600961898156649567158399238609234897401346515650801560688579675);
		dynuint256Arr_0[11] = uint256(56539106072908298546665520023773392506479484700019806659891398441363832832);
		dynuint256Arr_0[12] = uint256(181964496093033807158911141137809885354564706855592452158919303348085697758);
		dynuint256Arr_0[13] = uint256(301195929986568929053378996494284587685184910141316244441037348421006453165);
vm.warp(block.timestamp + 360621);
        vm.roll(block.number + 16);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.updateDynArrStruct(TupleTypes.DynamicArrayStruct(dynuint256Arr_0));
        vm.warp(block.timestamp + 360621);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.check_dynamicArrStruct();
    }
    
    function test_auto_check_enum_3() public { 
        vm.warp(block.timestamp + 158791);
        vm.roll(block.number + 9154);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.updateEnum(TupleTypes.Enumerable(0));
        vm.warp(block.timestamp + 251964);
        vm.roll(block.number + 29516);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_enum();
    }
    
    function test_auto_check_nestedStruct_4() public { 
        vm.warp(block.timestamp + 360620);
        vm.roll(block.number + 1);
        vm.prank(0x0000000000000000000000000000000000020000);
        target.updateNestedStruct(TupleTypes.NestedStruct(TupleTypes.ElementaryStruct(uint256(874364900813902571918085994229895916453255459538430557553580510831691886679),int256(49385132393605463265121312115022778824453542441252338466017534284003595185),string(hex"005fefbfbd00d4bdefbfbd22006d000000efbfbdefbfbd70efbfbdefbfbdefbfbd15efbfbdefbfbdefbfbd4eefbfbd3e42efbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbdefbfbd006fefbfbd00efbfbd003e6c00efbfbdefbfbd4d00"),true),uint256(226156424291633194186662080095093570025917938800079226639565593765455331334)));
        vm.warp(block.timestamp + 497821);
        vm.roll(block.number + 23885);
        vm.prank(0x0000000000000000000000000000000000030000);
        target.check_nestedStruct();
    }
    
}

    