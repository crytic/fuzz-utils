<img src="./logo.png" alt="Slither Static Analysis Framework Logo" width="500" />

# Automated tool for generating Foundry unit tests from smart contract fuzzer failed properties

`fuzz-utils` is a Python tool that generates unit tests from [Echidna](https://github.com/crytic/echidna) and [Medusa](https://github.com/crytic/medusa/tree/master) failed properties, using the generated reproducer files. It uses [Slither](https://github.com/crytic/slither) for determining types and jinja2 for generating the test files using string templates.

**Disclaimer**: Please note that `fuzz-utils` is **under development**. Currently, not all Solidity types are supported and some types (like `bytes*`, and `string`) might be improperly decoded from the corpora call sequences. We are investigating a better corpus format that will ease the creation of unit tests.

## Features
`fuzz-utils` provides support for:
- ✔️ Generating Foundry unit tests from the fuzzer corpus of single entry point fuzzing harnesses
- ✔️ Medusa and Echidna corpora
- ✔️ Solidity types: `bool`,`uint*`, `int*`, `address`, `struct`, `enum`, single-dimensional fixed-size arrays and dynamic arrays, multi-dimensional fixed-size arrays.

Multi-dimensional dynamic arrays, function pointers, and other more complex types are in the works, but are currently not supported.
## Installation and pre-requisites

To install `fuzz-utils`: 

```bash
pip install fuzz-utils
```

These commands will install all the Python libraries and tools required to run `fuzz-utils`. However, it won't install Echidna or Medusa, so you will need to download and install the latest version yourself from its official releases ([Echidna](https://github.com/crytic/echidna/releases), [Medusa](https://github.com/crytic/medusa/releases)).

## Example

In order to generate a test file for the [BasicTypes.sol](test/src/BasicTypes.sol) contract, based on the Echidna corpus reproducers for this contract ([corpus-basic](tests/test_data/echidna-corpora/corpus-basic/)), we need to `cd` into the `tests/test_data` directory which contains the Foundry project and run the command:
```bash
fuzz-utils ./src/BasicTypes.sol --corpus-dir echidna-corpora/corpus-basic --contract "BasicTypes" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
```

Running this command should generate a `BasicTypes_Echidna_Test.sol` file in the [tests](/tests/test_data/test/) directory of the Foundry project.

## Command-line options

Additional options are available for the script:

- `-cd`/`--corpus-dir` `path_to_corpus_dir`: The path to the corpus directory relative to the working directory.
- `-c`/`--contract` `contract_name`: The name of the contract.
- `-td`/`--test-directory` `path_to_test_directory`: The path to the test directory relative to the working directory.
- `-i`/`--inheritance-path` `relative_path_to_contract`: The relative path from the test directory to the contract (used for inheritance).
- `-f`/`--fuzzer` `fuzzer_name`: The name of the fuzzer, currently supported: `echidna` and `medusa`

## Contributing
For information about how to contribute to this project, check out the [CONTRIBUTING](CONTRIBUTING.md) guidelines.

## License
`fuzz-utils` is licensed and distributed under the [AGPLv3](LICENSE).
