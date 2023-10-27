/*
TODO:
file size test
stress test
*/
const path = require('path')
const chai = require('chai');
const chaiHttp = require('chai-http');
const app = require('../app/app'); // Import your Express app
const expect = chai.expect;
var fs = require('fs');
const ffmpeg = require("fluent-ffmpeg");

chai.use(chaiHttp);

function mergeFileWithItself(inputFile, outputFile, times, callback) {
  const command = ffmpeg();

  // Build the FFmpeg command to merge the file with itself
  command
    .input(inputFile)
    .input(inputFile)
    .mergeToFile(outputFile)
    .on('end', () => {
      callback(null);
    })
    .on('error', (err) => {
      callback(err);
    });
}

// Example usage:
const inputFile = path.join(__dirname, 'audio_long.wav');
const outputFile = path.join(__dirname, 'output.wav');
const times = 8;

let i = 0;

function callback(err) {
  if (err) {
    console.log(err);
  }
  i++;
  fs.unlinkSync(path.join(__dirname, 'audio_long.wav'));
  fs.renameSync(path.join(__dirname, 'output.wav'), path.join(__dirname, 'audio_long.wav'));
  if (i < times) {   
    mergeFileWithItself(inputFile, outputFile, times, callback);    
  } else {
    console.log('Created long audio file');
    const timestamps = fs.readFileSync(path.join(__dirname, './timestamps.txt')).toString()
    const trial_data = fs.readFileSync(path.join(__dirname, './trial_data.txt')).toString()
    console.log('Created long audio file')
    const audio =' base64,' + fs.readFileSync(path.join(__dirname, './audio_long.wav'), {encoding: 'base64'});
    console.log('Request started')
    chai.request(app)
      .post('/save')
      .send({
        audio: audio,
        timestamps: timestamps,
        trial_data: trial_data
      })
      .end((err, res) => {
        expect(res.text.startsWith("Recording saved with uuid:")).to.be.true;
        expect(res).to.have.status(200);        
        done();
      });
}
}

describe('API Tests', () => {
  it('should return "Recording saved with uuid: <uuid>" message', (done) => {
    const timestamps = fs.readFileSync(path.join(__dirname, './timestamps.txt')).toString()
    const trial_data = fs.readFileSync(path.join(__dirname, './trial_data.txt')).toString()
    const audio =' base64,' + fs.readFileSync(path.join(__dirname, './audio.wav'), {encoding: 'base64'}).toString();
    chai.request(app)
      .post('/save')
      .send({
        audio: audio,
        timestamps: timestamps,
        trial_data: trial_data
      })
      .end((err, res) => {
        expect(res.text.startsWith("Recording saved with uuid:")).to.be.true;
        expect(res).to.have.status(200);
        
        done();
      });
  });
  it('should return "Recording saved with uuid: <uuid>" message', (done) => {
    fs.unlinkSync(path.join(__dirname, 'audio_long.wav'));
    fs.createReadStream(path.resolve(__dirname, 'audio.wav')).pipe(fs.createWriteStream(path.resolve(__dirname, 'audio_long.wav')));
    mergeFileWithItself(inputFile, outputFile, times, (err) => {
      if (err) {
        console.log(err);
      }
      i++;
      fs.unlinkSync(path.join(__dirname, 'audio_long.wav'));
      fs.renameSync(path.join(__dirname, 'output.wav'), path.join(__dirname, 'audio_long.wav'));
      if (i < times) {   
        mergeFileWithItself(inputFile, outputFile, times, callback);    
      } else {
        console.log('end')
      }
    });
    
  });
});

