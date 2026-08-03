const Arithmetic = (() => {

    function add(val1, val2) {
        const steps = [];
        const opA = IEEE754.fromDecimal(val1);
        const opB = IEEE754.fromDecimal(val2);

        // unpack operands
        steps.push({ title: "unpack operands", desc: `operand a: sign=${opA.sign}, exp=${opA.biasedExponent}. operand b: sign=${opB.sign}, exp=${opB.biasedExponent}.`, details: [] });

        if (Number.isNaN(val1) || Number.isNaN(val2)) return specialResult("nan", opA, opB, NaN, steps);
        if (!Number.isFinite(val1) || !Number.isFinite(val2)) return specialResult("infinity", opA, opB, val1 + val2, steps);
        if (val1 === 0) return normalResult(val2, steps);
        if (val2 === 0) return normalResult(val1, steps);

        // compare exponents and swap if needed
        let decA = IEEE754.decompose(val1);
        let decB = IEEE754.decompose(val2);
        if (decA.exponent < decB.exponent || (decA.exponent === decB.exponent && decA.mantissa < decB.mantissa)) {
            [decA, decB] = [decB, decA];
        }
        
        const expDiff = decA.exponent - decB.exponent;
        steps.push({ title: "exponent alignment", desc: `base exponent: ${decA.exponent}. shift operand b right by ${expDiff} bits.`, details: [] });

        // shift mantissa b right by expDiff & calculate grs
        let mantB = decB.mantissa;
        let gBit = 0, rBit = 0, sBit = 0;

        if (expDiff > 0) {
            const bitStr = mantB.toString(2).padStart(53, '0');
            if (expDiff <= 53) {
                const shiftedOut = bitStr.slice(-expDiff);
                gBit = parseInt(shiftedOut[0] || '0', 2);
                rBit = parseInt(shiftedOut[1] || '0', 2);
                sBit = shiftedOut.slice(2).includes('1') ? 1 : 0;
                mantB = mantB >> BigInt(expDiff);
            } else {
                gBit = 0; rBit = 0;
                sBit = bitStr.includes('1') ? 1 : 0;
                mantB = 0n;
            }
        }
        steps.push({ title: "calculate grs bits", desc: `g: ${gBit}, r: ${rBit}, s: ${sBit}.`, details: [] });

        // add / subtract mantissas
        const isSubtract = decA.sign !== decB.sign;
        let resSign = decA.sign;
        let extA = decA.mantissa << 3n;
        let extB = (mantB << 3n) | BigInt((gBit << 2) | (rBit << 1) | sBit);
        let resMant = isSubtract ? extA - extB : extA + extB;

        steps.push({ title: `mantissa ${isSubtract ? "subtraction" : "addition"}`, desc: `performed on grs-extended mantissas.`, details: [] });
        if (resMant === 0n) return normalResult(0, steps);

        // normalize result
        let resExp = decA.exponent;
        if (!isSubtract && resMant >= (1n << 56n)) {
            const droppedBit = Number(resMant & 1n);
            resMant = resMant >> 1n;
            resExp++;
            sBit = sBit | rBit | droppedBit;
            rBit = gBit;
            gBit = Number((resMant >> 2n) & 1n);
            steps.push({ title: "normalization (right shift)", desc: `carry out detected. shifted right, incremented exp to ${resExp}.`, details: [] });
        } else if (isSubtract) {
            const targetBit = 1n << 55n;
            while (resMant < targetBit && resMant > 0n) {
                resMant = resMant << 1n;
                resExp--;
            }
            steps.push({ title: "normalization (left shift)", desc: `shifted left to remove leading zeros. exp is ${resExp}.`, details: [] });
        }

        gBit = Number((resMant >> 2n) & 1n);
        rBit = Number((resMant >> 1n) & 1n);
        sBit = Number(resMant & 1n) | sBit;
        let mainMantissa = resMant >> 3n;

        // rounding (rtne)
        let roundUp = false;
        const lsb = Number(mainMantissa & 1n);
        if (gBit === 1 && (rBit === 1 || sBit === 1 || lsb === 1)) roundUp = true;
        steps.push({ title: "rounding (rtne)", desc: `evaluated grs bits. action: ${roundUp ? "round up" : "chop"}.`, details: [] });

        if (roundUp) {
            mainMantissa++;
            if (mainMantissa >= (1n << 53n)) {
                mainMantissa = mainMantissa >> 1n;
                resExp++;
            }
        }

        // assemble final result
        const finalMantissaBits = mainMantissa & ((1n << 52n) - 1n);
        const finalNum = IEEE754.encode(resSign, resExp + IEEE754.BIAS, finalMantissaBits);
        steps.push({ title: "final assembly", desc: `encoded into 64-bit precision. decimal: ${finalNum}`, details: [] });

        return { resultDecimal: finalNum, resultHex: IEEE754.doubleToHex(finalNum), steps };
    }

    function multiply(val1, val2) {
        const steps = [];
        const opA = IEEE754.fromDecimal(val1);
        const opB = IEEE754.fromDecimal(val2);

        steps.push({ title: "unpack operands", desc: `operand a exp: ${opA.unbiasedExponent}, operand b exp: ${opB.unbiasedExponent}`, details: [] });

        if (Number.isNaN(val1) || Number.isNaN(val2)) return specialResult("nan", opA, opB, NaN, steps);
        if ((Math.abs(val1) === 0 && !Number.isFinite(val2)) || (!Number.isFinite(val1) && Math.abs(val2) === 0)) return specialResult("nan", opA, opB, NaN, steps);
        if (!Number.isFinite(val1) || !Number.isFinite(val2)) return specialResult("infinity", opA, opB, val1 * val2, steps);
        if (val1 === 0 || val2 === 0) {
            const resSign = opA.sign ^ opB.sign;
            return normalResult(resSign === 1 ? -0 : 0, steps);
        }

        const decA = IEEE754.decompose(val1);
        const decB = IEEE754.decompose(val2);

        // calculate sign and exponent
        const resSign = decA.sign ^ decB.sign;
        let resExp = decA.exponent + decB.exponent;
        steps.push({ title: "calculate sign & exp", desc: `sign: ${resSign}, exp: ${resExp}`, details: [] });

        // multiply significands
        const product = decA.mantissa * decB.mantissa;
        steps.push({ title: "multiply significands", desc: `performed 53-bit by 53-bit multiplication.`, details: [] });

        // normalize & extract grs
        let normalizedProd = product;
        let isShifted = false;
        if (product >= (1n << 105n)) {
            normalizedProd = product >> 1n;
            resExp++;
            isShifted = true;
        }

        let mainMantissa = normalizedProd >> 52n;
        const remainingBits = normalizedProd & ((1n << 52n) - 1n);
        const remStr = remainingBits.toString(2).padStart(52, '0');

        const gBit = parseInt(remStr[0] || '0', 2);
        const rBit = parseInt(remStr[1] || '0', 2);
        const sBit = remStr.slice(2).includes('1') || (isShifted && (product & 1n) === 1n) ? 1 : 0;
        steps.push({ title: "normalize & extract grs", desc: `g: ${gBit}, r: ${rBit}, s: ${sBit}. exp adjusted to ${resExp}.`, details: [] });

        // rounding (rtne)
        let roundUp = false;
        const lsb = Number(mainMantissa & 1n);
        if (gBit === 1 && (rBit === 1 || sBit === 1 || lsb === 1)) roundUp = true;
        steps.push({ title: "rounding (rtne)", desc: `evaluated grs bits. action: ${roundUp ? "round up" : "chop"}.`, details: [] });

        if (roundUp) {
            mainMantissa++;
            if (mainMantissa >= (1n << 53n)) {
                mainMantissa = mainMantissa >> 1n;
                resExp++;
            }
        }

        const finalMantissaBits = mainMantissa & ((1n << 52n) - 1n);
        const finalNum = IEEE754.encode(resSign, resExp + IEEE754.BIAS, finalMantissaBits);
        steps.push({ title: "final assembly", desc: `encoded into 64-bit precision. decimal: ${finalNum}`, details: [] });

        return { resultDecimal: finalNum, resultHex: IEEE754.doubleToHex(finalNum), steps };
    }

    function specialResult(label, opA, opB, resultVal, steps) {
        steps.push({ title: "special case handling", desc: `result is ${label}`, details: [] });
        return { resultDecimal: resultVal, resultHex: IEEE754.bitsToHex(IEEE754.getBits(resultVal)), steps };
    }

    function normalResult(resultVal, steps) {
        return { resultDecimal: resultVal, resultHex: IEEE754.bitsToHex(IEEE754.getBits(resultVal)), steps };
    }

    return { add, multiply };
})();
