# CSARCH2-Case-Study-1
This project is a web-based IEEE 754 calculator designed to run in Google Colab with Gradio as the graphical user interface.

Click this Google Colab link to proceed: https://colab.research.google.com/drive/1GFIvbTctJZK2SGuFbsU7FereZPWzCnd4?usp=sharing

The application covers three main functions. First, it converts a decimal input into IEEE 754 binary64 form and displays the result in grouped binary and hexadecimal output. Second, it demonstrates rounding for both decimal and binary inputs using chopping, round-up, round-down, and round-to-nearest, ties-to-even. Third, it performs IEEE 754 binary64 arithmetic using the GRS method for addition and multiplication, then presents the final binary, hexadecimal, decimal, and step-by-step solution.

## Project Overview

The purpose of this project is to make IEEE 754 operations easier to explore in a browser-based environment. Instead of using a command-line interface, the user interacts with a clean Gradio page that organizes each task into its own section. This is useful for class demonstrations, screenshots, and test case documentation because the interface keeps the input and output fields visible and consistent.

## Interface Style

The interface uses a black and white theme with a modern minimal layout. The visual design avoids decorative elements and unnecessary colors so that the project remains professional and easy to present. Each task is separated into its own section, the spacing is kept clean, and the output areas are large enough to make screenshots clear.

## How to Run in Google Colab

Open the Google Colab notebook using the link above. Once the notebook is open, run the setup cell by simply clicking the run button (usually located at the top left).

Once the app launches, Colab will generate a Gradio link that you can open to access the interface.

## Main Features

The Decimal to IEEE 754 section accepts a decimal number and converts it into IEEE 754 binary64 form. The output is shown in grouped binary format and in hexadecimal, which makes it easier to verify the bit pattern during testing.

The Rounding Methods section accepts either a decimal number or a signed binary floating-point number. It displays the result of chopping, round-up, round-down, and round-to-nearest, ties-to-even. This section is intended to demonstrate how the same value changes under different rounding rules.

The Arithmetic Using the GRS Method section accepts operands in decimal or IEEE hexadecimal form. It supports addition and multiplication and displays the complete solution flow, including the inputs, IEEE representation, exponent alignment, mantissa processing, GRS rounding, and final binary, hexadecimal, and decimal results.

## Example Inputs and Outputs

For Decimal to IEEE 754 conversion, a sample input is 12.75. The expected output is the IEEE 754 binary64 representation of the value, shown in grouped binary form, together with its hexadecimal equivalent.

For decimal rounding, a sample input is 123.456 with a target of 4 significant digits. The expected output is the chopped value, the round-up value, the round-down value, and the round-to-nearest, ties-to-even value.

For binary rounding, a sample input is -110.101101 with a target of 5 bits. The expected output is the corresponding rounded values under the same four rounding methods.

For arithmetic using the GRS method, a sample addition input is Operand A = 12.5 in decimal, Operand B = 400A000000000000 in IEEE hexadecimal, and Operation = +. A sample multiplication input is Operand A = 6.25 in decimal, Operand B = 2.0 in decimal, and Operation = *.

## Project Structure

The main application file is gradio_colab.py. The project README is this file, and the screenshots used for testing should be stored in a screenshots/ folder.

Test Case Documentation Guide

The only part that should remain incomplete before submission is the screenshot field for each test case. Everything else below is ready to paste into GitHub and can be reused as the documentation format for your screenshots.

Test Case Template

Test Case ID

TC-01

Feature

Decimal to IEEE 754 conversion

Description

This test verifies that a decimal value is converted correctly into IEEE 754 binary64 format and hexadecimal form.

Input

12.75

Expected Result

The output should display the grouped 64-bit binary representation and the uppercase hexadecimal representation that correspond to the input value.

Actual Result

[Insert the actual observed result here]

Screenshot

[Insert screenshot here]

Notes

[Insert any special observation here]

Test Case Skeletons

TC-01 Normal Conversion

Test Case ID

TC-01

Feature

Decimal to IEEE 754 conversion

Description

Verify that a positive decimal number with a fractional part is converted correctly.

Input

12.75

Expected Result

The interface should display the binary64 result in grouped form and the matching hexadecimal value.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-02 Special Conversion

Test Case ID

TC-02

Feature

Decimal to IEEE 754 conversion

Description

Verify the behavior when the input is zero.

Input

0

Expected Result

The interface should display the IEEE 754 representation for zero and the corresponding hexadecimal output.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-03 Edge Conversion

Test Case ID

TC-03

Feature

Decimal to IEEE 754 conversion

Description

Verify the behavior when the input is negative.

Input

-5.5

Expected Result

The interface should display the correct sign bit, binary64 representation, and hexadecimal output.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-04 Decimal Rounding

Test Case ID

TC-04

Feature

Rounding methods for decimal input

Description

Verify the four rounding methods for a decimal number.

Input

123.456
Target significant digits: 4

Expected Result

The interface should display chopped, round-up, round-down, and round-to-nearest, ties-to-even values.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-05 Binary Rounding

Test Case ID

TC-05

Feature

Rounding methods for binary input

Description

Verify the four rounding methods for a signed binary floating-point value.

Input

-110.101101
Target bits: 5

Expected Result

The interface should display chopped, round-up, round-down, and round-to-nearest, ties-to-even values.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-06 Addition Using GRS

Test Case ID

TC-06

Feature

IEEE 754 addition using the GRS method

Description

Verify that two operands can be added correctly and that the step-by-step solution is displayed.

Input

Operand A format: Decimal
Operand A: 12.5
Operand B format: IEEE Hex
Operand B: 400A000000000000
Operation: +

Expected Result

The interface should display the complete solution, including alignment, mantissa processing, GRS rounding, and final outputs in binary, hexadecimal, and decimal form.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-07 Multiplication Using GRS

Test Case ID

TC-07

Feature

IEEE 754 multiplication using the GRS method

Description

Verify that two operands can be multiplied correctly and that the step-by-step solution is displayed.

Input

Operand A format: Decimal
Operand A: 6.25
Operand B format: Decimal
Operand B: 2.0
Operation: *

Expected Result

The interface should display the complete solution, including mantissa multiplication, normalization, GRS rounding, and final outputs in binary, hexadecimal, and decimal form.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]

TC-08 Hexadecimal Operand Input

Test Case ID

TC-08

Feature

Arithmetic with hexadecimal operands

Description

Verify that hexadecimal IEEE 754 operands are accepted and processed correctly.

Input

Operand A format: IEEE Hex
Operand A: 400A000000000000
Operand B format: IEEE Hex
Operand B: 3FF0000000000000
Operation: +

Expected Result

The interface should accept the hexadecimal inputs and display the correct final result with the full solution flow.

Actual Result

[Insert the observed output here]

Screenshot

[Insert screenshot here]
