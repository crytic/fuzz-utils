"""
CryticPrint module
"""

from enum import Enum
from typing import Any
from colorama import Fore, Style, init as colorama_init


class PrintMode(Enum):
    """
    Enumeration of the different types of messages that can be logged
    """

    MESSAGE = 0
    SUCCESS = 1
    INFORMATION = 2
    WARNING = 3
    ERROR = 4


class Singleton(type):
    """
    Metaclass for implementing a singleton pattern
    """

    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CryticPrint(metaclass=Singleton):
    """
    CryticPrint logging and printing class
    """

    _log_output: str
    _log_enabled: bool

    def __init__(self) -> None:
        self._log_enabled = True
        self._log_output = ""
        colorama_init()

    def print(self, mode: PrintMode, message: str) -> None:
        """
        Generic print function for different modes
        """

        if mode is PrintMode.MESSAGE:
            self.print_message(message)
        elif mode is PrintMode.SUCCESS:
            self.print_success(message)
        elif mode is PrintMode.INFORMATION:
            self.print_information(message)
        elif mode is PrintMode.WARNING:
            self.print_warning(message)
        elif mode is PrintMode.ERROR:
            self.print_error(message)

    def print_message(self, message: str) -> None:
        """
        Print a generic message (light-blue colored)
        """

        self.log(message)
        print(Style.BRIGHT + Fore.LIGHTBLUE_EX + message + Style.RESET_ALL)

    def print_success(self, message: str) -> None:
        """
        Print a success message (light-green colored)
        """

        self.log(message)
        print(Fore.LIGHTGREEN_EX + message + Style.RESET_ALL)

    def print_information(self, message: str) -> None:
        """
        Print an informational message (light-cyan colored)
        """

        self.log(message)
        print(Fore.LIGHTCYAN_EX + message + Style.RESET_ALL)

    def print_warning(self, message: str) -> None:
        """
        Print a warning message (light-yellow colored)
        """

        self.log(message)
        print(Fore.LIGHTYELLOW_EX + message + Style.RESET_ALL)

    def print_error(self, message: str) -> None:
        """
        Print an error message (light-red colored)
        """

        self.log(message)
        print(Style.BRIGHT + Fore.LIGHTRED_EX + message + Style.RESET_ALL)

    def print_no_format(self, message: str) -> None:
        """
        Print an unformatted message (no color used)
        """

        self.log(message)
        print(message)

    def get_log_output(self) -> str:
        """
        Get the currently accumulated log output
        """

        return self._log_output

    def clear_log(self) -> None:
        """
        Clear the current log
        """

        self._log_output = ""

    def start_logging(self) -> None:
        """
        Start logging messages
        """

        self._log_enabled = True

    def stop_logging(self) -> None:
        """
        Stop logging messages
        """

        self._log_enabled = False

    def log(self, message: str) -> None:
        """
        Log a message
        """

        if self._log_enabled:
            self._log_output += f"{message}\n"
