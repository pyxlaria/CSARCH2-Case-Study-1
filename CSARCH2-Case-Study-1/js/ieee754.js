// ieee 754 double-precision (64-bit) module

const IEEE754 = (() => {
    // extracts the exact 64-bit binary representation of a javascript number
    function getBits(num) {
        let buf = new ArrayBuffer(8);
        let view = new DataView(buf);
        view.setFloat64(0, num, false);
        let hi = view.getUint32(0, false);
        let lo = view.getUint32(4, false);
        return (hi >>> 0).toString(2).padStart(32, '0') +
               (lo >>> 0).toString(2).padStart(32, '0');
    }

    // parses a 64-bit binary string into its ieee 754 components
    function parseBits(bits) {
        let sign = parseInt(bits[0], 2);
        let expBits = bits.substring(1, 12);
        let mantBits = bits.substring(12, 64);
        let biasedExp = parseInt(expBits, 2);

        let type = 'normalized';
        let unbiasedExp = biasedExp - 1023;

        if (biasedExp === 0 && /^0+$/.test(mantBits)) {
            type = sign === 0 ? '+zero' : '-zero';
            unbiasedExp = 0;
        } else if (biasedExp === 0) {
            type = 'denormalized';
            unbiasedExp = -1022;
        } else if (biasedExp === 2047 && /^0+$/.test(mantBits)) {
            type = sign === 0 ? '+infinity' : '-infinity';
            unbiasedExp = 2047;
        } else if (biasedExp === 2047) {
            type = 'nan';
            unbiasedExp = 2047;
        }

        return {
            sign: sign,
            signChar: sign === 0 ? '+' : '-',
            exponentBits: expBits,
            biasedExponent: biasedExp,
            unbiasedExponent: unbiasedExp,
            mantissaBits: mantBits,
            type: type,
            fullBits: bits
        };
    }

    // converts a decimal number to its full ieee 754 analysis
    function fromDecimal(num) {
        let bits = getBits(num);
        let parsed = parseBits(bits);
        
        let hex = '';
        for (let i = 0; i < 64; i += 4) {
            hex += parseInt(bits.substring(i, i + 4), 2).toString(16).toUpperCase();
        }

        let groups = parsed.mantissaBits.match(/.{1,4}/g).join(' ');
        let formatted = `${bits[0]} ${parsed.exponentBits} ${groups}`;

        return {
            ...parsed,
            decimalValue: num,
            binary: bits,
            binaryFormatted: formatted,
            hex: hex
        };
    }

    // converts a 16-character ieee 754 hex string to a javascript number
    function hexToDouble(hexStr) {
        hexStr = hexStr.replace(/^0x/i, '').replace(/\s/g, '').toUpperCase();
        if (hexStr.length !== 16) return null;

        let buf = new ArrayBuffer(8);
        let view = new DataView(buf);
        view.setUint32(0, parseInt(hexStr.substring(0, 8), 16), false);
        view.setUint32(4, parseInt(hexStr.substring(8, 16), 16), false);
        return view.getFloat64(0, false);
    }

    // converts a javascript number to its 16-character hex representation
    function doubleToHex(num) {
        let bits = getBits(num);
        let hex = '';
        for (let i = 0; i < 64; i += 4) {
            hex += parseInt(bits.substring(i, i + 4), 2).toString(16).toUpperCase();
        }
        return hex;
    }

    // converts a raw 64-bit binary string into its 16-character hex representation
    function bitsToHex(bits) {
        bits = String(bits).replace(/\s/g, '');
        if (bits.length !== 64) return null;

        let hex = '';
        for (let i = 0; i < 64; i += 4) {
            hex += parseInt(bits.substring(i, i + 4), 2).toString(16).toUpperCase();
        }
        return hex;
    }

    // breaks a number down into sign, bigint mantissa, and exponent
    function decompose(num) {
        let bits = getBits(num);
        let sign = parseInt(bits[0], 2);
        let bExp = parseInt(bits.substring(1, 12), 2);
        let mantissa = BigInt('0b' + bits.substring(12, 64));

        if (bExp === 0 && mantissa === 0n) return { sign, mantissa: 0n, exponent: 0, type: 'zero' };
        if (bExp === 0) return { sign, mantissa, exponent: -1022, type: 'denormalized' };
        if (bExp === 2047 && mantissa === 0n) return { sign, mantissa: 0n, exponent: 0, type: 'infinity' };
        if (bExp === 2047) return { sign, mantissa, exponent: 0, type: 'nan' };

        return {
            sign,
            mantissa: (1n << 52n) | mantissa,
            exponent: bExp - 1023,
            type: 'normalized'
        };
    }

    // packs ieee 754 components back into a javascript number
    function encode(sign, biasedExponent, mantissa) {
        let s = sign.toString();
        let e = biasedExponent.toString(2).padStart(11, '0');
        let m = mantissa.toString(2).padStart(52, '0');
        let bits = s + e + m;

        let buf = new ArrayBuffer(8);
        let view = new DataView(buf);
        view.setUint32(0, parseInt(bits.substring(0, 32), 2), false);
        view.setUint32(4, parseInt(bits.substring(32, 64), 2), false);
        return view.getFloat64(0, false);
    }

    return {
        getBits,
        fromDecimal,
        hexToDouble,
        doubleToHex,
        bitsToHex,
        decompose,
        encode,
        BIAS: 1023
    };
})();
