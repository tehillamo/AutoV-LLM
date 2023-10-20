const express = require('express');
require('log-timestamp')
const path = require('path')
const cors = require('cors')
const { v4: uuidv4 } = require('uuid');
const winston = require('winston');
const { combine, timestamp, json } = winston.format;

let config
if (process.env.NODE_ENV === "production") {
    config = require('../config_production.json');
    console.log('Using production config')
} else {
    config = require('../config.json');
    console.log('Using development config')
}

const logger = winston.createLogger({
    level: 'info',
    format: combine(timestamp(), json()),
    transports: [
        new winston.transports.File({
          filename: path.join(config.PATH_TO_LOGS, 'app.log'),
        }),
    ],
  });


const fs = require('fs');
const ffmpeg = require("fluent-ffmpeg");

const app = express();
app.use(cors());

// set upload limit
app.use(express.json({limit: '999mb'}));

// bind public folder
app.use(express.static('public'))

// bind index.html
app.get('/', (req, res) => {
    res.send();
});

/**
 * POST HTTP method
 * save Recording, timestamps and trial data
 * 
 * For every request a uuid is generated. Then we create a directory with this name and save the recording (audio.mp3) and timestamps (timestamps.txt)
 */
app.post('/save', (req, res) => {
    // Check if everything is present
    if (!req.body.audio) {
        logger.warn('Missing audio')
        res.status(400);
        return res.send('Missing audio');
    }
    if (!req.body.timestamps) {
        logger.warn('Missing timestamps')
        res.status(400);
        return res.send('Missing timestamps');
    }
    if (!req.body.trial_data) {
        logger.warn('Missing trial_data')
        res.status(400);
        return res.send('Missing trial_data');
    }

    // create user id
    uuid = uuidv4();

    // create directory
    fs.mkdirSync(path.join(config.PATH_TO_RESSOURCES, uuid), 0o777);

    logger.info("Save trial data")
    // save trial data
    fs.writeFile(path.join(config.PATH_TO_RESSOURCES, uuid, 'trial_data.txt'), JSON.stringify(req.body.trial_data), function(err) {
        if(err) {
            return logger.error(err);
        }
    })

    logger.info('Try to save recording');

    // convert base 64 to wav and save it
    const buffer = Buffer.from(
        req.body.audio.split('base64,')[1],  // only use encoded data after "base64,"
        'base64'
    )

    fs.writeFileSync(path.join(config.PATH_TO_RESSOURCES, uuid, 'tmp.wav'), buffer);

    // convert tmp.wav to mp3
    var outStream = fs.createWriteStream(path.join(config.PATH_TO_RESSOURCES, uuid, 'audio.mp3'));
    ffmpeg()
        .input(path.join(config.PATH_TO_RESSOURCES, uuid, 'tmp.wav'))
        .toFormat("mp3")
        .on('error', error => logger.error(`Encoding Error: ${error.message}`))
        .on('exit', () => logger.warn('Audio recorder exited'))
        .on('close', () => logger.warn('Audio recorder closed'))
        .on('end', () => {
            logger.info('Audio Transcoding succeeded !')            
            // delete tmp.wav
            fs.unlinkSync(path.join(config.PATH_TO_RESSOURCES, uuid, 'tmp.wav'));
        })
        .pipe(outStream, { end: true });
    

    // save timestamps
    fs.writeFile(path.join(config.PATH_TO_RESSOURCES, uuid, 'timestamps.txt'), req.body.timestamps.toString(), function(err) {
        if(err) {
            return logger.error(err);
        }
    }); 
    logger.info('Recording saved with uuid: ' + uuid);
    res.status(200);
    return res.send('Recording saved with uuid: ' + uuid);
});

module.exports = app; // for testing

