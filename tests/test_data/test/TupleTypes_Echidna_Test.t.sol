// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "../src/TupleTypes.sol";

contract TupleTypes_Echidna_Test is Test {
    TupleTypes target;

    function setUp() public {
        target = new TupleTypes();
    }
    function test_auto_check_elementaryStruct_0() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateElementaryStruct(TupleTypes.ElementaryStruct(uint256(2148418052922050082),int256(-403949730650687740),string(hex"00"),true));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_elementaryStruct();
    }
    
    function test_auto_check_dynamicArrStruct_1() public { 
        uint256[] memory dynUintArr_0 = new uint256[](1);
		dynUintArr_0[0] = uint256(1);

        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateDynArrStruct(TupleTypes.DynamicArrayStruct(dynUintArr_0));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_dynamicArrStruct();
    }
    
    function test_auto_check_elementaryStruct_2() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateElementaryStruct(TupleTypes.ElementaryStruct(uint256(1),int256(-1),string(hex"00"),true));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_elementaryStruct();
    }
    
    function test_auto_check_fixedArrStruct_3() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateFixedArrStruct(TupleTypes.FixedArrayStruct([uint256(1),uint256(0)]));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_fixedArrStruct();
    }
    
    function test_auto_check_nestedStruct_4() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateNestedStruct(TupleTypes.NestedStruct(TupleTypes.ElementaryStruct(uint256(397488236142920350601414084496085707151145526334912092168084),int256(-1),string(hex"00"),true),uint256(1)));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_nestedStruct();
    }
    
    function test_auto_check_nestedStruct_5() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateNestedStruct(TupleTypes.NestedStruct(TupleTypes.ElementaryStruct(uint256(38453434334052832885604039294228872033049929055),int256(-1),string(hex"00"),true),uint256(1)));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_nestedStruct();
    }
    
    function test_auto_check_inheritedStruct_6() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateInheritedStruct(IStruct.Inherited(uint256(1058821879679255229),true));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_inheritedStruct();
    }
    
    function test_auto_check_enum_7() public { 
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.updateEnum(TupleTypes.Enumerable(2));
        
        vm.prank(0x0000000000000000000000000000000000010000);
        target.check_enum();
    }
    
}

    