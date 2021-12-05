#!/usr/bin/env python3

from typing import List, Tuple


def calculate_most_common_bit(binary_numbers: List[str], pos: int) -> str:
    count = 0
    for number in binary_numbers:
        if number[pos] == "1":
            count += 1

    number_count = len(binary_numbers)
    return "1" if (count >= number_count / 2) else "0"


def calculate_least_common_bit(binary_numbers: List[str], pos: int) -> str:
    mcb = calculate_most_common_bit(binary_numbers, pos)
    return "1" if mcb == "0" else "0"


def calculate_oxygen_generator_rating(binary_numbers: List[str]) -> int:
    filtered_list = binary_numbers
    idx = 0

    while len(filtered_list) > 1:
        mcb = calculate_most_common_bit(filtered_list, idx)
        filtered_list = list(filter(lambda number: number[idx] == mcb, filtered_list))
        idx += 1

    return int(filtered_list[0], 2)


def calculate_co2_scrubber_rating(binary_numbers: List[str]) -> int:
    filtered_list = binary_numbers
    idx = 0

    while len(filtered_list) > 1:
        lcb = calculate_least_common_bit(filtered_list, idx)
        filtered_list = list(filter(lambda number: number[idx] == lcb, filtered_list))
        idx += 1

    return int(filtered_list[0], 2)


def calculate_gamma_and_epsilon_rate(binary_numbers: List[str]) -> Tuple[int, int]:
    number_of_entries = len(binary_numbers)
    number_of_bits = len(binary_numbers[0])

    bits_count = [0] * number_of_bits
    for number in binary_numbers:
        for i in range(number_of_bits):
            bits_count[i] += int(number[i])

    most_common_bits = [cnt > (number_of_entries / 2) for cnt in bits_count]

    gamma_rate = int("".join(["1" if bit else "0" for bit in most_common_bits]), 2)
    epsilon_rate = int("".join(["0" if bit else "1" for bit in most_common_bits]), 2)

    return (gamma_rate, epsilon_rate)


if __name__ == "__main__":
    data_path = "./data/03_diagnostic-report.txt"
    with open(data_path, "r") as file:
        binary_numbers = file.read().splitlines()

    gamma, epsilon = calculate_gamma_and_epsilon_rate(binary_numbers)
    power_consumption = gamma * epsilon
    print(
        f"Power consumption: {power_consumption}"
        f" (Gamma rate: {gamma}, Epsilon rate: {epsilon})"
    )

    oxygen_gen_rating = calculate_oxygen_generator_rating(binary_numbers)
    co2_scrubber_rating = calculate_co2_scrubber_rating(binary_numbers)
    life_support_rating = oxygen_gen_rating * co2_scrubber_rating
    print(
        f"Life support rating: {life_support_rating}"
        f" (Oxygen generator rating: {oxygen_gen_rating},"
        f" CO2 scrubber rating: {co2_scrubber_rating})"
    )
