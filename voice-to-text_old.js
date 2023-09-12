var jsPsychcVoiceText = (function (jspsych) {
  'use strict';

  const info = {
      name: "VoiceText",
      parameters: {
          /**
           * The HTML string to be displayed.
           */
          stimulus: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Stimulus",
              default: undefined,
          },
          /** For the experiment to run as choice by buttons 
           * Array containing the buttons the subject is allowed to press to respond to the stimulus.
           */
          choices_buttons: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Choices",
              default: null,
          },

          /** For the experiment to run as choice by keys
           * Array containing the key(s) the subject is allowed to press to respond to the stimulus.
           */
          choices_key: {
            type: jspsych.ParameterType.KEYS,
            pretty_name: "Choices",
            default: "ALL_KEYS",
        },
          /**
           * Any content here will be displayed below the stimulus.
           */
          prompt: {
              type: jspsych.ParameterType.HTML_STRING,
              pretty_name: "Prompt",
              default: null,
          },
          /**
           * How long to show the stimulus.
           */
          stimulus_duration: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Stimulus duration",
              default: null,
          },
          /**
           * How long to show trial before it ends.
           */
          trial_duration: {
              type: jspsych.ParameterType.INT,
              pretty_name: "Trial duration",
              default: null,
          },
          /**
           * If true, trial will end when subject makes a response.
           */
          response_ends_trial: {
              type: jspsych.ParameterType.BOOL,
              pretty_name: "Response ends trial",
              default: true,
          },
      },
  };
  /**
   * **html-keyboard-response**
   *
   * jsPsych plugin for displaying a stimulus and getting a keyboard response
   *
   * @author Tehilla Ostrovsky
   * @see {@link https://www.jspsych.org/plugins/jspsych-html-keyboard-response/ html-keyboard-response plugin documentation on jspsych.org}
   */
  class VoiceText {
      constructor(jsPsych) {
          this.jsPsych = jsPsych;
      }

   trial(display_element, trial) {

    // a function to determine if the experiemnt will run with keys or with buttons 



    
        var new_html_1 = '<div id="jspsych-voice-2-text"></div>';
        
        var new_html = '<div class="voice_to_text" style ="background-color:#f2f1ed; width:200; position:absolute;left:0%;top:5%;margin:50px; border-radius: 25px;border: 2px solid #73AD21;">'+
                       '<h5 style = "margin:20px">Start Recording</h1>' + 
                       //'<input name="" id="convert_text"></input>' + 
                       '<button id="click_record" style = "margin:20px"> Record &#127908; </button>'+
                       '</div>'
        
        var prompt = '<div id="prompt" style = "width: 500px">' + trial.prompt + '</div>'

        var button = '<input disabled type="button" id="continue-button" style = "position:relative;left:0%;margin-top:50%;" value="continue">'
        
        var ImgButton_1 = '<button disabled type="submit" id = "button_image-1" style = "margin = 20px">'+
                          '<img src="' + trial.stimulus[0] + '" style = "opacity: .01;height:150px; width:150px; margin:15px" id="image-response-stimulus-1"></img>'+
                          '</button>'

        var ImgButton_2 = '<button disabled type="submit" id = "button_image-2" style = "margin: 20px">'+
                          '<img src="' + trial.stimulus[1] + '" style = "opacity: .01;height:150px; width:150px; margin:15px" id="image-response-stimulus-2"></img>'+
                          '</button>'

        var green = '<div hidden id="choice_circle_green">you chose the left circle</div>'
        var blue = '<div hidden id="choice_circle_blue">you chose the right circle</div>'

        var q_text = '<div hidden id="q_text">Which of the two circles is greener?</div>'

        var jsarray = [];
        
        display_element.innerHTML = prompt; 

        display_element.innerHTML += q_text
        
        display_element.innerHTML += ImgButton_1; 
        display_element.innerHTML += ImgButton_2; 
        
        display_element.innerHTML += new_html_1;
        
        display_element.innerHTML += green
        display_element.innerHTML += blue
  

        
        display_element.innerHTML += new_html;
              
        display_element.innerHTML += button;
      
        

        click_record.addEventListener("click", function() { 
            
            // Check if microphone permission is granted - TO DO 
         document.getElementById("prompt").hidden = true;
          
          var speech = true;
          window.SpeechRecognition = window.webkitSpeechRecognition;
      
          const recognition = new SpeechRecognition();
          recognition.interimResults = true;
          
          
          recognition.addEventListener('result', e => {
              const transcript = Array.from(e.results)
                  .map(result => result[0]) // extract only the final array that has a full voice2text
                  .map(result => result.transcript)
                  .join('')
      
              //document.getElementById("convert_text").innerHTML = transcript;
              jsarray.push(transcript);
              console.log(jsarray)
                   
          });
          
          
          if (speech == true) {
              recognition.start();
         }
         
          document.getElementById('q_text').hidden = false; 
          
          document.getElementById('button_image-1').disabled = false;
          document.getElementById('image-response-stimulus-1').style.opacity = .9;
          
          document.getElementById('button_image-2').disabled = false;
          document.getElementById('image-response-stimulus-2').style.opacity = .9;
      

          if (document.getElementById('continue-button').onclick = function() {
            recognition.abort();
            console.log("Speech recognition aborted.");
          });
          
        //   // this converts the clicking into a funtion to enable 
        //   // the re-activating the recording button in the following choice 
        // if (document.getElementById('click_record').onclick = function() {
        
        // });
          
        });

          
        
        var jsText = jsarray
      
        var chosen_img = []
        // once the image is clicked, disable the rest of the buttons 
      document.getElementById('button_image-1').onclick = function() {
        chosen_img.push('button_image-1')
         document.getElementById('choice_circle_blue').hidden = false
         document.getElementById('button_image-1').style.border = "2px solid red"
         document.getElementById('button_image-2').disabled = true
         document.getElementById('button_image-2').style = "display: inblock;margin-bottom:solid 1px grey;"
         document.getElementById('continue-button').disabled = false;
      }


      document.getElementById('button_image-2').onclick = function() {
        chosen_img.push('button_image-2')
        document.getElementById('choice_circle_green').hidden = false
        document.getElementById('button_image-2').style.border = "2px solid red"
        document.getElementById('button_image-1').disabled = true
        document.getElementById('button_image-1').style = "display: inblock;margin-bottom:solid 1px grey;"
        document.getElementById('continue-button').disabled = false;
     }
        
        // start time
        var start_time = performance.now();
        // add event listeners to buttons
        
            display_element
                .querySelector("#continue-button")
                .addEventListener("click", (e) => {
                var btn_el = e.currentTarget;
                var choice = btn_el.getAttribute("continue-button"); // don't use dataset for jsdom compatibility
                after_response(choice);
            })
        

          // store response
          var response = {
            rt: null,
            button: null,
            text: null, 
        };


        // function to end trial when it is time
        const end_trial = () => {
            // kill any remaining setTimeout handlers
            this.jsPsych.pluginAPI.clearAllTimeouts();
            // gather the data to store for the trial
            var trial_data = {
                rt: response.rt,
                stimulus: trial.stimulus,
                response: chosen_img,
                text: jsText.slice(-1)
            };
            // clear the display
            display_element.innerHTML = "";
            // move on to the next trial
            this.jsPsych.finishTrial(trial_data);
        };
        // function to handle responses by the subject
        function after_response(choice) {
            // measure rt
            var end_time = performance.now();
            var rt = Math.round(end_time - start_time);
            response.button = parseInt(choice);
            response.rt = rt;
            // after a valid response, the stimulus will have the CSS class 'responded'
            // which can be used to provide visual feedback that a response was recorded
                 //display_element.querySelector("continue-button").className += //these two lines were commented out 
                 //  " responded";//these two lines were commented out 
            // disable all the buttons after a response
            var btns = document.querySelectorAll("continue-button");
            for (var i = 0; i < btns.length; i++) {
                //btns[i].removeEventListener('click');
                btns[i].setAttribute("disabled", "disabled");
            }
            if (trial.response_ends_trial) {
                end_trial();
            }
        }
        // hide image if timing is set
        if (trial.stimulus_duration !== null) {
            this.jsPsych.pluginAPI.setTimeout(() => {
                display_element.querySelector("jspsych-voice-2-text").style.visibility = "hidden";
            }, trial.stimulus_duration);
        }
        // end trial if time limit is set
        if (trial.trial_duration !== null) {
            this.jsPsych.pluginAPI.setTimeout(end_trial, trial.trial_duration);
        }
    } //closing brackets for trial

    simulate(trial, simulation_mode, simulation_options, load_callback) {
        if (simulation_mode == "data-only") {
            load_callback();
            this.simulate_data_only(trial, simulation_options);
        }
        if (simulation_mode == "visual") {
            this.simulate_visual(trial, simulation_options, load_callback);
        }
    }
    create_simulation_data(trial, simulation_options) {
        const default_data = {
            stimulus: trial.stimulus,
            rt: this.jsPsych.randomization.sampleExGaussian(500, 50, 1 / 150, true),
            response: this.jsPsych.randomization.randomInt(0, trial.choices.length - 1),
        };
        const data = this.jsPsych.pluginAPI.mergeSimulationData(default_data, simulation_options);
        this.jsPsych.pluginAPI.ensureSimulationDataConsistency(trial, data);
        return data;
    }
    simulate_data_only(trial, simulation_options) {
        const data = this.create_simulation_data(trial, simulation_options);
        this.jsPsych.finishTrial(data);
    }
    simulate_visual(trial, simulation_options, load_callback) {
        const data = this.create_simulation_data(trial, simulation_options);
        const display_element = this.jsPsych.getDisplayElement();
        this.trial(display_element, trial);
        load_callback();
        if (data.rt !== null) {
            this.jsPsych.pluginAPI.clickTarget(display_element.querySelector(`div[data-choice="${data.response}"] button`), data.rt);
        }
    }

}  
    

VoiceText.info = info;

return VoiceText;

})(jsPsychModule);
