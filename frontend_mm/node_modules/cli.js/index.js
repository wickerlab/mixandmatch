const cli = require('./cli');

module.exports = cli;

/* Call with no arguments to run as terminal / execute command-line args */
if (!module.parent) {
	cli();
}
