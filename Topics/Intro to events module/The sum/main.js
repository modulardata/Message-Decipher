const EventEmitter = require('events'); //do not change this line!

const emitter = new EventEmitter();

emitter.on('sum', (firstNum, secondNum) => {
  console.log(`The sum is ${firstNum + secondNum}`);
});

emitter.emit('sum', 1, 4);