
import unittest
import numpy as np
from PIL import Image
import os
from .least_significant_bit import LeastSignificantBit


class TestLeastSignificantBit(unittest.TestCase):
    def setUp(self, input_image_path='lena.png', output_image_path='output_image.png'):
        """Set up the LSBSteganography instance and mock data for testing."""
        self.stego = LeastSignificantBit(k_val=2)
        self.input_image_path = input_image_path
        self.output_image_path = output_image_path

        # Create a mock image (512x512 with 3 channels)
        self.image_data = np.full(
            (512, 512, 3), 255, dtype=np.uint8)  # White image
        Image.fromarray(self.image_data).save(self.input_image_path)

        # Generate a dummy message for testing
        self.generate_test_message()

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.input_image_path):
            os.remove(self.input_image_path)
        if os.path.exists(self.output_image_path):
            os.remove(self.output_image_path)

    def generate_test_message(self):
        """Generate a repeated test message to exactly match the required length."""
        base_message = "TestMessage123"
        required_length = (512 * 512 * 3) // 8  # 98304 characters
        self.message = (base_message * (required_length //
                        len(base_message) + 1))[:required_length]

    def test_message_to_bits(self):
        """Test if a message is correctly converted to a bit string."""
        bit_string = self.stego.message_to_bits(self.message)
        expected_bit_string = ''.join(
            f"{ord(char):08b}" for char in self.message)
        self.assertEqual(bit_string, expected_bit_string,
                         f"Bit string conversion failed. Expected: {expected_bit_string}, Got: {bit_string}")
        print("Message to bits test passed.")

    def test_bits_to_message(self):
        """Test if a bit string is correctly converted back to a message."""
        bit_string = ''.join(f"{ord(char):08b}" for char in self.message)
        reconstructed_message = self.stego.bits_to_message(bit_string)
        self.assertEqual(reconstructed_message, self.message,
                         f"Bit to message conversion failed. Expected: {self.message}, Got: {reconstructed_message}")
        print("Bits to message test passed.")

    def test_hiding_capacity(self):
        """Test if the hiding capacity is calculated correctly."""
        # Embed the test message
        self.stego.embed_message(
            self.input_image_path, self.output_image_path, (self.message * self.stego.k_val)[:-1])

        # Extract the message
        extracted_message = self.stego.extract_message(self.output_image_path)

        # Calculate hiding capacity
        # Total bits used for the message
        hiding_capacity = len(extracted_message) * 8
        max_capacity = 512 * 512 * 3 * self.stego.k_val  # w * h * c * k
        different_capacity = max_capacity - hiding_capacity

        # print(f"Extracted message length: {len(extracted_message)}")
        # Ensure the difference matches the delimiter size (8 bits for '\0')
        self.assertEqual(different_capacity, 8,
                         f"The difference in capacity is incorrect: {different_capacity}")
        print(
            f"Hiding capacity test passed. Max capacity: {max_capacity}, Hiding capacity: {hiding_capacity}")


# Run the tests
unittest.main(argv=[''], verbosity=2, exit=False)
