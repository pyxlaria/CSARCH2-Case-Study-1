import numpy as np
import struct


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
    while frac_part and len(frac_bin) < 60:
        frac_part *= 2
        bit = int(frac_part)
        frac_bin.append(str(bit))
        frac_part -= bit

    # normalize
    exponent = len(int_bin) - 1
    mantissa = int_bin[1:] + ''.join(frac_bin)

    # adjust mantissa to 23 bits
    mantissa = (mantissa + '0' * 52)[:52]

    # exponent with bias (1023)
    exponent_bin = f"{exponent + 1023:11b}"

    # merge into one binary string
    res = sign + exponent_bin + mantissa
    res_full = res + '0' * (64 - len(res))  # pad to 64 bits if necessary

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
    truncated = truncate_dec(float_num, digits)

    # round-up
    rounded_up = round_up_dec(float_num, digits)

    # round-down
    rounded_down = round_down_dec(float_num, digits)

    # round-to-nearest, ties-to-even
    rounded_to_nearest = round_to_nearest_dec(float_num, digits)

    return truncated, rounded_up, rounded_down, rounded_to_nearest

def truncate_bin(int_part, frac_part, len_bin, bits):
    # truncate a signed binary floating point string to a certain number of bits
    if len_bin <= bits:
        return int_part, frac_part  # no truncation needed
    elif len_bin > bits:
        # determine how many bits to keep from integer and fractional parts
        int_len = len(int_part)
        frac_len = len(frac_part)
        if int_len >= bits:
            # keep and truncate only the integer part, add zeros to fill in the rest of the integer part
            res = int_part[:bits]
            if int_len == bits:
                return res, ''
            else:
                res += '0' * (len_bin - bits)
                return res, ''
        else:
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
        if int_len >= bits:
            # keep and round up only the integer part, fill in rest of integer part with zeros
            res = bin(int(int_part[:bits], 2) + 1)[2:].zfill(bits)
            if int_len == bits:
                return res, ''
            else:
                res += '0' * (len_bin - bits)
                return res, ''
        else:
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
        if int_len >= bits:
            # keep and round down only the integer part, fill in rest of integer part with zeros
            res = int_part[:bits]
            if int_len == bits:
                return res, ''
            else:
                res += '0' * (len_bin - bits)
                return res, ''
        else:
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
            # keep and round integer part to nearest, fill in rest of integer part with zeros
            kept = int_part[:bits]

            # if integer bits already match target bits, use discarded fractional bits to decide.
            if int_len == bits:
                if not frac_part or '1' not in frac_part:
                    return kept, ''

                # compare discarded fraction against exactly one-half.
                if frac_part[0] == '1' and '1' not in frac_part[1:]:
                    # exactly half: ties-to-even uses kept LSB parity
                    if int(kept, 2) % 2 == 0:
                        return kept, ''
                    return bin(int(kept, 2) + 1)[2:].zfill(bits), ''

                # greater than half: round up
                if frac_part[0] == '1':
                    return bin(int(kept, 2) + 1)[2:].zfill(bits), ''

                # less than half: round down
                return kept, ''

            # For int_len > bits, use first discarded integer bit and sticky bits.
            first_discarded = int_part[bits]
            sticky_tail = int_part[bits + 1:] + frac_part
            if first_discarded == '0':
                res = kept
            elif '1' in sticky_tail:
                res = bin(int(kept, 2) + 1)[2:].zfill(bits)
            else:
                # exactly half: ties-to-even
                if int(kept, 2) % 2 == 0:
                    res = kept
                else:
                    res = bin(int(kept, 2) + 1)[2:].zfill(bits)

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
    truncated_int, truncated_frac = truncate_bin(int_part, frac_part, len_bin, bits)
    truncated_res = sign + truncated_int + ('.' + truncated_frac if truncated_frac else '')

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

    return truncated_res, rounded_up_res, rounded_down_res, rounded_nearest_res

# ============================================================
# IEEE-754 Arithmetic (GRS Method)
# ============================================================
def multiply_mantissas(mant1, mant2):

    value1 = int(mant1, 2)
    value2 = int(mant2, 2)

    product = value1 * value2

    # Convert back from Q52 fixed-point
    product >>= 52

    result_bits = format(product, "054b")

    print("len =", len(result_bits))
    print(result_bits)

    return result_bits

def normalize_product(mantissa, exponent):
    """
    Normalize a scaled mantissa after multiplication.
    """

    value = int(mantissa, 2)

    # Product >= 2.0
    if value >= (1 << 53):
        value >>= 1
        exponent += 1

    # Product < 1.0
    while value and value < (1 << 52):
        value <<= 1
        exponent -= 1

    mantissa = format(value, "053b")

    guard = "0"
    round_bit = "0"
    sticky = "0"

    return mantissa, exponent, guard, round_bit, sticky

def ieee_multiply(op1, op2):
    """
    Perform IEEE-754 double precision multiplication
    using the GRS method.
    """

    binary1 = decimal_to_ieee_binary64(op1)
    binary2 = decimal_to_ieee_binary64(op2)

    sign1, exp1_bits, mant1, exp1 = extract_ieee_fields(binary1)
    sign2, exp2_bits, mant2, exp2 = extract_ieee_fields(binary2)

    steps = []

    steps.append("INPUTS")
    steps.append(f"Operand A = {op1}")
    steps.append(f"Operand B = {op2}")

    steps.append("")
    steps.append("IEEE REPRESENTATION")
    steps.append(binary1)
    steps.append(binary2)

    result_sign = "0" if sign1 == sign2 else "1"
    exp = exp1 + exp2

    result_mantissa = multiply_mantissas(
        mant1,
        mant2)

    steps.append("")
    steps.append("MANTISSA MULTIPLICATION")

    steps.append(f"Exponent = {exp}")
    steps.append(f"Mantissa = {result_mantissa}")

    steps.append(f"Exponent = {exp}")
    steps.append(f"Mantissa = {result_mantissa}")

    result_mantissa, exp, g, r, s = normalize_product(
    result_mantissa,
    exp)

    steps.append("")
    steps.append("NORMALIZATION")
    steps.append(f"Exponent = {exp}")
    steps.append(f"Mantissa = {result_mantissa}")

    result_mantissa, exp = apply_grs_rounding(
    result_mantissa,
    exp,
    g,
    r,
    s)

    steps.append("")
    steps.append("GRS ROUNDING")
    steps.append(f"Guard  = {g}")
    steps.append(f"Round  = {r}")
    steps.append(f"Sticky = {s}")
    steps.append(f"Rounded Mantissa = {result_mantissa}")
    steps.append(f"Exponent = {exp}")

    binary_result = assemble_ieee_binary64(
    result_sign,
    exp,
    result_mantissa)

    steps.append("")
    steps.append("FINAL IEEE-754 BINARY")
    steps.append(binary_result)

    hex_result = binary64_to_hex(binary_result)

    steps.append("")
    steps.append("HEXADECIMAL")
    steps.append(hex_result)

    decimal_result = ieee_binary64_to_decimal(binary_result)

    steps.append("")
    steps.append("DECIMAL")
    steps.append(str(decimal_result))

    return (
        binary_result,
        hex_result,
        decimal_result,
        steps)


def add_mantissas(sign1, mant1, sign2, mant2):
    """
    Add or subtract two aligned mantissas depending on their signs.

    Returns:
        result_sign
        result_mantissa
    """

    value1 = int(mant1, 2)
    value2 = int(mant2, 2)

    # Same sign → addition
    if sign1 == sign2:
        result = value1 + value2
        result_sign = sign1

    # Different signs → subtraction
    else:
        if value1 >= value2:
            result = value1 - value2
            result_sign = sign1
        else:
            result = value2 - value1
            result_sign = sign2

    result_bits = format(result, "b")

    return result_sign, result_bits

def normalize_result(mantissa, exponent):
    """
    Normalize a binary mantissa after addition/subtraction.

    Returns:
        normalized_mantissa
        updated_exponent
    """

    # Zero result
    if int(mantissa, 2) == 0:
        return "0", -1023

    # Carry after addition
    if len(mantissa) > 53:
        mantissa = mantissa[:-1]
        exponent += 1

    # Left-normalize after subtraction
    else:
        while len(mantissa) < 53 or mantissa[0] != "1":
            mantissa = mantissa[1:] + "0"
            exponent -= 1

    return mantissa, exponent

def apply_grs_rounding(mantissa, exponent, guard, round_bit, sticky):
    """
    Apply Guard-Round-Sticky (GRS) rounding using
    round-to-nearest, ties-to-even.

    Returns:
        rounded_mantissa
        updated_exponent
    """

    # Round if:
    # G = 1 and
    # (R = 1 or S = 1 or LSB is odd)

    lsb = mantissa[-1]

    should_round = (
        guard == "1" and
        (
            round_bit == "1" or
            sticky == "1" or
            lsb == "1"
        )
    )

    if should_round:

        value = int(mantissa, 2) + 1

        mantissa = format(value, "b")

        # Overflow after rounding
        if len(mantissa) > 53:
            mantissa = mantissa[:-1]
            exponent += 1

    return mantissa, exponent

def assemble_ieee_binary64(sign, exponent, mantissa):
    """
    Assemble the final IEEE-754 double precision binary.

    mantissa includes the hidden leading 1.
    """

    # Special case: zero
    if int(mantissa, 2) == 0:
        return sign + ("0" * 63)

    biased = exponent + 1023

    exponent_bits = f"{biased:011b}"

    fraction = mantissa[1:]

    fraction = fraction.ljust(52, "0")[:52]

    return sign + exponent_bits + fraction

def binary64_to_hex(binary):
    return f"{int(binary,2):016X}"

def ieee_binary64_to_decimal(binary):
    integer = int(binary,2)

    packed = struct.pack(">Q", integer)

    return struct.unpack(">d", packed)[0]

def ieee_add(op1, op2):
    """
    Perform IEEE-754 double precision addition
    using the GRS method.

    Returns:
        binary_result
        hexadecimal_result
        decimal_result
        steps
    """
    binary1 = decimal_to_ieee_binary64(op1)
    binary2 = decimal_to_ieee_binary64(op2)
    sign1, exp1_bits, mant1, exp1 = extract_ieee_fields(binary1)
    sign2, exp2_bits, mant2, exp2 = extract_ieee_fields(binary2)

    steps = []
    steps.append("INPUTS")

    steps.append(f"Operand A = {op1}")
    steps.append(f"Operand B = {op2}")

    steps.append("")
    steps.append("IEEE REPRESENTATION")

    steps.append(binary1)
    steps.append(binary2)

    exp, mant1, mant2, g, r, s = align_exponents(
    exp1,
    mant1,
    exp2,
    mant2)

    steps.append("")
    steps.append("EXPONENT ALIGNMENT")

    steps.append(f"Aligned exponent = {exp}")

    steps.append(f"Mantissa A = {mant1}")
    steps.append(f"Mantissa B = {mant2}")

    steps.append(f"G={g} R={r} S={s}")

    result_sign, result_mantissa = add_mantissas(
    sign1,
    mant1,
    sign2,  
    mant2)

    result_mantissa, exp = normalize_result(
    result_mantissa,
    exp)

    result_mantissa, exp = apply_grs_rounding(
    result_mantissa,
    exp,
    g,
    r,
    s)

    steps.append("")
    steps.append("NORMALIZATION")

    steps.append(f"Exponent = {exp}")
    steps.append(f"Mantissa = {result_mantissa}")

    steps.append("")
    steps.append("MANTISSA RESULT")
    steps.append(result_mantissa)

    steps.append("")
    steps.append("GRS ROUNDING")

    steps.append(f"Guard  = {g}")
    steps.append(f"Round  = {r}")
    steps.append(f"Sticky = {s}")

    steps.append(f"Rounded Mantissa = {result_mantissa}")
    steps.append(f"Exponent = {exp}")

    binary_result = assemble_ieee_binary64(
    result_sign,
    exp,
    result_mantissa)

    steps.append("")
    steps.append("FINAL IEEE-754 BINARY")
    steps.append(binary_result)

    hex_result = binary64_to_hex(binary_result)

    steps.append("")
    steps.append("HEXADECIMAL")
    steps.append(hex_result)

    decimal_result = ieee_binary64_to_decimal(binary_result)

    steps.append("")
    steps.append("DECIMAL")
    steps.append(str(decimal_result))

    return (
    binary_result,
    hex_result,
    decimal_result,
    steps)

def extract_ieee_fields(binary64):
    """
    Extract the IEEE-754 single precision fields from a 32-bit binary string.

    Returns:
        sign        : '0' or '1'
        exponent    : exponent bits (8 bits)
        mantissa    : mantissa INCLUDING the hidden leading bit
        unbiased_exp: exponent value without bias
    """

    if len(binary64) != 64:
        raise ValueError("IEEE binary must contain exactly 64 bits.")

    sign = binary64[0]
    exponent = binary64[1:12]
    fraction = binary64[12:]

    exponent_value = int(exponent, 2)

    # Special case: subnormal numbers
    if exponent_value == 0:
        hidden_bit = "0"
        unbiased_exp = -1022

    else:
        hidden_bit = "1"
        unbiased_exp = exponent_value - 1023

    mantissa = hidden_bit + fraction

    return sign, exponent, mantissa, unbiased_exp

def align_exponents(exp1, mant1, exp2, mant2):
    """
    Align two mantissas by shifting the one with the smaller exponent.

    Returns:
        exponent
        aligned_mantissa1
        aligned_mantissa2
        guard
        round_bit
        sticky
    """

    guard = "0"
    round_bit = "0"
    sticky = "0"

    # Ensure exp1 >= exp2
    if exp2 > exp1:
        exp1, exp2 = exp2, exp1
        mant1, mant2 = mant2, mant1

    shift = exp1 - exp2

    if shift == 0:
        return exp1, mant1, mant2, guard, round_bit, sticky

    mant2 = list(mant2)

    for i in range(shift):

        # Bit shifted out
        shifted = mant2.pop()

        # Sticky accumulates everything after Round
        if guard == "1":
            sticky = "1" if (sticky == "1" or round_bit == "1") else "0"

        round_bit = guard
        guard = shifted

        # Shift right
        mant2.insert(0, '0')

    return exp1, mant1, ''.join(mant2), guard, round_bit, sticky

def decimal_to_ieee_binary64(value):
    """
    Convert a Python float into an IEEE-754 double-precision
    64-bit binary string.
    """

    packed = struct.pack(">d", float(value))
    integer = struct.unpack(">Q", packed)[0]

    return f"{integer:064b}"

def ieee_binary_to_decimal(binary64):
    """
    Convert a 64-bit IEEE binary string back to decimal.
    """

    integer = int(binary64, 2)

    packed = struct.pack(">Q", integer)

    return struct.unpack(">d", packed)[0]

if __name__ == "__test__":
    binary = decimal_to_ieee_binary64(12.75)

    s, e, m, exp = extract_ieee_fields(binary)

    print("Sign:", s)
    print("Exponent:", e)
    print("Mantissa:", m)
    print("Exponent Value:", exp)

def main():
    choice = input("Choose a task:\n1. Decimal → IEEE 754 Double\n2. Rounding Methods\n3. Arithmetic (GRS Method)\nEnter 1, 2, or 3: ")

    if choice == '1':
        n = float(input("Enter a decimal number: "))
        bin_rep = decimal_to_ieee_binary64(n)
        # format binary representation into groups of 4
        

        bin_formatted = " ".join(
        bin_rep[i:i+4] for i in range(0, len(bin_rep), 4)
        )
        print(bin_formatted)

        # convert binary to hexadecimal
        hex_rep = binary64_to_hex(bin_rep)
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
            truncated, rounded_up, rounded_down, rounded_to_nearest = round_decimal(num, digits)
            print("Truncated:", truncated)
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
            truncated, round_up, round_down, round_nearest = round_binary(bin_num, bits)
            print("Truncated:", truncated)
            print("Round-up:", round_up)
            print("Round-down:", round_down)
            print("Round-to-nearest, ties-to-even:", round_nearest)

    elif choice == '3':
        # -----------------------------
        # Operand A
        # -----------------------------
        fmt1 = input("Operand A format (D=Decimal, H=IEEE Hex): ").strip().upper()

        if fmt1 == "D":
            op1 = float(input("Operand A: "))

        elif fmt1 == "H":
            hex1 = input("Operand A: ").strip()
            binary = f"{int(hex1,16):064b}"
            op1 = ieee_binary64_to_decimal(binary)

        else:
            print("Invalid format.")
            return


        # -----------------------------
        # Operand B
        # -----------------------------
        fmt2 = input("Operand B format (D=Decimal, H=IEEE Hex): ").strip().upper()

        if fmt2 == "D":
            op2 = float(input("Operand B: "))

        elif fmt2 == "H":
            hex2 = input("Operand B: ").strip()
            binary = f"{int(hex2,16):064b}"
            op2 = ieee_binary64_to_decimal(binary)

        else:
            print("Invalid format.")
            return


        operation = input("Operation (+ or *): ").strip()

        if operation == "+":
            binary_result, hex_result, decimal_result, steps = ieee_add(op1, op2)

        elif operation == "*":
            binary_result, hex_result, decimal_result, steps = ieee_multiply(op1, op2)

        else:
            print("Invalid operation.")
            return

        print("\n========== SOLUTION ==========\n")

        for line in steps:
            print(line)

        print("\n========== FINAL ANSWER ==========\n")

        print("Binary:")
        print(binary_result)

        print()

        print("Hexadecimal:")
        print(hex_result)

        print()

        print("Decimal:")
        print("Binary:")
        print(" ".join(binary_result[i:i+4] for i in range(0, len(binary_result), 4)))        

    if __name__ == "__main__": # only activates main function if main is executed directly (just incase)
        main()
