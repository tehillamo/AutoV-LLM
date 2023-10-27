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
const FfmpegCommand  = require("fluent-ffmpeg");

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
    if (!req.body.uuid) {
        logger.warn('Missing uuid')
        res.status(400);
        return res.send('Missing uuid');
    }
    if (!req.body.index) {
        logger.warn('Missing index')
        res.status(400);
        return res.send('Missing index');
    }

    logger.info('Try to save recording for participant: ' + req.body.uuid);
    // convert base 64 to wav and save it
    const buffer = Buffer.from(
        req.body.audio.split('base64,')[1],  // only use encoded data after "base64,"
        'base64'
    )

    tmp_filename = "tmp__" + uuidv4() + "__" + req.body.index + ".wav";
    audio_filename = "audio_" + req.body.index + ".mp3";
    audio_filename = "audio_" + req.body.index + ".wav";

    uuid = req.body.uuid
    try {
        //fs.writeFileSync(path.join(config.PATH_TO_RESSOURCES, uuid, tmp_filename), buffer);
        fs.writeFileSync(path.join(config.PATH_TO_RESSOURCES, uuid, audio_filename), buffer);
    } catch (error) {
        logger.warn(error)
        console.log(error)
        res.status(200);
        return res.send({uuid: uuid});
    }

    // convert tmp.wav to mp3
/*     var outStream = fs.createWriteStream(path.join(config.PATH_TO_RESSOURCES, uuid, audio_filename));
    var command = new FfmpegCommand();
    command
        .input(path.join(config.PATH_TO_RESSOURCES, uuid, tmp_filename))
        .toFormat("mp3")
        .on('error', error => logger.error(`Encoding Error: ${error.message}`))
        .on('exit', () => logger.warn('Audio recorder exited'))
        .on('close', () => logger.warn('Audio recorder closed'))
        .on('end', () => {
            logger.info('Audio Transcoding succeeded !' + tmp_filename)    

            // delete tmp.wav
            try {
                fs.unlinkSync(path.join(config.PATH_TO_RESSOURCES, uuid, tmp_filename));
            } catch (error) {
                logger.warn(error)
                console.log(error)               
            }
            
            logger.info('Recording saved with uuid: ' + uuid + " and index: " + req.body.index);
            res.status(200);
            return res.send({uuid: uuid});
        })
        .pipe(outStream, { end: true }); */

    logger.info('Recording saved with uuid: ' + uuid + " and index: " + req.body.index);
    res.status(200);
    return res.send({uuid: uuid});

});

app.post('/createParticipant', (req, res) => {
    // create user id
    uuid = uuidv4();
    logger.info('Created new participant: ' + uuid);

    // create directory
    fs.mkdirSync(path.join(config.PATH_TO_RESSOURCES, uuid), 0o777);

    return res.status(200).send({uuid: uuid});
});

app.post('/saveTrialData', (req, res) => {
    if (!req.body.trial_data) {
        logger.warn('Missing trial_data')
        res.status(400);
        return res.send('Missing trial_data');
    }
    if (!req.body.uuid) {
        logger.warn('Missing uuid')
        res.status(400);
        return res.send('Missing uuid');
    }

    uuid = req.body.uuid

    logger.info("Save trial data for participant: " + uuid);
    // save trial data
    fs.writeFile(path.join(config.PATH_TO_RESSOURCES, uuid, 'trial_data.txt'), JSON.stringify(req.body.trial_data), function(err) {
        if(err) {
            return logger.error(err);
        }
    })

    res.status(200);

    return res.send({uuid: uuid});
});

app.delete('/delete', (req, res) => {
    if (!req.body.uuid) {
        logger.warn('Missing uuid')
        res.status(400);
        return res.send('Missing uuid');
    }

    uuid = req.body.uuid
    fs.rmSync(path.join(config.PATH_TO_RESSOURCES, uuid), { recursive: true, force: true });
    res.status(200);

    return res.send({uuid: uuid});
});


module.exports = app; // for testing

