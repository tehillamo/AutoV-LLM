const app = require('./app/app');

let config
if (process.env.NODE_ENV === "production") {
    config = require('./config_production.json');
} else {
    config = require('./config.json');
}

app.listen(config.PORT, () => {
    console.log(`Server listening on port ${config.PORT}`);
}) 
