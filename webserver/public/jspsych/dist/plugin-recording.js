let speechRecordingObject = {
    'startTime': 0,
    'timeStamps': []
}


/**
 * Create timestamps at each Trial start
 */
const onTrialStartRecording = function (trial) {
    startAudioRecording();
}

const onTrialFinishRecording = function (trial) {
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
            this.html_info =
                `
    <div>
      In our study we want to record your voice. Please give permission that we can use your microphone. Please click <b>"Allow"</b> to proceed.
    </div>
    `;
            this.html_permission_denied =
                `
    <div>
      You must give permission to record audio. Please allow the use of your microphone in your browser settings and reload the website.
    </div>
    `;
        }
        trial(display_element, trial) {
            if (trial.start === true) {

                display_element.innerHTML = this.html_info;
                audioRecorder.start()
                    .then(() => {
                        cancelAudioRecording();
                        this.createParticipant();
                    })
                    .catch(error => { //on error
                        // Permission not granted
                        if (error.message.includes("Permission denied") || error.message.includes("Permission dismissed")) {
                            console.log('Permission denied');
                            display_element.innerHTML = this.html_permission_denied;
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
                    this.jsPsych.finishTrial({})
                } else {
                    this.deleteData()
                }

            }
        }

        /**
         * Creates a participant by sending a POST request to the server.
         */
        createParticipant() {
            const headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Content-type': 'application/json'
            };
            speechRecordingObject.startTime = Date.now();
            console.log("Recording Audio...")
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

        deleteData() {
            const headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Content-type': 'application/json'
            };
            fetch('/delete', {
                method: 'DELETE',
                headers: headers,
                body: JSON.stringify({ uuid: uuid_jsRecording })
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
    SpeechRecording.info = info;

    return SpeechRecording;
})(jsPsychModule);