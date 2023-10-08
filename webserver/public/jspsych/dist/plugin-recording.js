let speechRecordingObject = {
  'startTime': 0,
  'timeStamps': []
}

/**
 * Create timestamps at each Trial start
 */
const onTrialStartRecording = function(trial) {
  if (!(trial.type.info.name == 'SpeechRecording')) {
    timeDifference = Date.now() - speechRecordingObject.startTime;
    speechRecordingObject.timeStamps.push(timeDifference);    
  }
}

var jsPsychSpeechRecording = (function (jspsych) {
    "use strict";
  
    const info = {
      name: "SpeechRecording",
      parameters: {
        start: {
          type: jspsych.ParameterType.BOOL,
          default: undefined,
        }

      },
};

class SpeechRecording {
    constructor(jsPsych) {
      this.jsPsych = jsPsych;
    }
    trial(display_element, trial) {
      if (trial.start === true) {  
        audioRecorder.start()
        .then(() => {
            speechRecordingObject.startTime = Date.now();
            console.log("Recording Audio...")   
            this.jsPsych.finishTrial({}) 
        })    
        .catch(error => { //on error
            // Permission not granted
            if (error.message.includes("Permission denied") || error.message.includes("Permission dismissed")) {
                console.log('Permission denied');
                alert('You need to give permission to record audio. Please click "Allow" in your browser settings and restart the session.')
            }
            //No Browser Support Error
            if (error.message.includes("mediaDevices API or getUserMedia method is not supported in this browser.")) {       
                console.log("To record audio, use browsers like Chrome and Firefox.");
            }
        });        
      }
      
      if (trial.start === false) {
        stopAudioRecording(this.jsPsych.data.allData.trials);
        this.jsPsych.finishTrial({}) 
      }    
    }    
  }
  SpeechRecording.info = info;

  return SpeechRecording;
})(jsPsychModule);