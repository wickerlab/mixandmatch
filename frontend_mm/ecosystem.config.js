module.exports = {
    apps: [
        {
            name: "mixandmatch",
            script: "node_modules/.bin/vite",
            args: "start:frontend",
            autorestart: true,
            watch: false,
            env: {
                NODE_ENV: "development",
            },
            env_production: {
                NODE_ENV: "production",
            },
        },
    ],
};
