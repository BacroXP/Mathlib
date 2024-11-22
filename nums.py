from num import num


import math

class pi(num):
    def __init__(self, dig: int):
        """
        Initialize the pi class with a specified number of digits.
        
        Args:
            dig (int): The number of digits of pi to represent.
        """
        # Initialize the parent class `num` with an initial value of 0 and a chunk size of 1000.
        super().__init__(0, 1000)
        
        # Set the negative attribute to False, as pi is positive.
        self.negative = False
        
        # Set the full_segments to represent the integer part of pi
        self.full_segments = ["3"]  # Pi's integer part is '3'
        
        # Initialize the split_segments to store the decimal digits of pi
        self.split_segments = ["0"] * ((dig // self.chunksize) + 1)
        
        # Calculate the required digits of pi
        self.calculate_digits(dig)


    def calculate_digits(self, n: int):
        """
        Calculate the digits of pi up to `n` digits.
        
        This method uses the math module to calculate pi to the specified number of digits.
        
        Args:
            n (int): The number of digits to calculate.
        """
        # Use Python's math library to get pi and then convert it to a string.
        pi_value = str(math.pi)
        
        # Only keep the part up to the specified number of digits.
        # Add 1 to account for the '3.' part of the pi number.
        pi_digits = pi_value[2:n+2]
        
        # Split the digits into chunks of `self.chunksize`
        num_chunks = (n // self.chunksize) + 1
        self.split_segments = [pi_digits[i * self.chunksize: (i + 1) * self.chunksize] for i in range(num_chunks)]


class e(num):
    def __init__(self, dig: int):
        """
        Initialize the e class with a specified number of digits.
        
        Args:
            dig (int): The number of digits of e to represent.
        """
        # Initialize the parent class `num` with an initial value of 0 and a chunk size of 1000.
        super().__init__(0, 1000)
        
        # Set the negative attribute to False, as e is positive.
        self.negative = False
        
        # Set the full_segments to represent the integer part of e
        self.full_segments = ["2"]  # e's integer part is '2'
        
        # Initialize the split_segments to store the decimal digits of e
        self.split_segments = ["0"] * ((dig // self.chunksize) + 1)
        
        # Calculate the required digits of e
        self.calculate_digits(dig)


    def calculate_digits(self, n: int):
        """
        Calculate the digits of e up to `n` digits.
        
        This method uses the math module to calculate e to the specified number of digits.
        
        Args:
            n (int): The number of digits to calculate.
        """
        # Use Python's math library to get e and then convert it to a string.
        e_value = str(math.e)
        
        # Only keep the part up to the specified number of digits.
        # Add 1 to account for the '2.' part of the e number.
        e_digits = e_value[2:n+2]
        
        # Split the digits into chunks of `self.chunksize`
        num_chunks = (n // self.chunksize) + 1
        self.split_segments = [e_digits[i * self.chunksize: (i + 1) * self.chunksize] for i in range(num_chunks)]


class i(num):
    def __init__(self, dig: int = 10):
        """
        Initialize the imaginary number i (square root of -1).
        
        Args:
            dig (int): The number of digits to represent for the imaginary number.
        """
        # Initialize the parent class `num` with a value of 1 for simplicity, and chunksize 10
        super().__init__(1, chunksize=10)
        
        # The number i should have no real part, so we store it in the imaginary part
        self.real_part = num(0)
        self.imaginary_part = num(1)  # 'i' is the imaginary unit
        
        # Set the negative flag based on the input (imaginary part remains positive)
        self.negative = False

    def __str__(self):
        """
        Return the string representation of the imaginary number.
        """
        return "i"

    def __repr__(self):
        """
        Return a more detailed string representation for debugging.
        """
        return f"i({''.join(self.split_segments)})"
    
    def __mul__(self, other):
        """
        Handle multiplication of the imaginary number by another number.
        This involves using the rules of complex number multiplication:
        i * i = -1.
        
        Args:
            other (num or i): The other number to multiply by.
        
        Returns:
            num: The result of the multiplication.
        """
        if isinstance(other, i):
            return num(-1)  # i * i = -1
        else:
            return super().__mul__(other)  # Call the parent multiplication method

    def __add__(self, other):
        """
        Add the imaginary unit to another number or imaginary number.
        """
        if isinstance(other, num):
            return super().__add__(other)
        return NotImplemented
    
    def __sub__(self, other):
        """
        Subtract the imaginary unit from another number or imaginary number.
        """
        if isinstance(other, num):
            return super().__sub__(other)
        return NotImplemented

