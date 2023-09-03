module.exports = {
    apps: [
        {
            name: 'mixandmatch',
            script: 'pm2.js', // Use the new script
            autorestart: true,
            watch: false,
            env: {
                NODE_ENV: 'development',
            },
            env_production: {
                NODE_ENV: 'production',
            },
        },
    ],
};