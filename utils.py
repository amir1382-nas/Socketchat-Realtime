from config import ENCODING, MESSAGE_DELIMITER

def encode_message(msg: str) -> bytes:

    """encode message to utf-8 and append delimiter."""
    return (msg + MESSAGE_DELIMITER).encode(ENCODING)

def decode_message(data: bytes) -> str:

    """decode bytes to sting and strip delimiter."""
    return data.decode(ENCODING).rstrip(MESSAGE_DELIMITER)