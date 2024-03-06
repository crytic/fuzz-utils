""" Generates a template fuzzer harness for a smart contract target """
# type: ignore[misc] # Ignores 'Any' input parameter
import os
from dataclasses import dataclass

from slither import Slither
from slither.core.declarations.contract import Contract
from slither.core.solidity_types.user_defined_type import UserDefinedType
from slither.core.solidity_types.array_type import ArrayType
import jinja2
from fuzz_utils.utils.file_manager import check_and_create_dirs, save_file
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.templates.foundry_templates import templates


@dataclass
class Actor:
    """Class for storing Actor contract data"""

    name: str
    constructor: str
    dependencies: str
    content: str
    path: str
    targets: list[Contract]
    imports: list[str]
    variables: list[str]
    functions: list[str]
    contract: Contract | None

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

    def __init__(self, target_name: str, slither: Slither, output_dir: str) -> None:
        self.target_name = target_name
        self.slither = slither
        self.target = self.get_target_contract(slither, target_name)
        self.output_dir = output_dir

    def generate_templates(self) -> None:
        """Generates the Harness and Actor fuzzing templates"""
        # Check if directories exists, if not, create them
        check_and_create_dirs(self.output_dir, ["utils", "actors", "harnesses"])
        # Generate the Actors
        actors: list[Actor] = self._generate_actors([self.target_name], ["Basic"])
        # Generate the harness
        self._generate_harness(actors, [self.target], f"{self.target_name}Harness")

    def _generate_harness(
        self, actors: list[Actor], target_contracts: list[Contract], name: str
    ) -> None:
        # Generate inheritance and variables
        imports: list[str] = []
        variables: list[str] = []

        for contract in target_contracts:
            imports.append(f'import "{contract.source_mapping.filename.relative}";')
            variables.append(f"{contract.name} {contract.name.lower()};")

        # Generate actor arrays and imports
        for actor in actors:
            variables.append(f"Actor{actor.name}[] {actor.name}_actors;")
            imports.append(f'import "{actor.path}";')

        # Generate constructor with contract and actor deployment
        constructor = "constructor() {\n"
        for contract in target_contracts:
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
            if actor.contract.constructor.parameters:
                constructor_arguments = ", ".join(
                    [x.name.strip("_") for x in actor.contract.constructor.parameters]
                )
            constructor += (
                f"            {actor.name}_actors.push(new Actor{actor.name}(address({constructor_arguments})));\n"
                + "        }\n"
            )
            constructor += "    }\n"

        # Generate dependencies
        dependencies: str = "PropertiesAsserts"

        # TODO Generate functions
        # Generate Functions
        functions: list[str] = []
        for actor in actors:
            temp_list = self._generate_harness_functions(actor)
            functions.extend(temp_list)

        # Generate harness class
        harness = Harness(
            name=name,
            constructor=constructor,
            dependencies=dependencies,
            content="",
            path="",
            targets=target_contracts,
            actors=actors,
            imports=imports,
            variables=variables,
            functions=functions,
        )

        # Generate harness content
        template = jinja2.Template(templates["HARNESS"])
        harness_content = template.render(harness=harness)
        harness.set_content(harness_content)

        # Save harness to file
        harness_output_path = os.path.join(self.output_dir, "harnesses")
        save_file(harness_output_path, f"/{name}", ".sol", harness_content)

    def _generate_actor(self, target_contract: Contract, name: str) -> Actor:
        # Generate inheritance
        imports: list[str] = [f'import "{target_contract.source_mapping.filename.relative}";']

        # Generate variables
        contract_name = target_contract.name
        target_name = target_contract.name.lower()
        variables: list[str] = [f"{contract_name} {target_name};"]

        # Generate constructor
        constructor = f"constructor(address _{target_name})" + "{\n"
        constructor += f"       {target_name} = {contract_name}(_{target_name});\n" + "    }\n"

        # Generate Functions
        functions = self._generate_actor_functions(target_contract)

        return Actor(
            name=name,
            constructor=constructor,
            imports=imports,
            dependencies="PropertiesAsserts",
            variables=variables,
            functions=functions,
            content="",
            path="",
            targets=[target_contract],
            contract=None,
        )

    def _generate_actors(self, targets: list[str], names: list[str]) -> list[Actor]:
        actor_contracts: list[Actor] = []

        # Check if dir exists, if not, create it
        actor_output_path = os.path.join(self.output_dir, "actors")

        # Loop over all targets and generate an actor for each
        for idx, target in enumerate(targets):
            target_contract: Contract = self.get_target_contract(self.slither, target)
            # Generate the actor
            actor: Actor = self._generate_actor(target_contract, names[idx])
            # Generate the templated string and append to list
            template = jinja2.Template(templates["ACTOR"])
            actor_content = template.render(actor=actor)
            # Save the file
            save_file(actor_output_path, f"/Actor{names[idx]}", ".sol", actor_content)

            # Save content and path to Actor
            actor.set_content(actor_content)
            actor.set_path(f"../actors/Actor{names[idx]}.sol")

            actor_slither = Slither(f"{actor_output_path}/Actor{names[idx]}.sol")
            actor.set_contract(self.get_target_contract(actor_slither, f"Actor{names[idx]}"))

            actor_contracts.append(actor)
        # Return Actors list
        return actor_contracts

    def _generate_actor_functions(self, target_contract: Contract) -> list[str]:
        functions: list[str] = []
        contracts: list[Contract] = [target_contract]
        if len(target_contract.inheritance) > 0:
            contracts = set(contracts) | set(target_contract.inheritance)

        for contract in contracts:
            if not contract.functions_declared or contract.is_interface:
                continue

            has_public_fn: bool = False
            for entry in contract.functions_declared:
                if (entry.visibility in ("public", "external")) and not entry.is_constructor:
                    has_public_fn = True
            if not has_public_fn:
                continue

            functions.append(
                f"// -------------------------------------\n    // {contract.name} functions\n    // -------------------------------------\n"
            )

            for entry in contract.functions_declared:
                # Don't create wrappers for pure and view functions
                if (
                    entry.pure
                    or entry.view
                    or entry.is_constructor
                    or entry.is_fallback
                    or entry.is_receive
                ):
                    continue
                if entry.visibility not in ("public", "external"):
                    continue

                # Determine if payable
                payable = " payable" if entry.payable else ""
                unused_var = "notUsed"
                # Loop over function inputs
                inputs_with_types = ""
                if isinstance(entry.parameters, list):
                    inputs_with_type_list = []

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

                    inputs_with_types: str = ", ".join(inputs_with_type_list)

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
                definition += (
                    f"        {self.target_name.lower()}.{entry.name}({', '.join([ unused_var if not x.name else x.name for x in entry.parameters])});\n"
                    + "    }\n"
                )
                functions.append(definition)

        return functions

    def _generate_harness_functions(self, actor: Actor) -> list[str]:
        functions: list[str] = []
        contracts: list[Contract] = [actor.contract]

        for contract in contracts:
            if not contract.functions_declared or contract.is_interface:
                continue
            print("contract", contract.name)

            has_public_fn: bool = False
            for entry in contract.functions_declared:
                if (entry.visibility in ("public", "external")) and not entry.is_constructor:
                    has_public_fn = True
            if not has_public_fn:
                continue

            functions.append(
                f"// -------------------------------------\n    // {contract.name} functions\n    // -------------------------------------\n"
            )

            for entry in contract.functions_declared:
                # Don't create wrappers for pure and view functions
                if (
                    entry.pure
                    or entry.view
                    or entry.is_constructor
                    or entry.is_fallback
                    or entry.is_receive
                ):
                    continue
                if entry.visibility not in ("public", "external"):
                    continue

                # Determine if payable
                payable = " payable" if entry.payable else ""
                # Loop over function inputs
                inputs_with_types = ""
                if isinstance(entry.parameters, list):
                    inputs_with_type_list = ["uint256 actorIndex"]

                    for parameter in entry.parameters:
                        location = ""
                        if parameter.type.is_dynamic or isinstance(
                            parameter.type, (ArrayType, UserDefinedType)
                        ):
                            location = f" {parameter.location}"
                        # TODO change it so that we detect if address should be payable or not
                        elif "address" == parameter.type.type:
                            location = " payable"
                        inputs_with_type_list.append(f"{parameter.type}{location} {parameter.name}")

                    inputs_with_types: str = ", ".join(inputs_with_type_list)

                # Loop over return types
                return_types = ""
                if isinstance(entry.return_type, list):
                    returns_list = []

                    for return_type in entry.return_type:
                        returns_list.append(f"{return_type.type}")

                    return_types = f" returns ({', '.join(returns_list)})"

                actor_array_var = f"{actor.name}_actors"
                # Generate function definition
                definition = (
                    f"function {entry.name}({inputs_with_types}) {entry.visibility}{payable}{return_types}"
                    + " {\n"
                )
                definition += f"        {contract.name} selectedActor = {actor_array_var}[clampBetween(actorIndex, 0, {actor_array_var}.length - 1)];\n"
                definition += (
                    f"        selectedActor.{entry.name}({', '.join([x.name for x in entry.parameters if x.name])});\n"
                    + "    }\n"
                )
                functions.append(definition)

        return functions

    def get_target_contract(self, slither: Slither, target_name: str) -> Contract:
        """Finds and returns Slither Contract"""
        contracts = slither.get_contract_from_name(target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == target_name:
                return contract

        handle_exit(f"\n* Slither could not find the specified contract `{target_name}`.")
