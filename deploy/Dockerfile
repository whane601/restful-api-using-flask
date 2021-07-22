# Base image
FROM ubuntu:16.04

# Apt
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    libxext6 \
    git \
    python3-setuptools \
    python3-pip \
    locales \
    cron \
    wget \
    logrotate \
    vim-tiny \
    bash-completion \
    netcat \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Setup language environment
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# install Python 3.9
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.9 python3.9-dev python3.9-venv
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.9 get-pip.py pip==20.2.4 --force-reinstall
RUN rm -rf get-pip.py

# set Python 3.9 as default python/python3 command version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1
RUN update-alternatives --set python /usr/bin/python3.9
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN update-alternatives --set python3 /usr/bin/python3.9

# install Python requirements
COPY requirements.txt /tmp
RUN pip3 install --no-cache-dir --ignore-installed -r /tmp/requirements.txt

# final
WORKDIR /opt/app_workspace
CMD tail -f /dev/null
