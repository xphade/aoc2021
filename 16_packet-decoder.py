#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from math import prod
from timeit import default_timer as timer
from typing import Callable, Dict, List, Tuple

HEADER_SIZE: int = 6
LITERAL_TYPE: int = 4
TYPE_FUNCTIONS: Dict[int, Callable[[List[int]], int]] = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    5: lambda l: 1 if l[0] > l[1] else 0,
    6: lambda l: 1 if l[0] < l[1] else 0,
    7: lambda l: 1 if l[0] == l[1] else 0,
}


def bin_from_hex(hex_number: str) -> str:
    """Calculate the binary representation of the given `hex_number`"""
    binary = bin(int(hex_number, 16))
    binary = binary[2:]

    mod = len(binary) % 4
    if mod != 0:
        binary = binary.zfill(len(binary) + (4 - mod))

    return binary


def read_packet_header(binary_string: str) -> Tuple[int, int]:
    """Read the header of the `binary_string`, returning packet version and type"""
    return (int(binary_string[:3], 2), int(binary_string[3:6], 2))


def is_literal_value_packet(type: int) -> bool:
    """Check if the `type` corresponds to a literal value packet"""
    return type == 4


class LiteralValuePacket:
    def __init__(self, version: int, raw_data: str) -> None:
        """Construct a new LiteralValuePacket"""
        self.version = version
        self.literal, self.length = self._read_data(raw_data)

    def _read_data(self, binary_string: str) -> Tuple[int, int]:
        """Read the raw data given by `binary_string`, return the value and length"""
        finished = False
        cursor = 0
        result = ""

        while not finished:
            finished = int(binary_string[cursor]) == 0  # 0 represents the last group
            result += binary_string[cursor + 1 : cursor + 5]
            cursor += 5

        return (int(result, 2), cursor)


class OperatorPacket:
    def __init__(self, version: int, type: int, raw_data: str) -> None:
        """Construct a new OperatorPacket"""
        self.version = version

        assert type in TYPE_FUNCTIONS
        self.packet_function = TYPE_FUNCTIONS[type]

        self.literal_packets: List[LiteralValuePacket] = []
        self.operator_packets: List[OperatorPacket] = []
        self.length = self._read_data(raw_data)

    def _read_data(self, binary_string: str) -> int:
        """Read the data given by `binary_string`, return the total number of bits"""
        length_type = int(binary_string[0])
        cursor = 1

        if length_type == 0:
            number_of_bits = int(binary_string[cursor : cursor + 15], 2)
            cursor += 15
            cursor += self._read_data_bits(binary_string[cursor:], number_of_bits)
        else:
            number_of_packets = int(binary_string[cursor : cursor + 11], 2)
            cursor += 11
            cursor += self._read_data_number(binary_string[cursor:], number_of_packets)

        return cursor

    def _read_data_bits(self, binary_string: str, total_bits: int) -> int:
        """Read data given by `binary_string` up to the given number of `total_bits`"""
        cursor = 0
        while cursor < total_bits:
            cursor += self._read_packet(binary_string[cursor:])
        return cursor

    def _read_data_number(self, binary_string: str, total_number: int) -> int:
        """Read `total_number` of packets from the data given by `binary_string`"""
        cursor = 0
        for _ in range(total_number):
            cursor += self._read_packet(binary_string[cursor:])
        return cursor

    def _read_packet(self, binary_string: str) -> int:
        """Read a packet from the given `binary_string`"""
        version, type = read_packet_header(binary_string)
        cursor = HEADER_SIZE

        if is_literal_value_packet(type):
            packet = LiteralValuePacket(version, binary_string[cursor:])
            self.literal_packets.append(packet)
            cursor += packet.length
        else:
            packet = OperatorPacket(version, type, binary_string[cursor:])
            self.operator_packets.append(packet)
            cursor += packet.length

        return cursor

    def sum_of_versions(self) -> int:
        """Calculate the total sum of version numbers contained in the packet"""
        version_sum = self.version
        version_sum += sum([lp.version for lp in self.literal_packets])
        version_sum += sum([op.sum_of_versions() for op in self.operator_packets])
        return version_sum

    def result(self) -> int:
        """Calculate the result of the packet"""
        values = [lp.literal for lp in self.literal_packets]
        values += [op.result() for op in self.operator_packets]
        return self.packet_function(values)


def main():
    data_path = get_input_path("Day 16: Packet Decoder")
    with open(data_path, "r") as file:
        transmission = file.readline()

    start = timer()

    binary_string = bin_from_hex(transmission)
    version, type = read_packet_header(binary_string)
    assert not is_literal_value_packet(type)
    packet = OperatorPacket(version, type, binary_string[HEADER_SIZE:])

    version_sum = packet.sum_of_versions()
    total_result = packet.result()

    stop = timer()

    print("Sum of all version numbers:", version_sum)
    print("Result of the transmission:", total_result)
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
