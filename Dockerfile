# base image
FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install refget-compliance
RUN python setup.py install

# set python path to current dir
ENV PYTHONPATH /usr/src/app

# port for serving the complaince report
EXPOSE 15800

# run the command
ENTRYPOINT ["refget-compliance", "report"]
