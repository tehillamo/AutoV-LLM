const express = require('express');
require('log-timestamp')
const path = require('path')
const cors = require('cors')
const { v4: uuidv4 } = require('uuid');
const config = require('./config.json');
const fs = require('fs');
const ffmpeg = require("fluent-ffmpeg");

const app = express();
app.use(cors());

// set upload limit
app.use(express.json({limit: '500mb'}));

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
 * For every request a uuid is generated. Then we create a directory with this name and save the recording (audio.wav) and timestamps (timestamps.txt)
 */
app.post('/save', (req, res) => {
    // Check authentication
    if (!(req.get("auth") == config.SECRET_KEY) || req.get("auth") === undefined) {
        console.log('Wrong secret')
        res.status(403);
        return res.send('Wrong secret');
    }

    // Check if everything is present
    if (!req.body.audio) {
        console.log('Missing audio')
        res.status(400);
        return res.send('Missing audio');
    }
    if (!req.body.timestamps) {
        console.log('Missing timestamps')
        res.status(400);
        return res.send('Missing timestamps');
    }
    if (!req.body.trial_data) {
        console.log('Missing trial_data')
        res.status(400);
        return res.send('Missing trial_data');
    }

    // create user id
    uuid = uuidv4();

    // create directory
    fs.mkdirSync(path.join(config.PATH_TO_RESSOURCES, uuid), 0o777);

    console.log("Save trial data")
    // save trial data
    fs.writeFile(path.join(config.PATH_TO_RESSOURCES, uuid, 'trial_data.txt'), JSON.stringify(req.body.trial_data), function(err) {
        if(err) {
            return console.log(err);
        }
    })

    console.log('Try to save recording');

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
        .on('error', error => console.log(`Encoding Error: ${error.message}`))
        .on('exit', () => console.log('Audio recorder exited'))
        .on('close', () => console.log('Audio recorder closed'))
        .on('end', () => {
            console.log('Audio Transcoding succeeded !')            
            // delete audio.wav
            fs.unlinkSync(path.join(config.PATH_TO_RESSOURCES, uuid, 'tmp.wav'));
        })
        .pipe(outStream, { end: true });
    

    // save timestamps
    fs.writeFile(path.join(config.PATH_TO_RESSOURCES, uuid, 'timestamps.txt'), req.body.timestamps.toString(), function(err) {
        if(err) {
            return console.log(err);
        }
    }); 
    console.log('Recording saved with uuid: ' + uuid);
    return res.send('Received a POST HTTP method');
});

app.listen(config.PORT, () => {
    console.log(`Server listening on port ${config.PORT}`);
})
