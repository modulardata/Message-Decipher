const fs = require("fs");
function main() {
    const readerStream = fs.createReadStream('./data.txt');
    readerStream.on('data', (chunk) => {
        console.log(chunk.toString());
    })
};
