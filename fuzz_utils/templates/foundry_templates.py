""" Defines the template strings used to generate the test file"""

__CONTRACT_TEMPLATE: str = """// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;
import "forge-std/Test.sol";
import "forge-std/console2.sol";
import "{{file_path}}";

contract {{target_name}}_{{fuzzer}}_Test is Test {
    {{target_name}} target;

    function setUp() public {
        target = new {{target_name}}();
        {%- if amount > 0 -%}
        vm.deal(address(target), {{amount}});
        {%- endif %}
    }
    {%- for test in tests -%}
    {{test}}
    {% endfor %}
}

    """

__CALL_TEMPLATE: str = """
        {%- if has_delay -%}
        vm.warp(block.timestamp + {{time_delay}});
        vm.roll(block.number + {{block_delay}});
        {%- endif %}
        vm.prank({{caller}});
        {%- if value > 0 %}
        target.{{function_name}}{value: {{value}}}({{function_parameters}});
        {%- else %}
        target.{{function_name}}({{function_parameters}});
        {%- endif %}
"""

__TRANSFER__TEMPLATE: str = """
        {%- if has_delay -%}
        vm.warp(block.timestamp + {{time_delay}});
        vm.roll(block.number + {{block_delay}});
        {%- endif %}
        vm.prank({{caller}});
        (bool success, ) = payable(address(target)).call{value: {{value}}}("");
        require(success, "Low level call failed.");
"""

__EMPTY_CALL_TEMPLATE: str = """
        // This is an empty call which just increases the block number and timestamp
        vm.warp(block.timestamp + {{time_delay}});
        vm.roll(block.number + {{block_delay}});
    """

__TEST_TEMPLATE: str = """
    function test_auto_{{function_name}}() public { {% for call in call_list %}
        {{call}}{% endfor %}
    }"""

__INTERFACE_TEMPLATE: str = """
interface I{target_name} {
    {% for struct in structs -%}
    {{struct}}
    {% endfor %}
    {% for function in functions -%}
    {{function}}
    {% endfor %}
}
"""

__HARNESS_TEMPLATE: str = """// SPDX-License-Identifier: UNLICENSED
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
///    Echidna: echidna {{harness.path}} --contract {{harness.name}} --test-mode assertion --test-limit 100000 --corpus-dir echidna-corpora/corpus-{{harness.name}}
///    Medusa: medusa fuzz --target {{harness.path}} --assertion-mode --test-limit 100000 --deployment-order "{{harness.name}}" --corpus-dir medusa-corpora/corpus-{{harness.name}}
///    Foundry: forge test --match-contract {{harness.name}}
/// --------------------------------------------------------------------

import "properties/util/PropertiesHelper.sol";
{% for import in harness.imports -%}
{{import}}
{% endfor %}
contract {{harness.name}} is {{harness.dependencies}} {
    {% for variable in harness.variables -%}
    {{variable}}
    {% endfor %}
    {{harness.constructor}}
    {%- for function in harness.functions %}
    {{function}}
    {%- endfor -%}
}
"""

__ACTOR_TEMPLATE: str = """// SPDX-License-Identifier: UNLICENSED
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
/// --------------------------------------------------------------------

import "properties/util/PropertiesHelper.sol";
{%- for import in actor.imports %}
{{import}}
{% endfor -%}

contract Actor{{actor.name}} is {{actor.dependencies}} {
    {%- for variable in actor.variables %}
    {{variable}}
    {% endfor -%}

    {{actor.constructor}}
    {%- for function in actor.functions %}
    {{function}}
    {%- endfor -%}
}
"""

templates: dict = {
    "CONTRACT": __CONTRACT_TEMPLATE,
    "CALL": __CALL_TEMPLATE,
    "TRANSFER": __TRANSFER__TEMPLATE,
    "EMPTY_CALL": __EMPTY_CALL_TEMPLATE,
    "TEST": __TEST_TEMPLATE,
    "INTERFACE": __INTERFACE_TEMPLATE,
    "HARNESS": __HARNESS_TEMPLATE,
    "ACTOR": __ACTOR_TEMPLATE,
}
