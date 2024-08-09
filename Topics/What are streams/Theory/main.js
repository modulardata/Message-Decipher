const { finished } = require("node:stream/promises");
const fs = require("node:fs");

async function run() {
  const stream = fs.createReadStream("file.txt");

  stream.on("data", (chunk) => {
    // Process the chunk (in this example, we're just consuming it)
    console.log(`Received ${chunk.length} bytes of data.`);
  });

  await finished(stream);
  console.log("Stream is finished");
}

run().catch(console.error);