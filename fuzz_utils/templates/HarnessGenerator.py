""" Generates a template fuzzer harness for a smart contract target """
# type: ignore[misc] # Ignores 'Any' input parameter
from slither import Slither
from slither.core.declarations.contract import Contract
from fuzz_utils.utils.error_handler import handle_exit
from fuzz_utils.templates.foundry_templates import templates
from dataclasses import dataclass
import jinja2


@dataclass
class Actor:
    """ Class for storing Actor contract data"""
    name: str
    constructor: str
    dependencies: str
    imports: list[str]
    variables: list[str]
    functions: list[str]


class HarnessGenerator:
    """
    Handles the generation of Foundry test files from Echidna reproducers
    """
    harness: dict

    def __init__(self, target_name: str, slither: Slither) -> None:
        self.name = "Echidna"
        self.target_name = target_name
        self.slither = slither
        self.target = self.get_target_contract(target_name)
        self.harness = {}

    def generate_harness(self) -> None:
        self._generate_actors([self.target_name], ["Basic"])

    def _generate_actor(self, target_contract: Contract, name: str) -> Actor:
        # Generate inheritance
        imports: list[str] = [f'import "{target_contract.source_mapping.filename.relative}";']

        # Generate variables
        contract_name = target_contract.name
        target_name = target_contract.name.lower()
        variables: list[str] = [f"{contract_name} {target_name};"]

        # Generate constructor
        f"{contract_name} {target_name};"
        constructor = f"constructor(address _{target_name})" + "{\n"
        constructor += f"{target_name} = {contract_name}(_{target_name});\n" + "}\n"

        # Generate Functions
        entry_points = target_contract.functions_entry_points
        functions: list[str] = []

        for entry in entry_points:
            # Don't create wrappers for pure and view functions
            if entry.pure or entry.view or entry.is_constructor or entry.is_fallback or entry.is_receive:
                continue

            # Determine if payable
            payable = " payable" if entry.payable else ""
            # Loop over function inputs
            inputs_with_types = ""
            if isinstance(entry.parameters, list):
                inputs_with_type_list = []

                for parameter in entry.parameters:
                    inputs_with_type_list.append(f"{parameter.type} {parameter.name}")
                
                inputs_with_types = ", ".join(inputs_with_type_list)
            
            # Loop over return types
            return_types = ""
            if isinstance(entry.return_type, list):
                returns_list = []

                for return_type in entry.return_type:
                    returns_list.append(f"{return_type.type}")

                return_types = f" returns ({', '.join(returns_list)})"

            # Generate function definition
            definition = f"function {entry.name}({inputs_with_types}) {entry.visibility}{payable}{return_types}" + " {\n"
            definition += f"{target_name}.{entry.name}({', '.join([x.name for x in entry.parameters])});\n" + "}\n"
            functions.append(definition)
        
        return Actor(name=name, constructor=constructor, imports=imports, dependencies="PropertiesAsserts", variables=variables, functions=functions)


    def _generate_actors(self, targets: list[str], names: list[str]) -> None:
        actor_contracts: list[str] = []

        # Loop over all targets and generate an actor for each
        for idx, target in enumerate(targets):
            target_contract: Contract = self.get_target_contract(target)
            # Generate the actor
            actor: Actor = self._generate_actor(target_contract, names[idx])
            # Generate the templated string and append to list
            template = jinja2.Template(templates["ACTOR"])
            actor_contracts.append(template.render(actor=actor))

        # Save the files
        print(actor_contracts)

    def get_target_contract(self, target_name: str) -> Contract:
        """Finds and returns Slither Contract"""
        contracts = self.slither.get_contract_from_name(target_name)
        # Loop in case slither fetches multiple contracts for some reason (e.g., similar names?)
        for contract in contracts:
            if contract.name == target_name:
                return contract

        handle_exit(f"\n* Slither could not find the specified contract `{target_name}`.")

