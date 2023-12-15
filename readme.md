# Automated Analysis of Verbal Reports
This is a sample implementation of our automated verbal reports analysis framework. The framework allows you to conduct your jsPsych study whilst recording the participants. Subsequently, analyses can be replicated by executing our data-pipeline.
## Overview
- [Automated Analysis of Verbal Reports](#automated-analysis-of-verbal-reports)
  - [Overview](#overview)
  - [Download Code](#download-code)
    - [Git (recommended)](#git-recommended)
    - [Download Zip file](#download-zip-file)
  - [Setup Development](#setup-development)
    - [Prerequisites](#prerequisites)
    - [Setup of Experiment Website and Back-End Server](#setup-of-experiment-website-and-back-end-server)
    - [Run the Data-Pipeline](#run-the-data-pipeline)
  - [Setup Production (Server)](#setup-production-server)
    - [Prerequisites](#prerequisites-1)
    - [Setup of Experiment Website and Back-End Server](#setup-of-experiment-website-and-back-end-server-1)
    - [Run the Data-Pipeline](#run-the-data-pipeline-1)
  - [Create a Study using jsPsych with Automated Recording](#create-a-study-using-jspsych-with-automated-recording)
  - [Ressources \& Outputs](#ressources--outputs)
  - [Evaluation Script](#evaluation-script)
    - [Speech2Text](#speech2text)
    - [Sentence Embeddings](#sentence-embeddings)
    - [Dimensionality Reduction](#dimensionality-reduction)
    - [Custom Scripts](#custom-scripts)
    - [Merge Behavioral Data](#merge-behavioral-data)
    - [Output](#output)
  - [Citing \& Authors](#citing--authors)
  - [References](#references)

You can choose between the setup for developing and a setup for production. We recommend testing and developing your study locally on your own computer. After everything works, you can run the setup on the server.

---


## Download Code
You can obtain the code using **either** one of the following ways:

### Git (recommended)
Open a console to check if Git is already installed. Open your terminal and type:
```
git --version
```
If Git is not installed, you need to install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). Then open your terminal and navigate to a preferred folder and run:
```
git clone https://github.com/tehillamo/LLM.git
```

### Download Zip file
Navigate in your browser to our GitHub repository [https://github.com/tehillamo/LLM](https://github.com/tehillamo/LLM). Then click on the green button `<> Code` and click on `Download ZIP`. After that, you need to unzip the file in a folder of your choice.

## Setup Development
### Prerequisites
 - npm (>= 9.5.1), Node.js (>= 18.16.1), Python (>= 3.10)

### Setup of Experiment Website and Back-End Server
 1. Open your terminal and navigate to our framework folder
 2. Run `cd LLM/webserver` to step into the webserver folder
 3. Run `npm install` to install all dependencies
 4. Run `npm run dev` to start the webserver
 5. Available in browser under `http:://localhost:8000`

### Run the Data-Pipeline 
 1. Open your terminal and navigate to our framework folder
 2. Run `cd LLM/data_pipeline` to step into the data pipeline folder
 3. We would recommend to create a virtual environment with `python -m venv venv`. If you do not want to do that skip to step 5
 4. Start virtual environment `source venv/bin/activate`
 5. Run `pip install -r requirements.txt` to install python dependencies
 6. Install [ffmpeg](https://www.ffmpeg.org/download.html)
 7. Start the corresponding script using `python scripts.py` and use `python scripts.py -h` for help

## Setup Production (Server)
### Prerequisites
 - Install [Docker](https://docs.docker.com/engine/install/) and [Docker-Compose](https://docs.docker.com/compose/install/)
  
### Setup of Experiment Website and Back-End Server
 1. Open your terminal and navigate to our framework folder
 2. Run `cd LLM/webserver` to step into the webserver folder
 3. Run `docker-compose -f docker-compose-prod.yaml up --build -d` to start the docker container 
 4. Available in browser under `http:://localhost:8080`
 5. To stop the container use `docker-compose stop`

### Run the Data-Pipeline
 1. Open your terminal and navigate to our framework folder
 2. Run `cd LLM/data_pipeline` to step into the data pipeline folder
 3. Run `docker-compose up -d` to start the docker container 
 4. To stop the container use `docker-compose stop`

---

## Create a Study using jsPsych with Automated Recording
We use the [jsPsych](https://www.jspsych.org/) framework to run our study. You can specify the different trials in [`/webserver/public/src/index.js`](/webserver/public/src/index.js). To make use of the recordings you need to specify the first and last trial, as well as some callback functions. To track the trials, it is necessary to initialize jsPsych with a trigger functions. `onTrialStartRecording(trial);` starts the recording as `onTrialFinishRecording(trial);` ends the recording of this trial and sends it to the server. When the study has finished, we send the data to the server using `sendData();`.
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
Then we specify our trials. The first and last trial should both be `jsPsychSpeechRecording`. The first trial indicates the start (`start: true`). The last trial specifies the end (`start: false`). The actual study trials can be declared between the two recording trials. If you need other plugins import them in [`/webserver/public/index.html`](/webserver/public/index.html). Just wrap the `jsPsychSpeechRecording` around your study trials.
```js
const trials = [
  {
    type: jsPsychSpeechRecording,
    start: true
  },
    // add your study trials here
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
The implementation of the `jsPsychSpeechRecording` plugin can be found in [`/webserver/public/jspsych/dist/plugin-recording.js`](/webserver/public/jspsych/dist/plugin-recording.js). Note that you must include the script in the html file. 
Our memory task study can be found in [`/webserver/public/index.html`](/webserver/public/index.html). You can find a template to integrate you own study here [`/webserver/public/index_template.html`](/webserver/public/index_template.html).

## Ressources & Outputs
All recordings and the trial data will be saved per default to the [`ressources`](ressources) folder. Each participant has a unique, random and anonymous id. For each participant we create a new folder inside [`ressources`](ressources). In this folder you can find the recordings and the behavioral data from the study.

## [Evaluation Script](data_pipeline/scripts.py)
We offer various scripts to automatically assess verbal report recordings. In the following sections, we describe each script's function and how to employ it. Our script is built in a modular fashion such that more scripts can be easily integrated. Furthermore the used machine learning models can also be changed. If you added scripts feel free to open a pull request such that we can add them to our repository.

### [Speech2Text](data_pipeline/speech2text.py)
This script transcribes the recordings into text. We are using OpenAI's whisper model [[1]](#references) for this. 

### [Sentence Embeddings](data_pipeline/embeddings.py)
We use Sentence-BERT [[2]](#references) to obtain embeddings for each transcribed verbal report. 

### [Dimensionality Reduction](data_pipeline/dimensionality_reduction.py)
We implemented three techniques to reduce the dimensionality:
- PCA
- t-SNE
- combination of PCA and t-SNE

### [Custom Scripts](data_pipeline/custom_scripts.py)
This is a collection of scripts we used for our analysis. These scripts may not be applicable to other scenarios, but we included them for the sake of completeness.

### [Merge Behavioral Data](data_pipeline/merge_behavioral_data.py)
In the last step we merge the data obtained from the study with the earlier computed data (transcribed text, embeddings, lower dimensional embeddings).

### Output
You can find the output of the evaluation script in `/output/`. The script produces a CSV file.

| CSV column        | Explanation | 
| :----------------: | :------ | 
| uuid        |   UUID of each participant (unique)   | 
| trial_number           |   Trial number of the study   | 
| transcribed_text    |  Transcribed text from the recording    | 
| embedding |  Embedding obtained from SentenceBERT   | 
| embedding_reduced_pca |  Lower dimensional embedding (PCA)   | 
| embedding_reduced_tsne |  Lower dimensional embedding (t-SNE)   | 
| embedding_reduced_both |  Lower dimensional embedding (first PCA to 50 dimensions, then t-SNE)   | 


## Citing & Authors
If you use our framework in yours studies or use it in your research, feel free to cite our work.
```
...
```



## References
[1] Radford, A., Kim, J.W., Xu, T., Brockman, G., Mcleavey, C. &amp; Sutskever, I.. (2023). Robust Speech Recognition via Large-Scale Weak Supervision. <i>Proceedings of the 40th International Conference on Machine Learning</i>, in <i>Proceedings of Machine Learning Research</i> 202:28492-28518 Available from https://proceedings.mlr.press/v202/radford23a.html.

[2] Reimers, N., & Gurevych, I. (2019). Sentence-bert: Sentence embeddings using siamese bert-networks. arXiv preprint arXiv:1908.10084.



