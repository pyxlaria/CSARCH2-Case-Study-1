/**
 * Main Web Application Controller (app.js)
 *
 * Handles DOM interaction, tab switching, input parsing,
 * event listeners, and UI rendering.
 */

document.addEventListener('DOMContentLoaded', () => {

    /* ──────────────── Tab Switching Logic ──────────────── */
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    /* ──────────────── Feature 1: IEEE 754 Converter ──────────────── */
    const converterInput = document.getElementById('converter-input');
    const btnConvert = document.getElementById('btn-convert');
    const converterResults = document.getElementById('converter-results');
    const binarySpacedDisplay = document.getElementById('binary-spaced-display');

    function executeConverter() {
        const valStr = converterInput.value.trim();
        let num;

        if (valStr.toLowerCase() === 'infinity' || valStr.toLowerCase() === '+infinity') {
            num = Infinity;
        } else if (valStr.toLowerCase() === '-infinity') {
            num = -Infinity;
        } else if (valStr.toLowerCase() === 'nan') {
            num = NaN;
        } else {
            num = Number(valStr);
        }

        if (valStr !== '' && (isNaN(num) && valStr.toLowerCase() !== 'nan')) {
            alert('Please enter a valid decimal number or special keyword (Infinity, -Infinity, NaN).');
            return;
        }

        const data = IEEE754.fromDecimal(num);

        // Render binary breakdown with colors
        const signBit = data.binary[0];
        const expBits = data.binary.substring(1, 12);
        const mantBits = data.binary.substring(12, 64);

        // Format mantissa into 4-bit nibbles for readability
        const mantNibbles = mantBits.match(/.{1,4}/g).join(' ');

        binarySpacedDisplay.innerHTML = `
            <span class="bit-sign" title="Sign Bit (1 bit)">${signBit}</span>
            <span class="bit-exp" title="Biased Exponent (11 bits)">${expBits}</span>
            <span class="bit-mant" title="Mantissa / Fraction (52 bits)">${mantNibbles}</span>
        `;

        // Update metrics
        document.getElementById('metric-hex').textContent = '0x' + data.hex;
        document.getElementById('metric-type').textContent = capitalize(data.type);
        document.getElementById('metric-sign').textContent = `${data.signChar} (${data.sign})`;
        document.getElementById('metric-biased-exp').textContent = `${data.biasedExponent} (${expBits})`;
        document.getElementById('metric-unbiased-exp').textContent = data.unbiasedExponent;

        converterResults.style.display = 'block';
    }

    btnConvert.addEventListener('click', executeConverter);
    converterInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') executeConverter(); });

    // Initial converter execution
    executeConverter();


    /* ──────────────── Feature 2: Rounding Methods ──────────────── */
    const roundingModeSelect = document.getElementById('rounding-mode-select');
    const roundingInput = document.getElementById('rounding-input');
    const roundingDigits = document.getElementById('rounding-digits');
    const btnRound = document.getElementById('btn-round');
    const roundingResults = document.getElementById('rounding-results');

    function executeRounding() {
        const mode = roundingModeSelect.value;
        const inputStr = roundingInput.value.trim();
        const digits = parseInt(roundingDigits.value, 10);

        if (isNaN(digits) || digits < 0) {
            alert('Please enter a valid non-negative target length.');
            return;
        }

        let result;
        if (mode === 'decimal') {
            if (!/^-?\d*(\.\d+)?$/.test(inputStr)) {
                alert('Please enter a valid decimal string (e.g. 3.14159).');
                return;
            }
            result = Rounding.roundDecimal(inputStr, digits);
        } else {
            if (!/^-?[01]*(\.[01]+)?$/.test(inputStr)) {
                alert('Please enter a valid binary string containing only 0s and 1s (e.g. 1.01011).');
                return;
            }
            result = Rounding.roundBinary(inputStr, digits);
        }

        document.getElementById('res-chopping').textContent = result.chopping.display;
        document.getElementById('res-round-up').textContent = result.roundUp.display;
        document.getElementById('res-round-down').textContent = result.roundDown.display;
        document.getElementById('res-rtne').textContent = result.rtne.display;

        roundingResults.style.display = 'block';
    }

    btnRound.addEventListener('click', executeRounding);
    roundingInput.addEventListener('keydown', (e) => { if (e.key === 'Enter') executeRounding(); });

    // Change sample defaults when mode changes
    roundingModeSelect.addEventListener('change', () => {
        if (roundingModeSelect.value === 'binary') {
            roundingInput.value = '1.010110011';
            roundingDigits.value = '4';
        } else {
            roundingInput.value = '3.1415926535';
            roundingDigits.value = '4';
        }
        executeRounding();
    });

    executeRounding();


    /* ──────────────── Feature 3: GRS Arithmetic ──────────────── */
    const opInputType = document.getElementById('op-input-type');
    const opType = document.getElementById('op-type');
    const operandA = document.getElementById('operand-a');
    const operandB = document.getElementById('operand-b');
    const btnArithmetic = document.getElementById('btn-arithmetic');
    const arithmeticResults = document.getElementById('arithmetic-results');
    const arithBinary = document.getElementById('arith-binary');
    const stepsAccordion = document.getElementById('steps-accordion');

    function executeArithmetic() {
        const inputType = opInputType.value;
        const operation = opType.value;
        const strA = operandA.value.trim();
        const strB = operandB.value.trim();

        let valA, valB;

        if (inputType === 'hex') {
            valA = IEEE754.hexToDouble(strA);
            valB = IEEE754.hexToDouble(strB);
            if (valA === null || valB === null) {
                alert('Please enter valid 16-character IEEE 754 Hexadecimal strings (e.g. 4025000000000000).');
                return;
            }
        } else {
            valA = parseNum(strA);
            valB = parseNum(strB);
            if (isNaN(valA) && strA.toLowerCase() !== 'nan' || isNaN(valB) && strB.toLowerCase() !== 'nan') {
                alert('Please enter valid numbers for both operands.');
                return;
            }
        }

        let resObj;
        if (operation === 'add') {
            resObj = Arithmetic.add(valA, valB);
        } else {
            resObj = Arithmetic.multiply(valA, valB);
        }

        // Render overall metrics
        document.getElementById('arith-dec').textContent = resObj.resultDecimal;
        document.getElementById('arith-hex').textContent = '0x' + resObj.resultHex;

        // Render binary breakdown
        const rawBits = IEEE754.getBits(resObj.resultDecimal);
        const s = rawBits[0];
        const e = rawBits.substring(1, 12);
        const m = rawBits.substring(12, 64).match(/.{1,4}/g).join(' ');

        arithBinary.innerHTML = `
            <span class="bit-sign" title="Sign Bit">${s}</span>
            <span class="bit-exp" title="Exponent">${e}</span>
            <span class="bit-mant" title="Mantissa">${m}</span>
        `;

        // Render step-by-step accordion
        stepsAccordion.innerHTML = '';
        resObj.steps.forEach((step, idx) => {
            const stepEl = document.createElement('div');
            stepEl.className = 'step-item';

            const detailsHtml = step.details.map(d => `<li>${escapeHtml(d)}</li>`).join('');

            stepEl.innerHTML = `
                <div class="step-header">
                    <span>${escapeHtml(step.title)}</span>
                    <span>▼</span>
                </div>
                <div class="step-body">
                    <p>${escapeHtml(step.desc)}</p>
                    <ul class="step-details-list">
                        ${detailsHtml}
                    </ul>
                </div>
            `;

            // Accordion toggle
            const header = stepEl.querySelector('.step-header');
            header.addEventListener('click', () => {
                const body = stepEl.querySelector('.step-body');
                const isVisible = body.style.display !== 'none';
                body.style.display = isVisible ? 'none' : 'block';
                header.querySelector('span:last-child').textContent = isVisible ? '▶' : '▼';
            });

            stepsAccordion.appendChild(stepEl);
        });

        arithmeticResults.style.display = 'block';
    }

    btnArithmetic.addEventListener('click', executeArithmetic);

    opInputType.addEventListener('change', () => {
        if (opInputType.value === 'hex') {
            operandA.value = '4025000000000000'; // 10.5
            operandB.value = '4002000000000000'; // 2.25
        } else {
            operandA.value = '10.5';
            operandB.value = '2.25';
        }
        executeArithmetic();
    });

    executeArithmetic();
});

/* ──────────────── Helper Utilities ──────────────── */
function setConverterPreset(val) {
    document.getElementById('converter-input').value = val;
    document.getElementById('btn-convert').click();
}

function parseNum(str) {
    const s = str.toLowerCase();
    if (s === 'infinity' || s === '+infinity') return Infinity;
    if (s === '-infinity') return -Infinity;
    if (s === 'nan') return NaN;
    return Number(str);
}

function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function escapeHtml(text) {
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
