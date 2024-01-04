<img src="./logo.png" alt="Slither Static Analysis Framework Logo" width="500" />

# Automated tool for generating Foundry unit tests for smart contract fuzzer failed properties

`test-generator` is a Python tool that generates unit tests from [Echidna](https://github.com/crytic/echidna) and [Medusa](https://github.com/crytic/medusa/tree/master) failed properties, using the generated reproducer files. It uses [Slither](https://github.com/crytic/slither) for determining types and jinja2 for generating strings from string templates.

## Installation and pre-requisites

In order to be able to use test-generator, you will need to install it first:

```bash
git clone git@github.com:crytic/test-generator.git
cd test-generator
pip3 install -e .
```

These commands will install all the Python libraries and tools required to run test-generator. However, it won't install Echidna or Medusa, so you will need to download and install the latest version yourself from its official releases ([Echidna](https://github.com/crytic/echidna/releases), [Medusa](https://github.com/crytic/medusa/releases)).

## Example

In order to generate a test file for the [BasicTypes.sol](test/src/BasicTypes.sol) contract, based on the Echidna corpus reproducers for this contract ([corpus-basic](test/echidna-corpora/corpus-basic/)), we need to `cd` into the `test` directory which contains the Foundry project and run the command:
```
test-generator ./src/BasicTypes.sol --corpus-dir echidna-corpora/corpus-basic --contract "BasicTypes" --test-directory "./test/" --inheritance-path "../src/" --fuzzer echidna
```

Running this command should generate a `BasicTypes_Echidna_Test.sol` file in the [tests](/test/test/) directory of the Foundry project.

## Supported input types

The tool currently supports all elementary types (uint*, int*, bool, address, bytes, bytes*, string), one-dimensional fixed-size and dynamic arrays, structs, and enums. Any other types may or may not work. 

## Command-line options

Additional options are available for the script:

- `-cd`/`--corpus-dir` `path_to_corpus_dir`: The path to the corpus directory relative to the working directory.
- `-c`/`--contract` `contract_name`: The name of the contract.
- `-td`/`--test-directory` `path_to_test_directory`: The path to the test directory relative to the working directory.
- `-i`/`--inheritance-path` `relative_path_to_contract`: The relative path from the test directory to the contract (used for inheritance).
- `-f`/`--fuzzer` `fuzzer_name`: The name of the fuzzer, currently supported: `echidna` and `medusa`
