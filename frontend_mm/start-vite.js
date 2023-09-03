import { createServer } from 'vite';

async function start() {
    const server = await createServer();
    await server.listen();
}

start().catch((error) => {
    console.error('Error starting Vite:', error);
});