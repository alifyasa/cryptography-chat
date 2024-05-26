async function generatePrivateKey(q) {
  // Generate a secure random private key in the range [1, q-1]
  const array = new Uint8Array(32); // Adjust the byte length as needed
  window.crypto.getRandomValues(array);
  let privateKey = BigInt('0x' + Array.from(array, byte => byte.toString(16).padStart(2, '0')).join(''));
  
  // Ensure privateKey is in the range [1, q-1]
  privateKey = privateKey % (q - BigInt(1)) + BigInt(1);
  return privateKey;
}

function modPow(base, exponent, modulus) {
  let result = BigInt(1);
  base = base % modulus;
  while (exponent > 0) {
    if (exponent % BigInt(2) === BigInt(1)) {
      result = (result * base) % modulus;
    }
    exponent = exponent >> BigInt(1);
    base = (base * base) % modulus;
  }
  return result;
}

async function generateKeys(alpha, p, q) {
  const privateKey = await generatePrivateKey(q);
  const publicKey = modPow(alpha, privateKey, p);
  return { privateKey, publicKey };
}