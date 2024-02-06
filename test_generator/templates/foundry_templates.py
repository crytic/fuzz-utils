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

templates: dict = {
    "CONTRACT": __CONTRACT_TEMPLATE,
    "CALL": __CALL_TEMPLATE,
    "TRANSFER": __TRANSFER__TEMPLATE,
    "EMPTY_CALL": __EMPTY_CALL_TEMPLATE,
    "TEST": __TEST_TEMPLATE,
    "INTERFACE": __INTERFACE_TEMPLATE,
}
