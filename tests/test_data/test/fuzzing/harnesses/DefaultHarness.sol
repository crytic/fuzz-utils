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
///    Echidna: echidna  --contract DefaultHarness --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-DefaultHarness
///    Medusa: medusa fuzz --target  --assertion-mode --test-limit 100000 --deployment-order "DefaultHarness" --corpus-dir medusa-corpora/corpus-DefaultHarness
///    Foundry: forge test --match-contract DefaultHarness
/// --------------------------------------------------------------------

import "properties/util/PropertiesHelper.sol";
import "src/BasicTypes.sol";
import "../actors/ActorDefault.sol";

contract DefaultHarness is PropertiesAsserts {
    BasicTypes basictypes;
    ActorDefault[] Default_actors;
    
    constructor() {
        basictypes = new BasicTypes();
        for(uint256 i; i < 3; i++) {
            Default_actors.push(new ActorDefault(address(basictypes)));
        }
    }

    // -------------------------------------
    // ActorDefault functions
    // test/fuzzing/actors/ActorDefault.sol
    // -------------------------------------

    function setBool(uint256 actorIndex, bool set) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setBool(set);
    }

    function check_bool(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_bool();
    }

    function setUint256(uint256 actorIndex, uint256 input) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setUint256(input);
    }

    function check_uint256(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_uint256();
    }

    function check_large_uint256(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_large_uint256();
    }

    function setInt256(uint256 actorIndex, int256 input) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setInt256(input);
    }

    function check_int256(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_int256();
    }

    function check_large_positive_int256(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_large_positive_int256();
    }

    function check_large_negative_int256(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_large_negative_int256();
    }

    function setAddress(uint256 actorIndex, address payable input) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setAddress(input);
    }

    function check_address(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_address();
    }

    function setString(uint256 actorIndex, string memory input) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setString(input);
    }

    function check_string(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_string();
    }

    function check_specific_string(uint256 actorIndex, string memory provided) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_specific_string(provided);
    }

    function setBytes(uint256 actorIndex, bytes memory input) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setBytes(input);
    }

    function check_bytes(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_bytes();
    }

    function setCombination(uint256 actorIndex, bool bool_input, uint256 unsigned_input, int256 signed_input, address payable address_input, string memory str_input, bytes memory bytes_input) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.setCombination(bool_input, unsigned_input, signed_input, address_input, str_input, bytes_input);
    }

    function check_combined_input(uint256 actorIndex) public {
        ActorDefault selectedActor = Default_actors[clampBetween(actorIndex, 0, Default_actors.length - 1)];
        selectedActor.check_combined_input();
    }
}