import dataclasses
from typing import ByteString


@dataclasses.dataclass
class PickleVersion:
    is_new_format: bool
    version: int


def get_pickle_version(data: ByteString) -> PickleVersion:
    """
    Returns used protocol version for serialization.

    :param data: serialized object in pickle format.
    :return: PickleVersion instance containing information about the protocol version.
    """
    if not data:
        raise ValueError("Data cannot be empty.")

    is_new_format: bool
    version: int

    if data[0] == 0x80:
        is_new_format = True
        version = data[1]
    else:
        is_new_format = False
        version = -1

    return PickleVersion(is_new_format=is_new_format, version=version)
