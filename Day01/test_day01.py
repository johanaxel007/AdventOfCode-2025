import unittest
from unittest.mock import patch, mock_open
import Day1.main_day1 as day1


class TestSecretEntrance(unittest.TestCase):
    # --- Test: read_input ---
    def test_read_input_standard(self):
        """Test reading a standard file with valid lines."""
        mock_data = 'L68\nR48\nL5\n'
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = day1.read_input('dummy.txt')
        self.assertEqual(result, ['L68', 'R48', 'L5'])

    def test_read_input_with_empty_lines(self):
        """Test that whitespace and empty lines are filtered out."""
        mock_data = 'L10\n\n  \n R20 \n'
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = day1.read_input('dummy.txt')
        # Note: logic strips the line, so " R20 " becomes "R20"
        self.assertEqual(result, ['L10', 'R20'])

    # --- Test: parse_line ---
    def test_parse_line_left(self):
        """Test parsing a Left rotation."""
        self.assertEqual(day1.parse_line('L68'), -68)

    def test_parse_line_right(self):
        """Test parsing a Right rotation."""
        self.assertEqual(day1.parse_line('R48'), 48)

    def test_parse_line_large_number(self):
        """Test parsing larger numbers."""
        self.assertEqual(day1.parse_line('R12345'), 12345)

    def test_parse_line_invalid_direction(self):
        """Test that invalid direction characters raise ValueError."""
        # The function raises ValueError manually for known bad chars,
        # or implicitly via int() conversion if format is wrong.
        with self.assertRaises(ValueError):
            day1.parse_line('X10')

    def test_parse_line_malformed_number(self):
        """Test that missing numbers raise ValueError (via int conversion)."""
        with self.assertRaises(ValueError):
            day1.parse_line('L')  # No number
        with self.assertRaises(ValueError):
            day1.parse_line('Labc')  # Not a number

    # --- Test: calculate_new_lock_value ---
    def test_calc_lock_no_wrap(self):
        """Test simple addition/subtraction within bounds."""
        # Start 50, move +10, size 100 -> 60
        self.assertEqual(day1.calculate_new_lock_value(10, 50, 100), 60)
        # Start 50, move -10, size 100 -> 40
        self.assertEqual(day1.calculate_new_lock_value(-10, 50, 100), 40)

    def test_calc_lock_wrap_high(self):
        """Test wrapping around the top (e.g., 90 + 20 = 110 -> 10)."""
        # Logic: 90 + 20 = 110. 110 >= 100. Returns 110 - 100 = 10.
        self.assertEqual(day1.calculate_new_lock_value(20, 90, 100), 10)

    def test_calc_lock_wrap_low(self):
        """Test wrapping around the bottom (e.g., 10 - 20 = -10 -> 90)."""
        # Logic: 10 - 20 = -10. -10 < 0. Returns -10 + 100 = 90.
        self.assertEqual(day1.calculate_new_lock_value(-20, 10, 100), 90)

    def test_calc_lock_exact_boundaries(self):
        """Test hitting 0 exactly from directions."""
        # 50 + 50 = 100 -> Wrap -> 0
        self.assertEqual(day1.calculate_new_lock_value(50, 50, 100), 0)
        # 50 - 50 = 0 -> No wrap needed -> 0
        self.assertEqual(day1.calculate_new_lock_value(-50, 50, 100), 0)

    def test_calc_lock_large_positive_rotation(self):
        """test large rotations that would lap multiple times."""
        # 50 + 150 = 200 -> Wrap -> 100 -> Wrap -> 0
        self.assertEqual(day1.calculate_new_lock_value(150, 50, 100), 0)

    def test_calc_lock_large_negative_rotation(self):
        """test large rotations that would lap multiple times."""
        # 50 - 250 = -200 -> Wrap -> -100 -> Wrap -> 0
        self.assertEqual(day1.calculate_new_lock_value(250, 50, 100), 0)

    # --- Test: apply_rotation ---
    def test_apply_rotation_returns_tuple(self):
        """Ensure it returns (new_value, count)."""
        val, count = day1.apply_rotation(10, 50, 100)
        self.assertEqual(val, 60)
        self.assertEqual(count, 0)

    def test_apply_rotation_counts_zero(self):
        """Ensure count is 1 when landing on 0."""
        # 90 + 10 = 100 -> wraps to 0
        val, count = day1.apply_rotation(10, 90, 100)
        self.assertEqual(val, 0)
        self.assertEqual(count, 1)

    # --- Test: calculate_password (Integration) ---
    def test_calculate_password_scenario(self):
        """
        Integration test with a defined sequence.
        Lock Size: 10
        Start: 0

        1. R5  -> 5  (count 0)
        2. R5  -> 10 -> 0 (count 1)
        3. L5  -> -5 -> 5 (count 0)
        4. L5  -> 0  (count 1)

        Total count should be 2.
        """
        rotations = ['R5', 'R5', 'L5', 'L5']
        result = day1.calculate_password(start=0, rotations=rotations, lock_size=10)
        self.assertEqual(result, 2)

    def test_calculate_password_no_zeros(self):
        """Test a sequence that never hits zero."""
        rotations = ['R1', 'R1', 'R1']
        result = day1.calculate_password(start=1, rotations=rotations, lock_size=10)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    _ = unittest.main()
