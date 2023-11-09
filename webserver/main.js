const app = require('./app/app');
const deleteUnfinishedTrials = require('./app/delete_unfinished_trials');
let cron = require('node-cron');

const fs = require('fs');
const path = require('path');

let config
if (process.env.NODE_ENV === "production") {
    config = require('./config_production.json');
} else {
    config = require('./config.json');
}

cron.schedule(`${config.TIME_FOR_DELETION_TASK} * * * *`, () => {
    console.log('Running deletion task');
    deleteUnfinishedTrials(config.PATH_TO_RESSOURCES, config.MINUTES_TO_DELETE);
});


app.listen(config.PORT, () => {
    console.log(`Server listening on port ${config.PORT}`);
});







