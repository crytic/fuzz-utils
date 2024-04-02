<img src="./logo.png" alt="Slither Static Analysis Framework Logo" width="500" />

# Automated utility tooling for smart contract fuzzers

`fuzz-utils` is a set of Python tools that aim to improve the developer experience when using smart contract fuzzing.
The tools include:
- automatically generate unit tests from [Echidna](https://github.com/crytic/echidna) and [Medusa](https://github.com/crytic/medusa/tree/master) failed properties, using the generated reproducer files. 
- automatically generate a Echidna/Medusa compatible fuzzing harness.

`fuzz-utils` uses [Slither](https://github.com/crytic/slither) for determining types and `jinja2` for generating the test files using string templates.

**Disclaimer**: Please note that `fuzz-utils` is **under development**. Currently, not all Solidity types are supported and some types (like `bytes*`, and `string`) might be improperly decoded from the corpora call sequences. We are investigating a better corpus format that will ease the creation of unit tests.

## Features
`fuzz-utils` provides support for:
- ✔️ Generating Foundry unit tests from the fuzzer corpus of single entry point fuzzing harnesses.
- ✔️ Generating fuzzing harnesses, `Actor` contracts, and templated `attack` contracts to ease fuzzing setup.
- ✔️ Supports Medusa and Echidna corpora
- ✔️ Test generation supports Solidity types: `bool`,`uint*`, `int*`, `address`, `struct`, `enum`, single-dimensional fixed-size arrays and dynamic arrays, multi-dimensional fixed-size arrays.

Multi-dimensional dynamic arrays, function pointers, and other more complex types are in the works, but are currently not supported.
## Installation and pre-requisites

To install `fuzz-utils`: 

```bash
pip install fuzz-utils
```

These commands will install all the Python libraries and tools required to run `fuzz-utils`. However, it won't install Echidna or Medusa, so you will need to download and install the latest version yourself from its official releases ([Echidna](https://github.com/crytic/echidna/releases), [Medusa](https://github.com/crytic/medusa/releases)).

## Tools
The available tool commands are:
- [`init`](#initializing-a-configuration-file) - Initializes a configuration file
- [`generate`](#generating-unit-tests) - generates unit tests from a corpus
- [`template`](#generating-fuzzing-harnesses) - generates a fuzzing harness

### Generating unit tests

The `generate` command is used to generate Foundry unit tests from Echidna or Medusa corpus call sequences.

**Command-line options:**
- `compilation_path`: The path to the Solidity file or Foundry directory. By default `.`
- `-cd`/`--corpus-dir` `path_to_corpus_dir`: The path to the corpus directory relative to the working directory. By default `corpus`
- `-c`/`--contract` `contract_name`: The name of the target contract. If the compilation path only contains one contract the target will be automatically derived.
- `-td`/`--test-directory` `path_to_test_directory`: The path to the test directory relative to the working directory. By default `test`
- `-i`/`--inheritance-path` `relative_path_to_contract`: The relative path from the test directory to the contract (used for overriding inheritance). If this configuration option is not provided the inheritance path will be automatically derived. 
- `-f`/`--fuzzer` `fuzzer_name`: The name of the fuzzer, currently supported: `echidna` and `medusa`. By default `medusa`
- `--named-inputs`: Includes function input names when making calls. By default`false`
- `--config`: Path to the fuzz-utils config JSON file. Empty by default.
- `--all-sequences`: Include all corpus sequences when generating unit tests. By default `false`

**Example**

In order to generate a test file for the [BasicTypes.sol](tests/test_data/src/BasicTypes.sol) contract, based on the Echidna corpus reproducers for this contract ([corpus-basic](tests/test_data/echidna-corpora/corpus-basic/)), we need to `cd` into the `tests/test_data` directory which contains the Foundry project and run the command:
```bash
fuzz-utils generate ./src/BasicTypes.sol --corpus-dir echidna-corpora/corpus-basic --contract "BasicTypes" --fuzzer echidna
```

Running this command should generate a `BasicTypes_Echidna_Test.sol` file in the [test](/tests/test_data/test/) directory of the Foundry project.

### Generating fuzzing harnesses

The `template` command is used to generate a fuzzing harness. The harness can include multiple `Actor` contracts which are used as proxies for user actions, as well as `attack` contracts which can be selected from a set of premade contracts that perform certain common attack scenarios.

**Command-line options:**
- `compilation_path`: The path to the Solidity file or Foundry directory
- `-n`/`--name` `name: str`: The name of the fuzzing harness.
- `-c`/`--contracts` `target_contracts: list`: The name of the target contract.
- `-o`/`--output-dir` `output_directory: str`: Output directory name. By default it is `fuzzing`
- `--config`: Path to the `fuzz-utils` config JSON file
- `--mode`: The strategy to use when generating the harnesses. Valid options: `simple`, `prank`, `actor`

**Generation modes**
The tool support three harness generation strategies:
- `simple` - The fuzzing harness will be generated with all of the state-changing functions from the target contracts. All function calls are performed directly, with the harness contract as the `msg.sender`.
- `prank` - Similar to `simple` mode, with the difference that function calls are made from different users by using `hevm.prank()`. The users can be defined in the configuration file as `"actors": ["0xb4b3", "0xb0b", ...]`
- `actor` - `Actor` contracts will be generated and all harness function calls will be proxied through these contracts. The `Actor` contracts can be considered as users of the target contracts and the functions included in these actors can be filtered by modifier, external calls, or by `payable`. This allows for granular control over user capabilities.

**Example**

In order to generate a fuzzing harness for the [TestERC20.sol](tests/test_data/src/TestERC20.sol) contract, we need to `cd` into the `tests/test_data/` directory which contains the Foundry project and run the command:
```bash
fuzz-utils template ./src/TestERC20.sol --name "ERC20Harness" --contracts TestERC20
```

Running this command should generate the directory structure in [tests/test_data/test/fuzzing](tests/test_data/test/fuzzing), which contains the fuzzing harness [ERC20Harness](tests/test_data/test/fuzzing/harnesses/ERC20Harness.sol) and the Actor contract [DefaultActor](tests/test_data/test/fuzzing/actors/ActorDefault.sol).

We can see that the tool has generated the `DefaultActor` contract which contains all the functions of our ERC20 token, and that our fuzzing harness `ERC20Harness` is able to call each of these functions by randomly selecting one of the deployed actors, simulating different users. 

This reduces the amount of time you need to set up fuzzing harness boilerplate and let's you focus on what really matters, defining invariants and testing the system.

## Utilities

### Initializing a configuration file

The `init` command can be used to initialize a default configuration file in the project root. 

**Configuration file:**
Using the configuration file allows for more granular control than just using the command-line options. Valid configuration options are listed below:
```json
{
    "generate": {
        "targetContract": "BasicTypes",              // The Echidna/Medusa fuzzing harness 
        "compilationPath": "./src/BasicTypes",       // Path to the file or Foundry directory
        "corpusDir": "echidna-corpora/corpus-basic", // Path to the corpus directory
        "fuzzer": "echidna",                         // `echidna` | `medusa`
        "testsDir": "./test/",                       // Path to the directory where the tests will be generated
        "inheritancePath": "../src/",                // Relative path from the testing directory to the contracts
        "namedInputs": false,                        // True | False, whether to include function input names when making calls
        "allSequences": false,                       // True | False, whether to generate tests for the entire corpus (including non-failing sequences)
    },
    "template": {
        "name": "DefaultHarness",                    // The name of the fuzzing harness that will be generated
        "targets": ["BasicTypes"],                   // The contracts to be included in the fuzzing harness
        "outputDir": "./test/fuzzing",               // The output directory where the files and directories will be saved
        "compilationPath": ".",                      // The path to the Solidity file (if single target) or Foundry directory
        "actors": [                                  // At least one actor is required. If the array is empty, the DefaultActor which wraps all of the functions from the target contracts will be generated
            {
                "name": "Default",                   // The name of the Actor contract, saved as `Actor{name}`
                "targets": ["BasicTypes"],           // The list of contracts that the Actor can interact with
                "number": 3,                         // The number of instances of this Actor that will be used in the harness
                "filters": {                         // Used to filter functions so that only functions that fulfill certain criteria are included
                    "strict": false,                 // If `true`, only functions that fulfill *all* the criteria will be included. If `false`, functions that fulfill *any* criteria will be included
                    "onlyModifiers": [],             // List of modifiers to include
                    "onlyPayable": false,            // If `true`, only `payable` functions will be included. If `false`, both payable and non-payable functions will be included
                    "onlyExternalCalls": [],         // Only include functions that make a certain external call. E.g. [`transferFrom`]
                },
            }
        ],
        "attacks": [                                 // A list of premade attack contracts to include. 
            {
                "name": "Deposit",                   // The name of the attack contract. 
                "targets": ["BasicTypes"],           // The list of contracts that the attack contract can interact with
                "number": 1,                         // The number of instances of this attack contract that will be used in the harness
                "filters": {                         // Used to filter functions so that only functions that fulfill certain criteria are included
                    "strict": false,                 // If `true`, only functions that fulfill *all* the criteria will be included. If `false`, functions that fulfill *any* criteria will be included
                    "onlyModifiers": [],             // List of modifiers to include
                    "onlyPayable": false,            // If `true`, only `payable` functions will be included. If `false`, both payable and non-payable functions will be included
                    "onlyExternalCalls": [],         // Only include functions that make a certain external call. E.g. [`transferFrom`]
                },
            }
        ],
    },
}
```

## Contributing
For information about how to contribute to this project, check out the [CONTRIBUTING](CONTRIBUTING.md) guidelines.

## License
`fuzz-utils` is licensed and distributed under the [AGPLv3](LICENSE).
