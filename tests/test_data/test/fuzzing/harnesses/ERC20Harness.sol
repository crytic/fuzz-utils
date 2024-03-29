// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

/// --------------------------------------------------------------------
/// @notice This file was automatically generated using fuzz-utils 
///
/// -- [ Prerequisites ]
/// 1. The generated contracts depend on crytic/properties utilities
///    which need to be installed, this can be done by running:
///    `forge install crytic/properties`
/// 2. Absolute paths are used for contract inheritance, requiring
///    the main directory that contains the contracts to be added to
///    the Foundry remappings. This can be done by adding:
///    `directoryName/=directoryName/` to foundry.toml or remappings.txt
///
/// -- [ Running the fuzzers ]
///    * The below commands contain example values which you can modify based
///    on your needs. For further information on the configuration options
///    please reference the fuzzer documentation *
///    Echidna: echidna  --contract ERC20Harness --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-ERC20Harness
///    Medusa: medusa fuzz --target  --assertion-mode --test-limit 100000 --deployment-order "ERC20Harness" --corpus-dir medusa-corpora/corpus-ERC20Harness
///    Foundry: forge test --match-contract ERC20Harness
/// --------------------------------------------------------------------

import "properties/util/PropertiesHelper.sol";
import "src/TestERC20.sol";
import "../actors/ActorDefault.sol";

contract ERC20Harness is PropertiesAsserts {
    TestERC20 testerc20;
    ActorDefault[] Default_actors;
    
    constructor() {
        testerc20 = new TestERC20();
        for(uint256 i; i < 3; i++) {
            Default_actors.push(new ActorDefault(address(testerc20)));
        }
    }

    // -------------------------------------
    // ActorDefault functions
    // test/fuzzing/actors/ActorDefault.sol
    // -------------------------------------

    function approve(uint256 actorIndex, address payable spender, uint256 amount) public returns (bool) {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.approve(spender, amount);
    }

    function transfer(uint256 actorIndex, address payable to, uint256 amount) public returns (bool) {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.transfer(to, amount);
    }

    function transferFrom(uint256 actorIndex, address payable from, address payable to, uint256 amount) public returns (bool) {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.transferFrom(from, to, amount);
    }

    function permit(uint256 actorIndex, address payable owner, address payable spender, uint256 value, uint256 deadline, uint8 v, bytes32 r, bytes32 s) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.permit(owner, spender, value, deadline, v, r, s);
    }
}