"""Default configuration file"""
default_config: dict = {
    "compilationPath": ".",
    "corpusDir": "",
    "generate": {
        "targetContract": "",
        "compilationPath": "",
        "corpusDir": "",
        "fuzzer": "",
        "testsDir": "",
        "inheritancePath": "",
        "namedInputs": False,
    },
    "template": {
        "name": "DefaultHarness",
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
