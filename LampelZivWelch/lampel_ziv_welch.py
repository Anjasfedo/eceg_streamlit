class LampelZivWelch:
    def __init__(self):
        # Initialize the dictionary size and next code index
        self.dictionary_size = 256

    def compress(self, input_string):
        if input_string == "":
            return ""
        """Compress the input string using the LZW algorithm."""
        # Initialize the dictionary for compression
        dictionary = {chr(i): i for i in range(
            self.dictionary_size)}  # ASCII characters
        next_code = self.dictionary_size  # Start assigning new codes from 256

        current_string = ""
        compressed_data = []

        # Iterate over each character in the input string
        for char in input_string:
            current_string_plus_char = current_string + char
            if current_string_plus_char in dictionary:
                current_string = current_string_plus_char  # Continue the string
            else:
                # Output the code for current_string
                compressed_data.append(dictionary[current_string])
                # Add new string to dictionary
                dictionary[current_string_plus_char] = next_code
                next_code += 1
                # Start a new current_string
                current_string = char

        # Output the code for the last current_string
        if current_string:
            compressed_data.append(dictionary[current_string])

        # Convert the compressed data to a string (encoded as characters)
        return "".join([chr(num) for num in compressed_data])

    def decompress(self, compressed_data):
        if compressed_data == "":
            return ""
        """Decompress the LZW compressed data."""
        # Convert the compressed data (string of characters) to a list of integers (ASCII codes)
        compressed_data = [ord(char) for char in compressed_data]

        # Initialize the dictionary for decompression
        dictionary = {i: chr(i) for i in range(
            self.dictionary_size)}  # ASCII characters
        next_code = self.dictionary_size  # Start assigning new codes from 256

        current_code = compressed_data[0]
        decompressed_string = dictionary[current_code]
        current_string = decompressed_string

        # Iterate over the compressed data
        for code in compressed_data[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = current_string + current_string[0]
            decompressed_string += entry

            # Add the new string to the dictionary
            dictionary[next_code] = current_string + entry[0]
            next_code += 1

            # Update the current string
            current_string = entry

        return decompressed_string

    def get_compression_ratio(self, input_string, compressed_data):
        """Calculate the compression ratio using the formula:
           ((original_bits - compressed_bits) / original_bits) * 100
        """
        # Get the length of the input message in bits (original data)
        original_bits = self.message_length_in_bits(input_string)

        # Get the length of the compressed data in bits
        compressed_bits = self.message_length_in_bits(compressed_data)

        # Calculate the compression ratio using the revised formula
        if original_bits > 0:
            ratio = ((original_bits - compressed_bits) / original_bits) * 100
        else:
            ratio = 0

        return ratio

    def message_in_bits(self, message):
        return ''.join(format(ord(c), '08b') for c in message)

    def message_length_in_bits(self, message):
        """Convert message to bits and return its length."""
        # Convert each character in the string to its binary representation (8 bits)
        bits = ''.join(format(ord(c), '08b') for c in message)
        return len(bits)
