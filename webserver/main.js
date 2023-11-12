const app = require('./app/app');
const deleteUnfinishedTrials = require('./app/delete_unfinished_trials');
let cron = require('node-cron');
const fs = require('fs');
const path = require('path');
const winston = require('winston');
const { combine, timestamp, json } = winston.format;

let config
if (process.env.NODE_ENV === "production") {
    config = require('./config_production.json');
} else {
    config = require('./config.json');
}

const logger = winston.createLogger({
    level: 'info',
    format: combine(timestamp(), json()),
    transports: [
        new winston.transports.File({
            filename: path.join(config.PATH_TO_LOGS, "app.log")
        })

    ],
});

winston.add(logger);



cron.schedule(`${config.TIME_FOR_DELETION_TASK} * * * *`, () => {
    deleteUnfinishedTrials(config.PATH_TO_RESSOURCES, config.MINUTES_TO_DELETE, logger);
});


app.listen(config.PORT, () => {
    logger.info(`Server listening on port ${config.PORT}`);
    console.log(`Server listening on port ${config.PORT}`);
});







