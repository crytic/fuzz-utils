pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract TupleTypes --test-mode assertion --test-limit 100000 --corpus-dir corpus-struct --crytic-args "--foundry-ignore-compile"
// Ran from test directory: test-generator ./src/TupleTypes.sol --corpus-dir corpus-struct --contract "TupleTypes" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
contract TupleTypes {
    struct ElementaryStruct {
        uint256 uintType;
        int256 intType;
        string stringType;
        bool boolType;
    }

    struct NestedStruct {
        ElementaryStruct structType;
        uint256 uintType;
    }

    struct FixedArrayStruct {
        uint256[2] fixedSized;
    }

    struct DynamicArrayStruct {
        uint256[] dynSized;
    }

    enum Enumerable {
        ZERO,
        ONE,
        TWO
    }

    ElementaryStruct testStruct;
    NestedStruct nestedStruct;
    FixedArrayStruct fixedArrayStruct;
    DynamicArrayStruct dynArrayStruct;
    Enumerable testEnum;

    // ------------------------------------
    //         --  Elementary struct  --
    // ------------------------------------

    function updateElementaryStruct(ElementaryStruct memory input) public {
        testStruct = input;
    }

    function check_elementaryStruct() public view {
        ElementaryStruct memory test = testStruct;
        if (
            test.uintType > 0 &&
            test.intType < 0 &&
            bytes(test.stringType).length > 0 &&
            test.boolType
        ) {
            assert(false);
        }
    }

    // ------------------------------------
    //         --  Nested struct  --
    // ------------------------------------
    function updateNestedStruct(NestedStruct memory input) public {
        nestedStruct = input;
    }

    function check_nestedStruct() public view {
        NestedStruct memory test = nestedStruct;
        if (
            test.structType.boolType &&
            test.structType.intType < 0 &&
            bytes(test.structType.stringType).length > 0 &&
            test.structType.uintType > 0 &&
            test.uintType > 0
        ) {
            assert(false);
        }
    }

    // ------------------------------------
    //         --  Fixed Arr struct  --
    // ------------------------------------
    function updateFixedArrStruct(FixedArrayStruct memory input) public {
        fixedArrayStruct = input;
    }

    function check_fixedArrStruct() public view {
        FixedArrayStruct memory test = fixedArrayStruct;
        uint256 count;
        for (uint256 i; i < test.fixedSized.length; i++) {
            if (test.fixedSized[i] > 0) {
                count++;
            }
        }

        if (count > 0) {
            assert(false);
        }
    }

    // ------------------------------------
    //         --  Dyn Arr struct  --
    // ------------------------------------
    function updateDynArrStruct(DynamicArrayStruct memory input) public {
        dynArrayStruct = input;
    }

    function check_dynamicArrStruct() public view {
        DynamicArrayStruct memory test = dynArrayStruct;
        uint256 count;
        for (uint256 i; i < test.dynSized.length; i++) {
            if (test.dynSized[i] > 0) {
                count++;
            }
        }

        if (count > 0) {
            assert(false);
        }
    }

    // ------------------------------------
    //         --  Enum  --
    // ------------------------------------

    function updateEnum(Enumerable input) public {
        testEnum = input;
    }

    function check_enum() public view {
        if (testEnum == Enumerable.TWO) {
            assert(false);
        }
    }
}
