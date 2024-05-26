class EllipticCurve {
    constructor(a, b, x, y, p, n) {
        this.a = a;
        this.b = b;
        this.G = {
            x,
            y
        }
        this.p = p; // Prime number for modular arithmetic
        this.n = n;
    }

    // Adding two points on the curve
    add(point1, point2) {

        if (point1 === null) return point2;
        if (point2 === null) return point1;

        const { x: x1, y: y1 } = point1;
        const { x: x2, y: y2 } = point2;

        if (x1 === x2 && y1 === y2) {
            return this.double(point1);
        }

        const m = this.mod(((y2 - y1) * this.modInverse(x2 - x1, this.p)));
        const x3 = this.mod(this.mod(m * m) - x1 - x2);
        const y3 = (m * (x1 - x3) - y1) % this.p;
        return { x: this.mod(x3), y: this.mod(y3) };
    }

    // Doubling a point on the curve
    double(point) {
        const { x: x1, y: y1 } = point;

        const m = this.mod((3 * x1 * x1 + this.a) * this.modInverse(2 * y1, this.p));
        const x3 = this.mod(this.mod(m * m) - 2 * x1);
        const y3 = (m * (x1 - x3) - y1) % this.p;
        return { x: this.mod(x3), y: this.mod(y3) };
    }

    // Scalar multiplication of a point on the curve
    multiply(point, scalar) {
        let result = null;
        let addend = point;

        while (scalar > 0) {
            if (scalar & 1) {
                result = this.add(result, addend);
            }
            addend = this.double(addend);
            scalar >>= 1;
        }

        return result;
    }

    // Modular Inverse using Extended Euclidean Algorithm
    modInverse(a, m) {
        // validate inputs
        [a, m] = [Number(a), Number(m)]
        if (Number.isNaN(a) || Number.isNaN(m)) {
            return NaN // invalid input
        }
        a = (a % m + m) % m
        if (!a || m < 2) {
            return NaN // invalid input
        }
        // find the gcd
        const s = []
        let b = m
        while (b) {
            [a, b] = [b, a % b]
            s.push({ a, b })
        }
        if (a !== 1) {
            return NaN // inverse does not exists
        }
        // find the inverse
        let x = 1
        let y = 0
        for (let i = s.length - 2; i >= 0; --i) {
            [x, y] = [y, x - y * Math.floor(s[i].a / s[i].b)]
        }
        return (y % m + m) % m
    }

    // Ensure values are positive & within the field
    mod(n) {
        return ((n % this.p) + this.p) % this.p;
    }

    findAllPoints() {
        let points = [];
        for (let x = 0; x < this.p; x++) {
            let ySquare = (x ** 3 + this.a * x + this.b) % this.p;
            for (let y = 0; y < this.p; y++) {
                if ((y * y) % this.p === ySquare) {
                    points.push({ x, y });
                }
            }
        }
        // Including the point at infinity, denoted here as null
        points.push(null);
        return points;
    }

    isCurveNonSingular() {
        const leftSide = (4 * Math.pow(this.a, 3) + 27 * Math.pow(this.b, 2)) % this.p;
        return leftSide !== 0;
    }

    invertPoint(point) {
        return {
            x: point.x,
            // Assuming we're working over a finite field, where `fieldSize` is the size of the field.
            // The negation of y in the field can be computed as `fieldSize - y`.
            // If fieldSize is not relevant to your case, you might directly use `-point.y`,
            // but typically you'll be working modulo some prime.
            y: this.mod(- point.y)
        };
    }

    subtract(pointP, pointQ) {
        // First, invert pointQ to get -Q
        const pointQInv = this.invertPoint(pointQ);
        // Then, use the add function to add P and -Q
        return this.add(pointP, pointQInv);
    }
}


// Random generate from new-server/service/randomizer_curve.py
const ECC_CURVE = new EllipticCurve(
    342,
    52,
    73,
    99,
    359,
    360
);

function encodeStringToCurve(string, curve) {
    const curvePoints = curve.findAllPoints();
    return btoa(string)
        .split("").map(c => c.charCodeAt(0)).map(n => curvePoints[n % curvePoints.length])
}

function decodePointsToString(points, curve) {
    const curvePoints = curve.findAllPoints();

    const decoded = points
        .map(p => curvePoints.findIndex(cPoint => p.x === cPoint.x && p.y === cPoint.y))
        .map(n => String.fromCharCode(n))
        .join("");

    return atob(decoded)
}

function encryptElement(point, publicKey, k) {
    const C1 = ECC_CURVE.multiply(ECC_CURVE.G, k);
    const S = ECC_CURVE.multiply(publicKey, k);
    const C2 = ECC_CURVE.add(point, S);
    return [C1, C2]
}

function decryptElement(points, privateKey) {
    const [C1, C2] = points;
    const S = ECC_CURVE.multiply(C1, privateKey);
    return ECC_CURVE.subtract(C2, S);
}

function encodeCipherText(ciphertext) {
    return btoa(JSON.stringify(ciphertext));
}

function decodeCipherText(ciphertext) {
    return JSON.parse(atob(ciphertext));
}

function eccEncrypt(string, publicKey) {
    const points = encodeStringToCurve(string, ECC_CURVE)
    const k = Math.floor(Math.random() * (ECC_CURVE.n - 1)) + 1;
    const cipherText = points.map(point => encryptElement(point, publicKey, k))
    return encodeCipherText(cipherText)
}

function eccDecrypt(string, privateKey) {
    const cipherText = decodeCipherText(string)
    const plainText = cipherText.map(points => decryptElement(points, privateKey))
    return decodePointsToString(plainText, ECC_CURVE)
}

function eccGenerateKeys() {
    const privateKey = Math.floor(Math.random() * (ECC_CURVE.n - 1)) + 1;
    const publicKey = ECC_CURVE.multiply(ECC_CURVE.G, privateKey)
    return { privateKey, publicKey }
}

// const { privateKey, publicKey } = eccGenerateKeys()
// const cipherText = eccEncrypt("Halo, Namaku Alif", publicKey)
// const plainText = eccDecrypt(cipherText, privateKey)
// console.log(cipherText, plainText)

export {
    eccGenerateKeys,
    eccEncrypt,
    eccDecrypt
}