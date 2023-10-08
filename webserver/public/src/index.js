var jsPsych = initJsPsych({
  on_trial_start: function(trial) {
    onTrialStartRecording(trial);
  },
  on_finish: function() {
    console.log(jsPsych.data)
    jsPsych.data.displayData();
  }
});

const trials = [
  {
    type: jsPsychSpeechRecording,
    start: true
  },
  {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world 1!',
    prompt: 'PLease press some key'
  },
  {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world 2!'
  },
  {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world 3!'
  },
  {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world 4!'
  },
  {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world 5!'
  },
  {
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world 6!'
  },
  {
    type: jsPsychSpeechRecording,
    start: false
  },
];


jsPsych.run(trials);
