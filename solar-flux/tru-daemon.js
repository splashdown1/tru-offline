const http = require('http');
const { CHANNELS, routeKeys } = require('./channels.js');

// heartbeat state
let heartbeat = {
  tick: 0,
  lastPulse: Date.now(),
  harmonic: [432, 528, 639, 741, 852],
  currentFreq: 432,
  resonance: 1.0,
  phase: 0,
  online: true
};

const TRU_PORT = 3456;
const TRU_HOST = '127.0.0.1';

async function pulse() {
  heartbeat.tick++;
  heartbeat.lastPulse = Date.now();
  heartbeat.currentFreq = heartbeat.harmonic[heartbeat.tick % heartbeat.harmonic.length];
  heartbeat.resonance = 1.0; // hardcoded channels are always ok
  heartbeat.phase = (heartbeat.phase + 0.0625) % (Math.PI * 2);
  return {
    tick: heartbeat.tick,
    freq: heartbeat.currentFreq,
    resonance: heartbeat.resonance,
    phase: heartbeat.phase,
    online: heartbeat.online,
    uptime: Date.now() - heartbeat.lastPulse,
    routes: heartbeat.resonance
  };
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-TRU-Key');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');

  if (url.pathname === '/health') {
    res.end(JSON.stringify({ status: 'ok', ...heartbeat }));
  } else if (url.pathname === '/pulse') {
    const state = await pulse();
    res.end(JSON.stringify(state));
  } else if (url.pathname === '/status') {
    const result = routeKeys.map(key => ({
      key,
      status: 'ok',
      count: CHANNELS[key].items.length,
      freq: CHANNELS[key].freq,
      weight: CHANNELS[key].weight,
      items: CHANNELS[key].items.slice(0, 5)
    }));
    res.end(JSON.stringify({ heartbeat, routes: result }));
  } else if (url.pathname === '/routes') {
    res.end(JSON.stringify(routeKeys));
  } else if (url.pathname === '/channel') {
    const ch = url.searchParams.get('name') || 'news';
    const data = CHANNELS[ch.toLowerCase()];
    if (!data) {
      res.writeHead(404);
      res.end(JSON.stringify({ error: 'channel not found', available: routeKeys }));
      return;
    }
    res.end(JSON.stringify({ key: ch, ...data }));
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'not found', available: ['/health','/pulse','/status','/routes','/channel?name='] }));
  }
});

server.listen(TRU_PORT, TRU_HOST, () => {
  console.log(`TRU heartbeat daemon active on ${TRU_HOST}:${TRU_PORT}`);
  console.log(`Solar Flux — ${routeKeys.length} channels, harmonic: ${heartbeat.harmonic.join('hz ')}hz`);
  console.log(`Channels: ${routeKeys.join(', ')}`);
  pulse();
});

process.on('SIGTERM', () => { heartbeat.online = false; server.close(); });