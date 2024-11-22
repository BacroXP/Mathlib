

class num():
    def __init__(self, num: int | float | str, chunksize: int = 10):
        """
        Initializes a `num` object by dividing a large number into manageable segments.
        
        Args:
            num (int | str): The number to be represented, can be a positive or negative integer or string.
        """
        self.full_segments = []  # List to store the integer part chunks
        self.split_segments = []  # List to store the fractional part chunks
        self.chunksize = chunksize  # Maximum number of digits in each segment
        self.chunkbase = 10 ** self.chunksize  # The base for chunks
        
        # Convert input to string and determine negativity
        if isinstance(num, (int, float)):
            num = str(num)
        elif not isinstance(num, str):
            raise ValueError("Input must be an int, float, or string representation of a number.")
        
        self.negative = num.startswith('-')  # Track if the number is negative
        if self.negative:
            num = num[1:]  # Remove the '-' for processing
        
        # Split the number into integer and fractional parts
        integer_part, *fractional_part = num.split('.')
        fractional_part = fractional_part[0] if fractional_part else '0'
        
        # Process integer part
        self.full_digits = len(integer_part)
        if integer_part:
            for i in range(0, len(integer_part), chunksize):
                self.full_segments.append(integer_part[max(0, len(integer_part) - i - chunksize): len(integer_part) - i])

        # Reverse segments to maintain correct order
        self.full_segments.reverse()

        # Process fractional part
        self.split_digits = len(fractional_part)
        if fractional_part:
            for i in range(0, len(fractional_part), chunksize):
                self.split_segments.append(fractional_part[i:i + chunksize])


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
        ret.full_segments = []
        
        # If the signs differ, delegate to subtraction logic
        if self.negative != sec_num.negative:
            if self.negative:
                return sec_num.subtract(self.negate())
            else:
                return self.subtract(sec_num.negate())
        
        # Both numbers have the same sign; result will inherit this sign
        ret.negative = self.negative

        # Initialize carry-over
        over = 0

        # --- Handle fractional parts ---
        # Pad fractional parts to the same length
        max_split_length = max(len(self.split_segments), len(sec_num.split_segments))
        split_self = self.split_segments + ["0"] * (max_split_length - len(self.split_segments))
        split_sec = sec_num.split_segments + ["0"] * (max_split_length - len(sec_num.split_segments))

        # Add fractional parts from least significant to most significant
        for x, y in zip(reversed(split_self), reversed(split_sec)):
            sol = str(int(x) + int(y) + over)
            if len(sol) > self.chunksize:
                ret.split_segments.insert(0, sol[-self.chunksize:])
                over = int(sol[:-self.chunksize])
            else:
                ret.split_segments.insert(0, sol)
                over = 0

        # Clean up trailing zeros in the least significant fractional part
        while ret.split_segments and ret.split_segments[-1] == "0":
            ret.split_segments.pop()

        # --- Handle integer parts ---
        # Pad integer parts to the same length
        max_full_length = max(len(self.full_segments), len(sec_num.full_segments))
        full_self = ["0"] * (max_full_length - len(self.full_segments)) + self.full_segments
        full_sec = ["0"] * (max_full_length - len(sec_num.full_segments)) + sec_num.full_segments

        # Add integer parts from least significant to most significant
        for x, y in zip(reversed(full_self), reversed(full_sec)):
            sol = str(int(x) + int(y) + over)
            if len(sol) > self.chunksize:
                ret.full_segments.insert(0, sol[-self.chunksize:])
                over = int(sol[:-self.chunksize])
            else:
                ret.full_segments.insert(0, sol)
                over = 0

        # If there is any remaining carry-over, prepend it as a new segment
        if over > 0:
            ret.full_segments.insert(0, str(over))

        # Clean up leading zeros in the most significant integer part
        ret.full_segments[0] = ret.full_segments[0].lstrip("0") or "0"

        return ret


    def sub(self, sec_num: "num") -> "num":
        """
        Subtracts `sec_num` from the current `num` object.

        Args:
            sec_num (num): The second number to subtract.

        Returns:
            num: A new `num` instance representing the subtraction result.
        """
        # Determine which number is larger for subtraction (accounting for sign)
        is_self_larger = self.full_segments > sec_num.full_segments if self.full_segments != sec_num.full_segments else not self.negative

        # Identify the larger and smaller number for subtraction
        larger, smaller = (self, sec_num) if is_self_larger else (sec_num, self)
        result_negative = self.negative if is_self_larger else not self.negative

        # Pad the smaller number with leading zeros to match the larger number's length
        diff = len(larger.full_segments) - len(smaller.full_segments)
        smaller_segments = ["0"] * diff + smaller.full_segments

        # Initialize variables for the result and borrowing
        result_segments = []
        borrow = 0

        # Perform chunk-based subtraction
        for x, y in zip(reversed(larger.full_segments), reversed(smaller_segments)):
            x_val = int(x) - borrow  # Apply any carried-over borrow
            y_val = int(y)

            # Handle borrowing if x_val < y_val
            if x_val < y_val:
                borrow = 1
                x_val += self.chunkbase  # Add chunkbase to x_val to borrow
            else:
                borrow = 0

            # Append the result of the current chunk subtraction
            result_segments.append(str(x_val - y_val))

        # Reverse and remove leading zeros
        result_segments.reverse()
        while len(result_segments) > 1 and result_segments[0] == "0":
            result_segments.pop(0)

        # Create a new `num` object for the result
        ret = num(0)
        ret.full_segments = result_segments
        ret.negative = result_negative
        return ret


    def __add__(self, sec_num: "num | int | float") -> "num":
        """
        Adds the current `num` object with another `num` object, integer, or float.

        Args:
            sec_num (num | int | float): The number to add.

        Returns:
            num: A new `num` instance representing the addition result.
        """
        # Convert non-`num` inputs to `num`
        if not isinstance(sec_num, num):
            sec_num = num(sec_num)

        # Case 1: Same sign addition
        if self.negative == sec_num.negative:
            return self.add(sec_num)

        # Case 2: Opposite sign addition
        elif self.negative:
            # Equivalent to sec_num - abs(self)
            return sec_num.sub(self)

        else:
            # Equivalent to self - abs(sec_num)
            return self.sub(sec_num)


    def __radd__(self, sec_num: "num | int | float") -> "num":
        """
        Handles reverse addition for `num` objects (e.g., `5 + num_instance`).

        Args:
            sec_num (num | int | float): The number to add.

        Returns:
            num: A new `num` instance representing the addition result.
        """
        return self + sec_num  # Call `__add__` for regular addition handling


    def __sub__(self, sec_num: "num | int | float") -> "num":
        """
        Subtracts `sec_num` from the current `num` object.

        Args:
            sec_num (num | int | float): The number to subtract.

        Returns:
            num: A new `num` instance representing the subtraction result.
        """
        # Use addition with the negation of `sec_num`
        return self + (-sec_num)


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
            sec_num = num(sec_num)  # Convert sec_num to a `num` instance

        # Prepare the result storage. The result will have at most len(self.full_segments) + len(sec_num.full_segments) full_segments
        result_full_segments = [0] * (len(self.full_segments) + len(sec_num.full_segments))
        result_split_segments = [0] * (len(self.split_segments) + len(sec_num.split_segments))

        # Multiply each segment of `self` with each segment of `sec_num`
        for i, x in enumerate(reversed(self.full_segments)):
            for j, y in enumerate(reversed(sec_num.full_segments)):
                product = int(x) * int(y) + result_full_segments[i + j]  # Multiply and add any existing value
                result_full_segments[i + j] = product % self.chunkbase  # Current segment value (modulo base)
                result_full_segments[i + j + 1] += product // self.chunkbase  # Carry to next segment (integer division)

        for i, x in enumerate(reversed(self.split_segments)):
            for j, y in enumerate(reversed(sec_num.split_segments)):
                product = int(x) * int(y) + result_split_segments[i + j]  # Multiply and add any existing value
                result_split_segments[i + j] = product % self.chunkbase  # Current segment value (modulo base)
                result_split_segments[i + j + 1] += product // self.chunkbase  # Carry to next segment (integer division)

        # Remove leading zeros from the result
        while len(result_full_segments) > 1 and result_full_segments[-1] == 0:
            result_full_segments.pop(-1)
        
        # Remove ending zeros from the result
        while len(result_split_segments) > 1 and result_split_segments[0] == 0:
            result_split_segments.pop(0)

        # Reverse the result full_segments and convert them to strings
        result_full_segments = list(map(str, reversed(result_full_segments)))
        result_split_segments = list(map(str, reversed(result_split_segments)))

        # Add leading zeros to each segment to ensure they match the chunk size (self.chunksize)
        for i, el in enumerate(result_full_segments):
            # Pad each segment to match the chunksize by adding leading zeros
            for _ in range(self.chunksize - len(el)):
                result_full_segments[i] = "0" + result_full_segments[i]
        
        for i, el in enumerate(result_split_segments):
            # Pad each segment to match the chunksize by adding leading zeros
            for _ in range(self.chunksize - len(el)):
                result_split_segments[i] = "0" + result_split_segments[i]

        # Remove leading zeros from the final result
        result_full_segments[0] = result_full_segments[0].lstrip("0") or "0"
        result_split_segments[0] = result_split_segments[0].lstrip("0") or "0"

        # Determine the sign of the result
        result_negative = self.negative != sec_num.negative  # Result is negative if signs differ

        # Create a new `num` instance for the result
        ret = num(0)
        ret.full_segments = result_full_segments
        ret.split_segments = result_split_segments
        ret.negative = result_negative  # Set the correct sign for the result
        return ret
    

    def __truediv__(self, sec_num: "num | int | float") -> "num":
        """
        Performs true division of the current `num` instance by another `num`, int, or float, 
        using chunk-based arithmetic and ensuring the divisor is also segmented properly.

        Args:
        - sec_num (num | int | float): The divisor, which can be another `num` object, 
                                    or an integer/float that will be converted to `num`.

        Returns:
        - num: The result of the division as a new `num` instance.
        """
        # Convert non-num inputs into a `num` object.
        if not isinstance(sec_num, num):
            sec_num = num(sec_num)

        # Handle division by zero.
        if sec_num == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")

        # Create a result `num` object and initialize its attributes.
        result = num(0)
        result.negative = self.negative != sec_num.negative  # Set the sign of the result.

        # Result storage (in chunks).
        chunk_result = []
        remainder = 0

        # Process the dividend chunk by chunk.
        for chunk in self.full_segments:
            # Bring down the next chunk, combining with any remainder from the previous step.
            current_value = remainder * (10 ** self.chunksize) + int(chunk)

            # Perform integer division for this chunk.
            chunk_quotient = current_value // int("".join(sec_num.full_segments))
            remainder = current_value % int("".join(sec_num.full_segments))

            # Convert the quotient back to a chunk, ensuring it respects chunk size.
            chunk_result.append(f"{chunk_quotient:0{self.chunksize}d}")

        # Clean up leading zeros from the result.
        if int(chunk_result[0]) == 0:
            chunk_result.remove(chunk_result[0])
        chunk_result[0] = chunk_result[0].lstrip("0") or "0"

        # Assign the final result.
        result.full_segments = chunk_result

        return result


    def __round__(self, ndigits: int = 0) -> "num":
        """
        Round the number to the nearest integer or specified number of digits.

        Parameters:
        - ndigits (int): Number of digits to round to. Defaults to 0 for rounding to the nearest integer.

        Returns:
        - num: A new `num` instance representing the rounded value.
        """
        # Create a new num object for the result
        res = num(0)
        res.chunksize = self.chunksize
        res.negative = self.negative

        # Handle rounding for the integer (full_segments) part
        res.full_segments = self.full_segments.copy()

        if ndigits >= 0:
            # Round fractional part to `ndigits` precision
            fractional_str = ''.join(self.split_segments)
            fractional_relevant = fractional_str[:ndigits]
            fractional_next_digit = fractional_str[ndigits:ndigits + 1]

            # Decide whether to round up based on the next digit
            if fractional_next_digit and int(fractional_next_digit) >= 5:
                fractional_relevant = str(int(fractional_relevant or "0") + 1)

            # Pad or truncate fractional segments to fit ndigits
            fractional_padded = fractional_relevant + "0" * (ndigits - len(fractional_relevant))
            res.split_segments = [fractional_padded[i:i + res.chunksize]
                                for i in range(0, len(fractional_padded), res.chunksize)]
        else:
            # Round full_segments when ndigits < 0 (e.g., -1 rounds to the nearest 10)
            abs_ndigits = abs(ndigits)
            rounding_index = len(self.full_segments) - (abs_ndigits // self.chunksize) - 1

            # Handle rounding for the relevant full_segment
            if rounding_index >= 0:
                relevant_segment = int(self.full_segments[rounding_index])
                next_digit = int(self.full_segments[rounding_index + 1][0]) if rounding_index + 1 < len(self.full_segments) else 0

                # Perform rounding based on next digit
                if next_digit >= 5:
                    relevant_segment += 1
                res.full_segments[rounding_index] = str(relevant_segment)

            # Truncate remaining full_segments and pad with zeros
            for i in range(rounding_index + 1, len(res.full_segments)):
                res.full_segments[i] = "0"

            # Clear fractional parts since we're rounding to a larger unit
            res.split_segments = []

        return res


    def __ceil__(self, ndigits: int = 0) -> "num":
        """
        Return the smallest integer greater than or equal to the number.

        If ndigits is specified:
        - Rounds up to the specified number of decimal places.

        Parameters:
        - ndigits (int): Number of decimal places to round to (default is 0, rounding to the nearest integer).

        Returns:
        - num: A new `num` instance representing the rounded-up value.
        """
        # Create a result num object
        res = num(0)
        res.chunksize = self.chunksize
        res.negative = self.negative

        if self.negative:
            # Negative numbers "round up" by truncating toward 0
            res.full_segments = self.full_segments.copy()
            if ndigits >= 0:
                # Handle fractional part truncation for negative numbers
                fractional_str = ''.join(self.split_segments)
                truncated_fraction = fractional_str[:ndigits]
                res.split_segments = [truncated_fraction[i:i + res.chunksize]
                                    for i in range(0, len(truncated_fraction), res.chunksize)]
            else:
                # Handle truncation for ndigits < 0 for negative numbers
                abs_ndigits = abs(ndigits)
                rounding_index = len(self.full_segments) - (abs_ndigits // self.chunksize) - 1

                # Truncate unnecessary segments
                for i in range(rounding_index + 1, len(self.full_segments)):
                    res.full_segments[i] = "0"

                res.split_segments = []
        else:
            # Positive numbers: Handle rounding up
            res.full_segments = self.full_segments.copy()

            if ndigits >= 0:
                # Round fractional part to `ndigits` precision
                fractional_str = ''.join(self.split_segments)
                fractional_relevant = fractional_str[:ndigits]
                fractional_next_digit = fractional_str[ndigits:ndigits + 1]

                # Decide whether to round up
                if fractional_next_digit and int(fractional_next_digit) > 0:
                    # Increment the fractional part
                    fractional_relevant = str(int(fractional_relevant or "0") + 1)

                # Pad or truncate fractional segments to fit ndigits
                fractional_padded = fractional_relevant + "0" * (ndigits - len(fractional_relevant))
                res.split_segments = [fractional_padded[i:i + res.chunksize]
                                    for i in range(0, len(fractional_padded), res.chunksize)]
            else:
                # Handle truncation for ndigits < 0
                abs_ndigits = abs(ndigits)
                rounding_index = len(self.full_segments) - (abs_ndigits // self.chunksize) - 1

                # Perform rounding at the relevant full_segment
                if rounding_index >= 0:
                    relevant_segment = int(self.full_segments[rounding_index])
                    res.full_segments[rounding_index] = str(relevant_segment + 1)

                # Zero out segments beyond the rounding index
                for i in range(rounding_index + 1, len(res.full_segments)):
                    res.full_segments[i] = "0"

                # Clear fractional parts since we’re rounding to a larger unit
                res.split_segments = []

        return res


    def __floor__(self, ndigits: int = 0) -> "num":
        """
        Return the largest integer less than or equal to the number, optionally truncating to `ndigits` after the decimal.

        Parameters:
        - ndigits (int): The number of digits to consider after the decimal point (default is 0, truncating to the integer).

        Returns:
        - num: A new `num` instance representing the floored value.
        """
        # Create a new num object for the result
        res = num(0)
        res.negative = self.negative
        res.chunksize = self.chunksize

        # Handle full (integer part) segments
        res.full_segments = self.full_segments.copy()

        # Handle split (fractional part) segments
        if ndigits >= 0:
            # Keep only `ndigits` digits from split segments
            fractional_str = ''.join(self.split_segments)
            fractional_truncated = fractional_str[:ndigits]
            fractional_padded = fractional_truncated + "0" * (ndigits - len(fractional_truncated))
            res.split_segments = [fractional_padded[i:i + res.chunksize]
                                for i in range(0, len(fractional_padded), res.chunksize)]
        else:
            # Discard all fractional parts when ndigits < 0
            res.split_segments = []

        # Adjust for negative numbers (subtract 1 if there's a fractional part)
        if self.negative and any(int(x) > 0 for x in self.split_segments):
            res -= num(1)

        return res

    
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
        ret.full_segments = self.full_segments  # Copy the full_segments of the original number
        ret.split_segments = self.split_segments # Copy the splt_segmnets of the original number
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
        ret.full_segments = self.full_segments  # Copy the full_segments of the original number
        ret.split_segments = self.split_segments # Copy the splt_segmnets of the original number
        ret.negative = self.negative  # Maintain the same negative flag
        
        return ret


    def __abs__(self) -> "num":
        """
        Return the absolute value of the `num` object.

        The result will have the same full_segments, but the negative flag is set to False.

        Returns:
        - A new `num` object that represents the absolute value of the current number.
        """
        ret = num(0)  # Create a new num instance for the result
        ret.full_segments = self.full_segments  # Copy the full_segments of the original number
        ret.split_segments = self.split_segments # Copy the splt_segmnets of the original number
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
        # Convert non-num types to a num object for comparison
        if not isinstance(sec_num, num):
            sec_num = num(sec_num)

        # Check full (before the decimal) and split (after the decimal) segments and the sign
        return (self.full_segments == sec_num.full_segments and
                self.split_segments == sec_num.split_segments and
                self.negative == sec_num.negative)


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
            
            # Compare the number of full_digits (length of the full_segments)
            if self.full_digits > sec_num.full_digits:
                return True
            elif sec_num.full_digits > self.full_digits:
                return False
            
            # Compare each segment from the most significant
            for seg1, seg2 in zip(self.full_segments, sec_num.full_segments):
                for char1, char2 in zip(seg1, seg2):
                    # Compare each character and return the result
                    if char1 != char2:
                        return char1 > char2

            for seg1, seg2 in zip(self.split_segments, sec_num.split_segments):
                for char1, char2 in zip(seg1, seg2):
                    # Compare each character and return the result
                    if char1 != char2:
                        return char1 > char2

        return False


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
        The full_segments are concatenated to form the full number.

        Returns:
        - A string representation of the number.
        """
        rep = ""  # Initialize an empty string for the result.
        
        # If the number is negative, add a minus sign.
        if self.negative:
            rep = "-"
        
        # Append each segment to the result string.
        for el in self.full_segments:
            rep += el
        
        rep += "."
        
        if self.split_segments:
            for el in self.split_segments:
                rep += el
        else:
            rep += "0"
        
        return rep  # Return the complete string representation of the number.

