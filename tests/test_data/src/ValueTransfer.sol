pragma solidity ^0.8.0;

// Ran from tests/test_data/ directory: echidna . --contract ValueTransfer --test-mode assertion --test-limit 1000000 --corpus-dir echidna-corpora/corpus-value
// Ran from tests/test_data/ directory: test-generator ./src/ValueTransfer.sol --corpus-dir echidna-corpora/corpus-value --contract "ValueTransfer" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
contract ValueTransfer {

    function check_balance() public {
        if (address(this).balance > 0) {
            assert(false);
        }
    }

    fallback() external payable {
        // Just receive Ether
    }
}