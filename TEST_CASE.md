# Test Documentation — Machine 3: Binary 64-bit Floating-Point Machine

## Purpose
This document captures test cases for **Machine 3**, covering all three required processes:

1. Decimal → IEEE 754 binary double-precision conversion (binary + hex output, including special cases)
2. Rounding methods (chopping, round-up, round-down, round-to-nearest ties-to-even) for both decimal and signed binary input
3. IEEE-754 arithmetic (addition and multiplication) using the Guard-Round-Sticky (GRS) method

Each test case lists the **Input**, the **Expected Output** (the mathematically/IEEE-754-correct result), the **Actual Output** (what the program produced when run), a **Pass/Fail** verdict, and a placeholder for a screenshot of the program run.


## 1. Decimal → IEEE 754 Double-Precision Conversion

Covers normal positive/negative values, positive/negative zero, the smallest subnormal, the largest finite double, and the three IEEE special values (±∞, NaN).


### Test Case 1.1 — Normal positive decimal

**Input:** `12.75`

**Expected Output:**
```
Binary: 0100 0000 0010 1001 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    4029800000000000
```
**Actual Output:**
```
Binary: 0100 0000 0010 1001 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    4029800000000000
```
**Result:** PASS

**Screenshot:**

<img width="529" height="467" alt="image" src="https://github.com/user-attachments/assets/e5955ec3-0a81-4e84-9177-7972986c61be" />



---

### Test Case 1.2 — Normal negative decimal

**Input:** `-0.1`

**Expected Output:**
```
Binary: 1011 1111 1011 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1010
Hex:    BFB999999999999A
```
**Actual Output:**
```
Binary: 1011 1111 1011 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1001 1010
Hex:    BFB999999999999A
```
**Result:** PASS

**Screenshot:**

<img width="516" height="459" alt="image" src="https://github.com/user-attachments/assets/fc44ccd7-8ac3-4540-b6e6-0cf2ba294f3c" />


---

### Test Case 1.3 — Special case — positive zero

**Input:** `0.0`

**Expected Output:**
```
Binary: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    0000000000000000
```
**Actual Output:**
```
Binary: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    0000000000000000
```
**Result:** PASS

**Screenshot:**

<img width="534" height="469" alt="image" src="https://github.com/user-attachments/assets/fb0c4fd3-57a7-4705-9377-92b90e3c2580" />


---

### Test Case 1.4 — Special case — negative zero

**Input:** `-0.0`

**Expected Output:**
```
Binary: 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    8000000000000000
```
**Actual Output:**
```
Binary: 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    8000000000000000
```
**Result:** PASS

**Screenshot:**

<img width="513" height="461" alt="image" src="https://github.com/user-attachments/assets/8216adf3-a054-47ed-b186-e5b6cd1ca836" />


---

### Test Case 1.5 — Edge case — smallest positive subnormal

**Input:** `5e-324`

**Expected Output:**
```
Binary: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001
Hex:    0000000000000001
```
**Actual Output:**
```
Binary: 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0001
Hex:    0000000000000001
```
**Result:** PASS

**Screenshot:**

<img width="522" height="462" alt="image" src="https://github.com/user-attachments/assets/4bb1624f-44f5-48a3-a36a-bae42d341959" />


---

### Test Case 1.6 — Edge case — largest finite double (DBL_MAX)

**Input:** `1.7976931348623157e+308`

**Expected Output:**
```
Binary: 0111 1111 1110 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111
Hex:    7FEFFFFFFFFFFFFF
```
**Actual Output:**
```
Binary: 0111 1111 1110 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111 1111
Hex:    7FEFFFFFFFFFFFFF
```
**Result:** PASS

**Screenshot:**

<img width="530" height="469" alt="image" src="https://github.com/user-attachments/assets/710012b2-d3ac-4e11-baad-77657206f247" />


---

### Test Case 1.7 — Special case — positive infinity

**Input:** `inf`

**Expected Output:**
```
Binary: 0111 1111 1111 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    7FF0000000000000
```
**Actual Output:**
```
Binary: 0111 1111 1111 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    7FF0000000000000
```
**Result:** PASS

**Screenshot:**

<img width="525" height="466" alt="image" src="https://github.com/user-attachments/assets/86fc5aac-66be-449e-b1be-1ec66e0548ee" />


---

### Test Case 1.8 — Special case — negative infinity

**Input:** `-inf`

**Expected Output:**
```
Binary: 1111 1111 1111 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    FFF0000000000000
```
**Actual Output:**
```
Binary: 1111 1111 1111 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    FFF0000000000000
```
**Result:** PASS

**Screenshot:**

<img width="530" height="469" alt="image" src="https://github.com/user-attachments/assets/efe5d7be-cadd-4b01-8da9-e9f5da5ae3f0" />


---

### Test Case 1.9 — Special case — Not-a-Number (NaN)

**Input:** `nan`

**Expected Output:**
```
Binary: 0111 1111 1111 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    7FF8000000000000
```
**Actual Output:**
```
Binary: 0111 1111 1111 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:    7FF8000000000000
```
**Result:** PASS

**Screenshot:**

<img width="523" height="463" alt="image" src="https://github.com/user-attachments/assets/37887f6a-7709-44ca-b71f-5f629a4d80b3" />


---


## 2. Rounding Methods

### 2a. Decimal Input

Covers a typical value, a negative value, zero, an exact tie (ties-to-even), and a value whose binary floating-point storage sits just below a round-number boundary.


### Test Case 2.1 — Normal case — typical decimal, 3 sig. digits

**Input:** num=`123.456`, digits=`3`

**Expected Output:**
```
Chopping:            123.0
Round-up:            124.0
Round-down:          123.0
Round-to-nearest(TE): 123.0
```
**Actual Output:**
```
Chopping:            123.0
Round-up:            124.0
Round-down:          123.0
Round-to-nearest(TE): 123.0
```
**Result:** PASS

**Screenshot:**

<img width="455" height="490" alt="image" src="https://github.com/user-attachments/assets/5c417769-c29c-44c0-aadc-e93df7d13864" />


---

### Test Case 2.2 — Normal case — negative decimal, 4 sig. digits

**Input:** num=`-45.6789`, digits=`4`

**Expected Output:**
```
Chopping:            -45.67
Round-up:            -45.67
Round-down:          -45.68
Round-to-nearest(TE): -45.68
```
**Actual Output:**
```
Chopping:            -45.67
Round-up:            -45.67
Round-down:          -45.68
Round-to-nearest(TE): -45.68
```
**Result:** PASS

**Screenshot:**

<img width="441" height="494" alt="image" src="https://github.com/user-attachments/assets/b16f26e8-dcbd-4b30-869c-836b63cc676d" />


---

### Test Case 2.3 — Special case — zero input

**Input:** num=`0`, digits=`3`

**Expected Output:**
```
Chopping:            0
Round-up:            0
Round-down:          0
Round-to-nearest(TE): 0
```
**Actual Output:**
```
Chopping:            0
Round-up:            0
Round-down:          0
Round-to-nearest(TE): 0
```
**Result:** PASS

**Screenshot:**

<img width="443" height="492" alt="image" src="https://github.com/user-attachments/assets/7c91ecbb-0a4e-4238-ae68-15c6ccd79559" />


---

### Test Case 2.4 — Edge case — exact tie (ties-to-even)

**Input:** num=`0.125`, digits=`2`

**Expected Output:**
```
Chopping:            0.12
Round-up:            0.13
Round-down:          0.12
Round-to-nearest(TE): 0.12
```
**Actual Output:**
```
Chopping:            0.12
Round-up:            0.13
Round-down:          0.12
Round-to-nearest(TE): 0.12
```
**Note:** 0.125 rounded to 2 significant digits ties exactly between 0.12 and 0.13; ties-to-even keeps the even digit 2 → 0.12.

**Result:** PASS

**Screenshot:**

<img width="442" height="491" alt="image" src="https://github.com/user-attachments/assets/c1c818cb-891f-4e47-b524-a7765ddf169a" />


---

### Test Case 2.5 — Edge case — value just below a power-of-ten boundary (float representation)

**Input:** num=`9.995`, digits=`3`

**Expected Output:**
```
Chopping:            9.99
Round-up:            10.0
Round-down:          9.99
Round-to-nearest(TE): 9.99
```
**Actual Output:**
```
Chopping:            9.99
Round-up:            10.0
Round-down:          9.99
Round-to-nearest(TE): 9.99
```
**Note:** 9.995 cannot be represented exactly in binary floating point; it is actually stored as 9.99499999999999921840…, so chopping/round-down/nearest correctly give 9.99 while round-up (ceiling) correctly jumps to 10.0.

**Result:** PASS

**Screenshot:**

<img width="441" height="491" alt="image" src="https://github.com/user-attachments/assets/3e919f3c-4d28-48c9-9b5d-510ef253c5d3" />


---


### 2b. Signed Binary Input

Covers a normal fractional value, a negative value with a carry, an exact tie, a value needing no truncation at all, and an edge case that surfaces a real bug in the sign-handling code.


### Test Case 2.6 — Normal case — fractional binary, round up needed

**Input:** binary=`1010.011`, bits=`5`

**Expected Output:**
```
Chopping:            1010.0
Round-up:            1010.1
Round-down:          1010.0
Round-to-nearest(TE): 1010.1
```
**Actual Output:**
```
Chopping:            1010.0
Round-up:            1010.1
Round-down:          1010.0
Round-to-nearest(TE): 1010.1
```
**Result:** PASS

**Screenshot:**

<img width="441" height="491" alt="image" src="https://github.com/user-attachments/assets/fea42407-c7fd-430c-9964-3b4de9605085" />


---

### Test Case 2.7 — Normal case — negative binary with carry on round-down

**Input:** binary=`-110.101`, bits=`4`

**Expected Output:**
```
Chopping:            -110.1
Round-up:            -110.1
Round-down:          -111.0
Round-to-nearest(TE): -110.1
```
**Actual Output:**
```
Chopping:            -110.1
Round-up:            -110.1
Round-down:          -111.0
Round-to-nearest(TE): -110.1
```
**Result:** PASS

**Screenshot:**

<img width="434" height="493" alt="image" src="https://github.com/user-attachments/assets/e4388339-4f17-406e-b845-09dd3fd318b3" />


---

### Test Case 2.8 — Edge case — exact tie (ties-to-even), 1 bit kept

**Input:** binary=`1.1000`, bits=`1`

**Expected Output:**
```
Chopping:            1
Round-up:            10
Round-down:          1
Round-to-nearest(TE): 10
```
**Actual Output:**
```
Chopping:            1
Round-up:            10
Round-down:          1
Round-to-nearest(TE): 10
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 2.9 — Edge case — no rounding needed (len ≤ target bits)

**Input:** binary=`101.1`, bits=`10`

**Expected Output:**
```
Chopping:            101.1
Round-up:            101.1
Round-down:          101.1
Round-to-nearest(TE): 101.1
```
**Actual Output:**
```
Chopping:            101.1
Round-up:            101.1
Round-down:          101.1
Round-to-nearest(TE): 101.1
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 2.10 — Edge case — explicit '+' sign (bug)

**Input:** binary=`+11.01`, bits=`3`

**Expected Output:**
```
Chopping:            +11.0
Round-up:            +11.1
Round-down:          +11.0
Round-to-nearest(TE): +11.1
```
**Actual Output:**
```
Chopping:            +11
Round-up:            100
Round-down:          +11
Round-to-nearest(TE): +11
```
**Note:** round_binary() does not strip a leading '+' sign the way it strips '-'. The '+' character is left attached to the integer part, which throws off the integer-part bit count and produces incorrect, sign-corrupted results ('100' instead of '11.1', etc.). Expected output above is what the unsigned equivalent ('11.01', bits=3) correctly produces. Note the CLI's own input validator (`main()`, choice 2) does not even allow '+' as a character, so this bug is only reachable through the Gradio UI / direct function calls, not the console menu.

**Result:** FAIL

**Screenshot:**

`[Insert screenshot here]`

---


## 3. Arithmetic (Addition and Multiplication) — GRS Method

Covers exact addition, addition that requires guard/round/sticky rounding (this surfaces a real 1-ULP bug), cancellation to zero, exact multiplication, a negative operand, a zero operand, and IEEE-hexadecimal-formatted input.

Each expected value below was independently verified against Python's native IEEE-754 double arithmetic (`a + b` / `a * b`, converted through `struct.pack('>d', ...)`), which is authoritative for binary64.


### Test Case 3.1 — Normal case — exact addition, no rounding

**Input:** A=`12.5` (D), B=`3.25` (D), Operation=`+`

**Expected Output:**
```
Binary:  0100 0000 0010 1111 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     402F800000000000
Decimal: 15.75
```
**Actual Output:**
```
Binary:  0100 0000 0010 1111 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     402F800000000000
Decimal: 15.75
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 3.2 — Edge case — addition requiring GRS rounding (classic 0.1 + 0.2)

**Input:** A=`0.1` (D), B=`0.2` (D), Operation=`+`

**Expected Output:**
```
Binary:  0011 1111 1101 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0100
Hex:     3FD3333333333334
Decimal: 0.30000000000000004
```
**Actual Output:**
```
Binary:  0011 1111 1101 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011 0011
Hex:     3FD3333333333333
Decimal: 0.3
```
**Note:** Correct IEEE-754 double addition of 0.1 + 0.2 rounds to 0x3FD3333333333334 (0.30000000000000004), which is what Python's native '+' operator and struct-based conversion both produce. The program's GRS implementation instead returns 0x3FD3333333333333 (0.3) — off by 1 ULP. This points to a bug in the guard/round/sticky bit bookkeeping during exponent alignment (align_exponents) for this case.

**Result:** FAIL

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 3.3 — Special case — cancellation to exact zero

**Input:** A=`5.0` (D), B=`-5.0` (D), Operation=`+`

**Expected Output:**
```
Binary:  0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     0000000000000000
Decimal: 0.0
```
**Actual Output:**
```
Binary:  0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     0000000000000000
Decimal: 0.0
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 3.4 — Normal case — exact multiplication

**Input:** A=`2.5` (D), B=`4.0` (D), Operation=`*`

**Expected Output:**
```
Binary:  0100 0000 0010 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     4024000000000000
Decimal: 10.0
```
**Actual Output:**
```
Binary:  0100 0000 0010 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     4024000000000000
Decimal: 10.0
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 3.5 — Normal case — negative operand multiplication

**Input:** A=`-3.0` (D), B=`2.0` (D), Operation=`*`

**Expected Output:**
```
Binary:  1100 0000 0001 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     C018000000000000
Decimal: -6.0
```
**Actual Output:**
```
Binary:  1100 0000 0001 1000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     C018000000000000
Decimal: -6.0
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 3.6 — Special case — zero operand (additive identity)

**Input:** A=`0.0` (D), B=`25.75` (D), Operation=`+`

**Expected Output:**
```
Binary:  0100 0000 0011 1001 1100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     4039C00000000000
Decimal: 25.75
```
**Actual Output:**
```
Binary:  0100 0000 0011 1001 1100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     4039C00000000000
Decimal: 25.75
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---

### Test Case 3.7 — Normal case — IEEE hexadecimal input format, multiplication

**Input:** A=`6.5` (0x401A000000000000), B=`1.25` (0x3FF4000000000000), Operation=`*`

**Expected Output:**
```
Binary:  0100 0000 0010 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     4020400000000000
Decimal: 8.125
```
**Actual Output:**
```
Binary:  0100 0000 0010 0000 0100 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000
Hex:     4020400000000000
Decimal: 8.125
```
**Result:** PASS

**Screenshot:**

`[Insert screenshot here]`

---


## Summary

| # | Section | Test Case | Result |
|---|---------|-----------|--------|
| 1 | Decimal to IEEE 754 | 1.1 Normal positive | PASS |
| 2 | Decimal to IEEE 754 | 1.2 Normal negative | PASS |
| 3 | Decimal to IEEE 754 | 1.3 Positive zero | PASS |
| 4 | Decimal to IEEE 754 | 1.4 Negative zero | PASS |
| 5 | Decimal to IEEE 754 | 1.5 Smallest subnormal | PASS |
| 6 | Decimal to IEEE 754 | 1.6 Largest finite double | PASS |
| 7 | Decimal to IEEE 754 | 1.7 +Infinity | PASS |
| 8 | Decimal to IEEE 754 | 1.8 -Infinity | PASS |
| 9 | Decimal to IEEE 754 | 1.9 NaN | PASS |
| 10 | Rounding (decimal) | 2.1 Typical value | PASS |
| 11 | Rounding (decimal) | 2.2 Negative value | PASS |
| 12 | Rounding (decimal) | 2.3 Zero | PASS |
| 13 | Rounding (decimal) | 2.4 Exact tie | PASS |
| 14 | Rounding (decimal) | 2.5 Float-boundary value | PASS |
| 15 | Rounding (binary) | 2.6 Round up needed | PASS |
| 16 | Rounding (binary) | 2.7 Negative with carry | PASS |
| 17 | Rounding (binary) | 2.8 Exact tie | PASS |
| 18 | Rounding (binary) | 2.9 No truncation needed | PASS |
| 19 | Rounding (binary) | 2.10 Leading '+' sign | FAIL (bug) |
| 20 | Arithmetic | 3.1 Exact addition | PASS |
| 21 | Arithmetic | 3.2 0.1 + 0.2 (GRS rounding) | FAIL (bug) |
| 22 | Arithmetic | 3.3 Cancellation to zero | PASS |
| 23 | Arithmetic | 3.4 Exact multiplication | PASS |
| 24 | Arithmetic | 3.5 Negative multiplication | PASS |
| 25 | Arithmetic | 3.6 Zero operand | PASS |
| 26 | Arithmetic | 3.7 Hex input multiplication | PASS |

**24 / 26 test cases passed.** The two failures point to concrete, reproducible bugs (see notes on Test Cases 2.10 and 3.2) rather than test-setup issues.
