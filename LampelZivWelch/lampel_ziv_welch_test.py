import unittest
from .lampel_ziv_welch import LampelZivWelch


class TestLZWCompression(unittest.TestCase):

    def setUp(self):
        """Set up the LZW object before each test."""
        self.lzw = LampelZivWelch()

    def test_compress_decompress(self):
        """Test that compression and decompression works correctly."""
        input_string = "ABABABABABA"
        compressed_data = self.lzw.compress(input_string)
        decompressed_string = self.lzw.decompress(compressed_data)

        self.assertEqual(decompressed_string, input_string,
                         "Decompressed string does not match the original")
        print(
            f"test_compress_decompress passed | Compressed Data: {compressed_data} | Decompressed Data: {decompressed_string}")

    def test_compression_ratio(self):
        """Test the compression ratio calculation."""
        input_string = "ABABABABABA"
        compressed_data = self.lzw.compress(input_string)

        # Compute the compression ratio
        ratio = self.lzw.get_compression_ratio(input_string, compressed_data)

        # Check that the ratio is a valid percentage
        self.assertGreaterEqual(ratio, 0, "Compression ratio should be >= 0")
        self.assertLessEqual(ratio, 100, "Compression ratio should be <= 100")
        print(f"test_compression_ratio passed | Compression Ratio: {ratio}%")

    def test_single_character_string(self):
        """Test compression and decompression of a string with only one character repeated."""
        input_string = "AAAAA"
        compressed_data = self.lzw.compress(input_string)
        decompressed_string = self.lzw.decompress(compressed_data)

        self.assertEqual(decompressed_string, input_string,
                         "Decompressed string for single-character input does not match the original")
        print(
            f"test_single_character_string passed | Compressed Data: {compressed_data} | Decompressed Data: {decompressed_string}")

    def test_empty_string(self):
        """Test compression and decompression of an empty string."""
        input_string = ""
        compressed_data = self.lzw.compress(input_string)
        decompressed_string = self.lzw.decompress(compressed_data)

        self.assertEqual(decompressed_string, input_string,
                         "Decompressed string for empty input does not match the original")
        print(
            f"test_empty_string passed | Compressed Data: {compressed_data} | Decompressed Data: {decompressed_string}")

    def test_large_input(self):
        """Test compression and decompression on a large input string."""
        input_string = "A" * 1000  # Large string of repeating 'A's
        compressed_data = self.lzw.compress(input_string)
        decompressed_string = self.lzw.decompress(compressed_data)

        self.assertEqual(decompressed_string, input_string,
                         "Decompressed string for large input does not match the original")
        print(
            f"test_large_input passed | Compressed Data: {compressed_data[:100]}... (truncated) | Decompressed Data: {decompressed_string[:100]}... (truncated)")

    def test_compression_ratio_with_large_input(self):
        """Test compression ratio on a large input string."""
        input_string = "A" * 1000
        compressed_data = self.lzw.compress(input_string)

        # Compute the compression ratio
        ratio = self.lzw.get_compression_ratio(input_string, compressed_data)

        # Check if the compression ratio makes sense for the input size
        self.assertGreater(
            ratio, 0, "Compression ratio should be greater than 0 for non-empty strings")
        self.assertLess(
            ratio, 100, "Compression ratio should be less than 100 for large inputs")
        print(
            f"test_compression_ratio_with_large_input passed | Compression Ratio: {ratio}%")

    def test_compression_edge_case(self):
        """Test compression and decompression on an edge case string."""
        input_string = "ABCABCABCABCABC"  # Patterned string
        compressed_data = self.lzw.compress(input_string)
        decompressed_string = self.lzw.decompress(compressed_data)

        self.assertEqual(decompressed_string, input_string,
                         "Decompressed string for edge case input does not match the original")
        print(
            f"test_compression_edge_case passed | Compressed Data: {compressed_data} | Decompressed Data: {decompressed_string}")

    def test_non_ascii_characters(self):
        """Test handling of non-ASCII characters."""
        input_string = "áéíóú"
        compressed_data = self.lzw.compress(input_string)
        decompressed_string = self.lzw.decompress(compressed_data)

        self.assertEqual(decompressed_string, input_string,
                         "Decompressed string for non-ASCII input does not match the original")
        print(
            f"test_non_ascii_characters passed | Compressed Data: {compressed_data} | Decompressed Data: {decompressed_string}")


unittest.main(argv=[''], verbosity=2, exit=False)
