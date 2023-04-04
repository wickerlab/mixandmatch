module.exports = {
	Group, Word, Capture
};

/*
 * match: token -> words ->
 *   case token?
 *     word take 1 words: [{ taken: 1 }]
 *     capture name: [{ taken: 1, capture: { [name]: take 1 words } }]
 *     group phrases: concat map map match phrases words
 *     phrase tokens: consume tokens words 0 {} false
 *   default: [{ taken: 0, failed: true }]
 *
 * consume: tokens -> words -> prev ->
 *   prev.failed: [prev]
 *   no tokens: [prev]
 *   default:
 *     concat
 *       map
 *         m ->
 *           m.failed: [merge prev m]
 *           default: consume drop 1 tokens words merge prev m
 *         match take 1 tokens drop prev.taken words
 */

const $ = c => `\x1b[35m${c}\x1b[0m`;

const concat = xs => [].concat(...xs.filter(Array.isArray));

/* Contains array of Group/Word/Capture */
function Phrase(tokens) {
	tokens = tokens.slice();

	const merge = (x, y) => ({
		taken: x.taken + y.taken,
		capture: concat([x.capture, y.capture]),
		failed: x.failed || y.failed
	});

	const consume = (tokens, words, prev) =>
		prev.failed ? [prev] :
		tokens.length === 0 ? [prev] :
		concat(
			tokens[0].match(words.slice(prev.taken))
				.map(m =>
					m.failed ? [merge(prev, m)] :
					consume(tokens.slice(1), words, merge(prev, m))));

	this.match = expr =>
		consume(tokens, expr, { taken: 0, capture: [], failed: false });

	this.toHelp = () => tokens.map(t => t.toHelp()).join(' ');
}

/* Contains array of Phrase */
function Group(optional, closeChar) {
	const sub = [];
	const phrases = [];

	const isRoot = closeChar === '$ROOT';

	this.closeChar = closeChar;

	this.append = x => sub.push(x);
	this.close = () => {
		this.endPhrase();
		if (optional) {
			this.endPhrase();
		}
		delete this.closeChar;
		delete this.append;
		delete this.close;
		delete this.endPhrase;
		if (sub.length) {
			throw new Error('Subexpression not closed');
		}
		return this;
	};

	this.optional = optional;
	this.choice = false;

	this.endPhrase = () => {
		phrases.push(new Phrase(sub));
		sub.length = 0;
		this.choice = phrases.length > (this.optional ? 2 : 1);
	};

	this.match = expr =>
		concat(phrases.map(phrase => phrase.match(expr)));

	this.toHelp = () => this.optional ?
		this.choice ?
			$('[ ') + phrases.slice(0, phrases.length - 1).map(c => c.toHelp()).join($(' | ')) + $(' ]') :
			$('[') + phrases.slice(0, phrases.length - 1).map(c => c.toHelp()).join($('|')) + $(']') :
		this.choice ?
			(isRoot ? '' : $('{ ')) + phrases.map(c => c.toHelp()).join($(' | ')) + (isRoot ? '' : $(' }')) :
			(isRoot ? '' : $('{')) + phrases.map(c => c.toHelp()).join($('|')) + (isRoot ? '' : $('}'));
}

/* Contains a character string */
function Word() {
	let word = '';

	this.append = c => word = word + c;

	this.match = expr =>
		expr.length === 0 || word.toLowerCase() !== expr[0].toLowerCase() ?
			[{ taken: 0, capture: [], failed: true }] :
			[{ taken: 1, capture: [], failed: false }];

	this.close = () => {
		delete this.append;
		delete this.close;
	};

	this.toString = () => word;

	this.toHelp = () => `\x1b[37m${word}\x1b[0m`;
}

/* Contains one or more Word, specifying the name of the group */
function Capture(closeChar) {
	const sub = [];
	let name = null;

	this.closeChar = closeChar;

	this.append = x => {
		if (!(x instanceof Word)) {
			throw new Error('"Capture" may only contain "Word"');
		}
		sub.push(x);
	};
	this.close = (delim = '_') => {
		if (sub.length === 0) {
			throw new Error('Capture group has no name');
		}
		name = sub.join(delim);
		delete this.closeChar;
		delete this.append;
		delete this.close;
	};

	this.match = expr =>
		expr.length === 0 ?
			[{ taken: 0, capture: [], failed: true }] :
			[{ taken: 1, capture: [[name, expr[0]]], failed: false }];

	this.toHelp = () => `\x1b[36;4m${sub.join(' ')}\x1b[0m`;
}
