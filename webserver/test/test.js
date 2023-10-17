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

chai.use(chaiHttp);

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
});