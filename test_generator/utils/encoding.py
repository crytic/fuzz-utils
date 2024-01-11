""" Converts fuzzer string and bytes formats to hex literals"""
import re

ascii_escape_map = {
    "\\NUL": "\x00",  # Null character
    "\\SOH": "\x01",
    "\\STX": "\x02",
    "\\ETX": "\x03",
    "\\EOT": "\x04",
    "\\ENQ": "\x05",
    "\\ACK": "\x06",
    "\\FF": "\x0c",
    "\\CR": "\x0d",
    "\\SO": "\x0e",
    "\\SI": "\x0f",
    "\\DLE": "\x10",
    "\\DC1": "\x11",
    "\\DC2": "\x12",
    "\\DC3": "\x13",
    "\\DC4": "\x14",
    "\\NAK": "\x15",
    "\\SYN": "\x16",
    "\\ETB": "\x17",
    "\\CAN": "\x18",
    "\\EM": "\x19",
    "\\SUB": "\x1a",
    "\\ESC": "\x1b",
    "\\FS": "\x1c",
    "\\GS": "\x1d",
    "\\RS": "\x1e",
    "\\US": "\x1f",
    "\\SP": "\x20",
    "\\DEL": "\x7f",
    "\\0": "\x00",
    "\\a": "\x07",  # Alert
    "\\b": "\x08",  # Backspace
    "\\f": "\x0c",
    "\\n": "\x0a",  # New line
    "\\r": "\x0d",
    "\\t": "\x09",  # Horizontal Tab
    "\\v": "\x0b",  # Vertical Tab
}


def parse_echidna_byte_string(s: str) -> str:
    """Parses Haskell byte sequence into a Solidity hex literal"""
    # Replace Haskell-specific escapes with Python bytes
    for key, value in ascii_escape_map.items():
        s = s.replace(key, value)

    # Handle octal escapes (like \\135)
    def octal_to_byte(match: re.Match) -> str:
        octal_value = match.group(0)[1:]  # Remove the backslash

        return chr(int(octal_value, 8))

    s = re.sub(r"\\[0-3]?[0-7][0-7]", octal_to_byte, s)

    # Convert to bytes and then to hexadecimal
    return s.encode().hex()


def parse_medusa_byte_string(s: str) -> str:
    """Decode bytes* or string type from Medusa format to Solidity hex literal"""
    return s.encode("utf-8").hex()
