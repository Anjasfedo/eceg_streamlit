import heapq
from collections import Counter


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanEncoding:
    @staticmethod
    def build_frequency_table(text):
        """Build a frequency table for the given text."""
        return Counter(text)

    @staticmethod
    def build_huffman_tree(freq_table):
        """Build the Huffman Tree based on the frequency table."""
        heap = [HuffmanNode(char, freq) for char, freq in freq_table.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)

        return heap[0] if heap else None

    @staticmethod
    def generate_huffman_codes(node, prefix='', codebook=None):
        """Recursively generate Huffman codes for each character."""
        if codebook is None:
            codebook = {}
        if node is None:
            return codebook

        if node.char is not None:
            codebook[node.char] = prefix
        else:
            HuffmanEncoding.generate_huffman_codes(
                node.left, prefix + '0', codebook)
            HuffmanEncoding.generate_huffman_codes(
                node.right, prefix + '1', codebook)

        return codebook

    @staticmethod
    def encode(text, codebook):
        """Encode the input text using the Huffman codebook and return as characters."""
        # Convert text to bitstring
        bitstring = ''.join(codebook[char] for char in text)

        # Add padding to make bitstring a multiple of 8
        padding = (8 - len(bitstring) % 8) % 8
        bitstring += '0' * padding

        # Convert bitstring to characters
        char_encoded = ''.join(
            chr(int(bitstring[i:i+8], 2)) for i in range(0, len(bitstring), 8))

        return char_encoded, padding

    @staticmethod
    def decode(encoded_text, huffman_tree, padding):
        """Decode the encoded characters back to the original text."""
        # Convert characters back to bitstring
        bitstring = ''.join(f'{ord(char):08b}' for char in encoded_text)

        # Remove padding
        if padding > 0:
            bitstring = bitstring[:-padding]

        decoded_text = []
        node = huffman_tree

        for bit in bitstring:
            node = node.left if bit == '0' else node.right
            if node.char is not None:
                decoded_text.append(node.char)
                node = huffman_tree

        return ''.join(decoded_text)

    @staticmethod
    def build_huffman(text):
        """Build the Huffman tree, generate codes, and encode the text."""
        freq_table = HuffmanEncoding.build_frequency_table(text)
        huffman_tree = HuffmanEncoding.build_huffman_tree(freq_table)
        codebook = HuffmanEncoding.generate_huffman_codes(huffman_tree)
        encoded_text, padding = HuffmanEncoding.encode(text, codebook)
        return encoded_text, codebook, huffman_tree, padding

    @staticmethod
    def get_compression_ratio(input_string, encoded_text):
        """Calculate the compression ratio."""
        original_bits = len(input_string) * 8
        compressed_bits = len(encoded_text) * 8
        return ((original_bits - compressed_bits) / original_bits) * 100 if original_bits else 0
