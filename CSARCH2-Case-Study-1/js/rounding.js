// rounding methods module

const Rounding = {
    // helper to add 1 to the last digit of a decimal string
    incrementDecimal: function(numStr) {
        let hasDot = numStr.includes('.');
        let chars = numStr.replace('.', '').split('');
        let dotPos = hasDot ? numStr.indexOf('.') : numStr.length;
        
        let carry = 1;
        for (let i = chars.length - 1; i >= 0 && carry; i--) {
            let sum = parseInt(chars[i]) + carry;
            chars[i] = (sum % 10).toString();
            carry = Math.floor(sum / 10);
        }
        
        let result = chars.join('');
        if (carry) { result = carry + result; dotPos++; }
        if (hasDot) {
            result = result.substring(0, dotPos) + '.' + result.substring(dotPos);
        }
        return result;
    },

    // applies the 4 rounding methods to a decimal string
    roundDecimal: function(inputStr, targetDigits) {
        inputStr = inputStr.trim();
        let isNeg = inputStr.startsWith('-');
        let absStr = isNeg ? inputStr.substring(1) : inputStr;
        
        if (!absStr.includes('.')) absStr += '.';
        let parts = absStr.split('.');
        let intPart = parts[0] || '0';
        let fracPart = parts[1] || '';
        
        // pad with zeros
        while (fracPart.length <= targetDigits) fracPart += '0';

        let keptFrac = fracPart.substring(0, targetDigits);
        let droppedFrac = fracPart.substring(targetDigits);
        let hasNonZero = /[1-9]/.test(droppedFrac);
        let truncated = targetDigits > 0 ? intPart + '.' + keptFrac : intPart;

        // 1. chopping
        let chopping = isNeg ? '-' + truncated : truncated;

        // 2. round-up (toward +infinity)
        let roundUp = '';
        if (isNeg) {
            roundUp = '-' + truncated;
        } else {
            roundUp = hasNonZero ? this.incrementDecimal(truncated) : truncated;
        }

        // 3. round-down (toward -infinity)
        let roundDown = '';
        if (isNeg) {
            roundDown = hasNonZero ? '-' + this.incrementDecimal(truncated) : '-' + truncated;
        } else {
            roundDown = truncated;
        }

        // 4. round-to-nearest (ties to even)
        let rtne = '';
        let firstDropped = parseInt(droppedFrac[0] || '0');
        let restDropped = droppedFrac.substring(1);
        let hasRest = /[1-9]/.test(restDropped);
        
        if (firstDropped > 5 || (firstDropped === 5 && hasRest)) {
            let r = this.incrementDecimal(truncated);
            rtne = isNeg ? '-' + r : r;
        } else if (firstDropped < 5) {
            rtne = isNeg ? '-' + truncated : truncated;
        } else {
            // exact tie, check last kept digit
            let lastKept = targetDigits > 0 ? keptFrac[keptFrac.length - 1] : intPart[intPart.length - 1];
            if (parseInt(lastKept) % 2 === 0) {
                rtne = isNeg ? '-' + truncated : truncated;
            } else {
                let r = this.incrementDecimal(truncated);
                rtne = isNeg ? '-' + r : r;
            }
        }

        let clean = s => s.endsWith('.') ? s.slice(0, -1) : s;
        return {
            chopping: { display: clean(chopping) },
            roundUp: { display: clean(roundUp) },
            roundDown: { display: clean(roundDown) },
            rtne: { display: clean(rtne) }
        };
    },

    // helper to add 1 to the last bit of a binary string
    addBinaryULP: function(binStr) {
        let hasDot = binStr.includes('.');
        let chars = binStr.replace('.', '').split('');
        let dotPos = hasDot ? binStr.indexOf('.') : binStr.length;
        
        let carry = 1;
        for (let i = chars.length - 1; i >= 0 && carry; i--) {
            let sum = parseInt(chars[i]) + carry;
            chars[i] = (sum % 2).toString();
            carry = Math.floor(sum / 2);
        }
        
        let result = chars.join('');
        if (carry) { result = '1' + result; dotPos++; }
        if (hasDot) {
            result = result.substring(0, dotPos) + '.' + result.substring(dotPos);
        }
        return result;
    },

    // applies the 4 rounding methods to a binary string
    roundBinary: function(inputStr, targetBits) {
        inputStr = inputStr.trim();
        let isNeg = inputStr.startsWith('-');
        let absStr = isNeg ? inputStr.substring(1) : inputStr;
        
        let intPart = '';
        let fracPart = '';
        if (absStr.includes('.')) {
            let parts = absStr.split('.');
            intPart = parts[0];
            fracPart = parts[1];
        } else {
            intPart = absStr;
            fracPart = '';
        }
        
        while (fracPart.length <= targetBits) fracPart += '0';

        let keptFrac = fracPart.substring(0, targetBits);
        let droppedFrac = fracPart.substring(targetBits);
        let hasNonZero = /1/.test(droppedFrac);
        let truncated = targetBits > 0 ? intPart + '.' + keptFrac : intPart;

        // 1. chopping
        let chopping = isNeg ? '-' + truncated : truncated;

        // 2. round-up
        let roundUp = '';
        if (isNeg) {
            roundUp = '-' + truncated;
        } else {
            roundUp = hasNonZero ? this.addBinaryULP(truncated) : truncated;
        }

        // 3. round-down
        let roundDown = '';
        if (isNeg) {
            roundDown = hasNonZero ? '-' + this.addBinaryULP(truncated) : '-' + truncated;
        } else {
            roundDown = truncated;
        }

        // 4. round-to-nearest (ties to even)
        let rtne = '';
        let firstDropped = droppedFrac[0] || '0';
        let restDropped = droppedFrac.substring(1);
        let hasRest = /1/.test(restDropped);
        
        if (firstDropped === '1' && hasRest) {
            let r = this.addBinaryULP(truncated);
            rtne = isNeg ? '-' + r : r;
        } else if (firstDropped === '0') {
            rtne = isNeg ? '-' + truncated : truncated;
        } else {
            let lastKept = keptFrac.length > 0 ? keptFrac[keptFrac.length - 1] : intPart[intPart.length - 1];
            if (lastKept === '0') {
                rtne = isNeg ? '-' + truncated : truncated;
            } else {
                let r = this.addBinaryULP(truncated);
                rtne = isNeg ? '-' + r : r;
            }
        }

        let clean = s => s.endsWith('.') ? s.slice(0, -1) : s;
        return {
            chopping: { display: clean(chopping) },
            roundUp: { display: clean(roundUp) },
            roundDown: { display: clean(roundDown) },
            rtne: { display: clean(rtne) }
        };
    }
};
