FROM ubuntu:20.04

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# Export ARGs as ENV vars so they can be shared among steps
ENV DEBIAN_FRONTEND=noninteractive \
    APT_OPTS="-q=2 --yes"

# Install build dependencies
RUN apt-get -qq update && \
    apt ${APT_OPTS} --no-install-recommends install apt-utils && \
    apt ${APT_OPTS} --no-install-recommends install \
      python3 \
      python3-pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt update
RUN apt install nodejs -y
RUN apt install npm -y

COPY . .

RUN npm install

CMD ["bash","start.sh"]
