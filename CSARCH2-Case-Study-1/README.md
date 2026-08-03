# csarch2 case study 1: binary 64-bit floating-point machine

this is a web app for simulating IEEE 754 binary double-precision (64-bit) floating-point operations.

## live deployment and video

- live site: [add link here]
- youtube video: [add link here]

## what it does

1. converts numbers to IEEE 754 double-precision
- turns any decimal number into 64-bit binary (sign, exponent, mantissa).
- gives the hexadecimal value.
- handles zero, infinity, and NaN.

2. demonstrates rounding methods
- shows chopping, round-up, round-down, and round-to-nearest (ties to even).
- works for both decimal and binary formats.

3. arithmetic operations (GRS method)
- adds and multiplies numbers using the guard, round, and sticky (GRS) bits.
- shows a step-by-step breakdown of how the answer is calculated.

## how to run it

since this is just html, css, and javascript, you don't need to install anything.

1. download or clone the repository.
2. open `index.html` in your web browser.

## about IEEE 754 (64-bit)

it uses 64 bits to store a number:
- sign: 1 bit
- exponent: 11 bits (bias is 1023)
- mantissa: 52 bits