let speechRecordingObject = {
  'startTime': 0,
  'timeStamps': []
}



/**
 * Create timestamps at each Trial start
 */
const onTrialStartRecording = function(trial) {
  startAudioRecording();
}

const onTrialFinishRecording = function(trial) {
  stopAudioRecording(trial);
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
        const headers = {
          'Access-Control-Allow-Origin':'*',
          'Access-Control-Allow-Methods':'POST',
          'Content-type': 'application/json'
        };
        fetch('/createParticipant', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({})
        }).then(response => {
            if (response.ok) {
              response.json().then(data => {
                uuid_jsRecording = data.uuid
                this.jsPsych.finishTrial({}) 
              });              
            }
            else throw Error(`Server returned ${response.status}: ${response.statusText}`)
        })
        .catch(err => {
            console.log(err);
        });    
      }
      
      if (trial.start === false) {
        const response = confirm("Your voice recording will be saved and sent to our server. Do you want to continue?");

        if (response === true) {
          this.jsPsych.finishTrial({}) 
        } else {
          const headers = {
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Methods':'POST',
            'Content-type': 'application/json'
          };
          fetch('/delete', {
            method: 'DELETE',
            headers: headers,
            body: JSON.stringify({uuid: uuid_jsRecording})
          }).then(response => {
              if (response.ok) {
                cancelAudioRecording();
                this.jsPsych.finishTrial({})              
              }
              else throw Error(`Server returned ${response.status}: ${response.statusText}`)
          })
          .catch(err => {
              console.log(err);
          });    
          
        } 

      }    
    }    
  }
  SpeechRecording.info = info;

  return SpeechRecording;
})(jsPsychModule);