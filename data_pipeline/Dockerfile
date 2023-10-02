FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# install ffmpeg
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY . .

CMD [ "python", "speech2text.py" , "--path", "./ressources", "--transcribe", "--output-path", "./output"]
#CMD [ "python", "speech2text.py" , "-h"]
