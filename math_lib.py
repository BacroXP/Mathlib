

class num():
    def __init__(self, num: int | str):
        """
        Initializes a `num` object by dividing a large number into manageable segments.
        
        Args:
            num (int | str): The number to be represented, can be a positive or negative integer or string.
        """
        self.segments = []  # List to store segments of the number as strings
        self.chunksize = 5  # Maximum number of digits in each segment
        
        self.digits = 0  # Total number of digits in the number
        self.negative = num < 0  # Track if the number is negative
        
        # Convert to string and calculate the absolute value to work with digits
        string = str(abs(num))
        self.digits = len(string)  # Count total digits
        
        # Handle leading segment (may have fewer digits than chunksize)
        self.segments.append(string[:len(string) % self.chunksize])
        
        # Split the number into chunks of `chunksize`
        for i in range(len(string) // self.chunksize):
            start_index = (len(string) % self.chunksize) + i * self.chunksize
            end_index = start_index + self.chunksize
            self.segments.append(string[start_index:end_index])
        
        # Remove empty leading segment if the number of digits is exactly divisible by chunksize
        if self.segments[0] == '':
            self.segments.pop(0)
        
        
    def add(self, sec_num: "num") -> "num":
        """
        Adds the current `num` object with another `num` object (`sec_num`).

        Args:
            sec_num (num): The second number to add.

        Returns:
            num: A new `num` instance representing the sum of the two numbers.
        """

        # Create the return variable (a new num instance to store the result)
        ret = num(0)
        ret.negative = self.negative  # Assume the result has the same sign as `self` initially

        # Carry-over variable to handle sums exceeding the chunk size
        over = 0
        ret.segments = []  # Initialize the result's segments list

        # Pad the shorter number with leading zeros to align segment lengths
        max_segments = max(len(self.segments), len(sec_num.segments))
        self.segments = ["0"] * (max_segments - len(self.segments)) + self.segments
        sec_num.segments = ["0"] * (max_segments - len(sec_num.segments)) + sec_num.segments

        # Loop over the segments in reverse (from least significant to most significant)
        for x, y in zip(reversed(self.segments), reversed(sec_num.segments)):
            # Calculate the sum of corresponding segments plus any carry-over
            sol = str(int(x) + int(y) + over)

            # If the result exceeds the chunk size, split it into a segment and carry-over
            if len(sol) > self.chunksize:
                ret.segments.insert(0, sol[-self.chunksize:])  # Keep the last `chunksize` digits
                over = int(sol[:-self.chunksize])  # Carry-over is the remaining leading digits
            else:
                # If no overflow, add the whole sum as a segment and reset carry-over
                ret.segments.insert(0, sol)
                over = 0

        # If there is any remaining carry-over after the loop, prepend it as a new segment
        if over > 0:
            ret.segments.insert(0, str(over))

        # Clean up leading zeros in the most significant segment
        ret.segments[0] = ret.segments[0].lstrip("0") or "0"

        # Return the resulting `num` object
        return ret


    def sub(self, sec_num: "num") -> "num":
        """
        Subtracts the `sec_num` from the current `num` object.

        Args:
            sec_num (num): The second number to subtract from the current number.

        Returns:
            num: A new `num` instance representing the result of the subtraction.
        """

        # Determine which number is larger for subtraction (taking sign into account)
        is_self_larger = self.segments > sec_num.segments if self.segments != sec_num.segments else not self.negative

        # Set the larger and smaller number
        larger, smaller = (self, sec_num) if is_self_larger else (sec_num, self)
        result_negative = self.negative if is_self_larger else not self.negative

        # Pad the smaller number's segments with zeros to match the larger number's length
        diff = len(larger.segments) - len(smaller.segments)
        smaller_segments = ["0"] * diff + smaller.segments

        # Prepare for the result calculation
        result_segments = []  # This will hold the segments of the result
        borrow = 0  # Variable to track borrow during subtraction
        base = 100000  # Base for each segment, based on the chunk size

        # Loop through each segment from least significant to most significant
        for x, y in zip(reversed(larger.segments), reversed(smaller_segments)):
            # Apply the borrow from the previous iteration
            x_val = int(x) - borrow
            y_val = int(y)

            # If the current segment of larger is smaller than the smaller segment, borrow
            if x_val < y_val:
                borrow = 1
                x_val += base  # Borrow means we need to add the base to the current segment value
            else:
                borrow = 0

            # Subtract the smaller segment from the larger segment and add to result
            result_segments.append(str(x_val - y_val))

        # Reverse the result segments to get them in correct order
        result_segments.reverse()

        # Remove leading zeros from the result
        while len(result_segments) > 1 and result_segments[0] == "0":
            result_segments.pop(0)

        # Create a new `num` object for the result
        ret = num(0)
        ret.segments = result_segments
        ret.negative = result_negative  # Set the sign of the result
        return ret


    def __add__(self, sec_num: "num | int | float") -> "num":
        """
        Adds the current `num` object with another `num` object, or an integer or float.

        Args:
            sec_num (num | int | float): The number to add.

        Returns:
            num: A new `num` instance representing the sum of the two numbers.
        """
        # If sec_num is not a num instance, convert it to a num instance
        if not isinstance(sec_num, num):
            sec_num = num(int(sec_num))  # Convert sec_num to a `num` instance

        # Case 1: Both numbers have the same sign (either both positive or both negative)
        if self.negative == sec_num.negative:
            return self.add(sec_num)  # Perform addition using the add method

        # Case 2: self is negative, and sec_num is positive
        elif self.negative:
            return sec_num.sub(self)  # Subtract self from sec_num (reverse subtraction)

        # Case 3: self is positive, and sec_num is negative
        else:
            return self.sub(sec_num)  # Subtract sec_num from self


    def __radd__(self, sec_num: "num | int | float") -> "num":
        """
        Handles reverse addition for `num` objects. This method is called when
        the `num` object is on the right side of an addition operation with
        a non-`num` object (e.g., `5 + num_instance`).

        Args:
            sec_num (num | int | float): The number to add.

        Returns:
            num: The result of the addition.
        """
        # Reverse addition is the same as regular addition
        return self + sec_num  # Simply call __add__ to handle the addition


    def __sub__(self, sec_num: "num | int | float") -> "num":
        """
        Subtracts another `num` object (or integer or float) from the current `num` object.

        Args:
            sec_num (num | int | float): The number to subtract.

        Returns:
            num: A new `num` instance representing the result of the subtraction.
        """
        # Subtract sec_num from self by adding the negative of sec_num
        return self + (-sec_num)  # Use the __add__ method by negating sec_num
    
    
    def __mul__(self, sec_num: "num | int | float") -> "num":
        """
        Multiplies the current `num` object with another `num` object, or an integer or float.

        Args:
            sec_num (num | int | float): The number to multiply.

        Returns:
            num: A new `num` instance representing the product of the two numbers.
        """
        # Convert sec_num to a num instance if it is not already a num
        if not isinstance(sec_num, num):
            sec_num = num(int(sec_num))  # Convert sec_num to a `num` instance

        # Base for each segment (chunk size)
        base = 10**size.chunksize

        # Prepare the result storage. The result will have at most len(self.segments) + len(sec_num.segments) segments
        result_segments = [0] * (len(self.segments) + len(sec_num.segments))

        # Multiply each segment of `self` with each segment of `sec_num`
        for i, x in enumerate(reversed(self.segments)):
            for j, y in enumerate(reversed(sec_num.segments)):
                product = int(x) * int(y) + result_segments[i + j]  # Multiply and add any existing value
                result_segments[i + j] = product % base  # Current segment value (modulo base)
                result_segments[i + j + 1] += product // base  # Carry to next segment (integer division)

        # Remove leading zeros from the result
        while len(result_segments) > 1 and result_segments[-1] == 0:
            result_segments.pop()

        # Reverse the result segments and convert them to strings
        result_segments = list(map(str, reversed(result_segments)))

        # Add leading zeros to each segment to ensure they match the chunk size (self.chunksize)
        for i, el in enumerate(result_segments):
            # Pad each segment to match the chunksize by adding leading zeros
            for _ in range(self.chunksize - len(el)):
                result_segments[i] = "0" + result_segments[i]

        # Remove leading zeros from the final result
        result_segments[0] = result_segments[0].lstrip("0") or "0"

        # Determine the sign of the result
        result_negative = self.negative != sec_num.negative  # Result is negative if signs differ

        # Create a new `num` instance for the result
        ret = num(0)
        ret.segments = result_segments
        ret.negative = result_negative  # Set the correct sign for the result
        return ret
    

    def __truediv__(self, sec_num: "num | int | float") -> "num":
        # Coming soon
        return 0


    def __round__(self, ndigits: int = 0) -> str:
        """
        Round the number to the nearest integer or specified number of digits.

        Parameters:
        - ndigits: Number of digits to round to (default is 0, rounding to the nearest integer).
        
        Returns:
        - A string representation of the rounded number, possibly in scientific notation.
        """
        rep = ""

        # Handle negative numbers
        if self.negative:
            rep = "-"

        # The first segment is the integer part
        rep += self.segments[0]

        # If there's more than one segment, we need to check rounding
        if len(self.segments) > 1:
            # Check the first digit of the second segment to decide rounding
            if int(self.segments[1][0]) >= 5:
                # Round up the first segment if the first digit of the next segment is >= 5
                rep = str(int(rep) + 1)

        # If we have multiple segments, add scientific notation
        if len(self.segments) > 1:
            rep += "e"

            # Calculate the exponent as the number of digits in the other segments
            exponent = (len(self.segments) - 1) * self.chunksize
            rep += str(exponent)

        return rep


    def __ceil__(self) -> str:
        """
        Return the smallest integer greater than or equal to the number.

        Always rounds up the first segment of the number.

        Returns:
        - A string representation of the number rounded up, possibly in scientific notation.
        """
        rep = ""

        # Handle negative numbers
        if self.negative:
            rep = "-"

        # The first segment is the integer part
        rep += self.segments[0]

        # Always round up if there's more than one segment
        if len(self.segments) > 1:
            # Increment the integer part to round up
            rep = str(int(rep) + 1)

        # If we have multiple segments, add scientific notation
        if len(self.segments) > 1:
            rep += "e"

            # Calculate the exponent as the number of digits in the other segments
            exponent = (len(self.segments) - 1) * self.chunksize
            rep += str(exponent)

        return rep


    def __floor__(self) -> str:
        """
        Return the largest integer less than or equal to the number.

        In this case, it simply returns the integer part as is, without rounding up.

        Returns:
        - A string representation of the number rounded down (or truncated), possibly in scientific notation.
        """
        rep = ""

        # Handle negative numbers
        if self.negative:
            rep = "-"

        # The first segment is the integer part
        rep += self.segments[0]

        # If we have multiple segments, add scientific notation
        if len(self.segments) > 1:
            rep += "e"

            # Calculate the exponent as the number of digits in the other segments
            exponent = (len(self.segments) - 1) * self.chunksize
            rep += str(exponent)

        return rep
    
    
    def __and__(self, sec_num: "num | int | float") -> bool:
        """
        Perform a logical AND operation between two `num` objects.

        The result is True if both numbers are non-zero (truthy); False otherwise.

        Parameters:
        - sec_num: The second number to compare with.

        Returns:
        - True if both numbers are non-zero, False otherwise.
        """
        return bool(self) and bool(sec_num)


    def __or__(self, sec_num: "num | int | float") -> bool:
        """
        Perform a logical OR operation between two `num` objects.

        The result is True if at least one number is non-zero (truthy); False if both are zero.

        Parameters:
        - sec_num: The second number to compare with.

        Returns:
        - True if at least one number is non-zero, False if both are zero.
        """
        return bool(self) or bool(sec_num)


    def __bool__(self) -> bool:
        """
        Return the truth value of the `num` object.

        A `num` object is considered True if it is non-zero, False if it is zero.

        Returns:
        - True if the number is non-zero, False if the number is zero.
        """
        return self.__ne__(0)


    def __neg__(self) -> "num":
        """
        Return the negation of the `num` object (multiply by -1).

        This operation reverses the sign of the number.

        Returns:
        - A new `num` object that is the negation of the current number.
        """
        ret = num(0)  # Create a new num instance for the result
        ret.segments = self.segments  # Copy the segments of the original number
        ret.negative = not self.negative  # Flip the negative flag
        
        return ret


    def __pos__(self) -> "num":
        """
        Return the positive version of the `num` object.

        This method ensures that the number is positive, without changing the value if it already is.

        Returns:
        - A new `num` object that is the positive version of the current number.
        """
        ret = num(0)  # Create a new num instance for the result
        ret.segments = self.segments  # Copy the segments of the original number
        ret.negative = self.negative  # Maintain the same negative flag
        
        return ret


    def __abs__(self) -> "num":
        """
        Return the absolute value of the `num` object.

        The result will have the same segments, but the negative flag is set to False.

        Returns:
        - A new `num` object that represents the absolute value of the current number.
        """
        ret = num(0)  # Create a new num instance for the result
        ret.segments = self.segments  # Copy the segments of the original number
        ret.negative = False  # Set negative flag to False to represent the absolute value
        
        return ret
    
    
    def __eq__(self, sec_num: "num | int | float") -> bool:
        """
        Check if the current number is equal to another `num`, `int`, or `float`.

        Parameters:
        - sec_num: The second number to compare with. It can be a `num` object, `int`, or `float`.

        Returns:
        - True if the numbers are equal, otherwise False.
        """
        # If sec_num is another num object
        if isinstance(sec_num, num):
            return (self.segments == sec_num.segments) and (self.negative == sec_num.negative)
        
        # If sec_num is an int or float, convert it to a string and compare
        elif isinstance(sec_num, int) or isinstance(sec_num, float):
            # Check if the sign of sec_num matches with self.negative
            if not ((sec_num < 0) == self.negative):
                return False
            
            # Convert sec_num to string and compare it with self (as a string)
            sec_num_str = str(sec_num)
            return str(self) == sec_num_str
        
        # If sec_num is not a supported type
        else:
            return NotImplemented


    def __gt__(self, sec_num: "num") -> bool:
        """
        Check if the current number is greater than another `num`.

        Parameters:
        - sec_num: The second number to compare with, which must be a `num` object.

        Returns:
        - True if the current number is greater than `sec_num`, otherwise False.
        """
        # If sec_num is another num object
        if isinstance(sec_num, num):
            # Check if the numbers are equal
            if self.__eq__(sec_num):
                return False
            
            # If the signs differ, the positive number is greater
            if self.negative != sec_num.negative:
                return sec_num.negative
            
            # Compare the number of digits (length of the segments)
            if self.digits > sec_num.digits:
                return True
            elif sec_num.digits > self.digits:
                return False
            
            # Compare each segment from the most significant
            for seg1, seg2 in zip(self.segments, sec_num.segments):
                for char1, char2 in zip(seg1, seg2):
                    # Compare each character and return the result
                    if char1 != char2:
                        return char1 > char2

        # If sec_num is not a num object, convert it to a num and compare
        sec_num = int(sec_num)  # Convert sec_num to an integer for comparison
        return self.__gt__(num(sec_num))


    def __ne__(self, sec_num: "num") -> bool:
        """
        Check if the current number is not equal to another `num`.

        Parameters:
        - sec_num: The second number to compare with, which must be a `num` object.

        Returns:
        - True if the numbers are not equal, otherwise False.
        """
        return not self.__eq__(sec_num)


    def __lt__(self, sec_num: "num") -> bool:
        """
        Check if the current number is less than another `num`.

        Parameters:
        - sec_num: The second number to compare with, which must be a `num` object.

        Returns:
        - True if the current number is less than `sec_num`, otherwise False.
        """
        return not self.__eq__(sec_num) and not self.__gt__(sec_num)


    def __ge__(self, sec_num: "num") -> bool:
        """
        Check if the current number is greater than or equal to another `num`.

        Parameters:
        - sec_num: The second number to compare with, which must be a `num` object.

        Returns:
        - True if the current number is greater than or equal to `sec_num`, otherwise False.
        """
        return self.__eq__(sec_num) or self.__gt__(sec_num)


    def __le__(self, sec_num: "num") -> bool:
        """
        Check if the current number is less than or equal to another `num`.

        Parameters:
        - sec_num: The second number to compare with, which must be a `num` object.

        Returns:
        - True if the current number is less than or equal to `sec_num`, otherwise False.
        """
        return self.__eq__(sec_num) or self.__lt__(sec_num)
    
    
    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the number.

        If the number is negative, a minus sign is prefixed.
        The segments are concatenated to form the full number.

        Returns:
        - A string representation of the number.
        """
        rep = ""  # Initialize an empty string for the result.
        
        # If the number is negative, add a minus sign.
        if self.negative:
            rep = "-"
        
        # Append each segment to the result string.
        for i in range(len(self.segments)):
            rep += self.segments[i]
        
        return rep  # Return the complete string representation of the number.


    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the number, suitable for debugging.

        If the number is negative, a minus sign is prefixed.
        The first segment is followed by an exponent (E) if the number has more than one segment.

        Returns:
        - A string representation that includes an exponent notation if the number has multiple segments.
        """
        rep = ""  # Initialize an empty string for the result.
        
        # If the number is negative, add a minus sign.
        if self.negative:
            rep = "-"
        
        # Add the first segment of the number to the result.
        rep += self.segments[0]

        # If the number has more than one segment, append the exponent notation.
        if len(self.segments) > 1:
            rep += "E"  # Add the "E" for scientific notation (exponent).
            
            # Calculate the exponent based on the number of segments and chunk size.
            idiv = ((len(self.segments) - 1) * self.chunksize) // 10
            fdiv = ((len(self.segments) - 1) * self.chunksize) / 10
            
            # Use the integer division result if it matches the float division result,
            # otherwise, use the float division result (to preserve precision).
            rep += str(idiv if idiv == fdiv else fdiv)
        
        return rep  # Return the detailed string representation suitable for debugging.

