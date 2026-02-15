FROM ubuntu:latest
LABEL authors="berin"

ENTRYPOINT ["top", "-b"]