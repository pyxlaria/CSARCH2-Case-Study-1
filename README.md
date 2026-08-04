# CSARCH2-Case-Study-1
This project is a web-based IEEE 754 calculator designed to run in Google Colab with Gradio as the graphical user interface.

Click this Google Colab link to proceed: https://colab.research.google.com/drive/1GFIvbTctJZK2SGuFbsU7FereZPWzCnd4?usp=sharing

The application covers three main functions. First, it converts a decimal input into IEEE 754 binary64 form and displays the result in grouped binary and hexadecimal output. Second, it demonstrates rounding for both decimal and binary inputs using chopping, round-up, round-down, and round-to-nearest, ties-to-even. Third, it performs IEEE 754 binary64 arithmetic using the GRS method for addition and multiplication, then presents the final binary, hexadecimal, decimal, and step-by-step solution.

## Project Overview

The purpose of this project is to make IEEE 754 operations easier to explore in a browser-based environment. Instead of using a command-line interface, the user interacts with a clean Gradio page that organizes each task into its own section. This is useful for class demonstrations, screenshots, and test case documentation because the interface keeps the input and output fields visible and consistent.

## Interface Style

The interface uses a black and white theme with a modern minimal layout. The visual design avoids decorative elements and unnecessary colors so that the project remains professional and easy to present. Each task is separated into its own section, the spacing is kept clean, and the output areas are large enough to make screenshots clear.

## How to Run in Google Colab

Open the Google Colab notebook using the link above. Once the notebook is open, scroll down and find step 2 (for terminal) or step 3 (for GUI), run the setup cell by simply clicking the run button (usually located at the top left).

Once the app launches, Colab will generate a Gradio link that you can open to access the interface. It is recommended that you click on the live deployment link.

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

The main application file is main.py. The project README is this file, and the screenshots used for testing should be stored in a screenshots/ folder.
