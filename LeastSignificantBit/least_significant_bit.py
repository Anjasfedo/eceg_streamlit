from PIL import Image
import numpy as np


class LeastSignificantBit:
    def __init__(self, k_val=1):
        """
        Initialize the LeastSignificantBit class.

        Args:
            k_val (int): The number of least significant bits to use for embedding.
        """
        if not (1 <= k_val <= 8):
            raise ValueError("k_val must be between 1 and 8.")
        self.k_val = k_val

    @staticmethod
    def message_to_bits(message):
        """
        Convert a string message to a bit string.
        """
        return ''.join(f"{ord(char):08b}" for char in message)

    @staticmethod
    def bits_to_message(bits):
        """
        Convert a bit string back to a human-readable message.
        """
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i + 8]
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            if char == '\0':
                break
            chars.append(char)
        return ''.join(chars)

    @staticmethod
    def split_bits_to_chunks(bits, chunk_size=2):
        """
        Split a binary string into chunks of a specified size.
        """
        return [bits[i:i + chunk_size] for i in range(0, len(bits), chunk_size)]

    @staticmethod
    def change_n_lsb(binary_number, new_lsbs, k_val):
        """
        Modify the n least significant bits (LSBs) of a binary number.
        """
        binary_literal = int(new_lsbs, 2)
        mask = ~((1 << k_val) - 1) & 0xFF
        return (binary_number & mask) | binary_literal

    def embed_message(self, input_image_path, output_image_path, message):
        """
        Modify pixel values of an image to embed a message.
        """
        message += '\0'
        message_bits = self.message_to_bits(message)

        image = Image.open(input_image_path)
        img_data = np.array(image)

        height, width, channels = img_data.shape
        capacity = height * width * channels * self.k_val
        if len(message_bits) > capacity:
            raise ValueError(
                f"Message too long! Capacity: {capacity} bits, Message: {len(message_bits)} bits.")

        bit_idx = 0
        for h in range(height):
            for w in range(width):
                for c in range(channels):
                    if bit_idx < len(message_bits):
                        original_value = img_data[h, w, c]
                        bits_to_embed = message_bits[bit_idx:bit_idx + self.k_val]
                        img_data[h, w, c] = self.change_n_lsb(
                            original_value, bits_to_embed, self.k_val)
                        bit_idx += self.k_val
                if bit_idx >= len(message_bits):
                    break
            if bit_idx >= len(message_bits):
                break

        stego_image = Image.fromarray(img_data)
        stego_image.save(output_image_path)
        return stego_image

    def extract_message(self, stego_image_path):
        """
        Extract a hidden message from an image that uses LSB encoding.
        """
        image = Image.open(stego_image_path)
        img_data = np.array(image)

        height, width, channels = img_data.shape
        extracted_bits = ""
        for h in range(height):
            for w in range(width):
                for c in range(channels):
                    pixel_value = img_data[h, w, c]
                    lsb_bits = format(pixel_value, '08b')[-self.k_val:]
                    extracted_bits += lsb_bits

        return self.bits_to_message(extracted_bits)
