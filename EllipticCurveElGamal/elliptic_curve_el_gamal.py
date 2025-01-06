import random

class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def is_infinity(self):
        """Check if the point is the point at infinity."""
        return self.x is None and self.y is None

    def __eq__(self, other):
        """Custom equality check for Point objects."""
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        """Make Point hashable by defining a unique hash."""
        return hash((self.x, self.y))

    def __repr__(self):
        if self.is_infinity():
            return "Point at Infinity"
        return f"Point({self.x}, {self.y})"

class EllipticCurveElGamal:
  def __init__(self):
    self.a = 6
    self.b = 7
    self.p = 61
    self.base_point = self.generate_random_valid_point()

    self.characters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z', '0', '1', '2', '3', '4', '5',
        '6', '7', '8', '9', ',', '.', '/', '?',
        ':', ';', '[', ']', '{', '}', '\\', '|',
        ' ', '!', '@', '#', '$', '%', '^', '&',
        '*', '(', ')', '-', '_', '=', '+', '~'
    ]

    self.valid_points = self.get_all_points()
    self.point_to_char, self.char_to_point = self.create_mappings()

  def elliptic_curve_equation(self, x):
    return (x**3 + self.a*x + self.b) % self.p

  # def is_on_curve(self, x, y):
  #   return self.elliptic_curve_equation(x)  == (y**2) % self.p

  # def generate_random_point(self):
  #   while True:
  #     x = random.randint(1, self.p - 1)
  #     y = random.randint(1, self.p - 1)
  #     if self.is_on_curve(x, y):
  #       return Point(x, y)

  def is_on_curve(self, x, y):
        """Check if a point (x, y) lies on the curve."""
        if x is None or y is None:
            return True
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0

  def generate_random_valid_point(self):
        """Generate a random point that lies on the elliptic curve."""
        while True:
            x = random.randint(0, self.p - 1)  # Random x-coordinate
            y_squared = (x**3 + self.a * x + self.b) % self.p  # Compute y^2

            # Check if y_squared is a quadratic residue modulo p
            if pow(y_squared, (self.p - 1) // 2, self.p) == 1:
                # Find a valid y-coordinate
                for y in range(self.p):
                    if (y**2) % self.p == y_squared:
                        return Point(x, y)

  # def calc_point_add(self, P, Q):
  #   R = Point()  # Initialize the result point R
  #   print(P, Q)

  #   slope = ((Q.y - P.y) / (Q.x - P.x))

  #   # Calculate Rx
  #   R.x = (slope**2 - P.x - Q.x)

  #   # Calculate Ry
  #   R.y = (slope * (P.x - R.x) - P.y)

  #   return R

  def calc_point_add(self, P, Q):
    """Calculate the addition of two points P and Q on the elliptic curve."""
    R = Point()  # Initialize the result point R

    if P.is_infinity():
        return Q
    if Q.is_infinity():
        return P

    # Handle the case where P and Q are inverses
    if P.x == Q.x and (P.y != Q.y or P.y == 0):
        return Point()  # Point at infinity

    # Calculate slope
    if P.x == Q.x and P.y == Q.y:
        # Point doubling
        slope = (3 * P.x**2 + self.a) * pow(2 * P.y, -1, self.p) % self.p
    else:
        # Regular point addition
        slope = (Q.y - P.y) * pow(Q.x - P.x, -1, self.p) % self.p

    # Calculate Rx
    R.x = (slope**2 - P.x - Q.x) % self.p

    # Calculate Ry
    R.y = (slope * (P.x - R.x) - P.y) % self.p

    return R

  def calc_point_doubling(self, P):
      """Calculate the point doubling 2P = P + P on the elliptic curve."""
      R = Point()  # Initialize the result point R

      if P.is_infinity() or P.y == 0:
          # Point at infinity for vertical tangent or zero y-coordinate
          return Point()

      # Calculate slope for point doubling
      slope = (3 * P.x**2 + self.a) * pow(2 * P.y, -1, self.p) % self.p

      # Calculate Rx
      R.x = (slope**2 - 2 * P.x) % self.p

      # Calculate Ry
      R.y = (slope * (P.x - R.x) - P.y) % self.p

      return R

  # def calc_point_subtraction(self, P, Q):
  #     """Calculate the subtraction of two points P - Q on the elliptic curve."""
  #     # Negate Q to get -Q
  #     Q_neg = Point(Q.x, (-Q.y) % self.p)

  #     # Add P and -Q
  #     return self.calc_point_add(P, Q_neg)

  def calc_point_subtraction(self, P, Q):
    """Calculate the subtraction of two points P - Q on the elliptic curve."""
    # Check if Q is the point at infinity
    if Q.is_infinity():
        return P  # P - Q = P when Q is the point at infinity

    # Check if P is the point at infinity
    if P.is_infinity():
        Q_neg = Point(Q.x, (-Q.y) % self.p)  # Negate Q
        return Q_neg  # 0 - Q = -Q

    # Negate Q to get -Q
    Q_neg = Point(Q.x, (-Q.y) % self.p)

    # Add P and -Q
    return self.calc_point_add(P, Q_neg)


  def calc_point_multiplication(self, P, k):
    """Calculate kP using the double-and-add method."""
    R = Point()  # Start with the point at infinity
    current_point = P

    while k > 0:
        if k % 2 == 1:
            # If the current bit is 1, add the current point
            R = self.calc_point_add(R, current_point)
        # Double the point
        current_point = self.calc_point_add(current_point, current_point)
        k //= 2  # Move to the next bit

    return R

  def generate_keys(self):
        """Generate a private and public key pair."""
        # Private key d: Random scalar
        private_key = random.randint(1, self.p - 1)

        # Public key e2 = d * e1 (base point)
        public_key = self.calc_point_multiplication(self.base_point, private_key)

        return private_key, public_key

  def encrypt(self, plaintext_point, public_key, k=None):
      """
      Encrypt a point on the elliptic curve using the public key.

      Args:
          plaintext_point (Point): The plaintext point to encrypt.
          public_key (Point): The public key.
          k (int, optional): The ephemeral key for deterministic testing. If None, a random k is used.

      Returns:
          tuple: A tuple containing the cipher points (C1, C2).
      """
      # Generate a random ephemeral key k if not provided
      if k is None:
          k = random.randint(1, self.p - 1)

      # Calculate C1 = k * e1 (base point)
      C1 = self.calc_point_multiplication(self.base_point, k)

      # Calculate k * e2 (public key)
      k_e2 = self.calc_point_multiplication(public_key, k)

      # Calculate C2 = P + k * e2
      C2 = self.calc_point_add(plaintext_point, k_e2)

      return C1, C2


  def decrypt(self, C1, C2, private_key):
        """
        Decrypt a ciphertext pair (C1, C2) using the private key.

        Args:
            C1 (Point): The first ciphertext point.
            C2 (Point): The second ciphertext point.
            private_key (int): The private key (d).

        Returns:
            Point: The plaintext point (P).
        """
        # Calculate d * C1
        d_C1 = self.calc_point_multiplication(C1, private_key)

        # Subtract d * C1 from C2 to get the plaintext point
        plaintext_point = self.calc_point_subtraction(C2, d_C1)

        return plaintext_point

  # def get_all_points(self):
  #       """
  #       Generate all valid points on the elliptic curve.

  #       Returns:
  #           list: A list of all valid points on the elliptic curve, including the point at infinity.
  #       """
  #       points = [Point()]  # Start with the point at infinity
  #       for x in range(self.p):
  #           y_squared = (x**3 + self.a * x + self.b) % self.p
  #           for y in range(self.p):
  #               if (y**2) % self.p == y_squared:
  #                   points.append(Point(x, y))
  #       return points

  def get_all_points(self):
      """
      Generate all valid points on the elliptic curve.

      Returns:
          list: A list of all valid points on the elliptic curve, including the point at infinity.
      """
      points = [Point()]  # Start with the point at infinity
      for x in range(self.p):
          y_squared = self.elliptic_curve_equation(x)
          for y in range(self.p):
              if (y**2) % self.p == y_squared:
                  points.append(Point(x, y))
      return points



  # def koblitz_encode(self, m, k=20):
  #     """
  #     Encode a number m as a point on the elliptic curve using Koblitz encoding.

  #     Args:
  #         m (int): The number to encode.
  #         k (int): The multiplier for encoding.

  #     Returns:
  #         Point: The encoded point on the elliptic curve.
  #     """
  #     if m <= 0:
  #         raise ValueError(f"Number m must be positive. Received: {m}")

  #     # Iterate to find a valid x value
  #     for i in range(1, k + 1):
  #         x = (k * m + i) % self.p  # Ensure x is within the field range
  #         y_squared = self.elliptic_curve_equation(x)
  #         if pow(y_squared, (self.p - 1) // 2, self.p) == 1:  # Check if y^2 is a quadratic residue
  #             # Find the corresponding y value
  #             for y in range(self.p):
  #                 if (y**2) % self.p == y_squared:
  #                     return Point(x, y)

  #     raise ValueError(f"Failed to encode number {m} as a valid point.")


  # def koblitz_decode(self, point, k=20):
  #     """
  #     Decode a point on the elliptic curve back to a number m.

  #     Args:
  #         point (Point): The point to decode.
  #         k (int): The multiplier used in encoding.

  #     Returns:
  #         int: The decoded number m.
  #     """
  #     if point.is_infinity():
  #         raise ValueError("Cannot decode the point at infinity.")

  #     x = point.x

  #     # Iterate to find the correct m value
  #     for m in range(1, self.p):
  #         if (k * m + 1) % self.p == x or (k * m + 2) % self.p == x:
  #             return m

  #     raise ValueError(f"Point {point} does not decode to a valid number.")

  # def is_quadratic_residue(self, a, mod):
  #   return pow(a, (mod - 1) // 2, mod) == 1

  # def koblitz_encode(self, m, k=100, used_points=None):
  #     """
  #     Encode a number m as a valid point on the elliptic curve, ensuring no duplicates.

  #     Args:
  #         m (int): The number to encode.
  #         k (int): The multiplier for encoding.
  #         used_points (set): A set of already-used points to avoid duplicates.

  #     Returns:
  #         Point: The encoded point on the elliptic curve.
  #     """
  #     if used_points is None:
  #         used_points = set()

  #     if m < 1 or m >= self.p:
  #         raise ValueError(f"Number m must be in the range [1, {self.p - 1}]. Received: {m}")

  #     for n in range(1, self.p):  # Iterate through offsets
  #         x = (k * m + n) % self.p
  #         y_squared = self.elliptic_curve_equation(x)

  #         # Explicitly check for y^2 = 0 (y = 0)
  #         if y_squared == 0:
  #             point = Point(x, 0)
  #             if point not in used_points:
  #                 used_points.add(point)
  #                 return point

  #         # Otherwise, proceed with quadratic residue check
  #         if self.is_quadratic_residue(y_squared, self.p):
  #             for y in range(self.p):
  #                 if (y**2) % self.p == y_squared:
  #                     point = Point(x, y)
  #                     if point not in used_points:
  #                         used_points.add(point)
  #                         return point

  #     raise ValueError(f"Failed to encode number {m} as a valid point after {self.p} attempts.")

  def create_mappings(self):
    valid_points = [point for point in self.valid_points]
    # print(f"Valid Points: {len(valid_points)}, Characters: {len(self.characters)}")
    if len(valid_points) != len(self.characters):
        raise ValueError("Mismatch between the number of valid points and characters.")
    point_to_char = {point: char for point, char in zip(valid_points, self.characters)}
    char_to_point = {char: point for point, char in point_to_char.items()}
    return point_to_char, char_to_point


  def encode_character(self, char):
        """Encode a character to a point on the elliptic curve."""
        if char not in self.char_to_point:
            raise ValueError(f"Character '{char}' not in mapping.")
        return self.char_to_point[char]

  def decode_point(self, point):
        """Decode a point on the elliptic curve to a character."""
        if point not in self.point_to_char:
            raise ValueError(f"Point '{point}' not in mapping.")
        return self.point_to_char[point]

  # def koblitz_decode(self, point, k=20):
  #   n = 1
  #   while True:
  #     m = (point.x - n) // k
  #     if m * k + n == point.x:
  #       # print(point.x)
  #       # print(point.x - n + 1)
  #       return m
  #     n += 1

  # def encrypt_message(self, message, public_key):
  #     """
  #     Encrypt a message using the elliptic curve encryption scheme.

  #     Args:
  #         message (str): The message to encrypt.
  #         public_key (Point): The public key to use for encryption.

  #     Returns:
  #         list: A list of encrypted tuples (C1, C2) representing the ciphertext.
  #     """
  #     ciphertext = []

  #     for char in message:
  #         # Encode character to a point
  #         plaintext_point = self.encode_character(char)

  #         # Encrypt the point
  #         C1, C2 = self.encrypt(plaintext_point, public_key)

  #         # Append the encrypted tuple to the ciphertext
  #         ciphertext.append((C1, C2))

  #         print(f"Character '{char}' encoded to {plaintext_point}, encrypted as (C1: {C1}, C2: {C2})")

  #     return ciphertext

  def encrypt_message(self, message, public_key):
      """
      Encrypt a message using the elliptic curve encryption scheme and return a character-based ciphertext.

      Args:
          message (str): The message to encrypt.
          public_key (Point): The public key to use for encryption.

      Returns:
          str: The encrypted message as a string of characters.
      """
      ciphertext = ""

      for char in message:
          # Encode character to a point
          plaintext_point = self.encode_character(char)

          # Encrypt the point
          C1, C2 = self.encrypt(plaintext_point, public_key)

          # Decode encrypted points back to characters
          encrypted_char_C1 = self.decode_point(C1)
          encrypted_char_C2 = self.decode_point(C2)

          # Append the encrypted characters to the ciphertext
          ciphertext += encrypted_char_C1 + encrypted_char_C2

          # print(f"Character '{char}' encoded to {plaintext_point}, encrypted as (C1: {C1}, C2: {C2}), "
          #       f"and represented as '{encrypted_char_C1}{encrypted_char_C2}'.")
      # print(ciphertext)
      return ciphertext

  def decrypt_message(self, ciphertext, private_key):
      """
      Decrypt a ciphertext into its plaintext message using the private key.

      Args:
          ciphertext (str): The encrypted message as a string of characters.
          private_key (int): The private key for decryption.

      Returns:
          str: The decrypted plaintext message.
      """
      plaintext = ""
      # Process ciphertext two characters at a time (C1 and C2)
      for i in range(0, len(ciphertext), 2):
          # Decode C1 and C2 back into points
          C1 = self.encode_character(ciphertext[i])
          C2 = self.encode_character(ciphertext[i + 1])

          # Decrypt the point
          decrypted_point = self.decrypt(C1, C2, private_key)

          # Decode the point back into the original character
          char = self.decode_point(decrypted_point)
          plaintext += char

          # print(f"Ciphertext pair '{ciphertext[i]}{ciphertext[i + 1]}' decrypted to point {decrypted_point}, "
          #       f"decoded to character '{char}'.")

      return plaintext
