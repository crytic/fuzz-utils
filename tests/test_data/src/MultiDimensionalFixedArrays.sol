pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract MultiDimensionalFixedArrays --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-multi-fixed-arr --crytic-args "--foundry-ignore-compile"
// Ran from test directory: test-generator ./src/MultiDimensionalFixedArrays.sol --corpus-dir echidna-corpora/corpus-multi-fixed-arr --contract "MultiDimensionalFixedArrays" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
contract MultiDimensionalFixedArrays {
    /* ----- 2-dimensional arrays */

    // ------------------------------
    //         --  bool array  --
    // ------------------------------
    bool[3][2] boolArr;

    function addBoolArr(bool[3][2] memory input) public {
        for (uint256 i; i < boolArr.length; i++) {
            boolArr[i] = input[i];
        }
    }

    function check_boolArr() public {
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
    uint256[2][3] uintArr;

    function addUintArr(uint256[2][3] memory input) public {
        for (uint256 i; i < uintArr.length; i++) {
            uintArr[i] = input[i];
        }
    }

    function check_uintArr() public {
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
    int256[2][1] intArr;

    function addIntArr(int256[2][1] memory input) public {
        for (uint256 i; i < intArr.length; i++) {
            intArr[i] = input[i];
        }
    }

    function check_intArr() public {
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
    address[4][2] addressArr;

    function addAddressArr(address[4][2] memory input) public {
        for (uint256 i; i < addressArr.length; i++) {
            addressArr[i] = input[i];
        }
    }

    function check_addressArr() public {
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
    string[2][1] strArr;

    function addStrArr(string[2][1] memory input) public {
        for (uint256 i; i < strArr.length; i++) {
            strArr[i] = input[i];
        }
    }

    function check_strArr() public {
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
    bytes[2][2] bytesArr;

    function addBytesArr(bytes[2][2] memory input) public {
        for (uint256 i; i < bytesArr.length; i++) {
            bytesArr[i] = input[i];
        }
    }

    function check_bytesArr() public {
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
