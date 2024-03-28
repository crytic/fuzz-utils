pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract BasicTypes --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-basic --crytic-args "--foundry-ignore-compile"
// Ran from test directory: fuzz-utils ./src/BasicTypes.sol --corpus-dir echidna-corpora/corpus-basic --contract "BasicTypes" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
contract BasicTypes {

    // ------------------------------
    //         --  bool  --
    // ------------------------------
    bool first;

    function setBool(bool set) public {
        first = set;
    }

    function check_bool() public {
        if (first) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  uint  --
    // ------------------------------
    uint256 _uint256 = 3;

    function setUint256(uint256 input) public {
        _uint256 = input;
    }

    function check_uint256() public {
        if (_uint256 % 2 == 0) {
            assert(false);
        }
    }

    function check_large_uint256() public {
        if (_uint256 == type(uint256).max) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  int  --
    // ------------------------------
    int256 _int256 = 3;

    function setInt256(int256 input) public {
        _int256 = input;
    }

    function check_int256() public {
        if (_int256 % 2 == 0) {
            assert(false);
        }
    }

    function check_large_positive_int256() public {
        if (_int256 == type(int256).max) {
            assert(false);
        }
    }

    function check_large_negative_int256() public {
        if (_int256 == type(int256).min) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  address  --
    // ------------------------------
    address providedAddress;

    function setAddress(address input) public {
        require(input != address(0));
        providedAddress = input;
    }

    function check_address() public {
        if (providedAddress != address(0)) {
            assert(false);
        }
    }
    // ------------------------------
    //         --  string  --
    // ------------------------------
    string providedString;

    function setString(string memory input) public {
        require(bytes(input).length > 20);
        providedString = input;
    }

    function check_string() public {
        if (bytes(providedString).length > 20) {
            assert(false);
        }
    }

    function check_specific_string(string memory provided) public {
        require(bytes(provided).length > 0);
        if (keccak256(bytes(provided)) == keccak256(bytes("TEST_STRING"))) {
            assert(false);
        }
    }

    // ------------------------------
    //         --  bytes  --
    // ------------------------------
    bytes providedBytes;
    bytes32 providedBytes32;

    // TODO bytes32, etc.
    function setBytes(bytes memory input) public {
        require(input.length > 20);
        providedBytes = input;
    }

    function check_bytes() public {
        if (providedBytes.length > 20) {
            assert(false);
        }
    }

    /// @notice bytes32 has decoding issues right now 
    /* function setBytes32(bytes32 input) public {
        require(input != bytes32(0));
        providedBytes32 = input;
    }

    function check_bytes32() public {
        if (providedBytes32 != bytes32(0)) {
            assert(false);
        }
    }  */

    // ------------------------------
    //         --  combination  --
    // ------------------------------
    bool combBool;
    uint256 combUint256;
    int256 combInt256;
    address combAddress;
    string combString;
    bytes combBytes;

    function setCombination(bool bool_input, uint256 unsigned_input, int256 signed_input, address address_input, string memory str_input, bytes memory bytes_input) public {
        combBool = bool_input;
        combUint256 = unsigned_input;
        combInt256 = signed_input;
        combAddress = address_input;
        combString = str_input;
        combBytes = bytes_input;
    }

    function check_combined_input() public {
        if (combBool && combUint256 > 0 && combInt256 < 0 && combAddress != address(0) && bytes(combString).length > 0 && combBytes.length > 0) {
            assert(false);
        }
    }
}