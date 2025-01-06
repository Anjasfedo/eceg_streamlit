from faker import Faker
import random


class DummyKTPGenerator:
    def __init__(self):
        self.faker = Faker('id_ID')  # Use Indonesian locale
        self.indonesian_jobs = [
            "Guru", "Dokter", "Petani", "Nelayan", "Pegawai Negeri", "Karyawan Swasta",
            "Wiraswasta", "Mahasiswa", "Pelajar", "Pengacara", "Arsitek", "Insinyur",
            "Pedagang", "Polisi", "Tentara", "Seniman", "Penulis", "Pilot", "Supir",
            "Teknisi", "Pemadam Kebakaran", "Apoteker"
        ]

    def generate_ktp(self):
        """Generate a single dummy KTP record."""
        nik = self.generate_nik()
        name = self.faker.name()
        birth_place = self.faker.city()
        birth_date = self.faker.date_of_birth().strftime('%d-%m-%Y')
        gender = random.choice(['Laki-Laki', 'Perempuan'])
        blood_type = random.choice(['A', 'B', 'AB', 'O'])
        address = self.faker.address().replace('\n', ', ')
        rt_rw = f"{random.randint(1, 20)}/{random.randint(1, 20)}"
        kelurahan = self.faker.city_suffix()
        religion = random.choice(
            ['Islam', 'Kristen', 'Katolik', 'Hindu', 'Buddha', 'Konghucu'])
        marital_status = random.choice(
            ['Belum Kawin', 'Kawin', 'Cerai Hidup', 'Cerai Mati'])
        # Select random Indonesian job
        occupation = random.choice(self.indonesian_jobs)
        nationality = 'WNI'  # Assuming all generated data is Indonesian
        valid_until = 'SEUMUR HIDUP'

        return {
            'NIK': nik,
            'Nama': name,
            'Tempat/Tgl Lahir': f"{birth_place}, {birth_date}",
            'Jenis Kelamin': gender,
            'Gol Darah': blood_type,
            'Alamat': address,
            'RT/RW': rt_rw,
            'Kel/Desa': kelurahan,
            'Agama': religion,
            'Status Perkawinan': marital_status,
            'Pekerjaan': occupation,
            'Kewarganegaraan': nationality,
            'Berlaku Hingga': valid_until,
        }

    def generate_nik(self):
        """Generate a dummy NIK (Indonesian identity number)."""
        province_code = random.randint(10, 34)  # Random province code
        regency_code = random.randint(1, 99)   # Random regency code
        district_code = random.randint(1, 99)  # Random district code
        date_of_birth = self.faker.date_of_birth()
        birth_date_part = date_of_birth.strftime('%d%m%y')  # Format DDMMYY
        random_sequence = random.randint(
            1000, 9999)       # Random sequence number
        return f"{province_code:02}{regency_code:02}{district_code:02}{birth_date_part}{random_sequence:04}"

    def generate_multiple_ktps(self, count=1):
        """Generate multiple dummy KTP records."""
        return [self.generate_ktp() for _ in range(count)]

    @staticmethod
    def merge_ktp_data(ktp):
        """
        Merge a single KTP dictionary into a formatted string with '#' as a separator.
        Replace spaces with '%'.
        """
        fields = [
            ktp.get('NIK', ''),
            ktp.get('Nama', ''),
            ktp.get('Tempat/Tgl Lahir', ''),
            ktp.get('Jenis Kelamin', ''),
            ktp.get('Gol Darah', ''),
            ktp.get('Alamat', ''),
            ktp.get('RT/RW', ''),
            ktp.get('Kel/Desa', ''),
            ktp.get('Agama', ''),
            ktp.get('Status Perkawinan', ''),
            ktp.get('Pekerjaan', ''),
            ktp.get('Kewarganegaraan', ''),
            ktp.get('Berlaku Hingga', '')
        ]
        merged = '#'.join(fields)
        return merged.replace(' ', '%').lower()

    @staticmethod
    def merge_multiple_ktps(ktps):
        """
        Merge multiple KTP dictionaries into formatted strings with '#' as a separator.
        Replace spaces with '%'.
        """
        return [DummyKTPGenerator.merge_ktp_data(ktp) for ktp in ktps]
