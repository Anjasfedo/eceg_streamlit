import unittest
from .huffman_encoding import HuffmanEncoding

class TestHuffmanEncoding(unittest.TestCase):

    def test_build_frequency_table(self):
        """Test the building of frequency table from text."""
        text = "hello"
        huffman = HuffmanEncoding(text)

        freq_table = huffman.build_frequency_table()
        expected_freq = {'h': 1, 'e': 1, 'l': 2, 'o': 1}

        self.assertEqual(freq_table, expected_freq,
                         f"Expected frequency table: {expected_freq}, but got: {freq_table}")

    def test_build_huffman_tree(self):
        """Test the construction of the Huffman Tree."""
        text = "hello"
        huffman = HuffmanEncoding(text)

        huffman.build_huffman_tree()
        root = huffman.huffman_tree

        self.assertIsNotNone(root, "Huffman tree root should not be None.")
        self.assertIsNone(
            root.char, "Root node should be an internal node, not a leaf.")

    # def test_generate_huffman_codes(self):
    #     """Test the generation of Huffman codes."""
    #     text = "hello"
    #     huffman = HuffmanEncoding(text)

    #     huffman.build_huffman_tree()
    #     codebook = huffman.generate_huffman_codes()

    #     # Sample check for codebook
    #     expected_codebook = {'h': '00', 'e': '01', 'l': '10', 'o': '11'}

    #     self.assertEqual(codebook, expected_codebook, f"Expected codebook: {expected_codebook}, but got: {codebook}")

    def test_encode(self):
        """Test the encoding of the text."""
        text = "hello"
        huffman = HuffmanEncoding(text)

        huffman.build_huffman_tree()
        huffman.generate_huffman_codes()

        encoded_text, padding = huffman.encode(text)

        # Check if encoded text is not empty
        self.assertGreater(len(encoded_text), 0,
                           "Encoded text should not be empty.")

        # Ensure that the padding is correct
        self.assertTrue(
            0 <= padding < 8, f"Padding should be between 0 and 7, but got {padding}.")

    def test_decode(self):
        """Test the decoding of the encoded text."""
        text = "hello"
        huffman = HuffmanEncoding(text)

        huffman.build_huffman_tree()
        huffman.generate_huffman_codes()

        encoded_text, padding = huffman.encode(text)

        decoded_text = huffman.decode(encoded_text, padding)

        self.assertEqual(
            decoded_text, text, f"Decoded text: {decoded_text} does not match original text: {text}.")

    def test_compression_ratio(self):
        """Test the compression ratio calculation."""
        original_text = "hello"
        huffman = HuffmanEncoding(original_text)

        huffman.build_huffman_tree()
        encoded_text, padding = huffman.encode(original_text)

        compression_ratio = huffman.get_compression_ratio(
            original_text, encoded_text)

        self.assertGreater(
            compression_ratio, 0, f"Expected positive compression ratio, but got {compression_ratio}.")

    def test_huffman_decoding(self):
        """Test the decoding using huffman_decoding method."""
        text = "hello"
        huffman = HuffmanEncoding(text)

        huffman.build_huffman_tree()
        huffman.generate_huffman_codes()

        encoded_text, padding = huffman.encode(text)

        decoded_text = huffman.huffman_decoding(encoded_text, padding)

        self.assertEqual(
            decoded_text, text, f"Decoded text: {decoded_text} does not match original text: {text}.")

    def test_encoded_text_length(self):
        """Test the length of the encoded text."""
        text = "hello"
        huffman = HuffmanEncoding(text)

        huffman.build_huffman_tree()
        huffman.generate_huffman_codes()

        encoded_text, padding = huffman.encode(text)

        encoded_length = huffman.encoded_text_length(encoded_text)

        # Check if length of encoded text is greater than 0
        self.assertGreater(
            encoded_length, 0, f"Encoded text length should be greater than 0, but got {encoded_length}.")

    # def test_decode_to_chars(self):
    #     """Test converting encoded bits back to characters."""
    #     text = "hello"
    #     huffman = HuffmanEncoding(text)

    #     huffman.build_huffman_tree()
    #     huffman.generate_huffman_codes()

    #     encoded_text, padding = huffman.encode(text)

    #     decoded_chars = huffman.decode_to_chars(encoded_text, padding)

    #     self.assertEqual(decoded_chars, text, f"Decoded characters: {decoded_chars} do not match the original text: {text}.")


unittest.main(argv=[''], verbosity=2, exit=False)
