function inject(str) {
	str = "var entities = {'player': [], 'friendly_bullets': [], 'bullets': [], 'ennemies': [], 'food': []}; var data = {'score': 0, 'level': 0, 'done': 0}; var player_i = 0; var bullet_i = 0; var saved_entities = entities; function add_entity(x, y, size, color) {switch (color) {case '#00b2e1': if (size > 15) {player_i += 1; if (player_i % 2 == 1) {var str = ''; for (var key in entities) {str += (entities[key]).length + ' ';} entities.timestamp = Date.now(); saved_entities = entities; entities = {'player': [], 'friendly_bullets': [], 'bullets': [], 'ennemies': [], 'food': []}; entities['player'].push([x, y]);}} else {bullet_i += 1; if (bullet_i % 2 == 1) {entities['friendly_bullets'].push([x, y])}} break; case '#ffe869': entities['food'].push([x, y]); break; case '#768dfc': entities['food'].push([x, y]); break; case '#fc7677': entities['food'].push([x, y]); break;}}; function add_text(text) {var ext; ext = text.match(/Score: ([0-9]+)/); if (!!ext) {data['score'] = parseInt(ext[1])} ext = text.match(/Lvl ([0-9]+) Tank/); if (!!ext) {data['level'] = parseInt(ext[1])} ext = text.match(/You were killed by:/); if (!!ext) {data['done'] = 1} ext = text.match(/This is the tale of.../); if (!!ext) {data['done'] = 0}}; " + str;
	str = str.replace(/cp5\.contexts\[\$0\]\.setTransform\(\$1,\$2,\$3,\$4,\$5,\$6\)/, 'cp5.contexts[$$0].setTransform($1,$2,$3,$4,$5,$6);add_entity($5, $6, $1, cp5.contexts[$$0].fillStyle)', str);
	str = str.replace(/cp5\.contexts\[\$0\]\.moveTo\(\$1,\$2\)/, 'cp5.contexts[$0].moveTo($1,$2);add_entity($1, $2, 1, cp5.contexts[$0].fillStyle)', str);
	str = str.replace(/cp5\.contexts\[\$0\]\.fillText\(UTF8ToString\(\$1\),0,0\)/, 'cp5.contexts[$0].fillText(UTF8ToString($1),0,0);add_text(UTF8ToString($1))', str);
	return str;
}

function listener(details) {
	console.log(details.url);
	let filter = browser.webRequest.filterResponseData(details.requestId);
	let decoder = new TextDecoder("utf-8");
	let encoder = new TextEncoder();
	filter.ondata = event => {
		let str = decoder.decode(event.data, {stream: true});
		str = inject(str);
		filter.write(encoder.encode(str));
		filter.disconnect();
	}
	return {};
}
browser.webRequest.onBeforeRequest.addListener(
	listener,
	{
		urls: ["https://static.diep.io/build_*.wasm.js"]
	},
	["blocking"]
);
