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

function encodeWithShiftCipher(text, shift) {
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const lowerAlphabet = "abcdefghijklmnopqrstuvwxyz";

    let result = "";

    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (alphabet.includes(char)) {
            const index = (alphabet.indexOf(char) + shift) % alphabet.length;
            result += alphabet[index];
        } else if (lowerAlphabet.includes(char)) {
            const index = (lowerAlphabet.indexOf(char) + shift) % lowerAlphabet.length;
            result += lowerAlphabet[index];
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

                // Prompt for shift number after decoding is done
                const shNumImp = parseInt(input('Enter the shift number: '));
                fs.readFile('message.txt', 'utf8', (err, data) => {
                    if (err) {
                        console.error('Error reading the file:', err);
                        return;
                    }

                    const encodedData = encodeWithShiftCipher(data, shNumImp);
                    console.log('Finished encoding the file');

                    fs.writeFile('encoded-message.txt', encodedData, 'utf8', (err) => {
                        if (err) {
                            console.error('Error writing the file:', err);
                            return;
                        }
                        console.log('Finished writing the file');
                    });
                });
            }
        });
    }
});
