import numpy

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

def main():
    n = float(input("Enter a decimal number: "))
    bin_rep = dec_to_ieee(n)
    # format binary representation into groups of 4
    bin_formatted = f"{bin_rep[0:4]} {bin_rep[4:8]} {bin_rep[8:12]} {bin_rep[12:16]} {bin_rep[16:20]} {bin_rep[20:24]} {bin_rep[24:28]} {bin_rep[28:32]}"
    print(bin_formatted)
    # convert binary to hexadecimal
    hex_rep = hex(int(bin_rep, 2))[2:]
    print(hex_rep)

if __name__ == "__main__": # only activates main function if main is executed directly (just incase)
    main()
