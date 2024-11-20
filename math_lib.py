

class num():
    def __init__(self, num):
        self.segments = []
        self.chunksize = 5
        
        self.digits = 0
        self.negative = num < 0
        
        string = str(abs(num))
        self.digits = len(string)
        
        self.segments.append(string[: len(string) % self.chunksize])
        
        for i in range(len(string) // self.chunksize):
            self.segments.append(string[(len(string) % self.chunksize) + i * self.chunksize: (len(string) % self.chunksize) + (i + 1) * self.chunksize])

        if self.segments[0] == '':
            self.segments.remove('')
        
    def add(self, sec_num: "num"):
        ret = num(0)
        ret.negative = self.negative

        over = 0
        ret.segments = []

        max_segments = max(len(self.segments), len(sec_num.segments))
        self.segments = ["0"] * (max_segments - len(self.segments)) + self.segments
        sec_num.segments = ["0"] * (max_segments - len(sec_num.segments)) + sec_num.segments

        for x, y in zip(reversed(self.segments), reversed(sec_num.segments)):
            sol = str(int(x) + int(y) + over)
            if len(sol) > self.chunksize:
                ret.segments.insert(0, sol[-self.chunksize:])
                over = int(sol[:-self.chunksize])
            else:
                ret.segments.insert(0, sol)
                over = 0
        
        if over > 0:
            ret.segments.insert(0, str(over))

        ret.segments[0] = ret.segments[0].lstrip("0") or "0"
        return ret

    def sub(self, sec_num: "num"):
        # Determine the larger number for subtraction
        is_self_larger = self.segments > sec_num.segments if self.segments != sec_num.segments else not self.negative

        larger, smaller = (self, sec_num) if is_self_larger else (sec_num, self)
        result_negative = self.negative if is_self_larger else not self.negative

        # Pad smaller number's segments with zeros to match the length
        diff = len(larger.segments) - len(smaller.segments)
        smaller_segments = ["0"] * diff + smaller.segments

        result_segments = []
        borrow = 0
        base = 100000  # Assume the base is 100000 as per the original logic

        # Process each segment from least significant to most significant
        for x, y in zip(reversed(larger.segments), reversed(smaller_segments)):
            x_val = int(x) - borrow
            y_val = int(y)

            if x_val < y_val:
                borrow = 1
                x_val += base
            else:
                borrow = 0

            result_segments.append(str(x_val - y_val))

        # Reverse and remove leading zeros
        result_segments.reverse()
        while len(result_segments) > 1 and result_segments[0] == "0":
            result_segments.pop(0)

        # Return the result as a new num instance
        ret = num(0)
        ret.segments = result_segments
        ret.negative = result_negative
        return ret


    def __add__(self, sec_num: "num | int | float"):
        if not isinstance(sec_num, num):
            sec_num = num(int(sec_num))
        
        if self.negative == sec_num.negative:
            return self.add(sec_num)
        elif self.negative:
            return sec_num.sub(self)
        else:
            return self.sub(sec_num)

    def __sub__(self, sec_num: "num | int | float"):
        if not isinstance(sec_num, num):
            sec_num = num(int(sec_num))
        
        return self + (-sec_num)
    
    def __mul__(self, sec_num: "num | int | float"):
        if not isinstance(sec_num, num):
            sec_num = num(int(sec_num))

        # if self == sec_num:
            # return self**2

    def __round__(self):
        rep = ""
        
        if self.negative:
            rep = "-"
        
        rep += self.segments[0]
        
        if len(self.segments) >= 2 and int(self.segments[1][:1]) >= 5:
            rep = str(int(rep) + 1)

        if len(self.segments) > 1:
            rep += "e"
            
            idiv = ((len(self.segments) - 1) * self.chunksize) // 10
            fdiv = ((len(self.segments) - 1) * self.chunksize) / 10
            
            rep += str(idiv if idiv == fdiv else fdiv)
        
        return rep
    
    def __ceil__(self):
        rep = ""
        
        if self.negative:
            rep = "-"
        
        rep += self.segments[0]
        
        rep = str(int(rep) + 1)

        if len(self.segments) > 1:
            rep += "e"
            
            idiv = ((len(self.segments) - 1) * self.chunksize) // 10
            fdiv = ((len(self.segments) - 1) * self.chunksize) / 10
            
            rep += str(idiv if idiv == fdiv else fdiv)
        
        return rep
    
    def __floor__(self):
        rep = ""
        
        if self.negative:
            rep = "-"
        
        rep += self.segments[0]

        if len(self.segments) > 1:
            rep += "e"
            
            idiv = ((len(self.segments) - 1) * self.chunksize) // 10
            fdiv = ((len(self.segments) - 1) * self.chunksize) / 10
            
            rep += str(idiv if idiv == fdiv else fdiv)
        
        return rep
    
    def __and__(self, sec_num):
        return bool(self) and bool(sec_num)
    
    def __or__(self, sec_num):
        return bool(self) or bool(sec_num)
    
    def __bool__(self):
        return self.__ne__(0)
    
    def __neg__(self):
        ret = num(0)
        ret.segments = self.segments
        ret.negative = not self.negative
        
        return ret
    
    def __pos__(self):
        ret = num(0)
        ret.segments = self.segments
        ret.negative = self.negative
        
        return ret
    
    def __abs__(self):
        ret = num(0)
        ret.segments = self.segments
        ret.negative = False
        
        return ret
    
    def __eq__(self, sec_num: "num | int | float"):
        if isinstance(sec_num, num):
            return (self.segments == sec_num.segments) and (self.negative == sec_num.negative)
        elif isinstance(sec_num, int) or isinstance(sec_num, float):
            if not ((sec_num < 0) == self.negative):
                return False
            
            sec_num_str = str(sec_num)
            return str(self) == sec_num_str
        else:
            return NotImplemented
    
    def __gt__(self, sec_num: "num"):
        if isinstance(sec_num, num):
            if self.__eq__(sec_num):
                return False
            
            if self.negative != sec_num.negative:
                return sec_num.negative
            
            if self.digits > sec_num.digits:
                return True
            elif sec_num.digits > self.digits:
                return False
            
            for seg1, seg2 in zip(self.segments, sec_num.segments):
                for char1, char2 in zip(seg1, seg2):
                    if char1 != char2:
                        return char1 > char2
        
        sec_num = int(sec_num)
        
        return self.__gt__(num(sec_num))
    
    def __ne__(self, sec_num: "num"):
        return not self.__eq__(sec_num)
    
    def __lt__(self, sec_num: "num"):
        return not self.__eq__(sec_num) and not self.__gt__(sec_num)
    
    def __ge__(self, sec_num: "num"):
        return self.__eq__(sec_num) or self.__gt__(sec_num)
    
    def __le__(self, sec_num: "num"):
        return self.__eq__(sec_num) or self.__lt__(sec_num)
    
    def __str__(self):
        rep = ""
        
        if self.negative:
            rep = "-"
        
        for i in range(len(self.segments)):
            rep += self.segments[i]
        
        return rep
    
    def __repr__(self):
        rep = ""
        
        if self.negative:
            rep = "-"
        
        rep += self.segments[0]

        if len(self.segments) > 1:
            rep += "E"
            
            idiv = ((len(self.segments) - 1) * self.chunksize) // 10
            fdiv = ((len(self.segments) - 1) * self.chunksize) / 10
            
            rep += str(idiv if idiv == fdiv else fdiv)
        
        return rep


print(num(100000) * num(100000))