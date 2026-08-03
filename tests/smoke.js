const fs = require('fs');
const vm = require('vm');

const files = [
  'js/ieee754.js',
  'js/rounding.js',
  'js/arithmetic.js'
];

let code = '';
for (const file of files) {
  code += fs.readFileSync(file, 'utf8') + '\n';
}

code += `
function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function eq(actual, expected, message) {
  if (!Object.is(actual, expected)) {
    throw new Error(\`\${message} | expected \${expected}, got \${actual}\`);
  }
}

eq(IEEE754.doubleToHex(13.625), '402B400000000000', 'doubleToHex should encode 13.625');
eq(IEEE754.bitsToHex(IEEE754.getBits(13.625)), '402B400000000000', 'bitsToHex should match getBits output');

assert(Rounding.roundDecimal('3.14159', 2).rtne.display === '3.14', 'decimal rtne should round 3.14159 to 3.14');
assert(Rounding.roundBinary('1.01011', 4).rtne.display === '1.0110', 'binary rtne should round 1.01011 to 1.0110');

let add = Arithmetic.add(10.5, 2.25);
eq(add.resultDecimal, 12.75, '10.5 + 2.25 should equal 12.75');
eq(add.resultHex, '4029800000000000', '10.5 + 2.25 hex should be correct');

let mul = Arithmetic.multiply(10.5, 2.25);
eq(mul.resultDecimal, 23.625, '10.5 * 2.25 should equal 23.625');
eq(mul.resultHex, '4037A00000000000', '10.5 * 2.25 hex should be correct');

let zeroAdd = Arithmetic.add(0, 1);
eq(zeroAdd.resultDecimal, 1, '0 + 1 should equal 1');
eq(zeroAdd.resultHex, '3FF0000000000000', '0 + 1 hex should be correct');

let infAdd = Arithmetic.add(Infinity, 1);
assert(!Number.isFinite(infAdd.resultDecimal), 'Infinity + 1 should stay infinite');
eq(infAdd.resultHex, '7FF0000000000000', 'Infinity + 1 hex should be +infinity');

console.log('All smoke tests passed.');
`;

vm.runInNewContext(code, { console });
