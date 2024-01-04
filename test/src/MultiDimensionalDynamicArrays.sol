pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract MultiDimensionalDynamicArrays --test-mode assertion --test-limit 100000 --corpus-dir corpus-multi-dyn-arr --crytic-args "--foundry-ignore-compile"
// Ran from test directory: test-generator ./src/MultiDimensionalDynamicArrays.sol --corpus-dir test/corpus-multi-dyn-arr --contract "MultiDimensionalDynamicArrays" --test-directory "./test/test/" --inheritance-path "../src/" --fuzzer echidna
contract MultiDimensionalDynamicArrays {
    // ----- 2-dimensional arrays ------

    // ------------------------------
    //         --  bool array  --
    // ------------------------------
    bool[][] boolArr;

    function addBoolArr(bool[][] memory input) public {
        for (uint256 i; i < input.length; i++) {
            boolArr[i] = input[i];
        }
    }

    function check_boolArr() public view {
        uint256 count;
        for (uint256 i; i < boolArr.length; i++) {
            for (uint256 j; j < boolArr[i].length; i++) {
                if (boolArr[i][j]) {
                    count++;
                }
            }
        }

        if (count > 3) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  uint array  --
    // ------------------------------
    uint256[][] uintArr;

    function addUintArr(uint256[][] memory input) public {
        for (uint256 i; i < input.length; i++) {
            uintArr[i] = input[i];
        }
    }

    function check_uintArr() public view {
        uint256 sum;
        for (uint256 i; i < uintArr.length; i++) {
            for (uint256 j; i < uintArr[i].length; i++) {
                sum += uintArr[i][j];
            }
        }
        if (sum > 10) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  int array  --
    // ------------------------------
    int256[][] intArr;

    function addIntArr(int256[][] memory input) public {
        for (uint256 i; i < input.length; i++) {
            intArr[i] = input[i];
        }
    }

    function check_intArr() public view {
        int256 sum;
        for (uint256 i; i < intArr.length; i++) {
            for (uint256 j; j < intArr[i].length; i++) {
                sum += intArr[i][j];
            }
        }
        if (sum == 5) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  address array  --
    // ------------------------------
    address[][] addressArr;

    function addAddressArr(address[][] memory input) public {
        for (uint256 i; i < input.length; i++) {
            addressArr[i] = input[i];
        }
    }

    function check_addressArr() public view {
        uint256 count = 1;
        // At least 3 should be non-zero
        for (uint256 i; i < addressArr.length; i++) {
            for (uint256 j; j < addressArr[i].length; i++) {
                if (addressArr[i][j] != address(0)) {
                    count++;
                }
            }
        }

        if (count > addressArr.length) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  string array  --
    // ------------------------------
    string[][] strArr;

    function addStrArr(string[][] memory input) public {
        for (uint256 i; i < input.length; i++) {
            strArr[i] = input[i];
        }
    }

    function check_strArr() public view {
        uint256 count;
        for (uint256 i; i < strArr.length; i++) {
            for (uint256 j; j < strArr[i].length; j++) {
                if (bytes(strArr[i][j]).length > 0) {
                    count++;
                }
            }
        }
        if (count == 2) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  bytes array  --
    // ------------------------------
    bytes[][] bytesArr;

    function addBytesArr(bytes[][] memory input) public {
        for (uint256 i; i < input.length; i++) {
            bytesArr[i] = input[i];
        }
    }

    function check_bytesArr() public view {
        uint256 count;
        for (uint256 i; i < bytesArr.length; i++) {
            for (uint256 j; j < bytesArr[i].length; j++) {
                if (bytesArr[i][j].length > 0) {
                    count++;
                }
            }
        }

        if (count == 4) {
            assert(false);
        }
    }
}
