const input = require('sync-input');
const fs = require('fs');
fs.readFile('secret-message.txt', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading the file:', err);
        return;
    }
    console.log(data);
    console.log('Finished reading the file');
});
