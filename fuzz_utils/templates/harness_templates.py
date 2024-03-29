""" Defines the template strings used to generate fuzzing harnesses"""

__PREFACE: str = """// SPDX-License-Identifier: UNLICENSED
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
///    `directoryName/=directoryName/` to foundry.toml or remappings.txt"""

__HARNESS_TEMPLATE: str = (
    __PREFACE
    + """
///
/// -- [ Running the fuzzers ]
///    * The below commands contain example values which you can modify based
///    on your needs. For further information on the configuration options
///    please reference the fuzzer documentation *
///    Echidna: echidna {{target.path}} --contract {{target.name}} --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-{{target.name}}
///    Medusa: medusa fuzz --target {{target.path}} --assertion-mode --test-limit 100000 --deployment-order "{{target.name}}" --corpus-dir medusa-corpora/corpus-{{target.name}}
///    Foundry: forge test --match-contract {{target.name}}
/// --------------------------------------------------------------------

import "{{remappings["properties"]}}util/PropertiesHelper.sol";
import "{{remappings["properties"]}}util/Hevm.sol";
{% for import in target.imports -%}
{{import}}
{% endfor %}
contract {{target.name}} is {{target.dependencies}} {
    {% for variable in target.variables -%}
    {{variable}}
    {% endfor %}
    {{target.constructor}}
    {%- for function in target.functions %}
    {{function}}
    {%- endfor -%}
}
"""
)

__ACTOR_TEMPLATE: str = (
    __PREFACE
    + """

import "{{remappings["properties"]}}util/PropertiesHelper.sol";
{%- for import in target.imports %}
{{import}}
{% endfor -%}

contract Actor{{target.name}} is {{target.dependencies}} {
    {%- for variable in target.variables %}
    {{variable}}
    {% endfor -%}

    {{target.constructor}}
    {%- for function in target.functions %}
    {{function}}
    {%- endfor -%}
}
"""
)

__ATTACK_DONATE_TEMPLATE: str = (
    __PREFACE
    + """

import "{{remappings["properties"]}}util/PropertiesHelper.sol";
{%- for import in target.imports %}
{{import}}
{% endfor -%}

contract SelfDestructor {
    address owner;

    constructor() payable {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner!");
        _;
    }

    function detonate(address payable to) public onlyOwner {
        require(address(this).balance > 0, "Not enough ETH balance!");
        selfdestruct(to);
    }

    receive() external payable {
        // receive ETH
    }

    fallback() external payable {
        // receiveETH
    }
}

interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 value) external returns (bool);
    function transferFrom(address from, address to, uint256 value) external returns (bool);
}

contract DonationAttack is {{target.dependencies}} {
    {%- for variable in target.variables %}
    {{variable}}
    {% endfor -%}
    address[] targets;
    IERC20[] tokens;

    // Should approve all targets for all tokens
    {{target.constructor}}
    function donateETH(uint256 targetIndex) public payable {
        require(msg.value > 0, "No value provided");
        address target = targets[clampBetween(targetIndex, 0, targets.length - 1)];
        (bool success,) = payable(target).call{value: msg.value}("");
        require(success, "Failed to donate ETH via a receive/fallback function.");
    }

    function selfdestructDonation(uint256 targetIndex) public payable {
        require(msg.value > 0, "No value provided");
        address target = targets[clampBetween(targetIndex, 0, targets.length - 1)];
        SelfDestructor bomb = new SelfDestructor{value: msg.value}();
        bomb.detonate(payable(target));
    }

    function tokenDonation(uint256 targetIndex, uint256 tokenIndex, uint256 amount) public {
        address target = targets[clampBetween(targetIndex, 0, targets.length - 1)];
        IERC20 token = tokens[clampBetween(tokenIndex, 0, tokens.length - 1)];
        token.transfer(target, amount);
    }

    {%- for function in target.functions %}
    {{function}}
    {%- endfor -%}
}
"""
)

templates: dict = {
    "HARNESS": __HARNESS_TEMPLATE,
    "ACTOR": __ACTOR_TEMPLATE,
    "ATTACKS": {"Donation": __ATTACK_DONATE_TEMPLATE},
}
