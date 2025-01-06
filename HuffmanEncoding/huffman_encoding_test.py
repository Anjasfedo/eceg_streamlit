import unittest
from HuffmanEncoding import HuffmanEncoding


class TestHuffmanEncoding(unittest.TestCase):
    def test_build_frequency_table(self):
        """Test the building of frequency table from text."""
        text = "hello"
        freq_table = HuffmanEncoding.build_frequency_table(text)
        expected_freq = {'h': 1, 'e': 1, 'l': 2, 'o': 1}

        self.assertEqual(freq_table, expected_freq,
                         f"Expected frequency table: {expected_freq}, but got: {freq_table}")

    def test_build_huffman_tree(self):
        """Test the construction of the Huffman Tree."""
        text = "hello"
        freq_table = HuffmanEncoding.build_frequency_table(text)
        huffman_tree = HuffmanEncoding.build_huffman_tree(freq_table)

        self.assertIsNotNone(
            huffman_tree, "Huffman tree root should not be None.")
        self.assertIsNone(huffman_tree.char,
                          "Root node should be an internal node, not a leaf.")

    def test_generate_huffman_codes(self):
        """Test the generation of Huffman codes."""
        text = "hello"
        freq_table = HuffmanEncoding.build_frequency_table(text)
        huffman_tree = HuffmanEncoding.build_huffman_tree(freq_table)
        codebook = HuffmanEncoding.generate_huffman_codes(huffman_tree)

        # Ensure that all characters have a code
        self.assertGreater(len(codebook), 0, "Codebook should not be empty.")
        for char in text:
            self.assertIn(char, codebook,
                          f"Character {char} missing from codebook.")

    def test_encode(self):
        """Test the encoding of the text."""
        text = "hello"
        freq_table = HuffmanEncoding.build_frequency_table(text)
        huffman_tree = HuffmanEncoding.build_huffman_tree(freq_table)
        codebook = HuffmanEncoding.generate_huffman_codes(huffman_tree)

        encoded_text, padding = HuffmanEncoding.encode(text, codebook)

        self.assertGreater(len(encoded_text), 0,
                           "Encoded text should not be empty.")
        self.assertTrue(
            0 <= padding < 8, f"Padding should be between 0 and 7, but got {padding}.")

    def test_decode(self):
        """Test the decoding of the encoded text."""
        text = "hello"
        freq_table = HuffmanEncoding.build_frequency_table(text)
        huffman_tree = HuffmanEncoding.build_huffman_tree(freq_table)
        codebook = HuffmanEncoding.generate_huffman_codes(huffman_tree)

        encoded_text, padding = HuffmanEncoding.encode(text, codebook)
        decoded_text = HuffmanEncoding.decode(
            encoded_text, huffman_tree, padding)

        self.assertEqual(
            decoded_text, text, f"Decoded text: {decoded_text} does not match original text: {text}.")

    def test_build_huffman(self):
        """Test the full Huffman encoding pipeline."""
        text = "hello"
        encoded_text, codebook, huffman_tree, padding = HuffmanEncoding.build_huffman(
            text)

        self.assertGreater(len(encoded_text), 0,
                           "Encoded text should not be empty.")
        self.assertIsNotNone(huffman_tree, "Huffman tree should not be None.")
        self.assertTrue(
            0 <= padding < 8, f"Padding should be between 0 and 7, but got {padding}.")
        self.assertGreater(len(codebook), 0, "Codebook should not be empty.")

    def test_get_compression_ratio(self):
        """Test the compression ratio calculation."""
        text = "hello"
        encoded_text, codebook, huffman_tree, padding = HuffmanEncoding.build_huffman(
            text)

        compression_ratio = HuffmanEncoding.get_compression_ratio(
            text, encoded_text)
        self.assertGreater(
            compression_ratio, 0, f"Expected positive compression ratio, but got {compression_ratio}.")

    def test_decoding_with_bundle(self):
        """Test decoding using bundled Huffman tree and padding."""
        text = "hello"
        encoded_text, codebook, huffman_tree, padding = HuffmanEncoding.build_huffman(
            text)

        # Simulate bundling tree and padding
        bundle = {"huffman_tree": huffman_tree, "padding": padding}

        # Decode using bundle
        decoded_text = HuffmanEncoding.decode(
            encoded_text, bundle["huffman_tree"], bundle["padding"])
        self.assertEqual(
            decoded_text, text, f"Decoded text: {decoded_text} does not match original text: {text}.")


if __name__ == "__main__":
    unittest.main(argv=[""], verbosity=2, exit=False)
