import unittest
from unittest.mock import patch, mock_open
import Day01.main_day01 as day01


class TestSecretEntrance(unittest.TestCase):
    # ==========================================
    # Shared Helper Tests
    # ==========================================

    # --- Test: read_input ---
    def test_read_input_standard(self):
        """Test reading a standard file with valid lines."""
        mock_data = 'L68\nR48\nL5\n'
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = day01.read_input('dummy.txt')
        self.assertEqual(result, ['L68', 'R48', 'L5'])

    def test_read_input_with_empty_lines(self):
        """Test that whitespace and empty lines are filtered out."""
        mock_data = 'L10\n\n  \n R20 \n'
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = day01.read_input('dummy.txt')
        self.assertEqual(result, ['L10', 'R20'])

    # --- Test: parse_line ---
    def test_parse_line_left(self):
        """Test parsing a Left rotation."""
        self.assertEqual(day01.parse_line('L68'), -68)

    def test_parse_line_right(self):
        """Test parsing a Right rotation."""
        self.assertEqual(day01.parse_line('R48'), 48)

    def test_parse_line_large_number(self):
        """Test parsing larger numbers."""
        self.assertEqual(day01.parse_line('R12345'), 12345)

    def test_parse_line_invalid_direction(self):
        """Test that invalid direction characters raise ValueError."""
        with self.assertRaises(ValueError):
            day01.parse_line('X10')

    def test_parse_line_malformed_number(self):
        """Test that missing numbers raise ValueError."""
        with self.assertRaises(ValueError):
            day01.parse_line('L')
        with self.assertRaises(ValueError):
            day01.parse_line('Labc')

    # --- Test: calculate_new_lock_value (Shared Logic) ---
    def test_calc_lock_no_wrap(self):
        """Test simple addition/subtraction within bounds."""
        self.assertEqual(day01.calculate_new_lock_value(10, 50, 100), 60)
        self.assertEqual(day01.calculate_new_lock_value(-10, 50, 100), 40)

    def test_calc_lock_wrap_high(self):
        """Test wrapping around the top."""
        # 90 + 20 = 110 -> 10
        self.assertEqual(day01.calculate_new_lock_value(20, 90, 100), 10)

    def test_calc_lock_wrap_low(self):
        """Test wrapping around the bottom."""
        # 10 - 20 = -10 -> 90
        self.assertEqual(day01.calculate_new_lock_value(-20, 10, 100), 90)

    def test_calc_lock_exact_boundaries(self):
        """Test hitting 0 exactly from directions."""
        self.assertEqual(day01.calculate_new_lock_value(50, 50, 100), 0)
        self.assertEqual(day01.calculate_new_lock_value(-50, 50, 100), 0)

    def test_calc_lock_large_positive_rotation(self):
        """Test large rotations that would lap multiple times (updated logic)."""
        # 50 + 150 = 200 -> 100 -> 0
        self.assertEqual(day01.calculate_new_lock_value(150, 50, 100), 0)

    def test_calc_lock_large_negative_rotation(self):
        """Test large negative rotations that would lap multiple times."""
        # 50 - 250 = -200 -> -100 -> 0
        self.assertEqual(day01.calculate_new_lock_value(-250, 50, 100), 0)  # Fixed sign in arg

    # ==========================================
    # Part 1 Specific Tests
    # ==========================================

    def test_part1_apply_rotation_returns_tuple(self):
        """Ensure it returns (new_value, count)."""
        val, count = day01.apply_rotation(10, 50, 100)
        self.assertEqual(val, 60)
        self.assertEqual(count, 0)

    def test_part1_apply_rotation_counts_zero(self):
        """Ensure count is 1 when landing on 0."""
        val, count = day01.apply_rotation(10, 90, 100)
        self.assertEqual(val, 0)
        self.assertEqual(count, 1)

    def test_part1_calculate_password_scenario(self):
        """Integration test with a defined sequence (Part 1)."""
        rotations = ['R5', 'R5', 'L5', 'L5']
        # Start 0, Size 10.
        # R5 -> 5 (0)
        # R5 -> 0 (1)
        # L5 -> 5 (0)
        # L5 -> 0 (1) -> Total 2
        result = day01.calculate_password(start=0, rotations=rotations, lock_size=10, method=day01.Methods.part1)
        self.assertEqual(result, 2)

    def test_part1_calculate_password_no_zeros(self):
        """Test a sequence that never hits zero."""
        rotations = ['R1', 'R1', 'R1']
        result = day01.calculate_password(start=1, rotations=rotations, lock_size=10, method=day01.Methods.part1)
        self.assertEqual(result, 0)

    # ==========================================
    # Part 2 Specific Tests (Tick-by-Tick)
    # ==========================================

    def test_part2_single_tick_basic_move(self):
        """Test basic movement without crossing zero."""
        # Start 10, move 5 -> 15. Zero not passed.
        new_val, count = day01.apply_rotation_single_tick(5, 10, 100)
        self.assertEqual(new_val, 15)
        self.assertEqual(count, 0)

    def test_part2_single_tick_pass_zero_forward(self):
        """Test crossing zero moving forward (Right)."""
        # Start 98, move 3 (Size 100).
        # 98 -> 99 -> 0 (Hit!) -> 1.
        new_val, count = day01.apply_rotation_single_tick(3, 98, 100)
        self.assertEqual(new_val, 1)
        self.assertEqual(count, 1)

    def test_part2_single_tick_pass_zero_backward(self):
        """Test crossing zero moving backward (Left)."""
        # Start 2, move -3 (Size 100).
        # 2 -> 1 -> 0 (Hit!) -> 99.
        new_val, count = day01.apply_rotation_single_tick(-3, 2, 100)
        self.assertEqual(new_val, 99)
        self.assertEqual(count, 1)

    def test_part2_single_tick_land_on_zero(self):
        """Test landing exactly on zero."""
        # Start 1, move -1.
        # 1 -> 0 (Hit!).
        new_val, count = day01.apply_rotation_single_tick(-1, 1, 100)
        self.assertEqual(new_val, 0)
        self.assertEqual(count, 1)

    def test_part2_single_tick_multiple_laps(self):
        """Verify multiple zeros are counted in one rotation.
        Start 0, Move 200, Size 100.
        Should pass zero at tick 100 and tick 200.
        """
        # Start 0. Move +200.
        # ... tick 100 = 0 (Count 1)
        # ... tick 200 = 0 (Count 2)
        new_val, count = day01.apply_rotation_single_tick(200, 0, 100)
        self.assertEqual(new_val, 0)
        self.assertEqual(count, 2)

    def test_part2_single_tick_negative_multiple_laps(self):
        """Verify multiple zeros counted in negative direction."""
        # Start 0. Move -200.
        # ... tick 100 = 0 (Count 1)
        # ... tick 200 = 0 (Count 2)
        new_val, count = day01.apply_rotation_single_tick(-200, 0, 100)
        self.assertEqual(new_val, 0)
        self.assertEqual(count, 2)

    def test_part2_integration_vs_part1_difference(self):
        """
        Demonstrate a scenario where Part 1 and Part 2 yield different results.
        Start: 0, Size: 10. Rotation: R20.
        """
        rotations = ['R20']

        # Part 1: Logic calculates final pos. 0 + 20 = 20 -> 0.
        # Final pos is 0, so count = 1.
        p1_result = day01.calculate_password(0, rotations, 10, method=day01.Methods.part1)
        self.assertEqual(p1_result, 1)

        # Part 2: Ticks every step.
        # Tick 1..9
        # Tick 10 -> 0 (Count 1)
        # Tick 11..19
        # Tick 20 -> 0 (Count 2)
        p2_result = day01.calculate_password(0, rotations, 10, method=day01.Methods.part2)
        self.assertEqual(p2_result, 2)

    def test_part2_full_scenario(self):
        """Complex integration test for Part 2."""
        # Size 10. Start 5.
        # R5  -> 5..0 (Count 1). Pos 0.
        # L10 -> 0..0 (Count 1). Pos 0. (Goes -1..-9..0).
        # R20 -> 0..0 (Count 1)..0 (Count 2). Pos 0.
        rotations = ['R5', 'L10', 'R20']

        # Total expected: 1 + 1 + 2 = 4
        result = day01.calculate_password(5, rotations, 10, method=day01.Methods.part2)
        self.assertEqual(result, 4)


if __name__ == '__main__':
    _ = unittest.main()
