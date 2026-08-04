import numpy as np


def dec_to_ieee(num):
    sign = '0' if num >= 0 else '1'
    num = abs(num)

    # get integer and fractional parts
    int_part = int(num)
    frac_part = num - int_part

    # convert integer part to binary
    int_bin = bin(int_part)[2:]

    # convert fractional part to binary
    frac_bin = []
    while frac_part and len(frac_bin) < 23:
        frac_part *= 2
        bit = int(frac_part)
        frac_bin.append(str(bit))
        frac_part -= bit

    # normalize
    exponent = len(int_bin) - 1
    mantissa = int_bin[1:] + ''.join(frac_bin)

    # adjust mantissa to 23 bits
    mantissa = (mantissa + '0' * 23)[:23]

    # exponent with bias (127)
    exponent_bin = f"{exponent + 127:08b}"

    # merge into one binary string
    res = sign + exponent_bin + mantissa
    res_full = res + '0' * (32 - len(res))  # pad to 32 bits if necessary

    return res_full

def bin_to_hex(bin_str):
    # converts binary string to hexadecimal
    hex_str = hex(int(bin_str, 2))[2:]  # convert to int and then to hex, remove '0x'
    return hex_str.upper()  # return in uppercase for consistency

def truncate_dec(num, digits):
    # truncate a number to a certain number of significant digits
    if num == 0:
        return 0
    elif num < 0:
        return -truncate_dec(-num, digits)
    else:
        return float(np.floor(num * 10**(digits - 1 - int(np.floor(np.log10(num))))) / 10**(digits - 1 - int(np.floor(np.log10(num)))))

def round_up_dec(num, digits):
    # round up a number to a certain number of significant digits
    if num == 0:
        return 0
    elif num < 0:
        return -round_down_dec(-num, digits)
    else:
        factor = 10 ** (digits - 1 - int(np.floor(np.log10(num))))
        return np.ceil(num * factor) / factor

def round_down_dec(num, digits):
    # round down a number to a certain number of significant digits
    if num == 0:
        return 0
    elif num < 0:
        return -round_up_dec(-num, digits)
    else:
        factor = 10 ** (digits - 1 - int(np.floor(np.log10(num))))
        return np.floor(num * factor) / factor

def round_to_nearest_dec(num, digits):
    # round to nearest, ties to even
    if num == 0:
        return 0
    elif num < 0:
        return -round_to_nearest_dec(-num, digits)
    else:
        factor = 10 ** (digits - 1 - int(np.floor(np.log10(num))))
        rounded = round(num * factor) / factor
        # check for tie and round to even
        if abs(rounded * factor - num * factor) == 0.5:
            if int(rounded * factor) % 2 != 0:
                rounded += 1 / factor
        return rounded

def round_decimal(num, digits):
    # rounding methods for decimal numbers
    float_num = float(num)

    # chopping
    chopped = truncate_dec(float_num, digits)

    # round-up
    rounded_up = round_up_dec(float_num, digits)

    # round-down
    rounded_down = round_down_dec(float_num, digits)

    # round-to-nearest, ties-to-even
    rounded_to_nearest = round_to_nearest_dec(float_num, digits)

    return chopped, rounded_up, rounded_down, rounded_to_nearest

def truncate_bin(int_part, frac_part, len_bin, bits):
    # truncate a signed binary floating point string to a certain number of bits
    if len_bin <= bits:
        return int_part, frac_part  # no truncation needed
    elif len_bin > bits:
        # determine how many bits to keep from integer and fractional parts
        int_len = len(int_part)
        frac_len = len(frac_part)
        # keep all of integer part and some of fractional part
        remaining_bits = bits - int_len
        return int_part, frac_part[:remaining_bits]

def round_up_bin(int_part, frac_part, len_bin, bits):
    # round up a signed binary floating point string to a certain number of bits
    if len_bin <= bits:
        return int_part, frac_part  # no rounding needed
    elif len_bin > bits:
        # determine how many bits to keep from integer and fractional parts
        int_len = len(int_part)
        frac_len = len(frac_part)
        # keep all of integer part and some of fractional part
        remaining_bits = bits - int_len
        new_frac = frac_part[:remaining_bits]
        if remaining_bits < frac_len and '1' in frac_part[remaining_bits:]:
            # need to round up
            new_frac = bin(int(new_frac, 2) + 1)[2:].zfill(remaining_bits)
            if len(new_frac) > remaining_bits:
                # carry over to integer part
                new_int = bin(int(int_part, 2) + 1)[2:]
                return new_int, new_frac[1:]  # drop the leading '1' from fractional part
        return int_part, new_frac

def round_down_bin(int_part, frac_part, len_bin, bits):
    # round down a signed binary floating point string to a certain number of bits
    
    if len_bin <= bits:
        return int_part, frac_part  # no rounding needed
    elif len_bin > bits:
        # determine how many bits to keep from integer and fractional parts
        int_len = len(int_part)
        frac_len = len(frac_part)
        # keep all of integer part and some of fractional part
        remaining_bits = bits - int_len
        new_frac = frac_part[:remaining_bits]
        return int_part, new_frac

def round_to_nearest_bin(int_part, frac_part, len_bin, bits):
    # round to nearest, ties to even for signed binary floating point string
    if len_bin <= bits:
        return int_part, frac_part  # no rounding needed
    elif len_bin > bits:
        # determine how many bits to keep from integer and fractional parts
        int_len = len(int_part)
        frac_len = len(frac_part)
        if int_len >= bits:
            # odd, round up
            res = bin(int(int_part[:bits], 2) + 1)[2:].zfill(bits)
            res += '0' * (len_bin - bits)
            return res, ''
        else:
            # keep all of integer part and some of fractional part
            remaining_bits = bits - int_len
            new_frac = frac_part[:remaining_bits]
            if remaining_bits < frac_len:
                next_bit = frac_part[remaining_bits]
                if next_bit == '1':
                    # check for tie
                    if remaining_bits + 1 < frac_len and frac_part[remaining_bits + 1] == '0':
                        # tie, round to even
                        if int(new_frac[-1]) % 2 != 0:
                            new_frac = bin(int(new_frac, 2) + 1)[2:].zfill(remaining_bits)
                    else:
                        # round up
                        new_frac = bin(int(new_frac, 2) + 1)[2:].zfill(remaining_bits)
                    if len(new_frac) > remaining_bits:
                        # carry over to integer part
                        new_int = bin(int(int_part, 2) + 1)[2:]
                        return new_int, new_frac[1:]  # drop the leading '1' from fractional part
            return int_part, new_frac

def round_binary(bin_str, bits):
    # rounding methods for signed binary floating point numbers
    # check for negative sign
    if bin_str[0] == '-': 
        sign = '-'
        bin_str = bin_str[1:]
    # check for positive sign or no sign
    elif bin_str[0] == '+' or bin_str[0] == '0' or bin_str[0] == '1':
        sign = ''
    # check for invalid input
    else:
        raise ValueError("Invalid binary input format")

    # determine the length of the binary string
    if '.' in bin_str:
        int_part, frac_part = bin_str.split('.')
        len_bin = len(int_part) + len(frac_part)
    else:
        int_part = bin_str
        frac_part = ''
        len_bin = len(bin_str)

    # chopping
    chopped_int, chopped_frac = truncate_bin(int_part, frac_part, len_bin, bits)
    chopped_res = sign + chopped_int + ('.' + chopped_frac if chopped_frac else '')

    # round-up
    if sign == '-':
        # for negative numbers, round-up is actually round-down in magnitude
        rounded_up_int, rounded_up_frac = round_down_bin(int_part, frac_part, len_bin, bits)
    else:
        rounded_up_int, rounded_up_frac = round_up_bin(int_part, frac_part, len_bin, bits)

    rounded_up_res = sign + rounded_up_int + ('.' + rounded_up_frac if rounded_up_frac else '')

    # round-down
    if sign == '-':
        # for negative numbers, round-down is actually round-up in magnitude
        rounded_down_int, rounded_down_frac = round_up_bin(int_part, frac_part, len_bin, bits)
    else:
        rounded_down_int, rounded_down_frac = round_down_bin(int_part, frac_part, len_bin, bits)
        
    rounded_down_res = sign + rounded_down_int + ('.' + rounded_down_frac if rounded_down_frac else '')

    # round-to-nearest, ties-to-even
    rounded_nearest_int, rounded_nearest_frac = round_to_nearest_bin(int_part, frac_part, len_bin, bits)
    rounded_nearest_res = sign + rounded_nearest_int + ('.' + rounded_nearest_frac if rounded_nearest_frac else '')

    return chopped_res, rounded_up_res, rounded_down_res, rounded_nearest_res

def main():
    choice = input("Choose a task:\n1. Decimal → IEEE 754 Double\n2. Rounding Methods\n3. Arithmetic (GRS Method)\nEnter 1, 2, or 3: ")

    if choice == '1':
        n = float(input("Enter a decimal number: "))
        bin_rep = dec_to_ieee(n)
        # format binary representation into groups of 4
        bin_formatted = f"{bin_rep[0:4]} {bin_rep[4:8]} {bin_rep[8:12]} {bin_rep[12:16]} {bin_rep[16:20]} {bin_rep[20:24]} {bin_rep[24:28]} {bin_rep[28:32]}"
        print(bin_formatted)

        # convert binary to hexadecimal
        hex_rep = bin_to_hex(bin_rep)
        print(hex_rep)

    elif choice == '2':
        round_choice = input("Choose an input format: \n1. Decimal\n2. Binary\nEnter 1 or 2: ")
        if round_choice == '1':
            user_input = input("Enter a decimal number: ")
            try:
                num = float(user_input)
            except ValueError:
                print("Invalid input. Please enter a valid decimal number.")
                return
            digits = int(input("Enter target significant digits: "))
            # implements rounding methods for decimal input
            chopped, rounded_up, rounded_down, rounded_to_nearest = round_decimal(num, digits)
            print("Chopped:", chopped)
            print("Round-up:", rounded_up)
            print("Round-down:", rounded_down)
            print("Round-to-nearest, ties-to-even:", rounded_to_nearest)

        elif round_choice == '2':
            try:
                bin_num = input("Enter a signed binary floating point number (e.g., -110.101): ")
                # validate binary input
                if not all(c in '01.-' for c in bin_num) or bin_num.count('.') > 1 or (bin_num[0] not in '-+' and not bin_num[0].isdigit()):
                    raise ValueError("Invalid binary input format")
            except ValueError as e:
                print(e)
                return
            bits = int(input("Enter target bits: "))
            # implement rounding methods for signed binary floating point input
            chopped, round_up, round_down, round_nearest = round_binary(bin_num, bits)
            print("Chopped:", chopped)
            print("Round-up:", round_up)
            print("Round-down:", round_down)
            print("Round-to-nearest, ties-to-even:", round_nearest)

    elif choice == '3':

        pass

if __name__ == "__main__": # only activates main function if main is executed directly (just incase)
    main()

