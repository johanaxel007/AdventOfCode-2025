def read_input(file_name: str) -> list[str]:
    """
    Read the input file and return a list of strings, split by comma.
    :param file_name: ex: input.txt
    :return: List of strings representing each line, split by comma from the file
    """
    input_raw: list[str] = open(file_name, 'r').readlines()

    all_ids: list[str] = []
    for id in input_raw:
        all_ids.extend(id.strip().split(','))

    return [id.strip() for id in all_ids if id.strip() != '']


def parse_product_id(product_id: str) -> list[int]:
    """
    Parse a product ID string into a list of integers.
    :param product_id: ex: '12-14'
    :return: List of integers representing the product ID. ex: [12, 13, 14]
    """
    parsed_id: list[str] = [id.strip() for id in product_id.split('-') if id.strip() != '']

    if len(parsed_id) != 2:
        raise ValueError('Invalid product ID: ' + product_id + ' - Invalid bounds format')

    lower_bound: int = int(parsed_id[0])
    upper_bound: int = int(parsed_id[1])

    if lower_bound > upper_bound:
        raise ValueError('Invalid product ID: ' + product_id + ' - Lower bound is greater than upper bound')

    return list(range(lower_bound, upper_bound + 1))


def parse_product_ids(product_ids: list[str]) -> list[int]:
    """
    Parse a list of product IDs into a list of valid integer ID's.
    :param product_ids: List of product IDs. ex: ['12-12', '13-14', '15-1168']
    :return: List of integers representing the product IDs. ex: [12, 12, 13, 14, 15, 12168]
    """
    all_ids_nested: list[list[int]] = [parse_product_id(id) for id in product_ids]

    all_ids: list[int] = []
    for id in all_ids_nested:
        all_ids.extend(id)

    return all_ids


# My original attempt at Part 1, before I realized the instructions was asking for ID's "made only of" some sequence of digits repeated twice.
# This method calculates all sequences of digits that repeat within the provided ID.
#
# def calculate_any_repeating_number_sequences(id: int) -> list[int]:
#     """
#     Identify sequences of digits that repeat immediately within the ID.
#     If a sequence of length 1 repeats (e.g., '11'), the value is the two digits (11).
#     If a sequence of length > 1 repeats (e.g., '1717'), the value is the sequence number (17).
#     """
#     id_str = str(id)
#     n = len(id_str)
#     repeating_sequences: list[int] = []
#     seen: set[int] = set()
#
#     # Iterate over possible lengths of the repeating sequence.
#     # The sequence must appear twice adjacently, so max length is half the string length.
#     for length in range(1, n // 2 + 1):
#         # Check every position where a sequence of 'length' could strictly repeat immediately
#         for i in range(n - 2 * length + 1):
#             chunk1 = id_str[i : i + length]
#             chunk2 = id_str[i + length : i + 2 * length]
#
#             if chunk1 == chunk2:
#                 # Calculate the value based on the chunk size
#                 # '113' (chunk '1') -> 11
#                 # '1717' (chunk '17') -> 17
#                 if length == 1:
#                     value = int(chunk1 + chunk1)
#                 else:
#                     value = int(chunk1)
#
#                 if value not in seen:
#                     repeating_sequences.append(value)
#                     seen.add(value)
#
#     return repeating_sequences


def calculate_only_repeating_number_sequences(id: int) -> list[int]:
    """
    Identify if the ENTIRE ID is made of a sequence repeated twice.
    Returns a list containing the sequence if true, empty list otherwise.
    """
    id_str = str(id)
    n = len(id_str)

    # If length is odd, it cannot be two equal halves (e.g., 123)
    if n % 2 != 0:
        return []

    mid_point = n // 2
    first_half = id_str[:mid_point]
    second_half = id_str[mid_point:]

    if first_half == second_half:
        # We found a match! The instructions imply the ID is invalid.
        # We return the sequence found to satisfy the "len > 0" check in calculate_answer.
        return [int(first_half)]

    return []


def calculate_answer(ids: list[int]) -> int:
    invalid_ids: list[int] = []

    for id in ids:
        repeating_sequences = calculate_only_repeating_number_sequences(id)
        if len(repeating_sequences) > 0:
            invalid_ids.append(id)

    return sum(invalid_ids)


if __name__ == '__main__':
    input_product_ids: list[str] = read_input('input.txt')
    input_product_ids_parsed: list[int] = parse_product_ids(input_product_ids)

    # --- Part 1 ---
    password_part_1 = calculate_answer(input_product_ids_parsed)
    print(f'PW Part 1: {password_part_1}')

    # --- Part 2 ---
    # password_part_2 = calculate_answer(input_product_ids_parsed)
    # print(f'PW Part 2: {password_part_2}')
