# Overview
Server for project

---

# Setup Production
## Prerequisites
 - [Docker](https://docs.docker.com/engine/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)

## Setup of experiment website and back-end server
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/webserver` to step into the project folder
 3. Run `docker-compose up -d` to start the docker container 
 4. To stop the container use `sudo docker-compose stop`

## Setup of data-pipeline
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/data_pipeline` to step into the project folder
 3. Run `docker-compose up -d` to start the docker container 
 4. To stop the container use `sudo docker-compose stop`

Note that you only need to clone the repository once.

 ---

 # Setup Development
 ## Prerequisites
 - npm (>= 9.5.1), Node.js (>= 18.16.1), Python (>= 3.10)

## Setup of experiment website and back-end server
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/webserver` to step into the project folder
 3. Run `npm install` to install all dependencies
 4. Run `node server.js` to start the webserver
 5. Available in browser under `http:://localhost:8000`



## Setup of data-pipeline
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/data_pipeline` to step into the project folder
 3. Create a virtual environment with `python -m venv venv`
 4. Start virtual environment `source venv/bin/activate`
 5. Run `pip install -r requirements.txt` to install python dependencies
 6. Install ffmpeg with `apt-get install ffmpeg`
 7. Start the corresponding script using `python <script-name>` and use `python <script-name> -h` for help
 
Note that you only need to clone the repository once.

---

# Create a study using jsPsych with automated recording
We use the [jsPsych](https://www.jspsych.org/) framework to run our study. You can specify the different trials in `/webserver/public/src/index.js`. To make use of the recordings you need to specify the first and last trial and a callback function. We need to initialize jsPsych with a trigger function so that we can track the different trial times:
```js
var jsPsych = initJsPsych({
  on_trial_start: function(trial) {
    onTrialStartRecording(trial);
  }
});
```
Then we specify our trials. The first and last trial must to be of type `jsPsychSpeechRecording`. The first trial indicates the start (`start: true`) and an `auth_secret` which is used for authentication to the API. Note that this `auth_secret` must match the one in `/webserver/config.json`. The last trial specifies the end (`start: false`). The actual study trials can be declared between the two recording trials. If you need other plugins import them in `/webserver/public/index.html`.
```js
const trials = [
  {
    type: jsPsychSpeechRecording,
    start: true,
    auth_secret: 'test'
  },
    ...
  {
    type: jsPsychSpeechRecording,
    start: false
  },
];
```
After that, we can run the study.
```js
jsPsych.run(trials);
```
The implementation of the `jsPsychSpeechRecording` plugin can be found in `/webserver/public/jspsych/dist/plugin-recording.js` and `/webserver/public/jspsych/dist/plugin-recording-util.js`.

# Ressources
All recordings and the trial data will be saved to the `ressources` folder. Each participant has a unique id. For each participant we create a new folder inside `ressources`. In this folder you can find the whole recording, the timestamps which indicate when each trial started in ms, and the trial data.

# Evaluation Script
We provide different scripts to automatically evaluate the recordings of the verbal reports. In the following we explain each script and how to use it.

## speech2text
This scripts transcribes the recordings. Firstly, we cut each participant' audio into the different trials using the timestamps.
