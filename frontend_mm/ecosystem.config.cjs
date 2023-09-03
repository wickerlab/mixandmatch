module.exports = {
    apps: [
        {
            name: 'mixandmatch',
            script: 'start-vite.js', // Use the custom script
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
