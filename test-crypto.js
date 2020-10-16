const crypto = require('crypto');
const fs = require('fs');

const privKey = fs.readFileSync('priv.pem');
const data = fs.readFileSync('requirements.txt');

const signer = crypto.createSign('RSA-SHA256');
signer.write(data);
signer.end();

const signature = signer.sign(privKey, 'base64');

console.log(signature);
