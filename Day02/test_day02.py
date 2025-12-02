import unittest
from unittest.mock import patch, mock_open
import Day02.main_day02 as day02


class TestSecretEntrance(unittest.TestCase):
    # ==========================================
    # Shared Helper Tests
    # ==========================================

    # --- Test: read_input ---
    def test_read_input_standard(self):
        """Test reading a standard file with valid lines."""
        mock_data = '12-12,345-453,698-127,15345-123'
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = day02.read_input('dummy.txt')
        self.assertEqual(result, ['12-12', '345-453', '698-127', '15345-123'])

    def test_read_input_with_empty_lines(self):
        """Test that whitespace and empty lines are filtered out."""
        mock_data = '12-12,345-453,\n\n  \n 698-127,15345-123 \n'
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = day02.read_input('dummy.txt')
        self.assertEqual(result, ['12-12', '345-453', '698-127', '15345-123'])

    # --- Test: parse_product_id ---
    def test_parse_product_id_single_item_range(self):
        """Test parsing a range where start equals end (e.g., 12-12)."""
        # Range(12, 13) -> [12]
        result = day02.parse_product_id('12-12')
        self.assertEqual(result, [12])

    def test_parse_product_id_expansion(self):
        """Test parsing a standard range (e.g., 12-14)."""
        # Range(12, 15) -> [12, 13, 14]
        result = day02.parse_product_id('12-14')
        self.assertEqual(result, [12, 13, 14])

    def test_parse_product_id_invalid_format_missing_part(self):
        """Test that missing ID parts raise ValueError (e.g., '12-')."""
        with self.assertRaises(ValueError):
            day02.parse_product_id('12-')

    def test_parse_product_id_invalid_format_empty(self):
        """Test that empty strings raise ValueError."""
        with self.assertRaises(ValueError):
            day02.parse_product_id('')

    def test_parse_product_id_invalid_bounds(self):
        """Test that lower bound > upper bound raises ValueError."""
        with self.assertRaises(ValueError):
            day02.parse_product_id('14-12')

    # --- Test: parse_product_ids ---
    def test_parse_product_ids_standard(self):
        """Test parsing a list of product IDs with range expansion."""
        # '12-12' -> [12]
        # '5-7'   -> [5, 6, 7]
        # '20-21' -> [20, 21]
        input_ids = ['12-12', '5-7', '20-21']
        result = day02.parse_product_ids(input_ids)
        self.assertEqual(result, [12, 5, 6, 7, 20, 21])

    # --- Test: calculate_only_repeating_number_sequences ---

    def test_check_odd_length_ignored(self):
        """112 is odd length, so it cannot be XX. Should be empty (Valid ID)."""
        result = day02.calculate_only_repeating_number_sequences(112)
        self.assertEqual(result, [])

    def test_check_simple_repeat(self):
        """55 is 5 repeated twice. Should return [5]."""
        result = day02.calculate_only_repeating_number_sequences(55)
        self.assertEqual(result, [5])

    def test_check_double_digit_repeat(self):
        """6464 is 64 repeated twice. Should return [64]."""
        result = day02.calculate_only_repeating_number_sequences(6464)
        self.assertEqual(result, [64])

    def test_check_triple_digit_repeat(self):
        """123123 is 123 repeated twice."""
        result = day02.calculate_only_repeating_number_sequences(123123)
        self.assertEqual(result, [123])

    def test_check_large_number_example(self):
        """Example from instruction: 1188511885."""
        result = day02.calculate_only_repeating_number_sequences(1188511885)
        self.assertEqual(result, [11885])

    def test_check_almost_match_fails(self):
        """123124 is not a repeat."""
        result = day02.calculate_only_repeating_number_sequences(123124)
        self.assertEqual(result, [])

    # --- Test: calculate_any_repeating_number_sequences ---
    # def test_calculate_any_repeating_number_sequences_no_sequences(self):
    #     """Test parsing a number with no repeating number sequences."""
    #     result = day02.calculate_any_repeating_number_sequences(123456789)
    #     self.assertEqual(result, [])
    #
    # def test_calculate_any_repeating_number_sequences_with_sequence_at_start(self):
    #     """Test parsing a number with 1 repeating number sequences at the start."""
    #     result = day02.calculate_any_repeating_number_sequences(113)
    #     self.assertEqual(result, [11])
    #
    # def test_calculate_any_repeating_number_sequences_with_sequence_at_end(self):
    #     """Test parsing a number with 1 repeating number sequences at the end."""
    #     result = day02.calculate_any_repeating_number_sequences(311)
    #     self.assertEqual(result, [11])
    #
    # def test_calculate_any_repeating_number_sequences_with_repeating_number_sequence_at_start_and_end(self):
    #     """Test parsing a number with 1 repeating number sequences at the end."""
    #     result = day02.calculate_any_repeating_number_sequences(1717)
    #     self.assertEqual(result, [17])
    #
    # def test_calculate_any_repeating_number_sequences_multiple_distinct_groups(self):
    #     """Test a number with multiple separate repeating groups (11 and 22)."""
    #     # '1'=='1' -> 11, '2'=='2' -> 22
    #     result = day02.calculate_any_repeating_number_sequences(1122)
    #     # Order usually depends on appearance, but checking set equality is safer
    #     self.assertEqual(set(result), {11, 22})
    #
    # def test_calculate_any_repeating_number_sequences_triple_digits(self):
    #     """Test a number like 111. It contains '11' twice, but should return unique sequences."""
    #     result = day02.calculate_any_repeating_number_sequences(111)
    #     self.assertEqual(result, [11])
    #
    # def test_calculate_any_repeating_number_sequences_long_pattern(self):
    #     """Test a longer repeating pattern (123-123)."""
    #     result = day02.calculate_any_repeating_number_sequences(123123)
    #     self.assertEqual(result, [123])
    #
    # def test_calculate_any_repeating_number_sequences_nested_pattern(self):
    #     """
    #     Test 1111.
    #     1. '1' repeats -> 11.
    #     2. '11' repeats -> 11.
    #     Result should be unique [11].
    #     """
    #     result = day02.calculate_any_repeating_number_sequences(1111)
    #     self.assertEqual(result, [11])
    #
    # def test_calculate_any_repeating_number_sequences_zeros(self):
    #     """Test handling of 0."""
    #     # '00' -> 0
    #     result = day02.calculate_any_repeating_number_sequences(1001)
    #     self.assertEqual(result, [0])
    #
    # def test_calculate_any_repeating_number_sequences_zeros_pattern(self):
    #     """Test handling of 0 in a pattern."""
    #     # '10' repeats -> 10
    #     result = day02.calculate_any_repeating_number_sequences(1010)
    #     self.assertEqual(result, [10])

    # --- Test: calculate_answer (Integration) ---
    def test_calculate_answer_instruction_example(self):
        """
        Tests the specific logic from the instruction example.
        Invalid IDs (to be summed):
        - 11 (from 11-22)
        - 22 (from 11-22)
        - 99 (from 95-115)
        - 1010 (from 998-1012)
        Sum = 11 + 22 + 99 + 1010 = 1142
        """
        # I'll pick a few ranges from the example to verify summation
        ids = [
            # ---
            11,
            12,
            22,  # 11, 22 invalid. 12 valid.
            # ---
            99,
            100,
            101,  # 99 invalid.
            # ---
            1010,
            1011,  # 1010 invalid.
        ]
        result = day02.calculate_answer(ids)
        self.assertEqual(result, 11 + 22 + 99 + 1010)

    # # --- Test: calculate_answer (Integration) ---
    # def test_calculate_answer_mixed(self):
    #     """
    #     Test the final summation logic.
    #     123 -> No repeats -> Valid (Drop)
    #     112 -> Has '11' -> Invalid (Keep)
    #     1212 -> Has '12' -> Invalid (Keep)
    #     456 -> No repeats -> Valid (Drop)
    #
    #     Sum = 112 + 1212 = 1324
    #     """
    #     ids = [123, 112, 1212, 456]
    #     result = day02.calculate_answer(ids)
    #     self.assertEqual(result, 1324)
    #
    # def test_calculate_answer_all_invalid(self):
    #     """Test case where all IDs have repeats."""
    #     ids = [11, 22, 1212, 33]
    #     result = day02.calculate_answer(ids)
    #     self.assertEqual(result, 1278)
    #
    # def test_calculate_answer_all_valid(self):
    #     """Test case where no IDs have repeats."""
    #     ids = [123, 456, 789, 9182]
    #     result = day02.calculate_answer(ids)
    #     self.assertEqual(result, 0)


if __name__ == '__main__':
    _ = unittest.main()
