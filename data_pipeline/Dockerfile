FROM python:3.10-bullseye

WORKDIR /usr/src/app

COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# install ffmpeg
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg

COPY . .

CMD [ "python", "-u", "scripts.py", "--device", "cpu"]
#python3 scripts.py --path ../ressources --output ../output --behavioral_columns stimulus response rt pair
