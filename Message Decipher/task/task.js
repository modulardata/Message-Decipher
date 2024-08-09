const input = require('sync-input');
const fs = require('fs');

function atbashCipher(text) {
	const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	const reversedAlphabet = "ZYXWVUTSRQPONMLKJIHGFEDCBA";
	const lowerAlphabet = "abcdefghijklmnopqrstuvwxyz";
	const reversedLowerAlphabet = "zyxwvutsrqponmlkjihgfedcba";

	let result = "";

	for (let i = 0; i < text.length; i++) {
		const char = text[i];
		if (alphabet.includes(char)) {
			result += reversedAlphabet[alphabet.indexOf(char)];
		} else if (lowerAlphabet.includes(char)) {
			result += reversedLowerAlphabet[lowerAlphabet.indexOf(char)];
		} else {
			result += char;
		}
	}

	return result;
}

fs.readFile('secret-message.txt', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
    } else {
        data = atbashCipher(data);
        console.log('Finished decoding the file');

        fs.writeFile('decoded-message.txt', data, 'utf8', (err) => {
            if (err) {
                console.error('Error writing the file:', err);
            } else {
                console.log('Finished writing the file');
            }
        });
    }
});

