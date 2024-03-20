""" Generates a template fuzzer harness for a smart contract target """
# type: ignore[misc] # Ignores 'Any' input parameter
import os
from dataclasses import dataclass

from slither import Slither
from slither.core.declarations.contract import Contract
from slither.core.declarations.function_contract import FunctionContract
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.solidity_types.array_type import ArrayType
import jinja2
from fuzz_utils.utils.crytic_print import CryticPrint
from fuzz_utils.utils.file_manager import check_and_create_dirs, save_file
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.templates.harness_templates import templates

# pylint: disable=too-many-instance-attributes
@dataclass
class Actor:
    """Class for storing Actor contract data"""

    name: str
    constructor: str
    dependencies: str
    content: str
    path: str
    number: int
    targets: list[Contract]
    imports: list[str]
    variables: list[str]
    functions: list[str]
    contract: Contract

    def set_content(self, content: str) -> None:
        """Set the content field of the class"""
        self.content = content

    def set_path(self, path: str) -> None:
        """Set the path field of the class"""
        self.path = path

    def set_contract(self, contract: Contract) -> None:
        """Set the contract field of the class"""
        self.contract = contract


@dataclass
class Harness:
    """Class for storing Harness contract data"""

    name: str
    constructor: str
    dependencies: str
    content: str
    path: str
    targets: list[Contract]
    actors: list[Actor]
    imports: list[str]
    variables: list[str]
    functions: list[str]

    def set_content(self, content: str) -> None:
        """Sets the content field of the class"""
        self.content = content

    def set_path(self, path: str) -> None:
        """Sets the path field of the class"""
        self.path = path


class HarnessGenerator:
    """
    Handles the generation of Foundry test files from Echidna reproducers
    """

    config: dict = {
        "name": "DefaultHarness",
        "compilationPath": ".",
        "targets": [],
        "outputDir": "./test/fuzzing",
        "actors": [
            {
                "name": "Default",
                "targets": [],
                "number": 3,
                "filters": {
                    "strict": False,
                    "onlyModifiers": [],
                    "onlyPayable": False,
                    "onlyExternalCalls": [],
                },
            }
        ],
        "attacks": [],
    }

    def __init__(
        self,
        compilation_path: str,
        targets: list[str],
        slither: Slither,
        output_dir: str,
        config: dict,
        remappings: dict,
    ) -> None:
        for key, value in config.items():
            if key in self.config and value:
                self.config[key] = value
            # TODO add checks for attack config
            if key == "actors":
                for idx, actor in enumerate(config[key]):
                    if not "name" in actor or not "targets" in actor:
                        handle_exit("Actor is missing attributes")
                    if not "number" in actor:
                        self.config["actors"][idx]["number"] = 3
                        CryticPrint().print_warning(
                            "Missing number argument in actor, using 3 as default."
                        )
                    if not "filters" in actor:
                        self.config["actors"][idx]["filters"] = {
                            "onlyModifiers": [],
                            "onlyPayable": False,
                            "onlyExternalCalls": [],
                        }
                        CryticPrint().print_warning(
                            "Missing filters argument in actor, using none as default."
                        )

        if targets:
            self.config["targets"] = targets
        if output_dir:
            self.config["outputDir"] = output_dir
        if compilation_path:
            self.config["compilationPath"] = compilation_path
        if "actors" not in config:
            self.config["actors"][0]["targets"] = self.config["targets"]
        if remappings:
            self.remappings = remappings

        CryticPrint().print_no_format(f"    Config: {self.config}")

        self.slither = slither
        self.targets = [
            self.get_target_contract(slither, contract) for contract in self.config["targets"]
        ]
        self.output_dir = self.config["outputDir"]

    def generate_templates(self) -> None:
        """Generates the Harness and Actor fuzzing templates"""
        CryticPrint().print_information(
            f"Generating the fuzzing Harness for contracts: {self.config['targets']}"
        )

        # Check if directories exists, if not, create them
        check_and_create_dirs(self.output_dir, ["utils", "actors", "harnesses", "attacks"])
        # Generate the Actors
        actors: list[Actor] = self._generate_actors()
        CryticPrint().print_success("    Actors generated!")
        # Generate the Attacks
        attacks: list[Actor] = self._generate_attacks()
        CryticPrint().print_success("    Attacks generated!")
        # Generate the harness
        self._generate_harness(actors, attacks)
        CryticPrint().print_success("    Harness generated!")
        CryticPrint().print_success(f"Files saved to {self.config['outputDir']}")

    # pylint: disable=too-many-locals
    def _generate_harness(self, actors: list[Actor], attacks: list[Actor]) -> None:
        CryticPrint().print_information(f"Generating {self.config['name']} Harness")

        # Generate inheritance and variables
        imports: list[str] = []
        variables: list[str] = []

        for contract in self.targets:
            imports.append(f'import "{contract.source_mapping.filename.relative}";')
            variables.append(f"{contract.name} {contract.name.lower()};")

        # Generate actor variables and imports
        for actor in actors:
            variables.append(f"Actor{actor.name}[] {actor.name}_actors;")
            imports.append(f'import "{actor.path}";')

        # Generate attack variables and imports
        for attack in attacks:
            variables.append(f"Attack{attack.name} {attack.name.lower()}Attack;")
            imports.append(f'import "{attack.path}";')

        # Generate constructor with contract, actor, and attack deployment
        constructor = "constructor() {\n"
        for contract in self.targets:
            inputs: list[str] = []
            if contract.constructor:
                constructor_parameters = contract.constructor.parameters
                for param in constructor_parameters:
                    constructor += f"        {param.type} {param.name};\n"
                    inputs.append(param.name)
            inputs_str: str = ", ".join(inputs)
            constructor += f"        {contract.name.lower()} = new {contract.name}({inputs_str});\n"

        for actor in actors:
            constructor += "        for(uint256 i; i < 3; i++) {\n"
            constructor_arguments = ""
            if actor.contract and hasattr(actor.contract.constructor, "parameters"):
                constructor_arguments = ", ".join(
                    [f"address({x.name.strip('_')})" for x in actor.contract.constructor.parameters]
                )
            constructor += (
                f"            {actor.name}_actors.push(new Actor{actor.name}({constructor_arguments}));\n"
                + "        }\n"
            )

        for attack in attacks:
            constructor_arguments = ""
            if attack.contract and hasattr(attack.contract.constructor, "parameters"):
                constructor_arguments = ", ".join(
                    [f"address({x.name.strip('_')})" for x in actor.contract.constructor.parameters]
                )
            constructor += f"        {attack.name.lower()}Attack = new {attack.name}({constructor_arguments});\n"
        constructor += "    }\n"
        # Generate dependencies
        dependencies: str = "PropertiesAsserts"

        # Generate Functions
        functions: list[str] = []
        for actor in actors:
            function_body = f"        {actor.contract.name} selectedActor = {actor.name}_actors[clampBetween(actorIndex, 0, {actor.name}_actors.length - 1)];\n"
            temp_list = self._generate_functions(
                actor.contract, None, ["uint256 actorIndex"], function_body, "selectedActor"
            )
            functions.extend(temp_list)

        for attack in attacks:
            temp_list = self._generate_functions(
                attack.contract, None, [], None, f"{attack.name.lower()}Attack"
            )
            functions.extend(temp_list)

        # Generate harness class
        harness = Harness(
            name=self.config["name"],
            constructor=constructor,
            dependencies=dependencies,
            content="",
            path="",
            targets=self.targets,
            actors=actors,
            imports=imports,
            variables=variables,
            functions=functions,
        )

        content, path = self._render_template(
            templates["HARNESS"], "harnesses", self.config["name"], harness
        )
        harness.set_content(content)
        harness.set_path(path)

    def _generate_attacks(self) -> list[Actor]:
        CryticPrint().print_information("Generating Attack contracts:")
        attacks: list[Actor] = []

        # Check if dir exists, if not, create it
        attack_output_path = os.path.join(self.output_dir, "attacks")

        for attack_config in self.config["attacks"]:
            name = attack_config["name"]
            if name in templates["ATTACKS"]:
                CryticPrint().print_information(f"    Attack: {name}...")
                targets = [
                    contract
                    for contract in self.targets
                    if contract.name in attack_config["targets"]
                ]
                attack: Actor = self._generate_actor(targets, attack_config, True)

                # Generate the templated string and append to list
                content, path = self._render_template(
                    templates["ATTACKS"][name], "attacks", f"/Attack{name}", attack
                )

                # Save content and path to Actor
                attack.set_content(content)
                attack.set_path(path)

                attack_slither = Slither(f"{attack_output_path}/Attack{name}.sol")
                attack.set_contract(self.get_target_contract(attack_slither, f"{name}Attack"))

                attacks.append(attack)
            else:
                CryticPrint().print_warning(
                    f"Attack `{name}` was skipped since it could not be found in the available templates"
                )

        return attacks

    def _generate_actor(
        self, target_contracts: list[Contract], actor_config: dict, list_targets: bool
    ) -> Actor:
        imports: list[str] = []
        variables: list[str] = []
        functions: list[str] = []
        constructor_args: list[str] = []
        constructor = ""

        for contract in target_contracts:
            # Generate inheritance
            imports.append(f'import "{contract.source_mapping.filename.relative}";')

            # Generate variables
            contract_name = contract.name
            target_name = contract.name.lower()
            variables.append(f"{contract_name} {target_name};")

            # Generate constructor
            constructor_args.append(f"address _{target_name}")
            constructor += f"       {target_name} = {contract_name}(_{target_name});\n"
            if list_targets:
                constructor += f"       targets.push(_{target_name});\n"

            # Generate Functions

            functions.extend(
                self._generate_functions(
                    contract, actor_config["filters"], [], None, contract.name.lower()
                )
            )

        constructor = (
            f"constructor({', '.join(constructor_args)})" + "{\n" + constructor + "    }\n"
        )

        return Actor(
            name=actor_config["name"],
            constructor=constructor,
            imports=imports,
            dependencies="PropertiesAsserts",
            variables=variables,
            functions=functions,
            content="",
            path="",
            number=actor_config["number"] if "number" in actor_config else 1,
            targets=target_contracts,
            contract=None,
        )

    def _generate_actors(self) -> list[Actor]:
        CryticPrint().print_information("Generating Actors:")
        actor_contracts: list[Actor] = []

        # Check if dir exists, if not, create it
        actor_output_path = os.path.join(self.output_dir, "actors")  # Input param: directory

        # Loop over actors list
        for actor_config in self.config["actors"]:
            name = actor_config["name"]
            target_contracts: list[Contract] = [
                self.get_target_contract(self.slither, contract)
                for contract in actor_config["targets"]
            ]

            CryticPrint().print_information(f"    Actor: {name}Actor...")
            # Generate the Actor
            actor: Actor = self._generate_actor(target_contracts, actor_config, False)

            content, path = self._render_template(
                templates["ACTOR"], "actors", f"Actor{name}", actor
            )

            # Save content and path to Actor
            actor.set_content(content)
            actor.set_path(path)

            actor_slither = Slither(f"{actor_output_path}/Actor{name}.sol")
            actor.set_contract(self.get_target_contract(actor_slither, f"Actor{name}"))

            actor_contracts.append(actor)

        # Return Actors list
        return actor_contracts

    def _generate_functions(
        self,
        target_contract: Contract,
        filters: dict | None,
        prepend_variables: list[str],
        function_body: str | None,
        contract_name: str,
    ) -> list[str]:
        functions: list[str] = []
        contracts: list[Contract] = [target_contract]
        if len(target_contract.inheritance) > 0:
            contracts = list(set(contracts) | set(target_contract.inheritance))

        for contract in contracts:
            if should_skip_contract_functions(contract):
                continue
            temp_functions = self._fetch_contract_functions(
                contract, filters, prepend_variables, function_body, contract_name
            )
            if len(temp_functions) > 0:
                functions.extend(temp_functions)

        return functions

    # pylint: disable=too-many-locals,too-many-branches,no-self-use
    def _fetch_contract_functions(
        self,
        contract: Contract,
        filters: dict | None,
        prepend_variables: list[str],
        function_body: str | None,
        contract_name: str,
    ) -> list[str]:
        functions: list[str] = []

        functions.append(
            f"// -------------------------------------\n    // {contract.name} functions\n    // {contract.source_mapping.filename.relative}\n    // -------------------------------------\n"
        )

        for entry in contract.functions_declared:
            # Don't create wrappers for pure and view functions
            if should_skip_function(entry, filters):
                continue

            # Determine if payable
            payable = " payable" if entry.payable else ""
            unused_var = "notUsed"
            # Loop over function inputs
            inputs_with_types = ""
            if isinstance(entry.parameters, list):
                inputs_with_type_list = prepend_variables if len(prepend_variables) > 0 else []

                for parameter in entry.parameters:
                    location = ""
                    if parameter.type.is_dynamic or isinstance(
                        parameter.type, (ArrayType, UserDefinedType)
                    ):
                        location = f" {parameter.location}"
                    # TODO change it so that we detect if address should be payable or not
                    elif "address" == parameter.type.type:
                        location = " payable"
                    inputs_with_type_list.append(
                        f"{parameter.type}{location} {parameter.name if parameter.name else unused_var}"
                    )

                inputs_with_types = ", ".join(inputs_with_type_list)

            # Loop over return types
            return_types = ""
            if isinstance(entry.return_type, list):
                returns_list = []

                for return_type in entry.return_type:
                    returns_list.append(f"{return_type.type}")

                return_types = f" returns ({', '.join(returns_list)})"

            # Generate function definition
            definition = (
                f"function {entry.name}({inputs_with_types}) {entry.visibility}{payable}{return_types}"
                + " {\n"
            )
            if function_body:
                definition += function_body
            definition += (
                f"        {contract_name}.{entry.name}({', '.join([ unused_var if not x.name else x.name for x in entry.parameters])});\n"
                + "    }\n"
            )
            functions.append(definition)

        return functions

    def _render_template(
        self, template_str: str, directory_name: str, file_name: str, target: Harness | Actor
    ) -> tuple[str, str]:
        output_path = os.path.join(self.output_dir, directory_name)
        template = jinja2.Template(template_str)
        content = template.render(target=target, remappings=self.remappings)
        save_file(output_path, f"/{file_name}", ".sol", content)

        return content, f"../{directory_name}/{file_name}.sol"

    # pylint: disable=no-self-use
    def get_target_contract(self, slither: Slither, target_name: str) -> Contract:
        """Finds and returns Slither Contract"""
        contracts = slither.get_contract_from_name(target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == target_name:
                return contract

        handle_exit(f"\n* Slither could not find the specified contract `{target_name}`.")


# Utility functions
def should_skip_contract_functions(contract: Contract) -> bool:
    """Determines if the contract has applicable functions to include in a harness or actor. Returns bool"""
    if not contract.functions_declared or contract.is_interface:
        return True

    for entry in contract.functions_declared:
        if (
            (entry.visibility in ("public", "external"))
            and not entry.view
            and not entry.pure
            and not entry.is_constructor
        ):
            return False

    return True


# pylint: disable=too-many-branches
def should_skip_function(function: FunctionContract, config: dict | None) -> bool:
    """Determines if a function matches the filters. Returns bool"""
    # Don't create wrappers for pure and view functions
    if (
        function.pure
        or function.view
        or function.is_constructor
        or function.is_fallback
        or function.is_receive
    ):
        return True
    if function.visibility not in ("public", "external"):
        return True

    any_match: list[bool] = [False, False, False]
    empty: list[bool] = [False, False, False]

    if config:
        if len(config["onlyModifiers"]) > 0:
            inclusionSet = set(config["onlyModifiers"])
            modifierSet = {[x.name for x in function.modifiers]}
            if inclusionSet & modifierSet:
                any_match[0] = True
        else:
            empty[0] = True

        if config["onlyPayable"]:
            if function.payable:
                any_match[1] = True
        else:
            empty[1] = True

        if len(config["onlyExternalCalls"]) > 0:
            functions = []
            for _, func in function.all_high_level_calls():
                functions.append(func)

            inclusionSet = set(config["onlyExternalCalls"])
            functionsSet = set(x.name for x in functions)
            if inclusionSet & functionsSet:
                any_match[2] = True
        else:
            empty[2] = True

        if config["strict"]:
            if False in empty:
                if False in any_match:
                    return True
            # If all are empty and at least one condition is false, skip function
            return False

        # If at least one is non-empty and at least one condition is true, don't skip function
        if False in empty:
            if True in any_match:
                return False
            return True

        # All are empty, don't skip any function
        return False

    return False
