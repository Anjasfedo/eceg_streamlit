import heapq
from collections import Counter

# HuffmanNode class for tree structure


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char    # Character
        self.freq = freq    # Frequency of the character
        self.left = None    # Left child
        self.right = None   # Right child

    def __lt__(self, other):
        # This ensures that the priority queue is ordered by frequency (min-heap)
        return self.freq < other.freq

# HuffmanCoding class that encapsulates all methods for encoding and decoding


class HuffmanEncoding:
    def __init__(self, text=None):
        self.text = text
        self.freq_table = None
        self.huffman_tree = None
        self.codebook = None
        if text:
            self.build_huffman(text)

    # Step 2: Build the frequency table
    def build_frequency_table(self):
        """Build a frequency table for the given text."""
        self.freq_table = Counter(self.text)
        return self.freq_table

    # Step 3: Build the Huffman Tree
    def build_huffman_tree(self):
        """Build the Huffman Tree based on the frequency table."""
        # Create a priority queue (min-heap) with HuffmanNode objects
        heap = [HuffmanNode(char, freq)
                for char, freq in self.freq_table.items()]
        heapq.heapify(heap)

        # Build the Huffman tree
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            # Create a new internal node with these two nodes as children
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right

            # Push the merged node back to the heap
            heapq.heappush(heap, merged)

        # The heap will now contain only one node, which is the root of the Huffman tree
        self.huffman_tree = heap[0]
        return self.huffman_tree

    # Step 4: Generate Huffman Codes
    def generate_huffman_codes(self, node=None, prefix='', codebook=None):
        """Recursively generate Huffman codes for each character."""
        if codebook is None:
            codebook = {}
        if node is None:
            node = self.huffman_tree

        # If it's a leaf node, assign the prefix as the Huffman code for the character
        if node.char is not None:
            codebook[node.char] = prefix
        else:
            # Recursively assign the prefix to the left and right children
            if node.left:
                self.generate_huffman_codes(node.left, prefix + '0', codebook)
            if node.right:
                self.generate_huffman_codes(node.right, prefix + '1', codebook)

        self.codebook = codebook
        return self.codebook

    # Step 5: Encode the text
    def encode(self, text=None):
        """Encode the input text using the Huffman codebook."""
        if text is None:
            text = self.text
        encoded_text = ''.join(self.codebook[char] for char in text)

        # Ensure the encoded text is a multiple of 8 bits (add padding if necessary)
        padding = 8 - len(encoded_text) % 8
        encoded_text += '0' * padding  # Add padding with '0's
        return encoded_text, padding

    # Step 6: Decode the encoded text
    def decode(self, encoded_text, padding):
        """Decode the encoded text back to the original text."""
        # Remove the padding
        encoded_text = encoded_text[:-padding]

        decoded_text = []
        node = self.huffman_tree
        for bit in encoded_text:
            # Traverse the tree based on the bits (0 for left, 1 for right)
            if bit == '0':
                node = node.left
            else:
                node = node.right

            # If we reach a leaf node, append the character and reset the node to the root
            if node.char is not None:
                decoded_text.append(node.char)
                node = self.huffman_tree

        return ''.join(decoded_text)

    # Main method to perform Huffman Encoding
    def build_huffman(self, text):
        """Build the Huffman tree, generate codes, and encode the text."""
        self.text = text
        self.build_frequency_table()
        self.build_huffman_tree()
        self.generate_huffman_codes()

        encoded_text, padding = self.encode(text)
        return encoded_text, self.codebook, self.huffman_tree, padding

    # Method to perform Huffman Decoding
    def huffman_decoding(self, encoded_text, padding):
        """Decode the encoded text back to the original string."""
        return self.decode(encoded_text, padding)

    def get_compression_ratio(self, input_string, encoded_text):
        """Calculate the compression ratio using the formula:
           ((original_bits - compressed_bits) / original_bits) * 100
        """
        # Get the length of the input message in bits (original data)
        original_bits = self.message_length_in_bits(input_string)

        # Get the length of the compressed data in bits
        compressed_bits = len(encoded_text)

        # Calculate the compression ratio using the revised formula
        if original_bits > 0:
            ratio = ((original_bits - compressed_bits) / original_bits) * 100
        else:
            ratio = 0

        return ratio

    def encoded_text_length(self, encoded_text):
        return len(encoded_text)

    def message_length_in_bits(self, message):
        """Convert message to bits and return its length."""
        # Convert each character in the string to its binary representation (8 bits)
        bits = ''.join(format(ord(c), '08b') for c in message)
        return len(bits)

    def decode_to_chars(self, encoded_text, padding):
        """Convert encoded bits (string of '0' and '1') to actual characters."""
        # Step 1: Group the bits into chunks of 8 (1 byte)
        byte_chunks = [encoded_text[i:i+8]
                       for i in range(0, len(encoded_text), 8)]

        # Step 2: Convert each byte to an integer and then to a character
        decoded_chars = []
        for byte in byte_chunks:
            # If the byte is not of length 8, pad it (this happens if the last chunk is incomplete)
            byte = byte.ljust(8, '0')
            # Convert the binary string to an integer
            byte_as_int = int(byte, 2)
            # Convert integer to character using chr()
            decoded_chars.append(chr(byte_as_int))

        return ''.join(decoded_chars)

    def encode_text_to_bits(self, text):
        """Convert decoded text (characters) back to a bitstream."""
        bitstream = []

        for char in text:
            # Convert each character to its integer (ASCII/Unicode) value
            char_int = ord(char)

            # Convert the integer to binary and ensure it's 8 bits long (padded with leading zeros)
            bitstream.append(f'{char_int:08b}')

        return ''.join(bitstream)