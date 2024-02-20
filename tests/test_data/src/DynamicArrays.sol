pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract DynamicArrays --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-dyn-arr --crytic-args "--foundry-ignore-compile"
// Ran from test directory: fuzz-utils ./src/DynamicArrays.sol --corpus-dir echidna-corpora/corpus-dyn-arr --contract "DynamicArrays" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
contract DynamicArrays {

    // ------------------------------
    //         --  bool array  --
    // ------------------------------
    bool[] boolDynArr;

    function addBoolArr(bool[] memory input) public {
        for(uint256 i; i < input.length; i++) {
            boolDynArr.push(input[i]);
        }  
    }

    function check_boolArr() public {
        uint256 count;
        for(uint256 i; i < boolDynArr.length; i++) {
            if (boolDynArr[i]) {
                count++;
            }
        }

        if (count > 3) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  uint array  --
    // ------------------------------
    uint256[] uintDynArr;

    function addUintArr(uint256[] memory input) public {
        for (uint256 i; i < input.length; i++) {
            uintDynArr.push(input[i]);
        }
    }

    function check_uintDynArr() public {
        uint256 sum;
        for(uint256 i; i < uintDynArr.length; i++) {
            sum += uintDynArr[i];
        }

        if (sum != 0 && sum % 3 == 0) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  int array  --
    // ------------------------------
    int256[] intDynArr;

    function addIntArr(int256[] memory input) public {
        for (uint256 i; i < input.length; i++) {
            intDynArr.push(input[i]);
        }
    }

    function check_intDynArr() public {
        int256 sum;
        for(uint256 i; i < intDynArr.length; i++) {
            sum += intDynArr[i];
        }

        if (sum != 0 && sum % 3 == 0) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  address array  --
    // ------------------------------
    address[] addressDynArr;

    function addAddressArr(address[] memory input) public {
        for(uint256 i; i < input.length; i++) {
            addressDynArr.push(input[i]);
        }
    }

    function check_addressDynArr() public {
        uint256 count = 0;
        // At least 3 should be non-zero
        for(uint256 i; i < addressDynArr.length; i++) {
            if(addressDynArr[i] != address(0)) {
                count++;
            }
        }

        if (count > 3) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  string array  --
    // ------------------------------
    string[] strDynArr;

    function addStrArr(string[] memory input) public {
        for(uint256 i; i < input.length; i++) {
            strDynArr.push(input[i]);
        }
    }

    function check_strDynArr() public {
        uint256 count;
        for(uint256 i; i < strDynArr.length; i++) {
            if (bytes(strDynArr[i]).length > 0) {
                count++;
            }
        }
        if (count > 3) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  bytes array  --
    // ------------------------------
    bytes[] bytesDynArr;

    function addBytesArr(bytes[] memory input) public {
        for(uint256 i; i < input.length; i++) {
            bytesDynArr.push(input[i]);
        }
    }

    function check_bytesArr() public {
        uint256 count;
        for(uint256 i; i < bytesDynArr.length; i++) {
            if(bytesDynArr[i].length > 0) {
                count++;
            }
        }

        if (count > 3) {
            assert(false);
        }
    }
}