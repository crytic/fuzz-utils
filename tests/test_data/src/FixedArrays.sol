pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract FixedArrays --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-fixed-arr --crytic-args "--foundry-ignore-compile"
// Ran from test directory: test-generator ./src/FixedArrays.sol --corpus-dir echidna-corpora/corpus-fixed-arr --contract "FixedArrays" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
contract FixedArrays {

    // ------------------------------
    //         --  bool array  --
    // ------------------------------
    bool[3] boolArr;

    function addBoolArr(bool[3] memory input) public {
        for(uint256 i; i < boolArr.length; i++) {
            boolArr[i] = input[i];
        }  
    }

    function check_boolArr() public {
        if (boolArr[0] && !boolArr[1] && boolArr[2]) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  uint array  --
    // ------------------------------
    uint256[2] uintArr;

    function addUintArr(uint256[2] memory input) public {
        for(uint256 i; i < uintArr.length; i++) {
            uintArr[i] = input[i];
        }
    }

    function check_uintArr() public {
        uint256 sum;
        for(uint256 i; i < uintArr.length; i++) {
            sum += uintArr[i];
        }
        if (sum == 5) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  int array  --
    // ------------------------------
    int256[2] intArr;

    function addIntArr(int256[2] memory input) public {
        for(uint256 i; i < intArr.length; i++) {
            intArr[i] = input[i];
        }
    }

    function check_intArr() public {
        int256 sum;
        for(uint256 i; i < intArr.length; i++) {
            sum += intArr[i];
        }
        if (sum == 5) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  address array  --
    // ------------------------------
    address[4] addressArr;

    function addAddressArr(address[4] memory input) public {
        for(uint256 i; i < addressArr.length; i++) {
            addressArr[i] = input[i];
        }
    }

    function check_addressArr() public {
        uint256 count = 1;
        // At least 3 should be non-zero
        for(uint256 i; i < addressArr.length; i++) {
            if(addressArr[i] != address(0)) {
                count++;
            }
        }

        if (count == addressArr.length) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  string array  --
    // ------------------------------
    string[2] strArr;

    function addStrArr(string[2] memory input) public {
        for(uint256 i; i < strArr.length; i++) {
            strArr[i] = input[i];
        }
    }

    function check_strArr() public {
        if (bytes(strArr[0]).length > 0 && bytes(strArr[1]).length > 0) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  bytes array  --
    // ------------------------------
    bytes[2] bytesArr;

    function addBytesArr(bytes[2] memory input) public {
        for(uint256 i; i < bytesArr.length; i++) {
            bytesArr[i] = input[i];
        }
    }

    function check_bytesArr() public {
        if (bytesArr[0].length > 0 && bytesArr[1].length > 0) {
            assert(false);
        }
    }
}