"""Default configuration file"""
default_config: dict = {
    "generate": {
        "targetContract": "",
        "compilationPath": ".",
        "corpusDir": "",
        "fuzzer": "",
        "testsDir": "",
        "inheritancePath": "",
        "namedInputs": False,
        "allSequences": False,
    },
    "template": {
        "name": "DefaultHarness",
        "mode": "simple",
        "targets": [],
        "outputDir": "./test/fuzzing",
        "compilationPath": ".",
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
    },
}
