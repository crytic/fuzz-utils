""" Converts fuzzer string and bytes formats to hex literals"""
import re

ascii_escape_map = {
    "\\NUL": b"\x00",  # Null character
    "\\SOH": b"\x01",
    "\\STX": b"\x02",
    "\\ETX": b"\x03",
    "\\EOT": b"\x04",
    "\\ENQ": b"\x05",
    "\\ACK": b"\x06",
    "\\FF": b"\x0c",
    "\\CR": b"\x0d",
    "\\SO": b"\x0e",
    "\\SI": b"\x0f",
    "\\DLE": b"\x10",
    "\\DC1": b"\x11",
    "\\DC2": b"\x12",
    "\\DC3": b"\x13",
    "\\DC4": b"\x14",
    "\\NAK": b"\x15",
    "\\SYN": b"\x16",
    "\\ETB": b"\x17",
    "\\CAN": b"\x18",
    "\\EM": b"\x19",
    "\\SUB": b"\x1a",
    "\\ESC": b"\x1b",
    "\\FS": b"\x1c",
    "\\GS": b"\x1d",
    "\\RS": b"\x1e",
    "\\US": b"\x1f",
    "\\SP": b"\x20",
    "\\DEL": b"\x7f",
    "\\0": b"\x00",
    "\\a": b"\x07",  # Alert
    "\\b": b"\x08",  # Backspace
    "\\f": b"\x0c",
    "\\n": b"\x0a",  # New line
    "\\r": b"\x0d",
    "\\t": b"\x09",  # Horizontal Tab
    "\\v": b"\x0b",  # Vertical Tab
}


def parse_echidna_byte_string(s: str, isBytes: bool) -> str:
    """Parses Haskell byte sequence into a Solidity hex literal or unicode literal"""
    # Replace Haskell-specific escapes with Python bytes
    # Resultant bytes object
    result_bytes = bytearray()

    # Regular expression to match decimal values like \160
    decimal_pattern = re.compile(r"\\(\d{1,3})")

    # Iterator over the string
    i = 0
    while i < len(s):
        # Check for escape sequence
        if s[i] == "\\":
            matched = False
            # Check for known escape sequences
            for seq, byte in ascii_escape_map.items():
                if s.startswith(seq, i):
                    result_bytes.extend(byte)
                    i += len(seq)
                    matched = True
                    break
            if not matched:
                # Check for decimal escape
                dec_match = decimal_pattern.match(s, i)
                if dec_match:
                    # Convert the decimal escape to bytes
                    decimal_value = int(dec_match.group(1))
                    result_bytes.append(decimal_value)
                    i += len(dec_match.group(0))
                else:
                    # Unknown escape, skip the backslash and process the next character normally
                    i += 1
        else:
            # Normal character, encode and add
            result_bytes.append(ord(s[i]))
            i += 1

    # Convert the resultant bytes to hexadecimal string
    if not isBytes:
        return byte_to_escape_sequence(bytes(result_bytes))
    return result_bytes.hex()


def byte_to_escape_sequence(byte_data: bytes) -> str:
    """Generates unicode escaped string from bytes"""
    arr = []
    for b in byte_data:
        arr.append(f"\\u{b:04x}")
    return "".join(arr)
