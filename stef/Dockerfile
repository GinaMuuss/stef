#FROM ubuntu:18.04
FROM jinajita/kivs_evaluate:latest
RUN apt update
RUN apt install -y python3 python3-pip openjdk-8-jdk
RUN pip3 install pipenv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY ./ /evaluation/solution/
RUN if [ -f "/evaluation/solution/run.sh" ]; then chmod +x /evaluation/solution/run.sh; fi
RUN if [ -f "/evaluation/solution/setup.sh" ]; then chmod +x /evaluation/solution/setup.sh; fi
