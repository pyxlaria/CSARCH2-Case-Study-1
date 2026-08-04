# CSARCH2-Case-Study-1
This project is a web-based IEEE 754 calculator built for Google Colab. The interface is intentionally simple, black and white, and focused on the actual outputs rather than visual decoration.

The current implementation covers three main tasks:

Convert a decimal number to IEEE 754 binary64, then display the result in grouped binary and hexadecimal.

Demonstrate rounding for both decimal and binary inputs using chopping, round-up, round-down, and round-to-nearest ties-to-even.

Perform IEEE 754 binary64 arithmetic using the GRS method for addition and multiplication, then show the final binary, hexadecimal, decimal, and step-by-step solution.

Main Features

1. Decimal to IEEE 754 Conversion

Accepts a decimal number.

Converts it to IEEE 754 binary64.

Displays the 64-bit binary output in grouped form.

Displays the hexadecimal equivalent.

2. Rounding Methods

Supports decimal input and signed binary floating-point input.

Shows all four rounding methods:

Chopping

Round-up

Round-down

Round-to-nearest, ties-to-even

3. Arithmetic Using the GRS Method

Accepts operands in decimal or IEEE hexadecimal form.

Supports addition and multiplication.

Shows the full solution flow, including:

Input values

IEEE representation

Exponent alignment

Mantissa handling

GRS rounding

Final binary, hexadecimal, and decimal results

Interface Style

The GUI is designed to stay minimal.

Black and white only

Clean spacing

Separate sections for each task

No extra visual clutter

This keeps the focus on the computation and the output, which is the main requirement of the project.

How to Run in Google Colab

Upload the Python file to your Colab notebook.

Make sure Gradio is installed.

Run the script.

Open the generated Gradio link.

If Gradio is not installed yet, run:

!pip install gradio

Then run the script again.

Example Inputs

Task 1: Decimal to IEEE 754

Example input:

12.75

Expected output:

64-bit IEEE binary64 representation

Hexadecimal form

Task 2: Rounding Methods

Decimal example:

Number: 123.456
Target significant digits: 4

Binary example:

Signed binary input: -110.101101
Target bits: 5

Expected output:

Chopped value

Round-up value

Round-down value

Round-to-nearest, ties-to-even value

Task 3: Arithmetic Using GRS

Example addition:

Operand A format: Decimal
Operand A: 12.5
Operand B format: IEEE Hex
Operand B: 400A000000000000
Operation: +

Example multiplication:

Operand A format: Decimal
Operand A: 6.25
Operand B format: Decimal
Operand B: 2.0
Operation: *

Expected output:

Final 64-bit binary result

Final hexadecimal result

Final decimal result

Step-by-step solution

Project Structure

gradio_colab.py
README.md
screenshots/

The screenshots folder can be used for saved outputs and test case images.

Test Case Documentation Skeleton

Use the template below when adding screenshots to the repository.

Test Case Template

Test Case ID

TC-01

Feature

Decimal to IEEE 754 conversion

Description

Verify that a decimal input is converted to IEEE 754 binary64 and hexadecimal correctly.

Input

12.75

Expected Result

The binary64 representation should appear in grouped binary form.

The hexadecimal value should appear in uppercase.

The output should match the computed IEEE 754 value for the input.

Screenshot

[Insert screenshot here]

Notes

Add any special observation here.

Suggested Test Case List

TC-01 Normal Conversion

Decimal input: a positive number with a fractional part

Example: 12.75

Screenshot: insert here

TC-02 Special Conversion

Decimal input: zero

Example: 0

Screenshot: insert here

TC-03 Edge Conversion

Decimal input: a negative value

Example: -5.5

Screenshot: insert here

TC-04 Decimal Rounding

Decimal input with target significant digits

Example: 123.456 with 4 digits

Screenshot: insert here

TC-05 Binary Rounding

Signed binary input with target bits

Example: -110.101101 with 5 bits

Screenshot: insert here

TC-06 Addition

Decimal operands using the GRS method

Example: 12.5 + 3.25

Screenshot: insert here

TC-07 Multiplication

Decimal operands using the GRS method

Example: 6.25 * 2.0

Screenshot: insert here

TC-08 Hexadecimal Operand Input

Use IEEE hexadecimal input for one or both operands

Example: 400A000000000000 and 3FF0000000000000

Screenshot: insert here

Sample Format for Screenshots Section

You can copy this format for every screenshot entry:

### TC-01
**Feature:** Decimal to IEEE 754 conversion  
**Input:** 12.75  
**Expected Result:** Binary64 and hexadecimal output are displayed  
**Actual Result:** [Insert observation here]  
**Screenshot:** [Insert image here]

Short Project Summary

This project serves as a learning tool for IEEE 754 binary64 representation, rounding behavior, and arithmetic under the GRS method. The Gradio interface makes it easier to test inputs quickly in Colab while keeping the layout clean and minimal.

Files

gradio_colab.py contains the Gradio-based application

README.md contains the project description and test case guide

screenshots/ is the recommended folder for output images
