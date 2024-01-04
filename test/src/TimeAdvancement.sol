pragma solidity ^0.8.0;

// Ran from test directory: echidna . --contract TimeAdvancement --test-mode assertion --test-limit 10000 --corpus-dir echidna-corpora/corpus-time --crytic-args "--foundry-ignore-compile"
// Ran from test directory: test-generator ./src/TupleTypes.sol --corpus-dir echidna-corpora/corpus-struct --contract "TupleTypes" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna

contract TimeAdvancement {
    bool timeSet;
    bool blockSet;
    uint256 timestamp;
    uint256 blockNumber;

    // ------------------------------
    //         --  timestamp  --
    // ------------------------------

    function setTimestamp() public {
        timeSet = true;
        timestamp = block.timestamp;
    }

    function check_timestamp() view public {
        if (timeSet) {
            assert(block.timestamp <= timestamp);
        }
    }
    // ------------------------------
    //         --  block number  --
    // ------------------------------

    function setBlock() public {
        blockSet = true;
        blockNumber = block.number;
    }

    function check_block() view public {
        if (blockSet) {
            assert(block.number <= blockNumber);
        }
    }

    // ------------------------------
    //         --  both  --
    // ------------------------------

    function check_time_and_block() view public {
        if (blockSet && timeSet) {
            assert(block.timestamp <= timestamp || block.number <= blockNumber);
        }
    }

}