const { Group, Word, Optional, Capture, Choice } = require('./grammar');

module.exports = syntax => (syntax + '\0').split('').reduce(({ stack, word }, c, i) => {
	const top = stack[0];
	/* Word */
	if (/[-\w]/.test(c) || top instanceof Capture && c !== top.closeChar && !/\s/.test(c)) {
		if (word === null) {
			word = new Word();
			top.append(word);
		}
		word.append(c);
		return { stack, word };
	} else if (word) {
		word.close();
	}
	/* Whitespace */
	if (/\s/.test(c)) {
		return { stack, word: null };
	}
	/* Group / Capture */
	const push = x => (stack.unshift(x), top.append(x), null);
	const close = x => {
		if (top.closeChar === x) {
			top.close();
			stack.shift();
			return true;
		} else {
			return false;
		}
	};
	const unexpected = () => new Error(`Unexpected "${c}" at position ${i + 1} in specification ${syntax}`);
	switch (c) {
	case '|':
		if (top instanceof Group) {
			top.endPhrase();
			break;
		}
		throw unexpected();
	case '[':
		push(new Group(true, ']'));
		break;
	case '(':
		push(new Group(false, ')'));
		break;
	case '{':
		push(new Capture('}'));
		break;
	case ']':
	case ')':
	case '}':
		if (close(c)) {
			break;
		}
		throw unexpected();
	case '\0':
		if (stack.length !== 1) {
			throw new Error('Missing close parentheses: ' + stack
				.map(x => x.closeChar)
				.filter(x => x)
				.join(' '));
		}
		top.close();
		return stack.shift();
	default:
		throw unexpected();
	}
	return { stack, word: null };
}, { stack: [new Group(false, '$ROOT')], word: null });
