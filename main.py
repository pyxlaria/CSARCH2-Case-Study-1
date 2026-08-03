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

def round_binary(bin_str, bits):
    if not isinstance(bin_str, str):
        raise TypeError("bin_str must be a string")

    bin_str = bin_str.strip()
    if not bin_str:
        raise ValueError("Binary input cannot be empty")

    negative = bin_str.startswith('-')
    if negative:
        bin_str = bin_str[1:]
    elif bin_str.startswith('+'):
        bin_str = bin_str[1:]

    if '.' not in bin_str:
        bin_str = bin_str + '.0'

    int_part, frac_part = bin_str.split('.', 1)
    int_part = int_part or '0'
    frac_part = frac_part or ''

    if not set(int_part).issubset({'0', '1'}) or not set(frac_part).issubset({'0', '1'}):
        raise ValueError("Input must be a binary floating-point number")

    if bits < 0:
        raise ValueError("bits must be zero or a positive integer")

    def format_value(int_bits, frac_bits):
        if bits == 0:
            return ('-' if negative else '') + int_bits
        return ('-' if negative else '') + int_bits + '.' + frac_bits

    def increment_fraction(int_bits, frac_bits):
        if not frac_bits:
            return str(int(int_bits, 2) + 1), ''

        frac_val = int(frac_bits, 2) + 1
        if frac_val == (1 << len(frac_bits)):
            return str(int(int_bits, 2) + 1), '0' * len(frac_bits)
        return int_bits, format(frac_val, f'0{len(frac_bits)}b')

    def round_fraction(mode, int_bits, frac_bits):
        kept = frac_bits[:bits]
        discarded = frac_bits[bits:]

        if mode == 'trunc':
            return int_bits, kept

        if not discarded or all(ch == '0' for ch in discarded):
            return int_bits, kept

        if mode == 'up':
            if negative:
                return int_bits, kept
            return increment_fraction(int_bits, kept)

        if mode == 'down':
            if negative:
                return increment_fraction(int_bits, kept)
            return int_bits, kept

        if mode == 'nearest':
            first_discard = discarded[0]
            if first_discard == '0':
                return int_bits, kept
            if len(discarded) > 1 and any(ch == '1' for ch in discarded[1:]):
                return increment_fraction(int_bits, kept)
            if kept and kept[-1] == '1':
                return increment_fraction(int_bits, kept)
            return int_bits, kept

        raise ValueError("Unknown rounding mode")

    if bits == 0:
        return (
            ('-' if negative else '') + int_part,
            ('-' if negative else '') + int_part,
            ('-' if negative else '') + int_part,
            ('-' if negative else '') + int_part,
        )

    int_bits, frac_bits = round_fraction('trunc', int_part, frac_part)
    trunc_res = format_value(int_bits, frac_bits)

    int_bits, frac_bits = round_fraction('up', int_part, frac_part)
    up_res = format_value(int_bits, frac_bits)

    int_bits, frac_bits = round_fraction('down', int_part, frac_part)
    down_res = format_value(int_bits, frac_bits)

    int_bits, frac_bits = round_fraction('nearest', int_part, frac_part)
    nearest_res = format_value(int_bits, frac_bits)

    return trunc_res, up_res, down_res, nearest_res

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
            num = float(input("Enter a decimal number: "))
            digits = int(input("Enter target significant digits: "))
            # implements rounding methods for decimal input
            chopped, rounded_up, rounded_down, rounded_to_nearest = round_decimal(num, digits)
            print("Chopped:", chopped)
            print("Round-up:", rounded_up)
            print("Round-down:", rounded_down)
            print("Round-to-nearest, ties-to-even:", rounded_to_nearest)

        elif round_choice == '2':
            bin_num = input("Enter a binary number: ")
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

