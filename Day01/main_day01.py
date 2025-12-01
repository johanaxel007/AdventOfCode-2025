# Advent of Code 2025 - Day 1 - Secret Entrance
# https://adventofcode.com/2025/day/1
# Done by: johanaxel007


from enum import StrEnum


class Methods(StrEnum):
    part1 = 'apply_rotation'
    part2 = 'apply_rotation_single_tick'


def read_input(file_name: str) -> list[str]:
    """
    Read the input file and return a list of strings.
    :param file_name: ex: input.txt
    :return: List of strings representing each line from the file
    """
    input_raw: list[str] = open(file_name, 'r').readlines()
    return [line.strip() for line in input_raw if line.strip() != '']


def parse_line(line: str) -> int:
    """
    Parse a line of input and return an integer.
    :param line: ex: 'L68'
    :return: Integer representing the rotation_step. eg(L68 -> -68, R48 -> 48)
    """
    rotation: str = line[0]
    distance: int = int(line[1:])

    if rotation == 'L':
        return -1 * distance
    elif rotation == 'R':
        return 1 * distance
    else:
        raise ValueError('Invalid rotation_step: ' + rotation)


def calculate_new_lock_value(rotation_step: int, current_lock_value: int, lock_size: int) -> int:
    """
    Calculate the new lock value after a rotation. Accounts for the lock being circular by making sure the value is always between 0 and lock_size - 1.
    :param rotation_step: The rotation step amount to apply.
    :param current_lock_value: The current value of the lock.
    :param lock_size: The max bound of the lock.
    :return: The new lock value.
    """
    new_value: int = current_lock_value + rotation_step

    while new_value < 0:
        new_value += lock_size
    while new_value >= lock_size:
        new_value -= lock_size

    return new_value


def apply_rotation(rotation: int, current_lock_value: int, lock_size: int) -> tuple[int, int]:
    """
    Apply a full rotation to the lock and return the new lock value and the number of times the lock was at 0.
    :param rotation: The full rotation (eg: -68 or 48)
    :param current_lock_value: The current value of the lock.
    :param lock_size: The max bound of the lock.
    :return: Tuple of (new_lock_value, at_zero_count)
    """
    new_value = current_lock_value
    at_zero_count: int = 0

    new_value = calculate_new_lock_value(rotation, new_value, lock_size)

    if new_value == 0:
        at_zero_count += 1

    return new_value, at_zero_count


def apply_rotation_single_tick(rotation: int, current_lock_value: int, lock_size: int) -> tuple[int, int]:
    """
    Apply a full rotation to the lock and return the new lock value and the number of times the lock was passed 0 using 0x434C49434B method.
    :param rotation: The full rotation (eg: -68 or 48)
    :param current_lock_value: The current value of the lock.
    :param lock_size: The max bound of the lock.
    :return: Tuple of (new_lock_value, at_zero_count)
    """
    new_value = current_lock_value
    at_zero_count: int = 0

    rotation_steps: int = abs(rotation)
    rotation_direction: int = 1 if rotation > 0 else -1

    while rotation_steps > 0:
        new_value = calculate_new_lock_value(rotation_direction, new_value, lock_size)

        if new_value == 0:
            at_zero_count += 1

        rotation_steps -= 1

    return new_value, at_zero_count


def calculate_password(start: int, rotations: list[str], lock_size: int = 100, method: Methods = Methods.part1) -> int:
    """
    Calculate the password by counting how many times the lock points at 0 after each rotation.
    :param start: The starting point of the lock
    :param rotations: The full rotations list (eg: L68, R48)
    :param lock_size: The max bound of the lock.
    :return: The password.
    """
    current_lock_value: int = start
    at_zero_count_total: int = 0

    for rotation in rotations:
        rotation_value: int = parse_line(rotation)
        new_value: int = current_lock_value
        at_zero_count: int = 0

        match method:
            case Methods.part1:
                new_value, at_zero_count = apply_rotation(rotation_value, current_lock_value, lock_size)
            case Methods.part2:
                new_value, at_zero_count = apply_rotation_single_tick(rotation_value, current_lock_value, lock_size)

        current_lock_value = new_value
        at_zero_count_total += at_zero_count

    return at_zero_count_total


if __name__ == '__main__':
    input_rotations: list[str] = read_input('input.txt')
    start_point: int = 50
    lock_size: int = 100

    # --- Part 1 ---
    password_part_1 = calculate_password(start_point, input_rotations, lock_size, Methods.part1)
    print(f"PW Part 1: {password_part_1}")

    # --- Part 2 ---
    password_part_2 = calculate_password(start_point, input_rotations, lock_size, Methods.part2)
    print(f"PW Part 2: {password_part_2}")
