const EventEmitter = require('events');

const emitter = new EventEmitter();

emitter.on('main', () => {
	console.log('It is main event!');
})

emitter.on('initial', (eventName) => {
	console.log(`It is ${eventName} event!`);
});

emitter.emit('initial', 'main');