const modes = ['partial', 'complete', 'one'];

const zip = (...xs) => {
	const iters = xs.map(x => x[Symbol.iterator]());
	let done = false;
	return {
		[Symbol.iterator]() { return this; },
		next() {
			if (done) {
				return { done };
			}
			const items = iters.map(it => it.next());
			if (items.some(item => item.done)) {
				iters
					.filter(it => typeof it.return === 'function')
					.forEach(it => it.return());
				done = true;
				return { done };
			}
			return { value: items.map(item => item.value) };
		}
	};
};

const same = (a, b) =>
	a.taken === b.taken &&
	a.failed === b.failed &&
	a.capture.size === b.capture.size &&
	[...zip(a.capture, b.capture)]
		.reduce((z, [[k1, v1], [k2, v2]]) => z && k1 === k2 && v1 === v2, true);

const allSame = (x, ...xs) =>
	xs.reduce((r, b) => r && same(x, b), true);

const limit = (res, word_count, mode) => {
	if (!~modes.indexOf(mode)) {
		throw new Error(`Unknown mode: ${mode}`);
	}
	res = res
		.filter(res => mode === 'partial' ? res.taken > 0 : !res.failed)
		.filter(res => mode !== 'one' ? true : res.taken === word_count)
		.map(({ taken, capture, failed }) => ({ taken, capture: new Map(capture), failed }));
	if (mode === 'one') {
		if (res.length === 0) {
			throw new Error('Failed to match expression');
		} else if (res.length > 1) {
			const x = res[0];
			if (!allSame(...res)) {
				throw new Error('Expression is ambiguous');
			}
		}
		return res[0];
	} else {
		return res;
	}
};

module.exports = (spec, words, mode = 'one') =>
	limit(spec.match(words), words.length, mode);

module.exports.limit = limit;
