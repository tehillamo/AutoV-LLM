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

        let html_content = 
        `
        <div>
          In our study we want to record your voice. Please give permission that we can use your microphone. Please click <b>"Allow"</b> to proceed.
        </div>
        `;
        display_element.innerHTML = html_content;

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
                let html_content = 
                `
                <div>
                  You must give permission to record audio. Please allow the use of your microphone in your browser settings and reload the website.
                </div>
                `;
                display_element.innerHTML = html_content;
            }
            //No Browser Support Error
            if (error.message.includes("mediaDevices API or getUserMedia method is not supported in this browser.")) {       
                console.log("To record audio, use browsers like Chrome and Firefox.");
            }
        });        
      }
      
      if (trial.start === false) {
        const response = confirm("Your voice recording will be saved and sent to our server. Do you want to continue?");

        if (response === true) {
          stopAudioRecording(this.jsPsych.data.allData.trials, this.jsPsych);
        } else {
          cancelAudioRecording();
          this.jsPsych.finishTrial({}) 
        } 

      }    
    }    
  }
  SpeechRecording.info = info;

  return SpeechRecording;
})(jsPsychModule);