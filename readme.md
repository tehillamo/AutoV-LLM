# Automated Analysis of Verbal Reports
This is a sample implementation of our automated verbal reports analysis framework. The framework allows you to conduct your jsPsych study whilst recording the participants. Subsequently, analyses can be replicated by executing our data-pipeline.
## Overview
- [Automated Analysis of Verbal Reports](#automated-analysis-of-verbal-reports)
  - [Overview](#overview)
  - [Setup Production](#setup-production)
    - [Prerequisites](#prerequisites)
    - [Setup of Experiment Website and Back-End Server](#setup-of-experiment-website-and-back-end-server)
    - [Setup of Data-Pipeline](#setup-of-data-pipeline)
  - [Setup Development](#setup-development)
    - [Prerequisites](#prerequisites-1)
    - [Setup of Experiment Website and Back-End Server](#setup-of-experiment-website-and-back-end-server-1)
    - [Setup of Data-Pipeline](#setup-of-data-pipeline-1)
  - [Create a Study using jsPsych with Automated Recording](#create-a-study-using-jspsych-with-automated-recording)
  - [Ressources \& Outputs](#ressources--outputs)
  - [Evaluation Script](#evaluation-script)
    - [Sentence Embeddings](#sentence-embeddings)
  - [Citing \& Authors](#citing--authors)
  - [References](#references)


---

## Setup Production
### Prerequisites
 - [Docker](https://docs.docker.com/engine/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)

### Setup of Experiment Website and Back-End Server
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/webserver` to step into the project folder
 3. Run `docker-compose up -d` to start the docker container 
 4. To stop the container use `docker-compose stop`

### Setup of Data-Pipeline
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/data_pipeline` to step into the project folder
 3. Run `docker-compose up -d` to start the docker container 
 4. To stop the container use `docker-compose stop`

Note that you only need to clone the repository once.


## Setup Development
### Prerequisites
 - npm (>= 9.5.1), Node.js (>= 18.16.1), Python (>= 3.10)

### Setup of Experiment Website and Back-End Server
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/webserver` to step into the project folder
 3. Run `npm install` to install all dependencies
 4. Run `npm run dev` to start the webserver
 5. Available in browser under `http:://localhost:8000`



### Setup of Data-Pipeline 
 1. Clone the git repository with `git clone https://github.com/tehillamo/LLM.git`
 2. Run `cd LLM/data_pipeline` to step into the project folder
 3. Create a virtual environment with `python -m venv venv`
 4. Start virtual environment `source venv/bin/activate`
 5. Run `pip install -r requirements.txt` to install python dependencies
 6. Install ffmpeg with `apt-get install ffmpeg`
 7. Start the corresponding script using `python scripts.py` and use `python scripts.py -h` for help
 
Note that you only need to clone the repository once.

---

## Create a Study using jsPsych with Automated Recording
We use the [jsPsych](https://www.jspsych.org/) framework to run our study. You can specify the different trials in `/webserver/public/src/index.js`. To make use of the recordings you need to specify the first and last trial, as well as a callback function. To track the trials, it is necessary to initialize jsPsych with a trigger functions. `onTrialStartRecording(trial);` starts the recording as `onTrialFinishRecording(trial);` ends the recording of this trial and sends it to our server. When the study has finished, we send the data to our server using `sendData();`.
```js
var jsPsych = initJsPsych({
  on_trial_start: function(trial) {
    onTrialStartRecording(trial);
  },
  on_trial_finish: function(trial) {
    onTrialFinishRecording(trial);
  },
  on_finish: function() {
    sendData(jsPsych.data.allData.trials);
  }
});
```
Then we specify our trials. The first and last trial should both be `jsPsychSpeechRecording`. The first trial indicates the start (`start: true`). The last trial specifies the end (`start: false`). The actual study trials can be declared between the two recording trials. If you need other plugins import them in `/webserver/public/index.html`. Just wrap the `jsPsychSpeechRecording` around your study trials.
```js
const trials = [
  {
    type: jsPsychSpeechRecording,
    start: true
  },
    ...
  {
    type: jsPsychSpeechRecording,
    start: false
  }
];
```
After that, we can run the study.
```js
jsPsych.run(trials);
```
The implementation of the `jsPsychSpeechRecording` plugin can be found in `/webserver/public/jspsych/dist/plugin-recording.js`. Note that you must include the script in the html file.

## Ressources & Outputs
All recordings and the trial data will be saved per default to the `ressources` folder. Each participant has a unique, random and anonymous id. For each participant we create a new folder inside `ressources`. In this folder you can find the whole recording, the timestamps which indicate when each trial started in ms, and the trial data.

## Evaluation Script
We offer various scripts to automatically assess verbal report recordings. In the following sections, we describe each script's function and how to employ it.
Initially, we slice the audio by the trial timestamps, yielding one recording per trial. Next, we transcribe each of these trial recordings utilising OpenAI's whisper model [[1]](#references). 
This constitutes the essential element of our framework. With the transcribed records, we can conduct diverse analyses.
### Sentence Embeddings
We use Sentence-BERT [[2]](#references) to obtain embeddings for each transcribed verbal report. Now, we can epmloy numerical methods to analyse, e.g. similarity, clusters and general answer structures.

## Citing & Authors
If you use our framework in yours studies or use it in your research, feel free to cite our work.
```
...
```



## References
[1] Radford, A., Kim, J.W., Xu, T., Brockman, G., Mcleavey, C. &amp; Sutskever, I.. (2023). Robust Speech Recognition via Large-Scale Weak Supervision. <i>Proceedings of the 40th International Conference on Machine Learning</i>, in <i>Proceedings of Machine Learning Research</i> 202:28492-28518 Available from https://proceedings.mlr.press/v202/radford23a.html.

[2] Reimers, N., & Gurevych, I. (2019). Sentence-bert: Sentence embeddings using siamese bert-networks. arXiv preprint arXiv:1908.10084.



