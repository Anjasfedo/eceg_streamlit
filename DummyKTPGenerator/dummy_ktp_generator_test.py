import unittest
from unittest.mock import patch
from DummyKTPGenerator import DummyKTPGenerator  # Import your package


class TestDummyKTPGenerator(unittest.TestCase):
    def setUp(self):
        """Initialize the DummyKTPGenerator instance."""
        self.generator = DummyKTPGenerator()

    def test_generate_nik(self):
        """Test if the generated NIK is valid."""
        nik = self.generator.generate_nik()
        self.assertEqual(
            len(nik), 16, f"Generated NIK length is incorrect: {len(nik)}")
        self.assertTrue(
            nik.isdigit(), f"Generated NIK contains non-numeric characters: {nik}")
        print(f"Generated NIK is valid: {nik}")

    def test_generate_ktp_structure(self):
        """Test if the generated KTP record has all required fields."""
        ktp = self.generator.generate_ktp()
        expected_keys = [
            'NIK', 'Nama', 'Tempat/Tgl Lahir', 'Jenis Kelamin', 'Gol Darah',
            'Alamat', 'RT/RW', 'Kel/Desa', 'Agama', 'Status Perkawinan',
            'Pekerjaan', 'Kewarganegaraan', 'Berlaku Hingga'
        ]
        for key in expected_keys:
            self.assertIn(
                key, ktp, f"Field '{key}' is missing from the KTP record.")
            self.assertIsInstance(
                ktp[key], str, f"Field '{key}' is not a string: {ktp[key]}")
        print(f"Generated KTP structure is valid: {ktp}")

    def test_generate_multiple_ktps(self):
        """Test if multiple KTP records are generated correctly."""
        count = 5
        ktps = self.generator.generate_multiple_ktps(count)
        self.assertEqual(len(ktps), count,
                         f"Generated KTP count is incorrect: {len(ktps)}")
        for ktp in ktps:
            self.assertIsInstance(
                ktp, dict, f"Generated KTP is not a dictionary: {ktp}")
        print(f"Generated {count} KTP records successfully.")

    def test_merge_ktp_data(self):
        """Test if a single KTP record is merged into the correct format."""
        ktp = self.generator.generate_ktp()
        merged_data = self.generator.merge_ktp_data(ktp)
        self.assertIsInstance(
            merged_data, str, f"Merged KTP data is not a string: {merged_data}")
        self.assertIn('#', merged_data,
                      f"Merged KTP data does not contain '#': {merged_data}")
        self.assertNotIn(' ', merged_data,
                         f"Merged KTP data contains spaces: {merged_data}")
        self.assertIn(
            '%', merged_data, f"Merged KTP data does not replace spaces with '%': {merged_data}")
        print(f"Merged KTP data is valid: {merged_data}")

    def test_merge_multiple_ktps(self):
        """Test if multiple KTP records are merged correctly."""
        ktps = self.generator.generate_multiple_ktps(3)
        merged_data_list = self.generator.merge_multiple_ktps(ktps)
        self.assertEqual(len(merged_data_list), 3,
                         f"Merged data list count is incorrect: {len(merged_data_list)}")
        for merged_data in merged_data_list:
            self.assertIsInstance(
                merged_data, str, f"Merged data is not a string: {merged_data}")
            self.assertIn('#', merged_data,
                          f"Merged data does not contain '#': {merged_data}")
            self.assertNotIn(' ', merged_data,
                             f"Merged data contains spaces: {merged_data}")
            self.assertIn(
                '%', merged_data, f"Merged data does not replace spaces with '%': {merged_data}")
        print(f"Merged multiple KTP records successfully.")

    @patch('random.choice')
    def test_generate_ktp_with_mocked_gender(self, mock_random_choice):
        """Test KTP generation with mocked gender."""
        mock_random_choice.side_effect = lambda x: x[0]  # Always pick the first option
        ktp = self.generator.generate_ktp()
        self.assertEqual(ktp['Jenis Kelamin'], 'Laki-Laki',
                         f"Mocked gender is incorrect: {ktp['Jenis Kelamin']}")
        print(
            f"Generated KTP with mocked gender successfully: {ktp['Jenis Kelamin']}")


# Run the tests
unittest.main(argv=[''], verbosity=2, exit=False)
