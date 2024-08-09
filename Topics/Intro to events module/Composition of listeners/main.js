const EventEmitter = require('events'); //do not change this line!

const emitter = new EventEmitter();

emitter.on('more', () => {
    console.log('The second number is less!');
})

emitter.on('less', () => {
    console.log('The first number is less!');
})
emitter.on('comparison', (firstNum, secondNum) => {
    if (firstNum < secondNum) {
        emitter.emit('less');
    } else {
        emitter.emit('more');
    }
});

emitter.emit('comparison', 5, 11);