const { spawn } = require('child_process');

const startVite = spawn('node_modules/.bin/vite', ['start:frontend'], {
    stdio: 'inherit',
});

startVite.on('close', (code) => {
    console.log(`Vite process exited with code ${code}`);
});
