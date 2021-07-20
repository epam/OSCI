FROM mcr.microsoft.com/azure-functions/python:3.0-python3.7-appservice

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY __app__/requirements.txt /
RUN pip install -r /requirements.txt

COPY osci/requirements.txt /home/site/wwwroot/osci/
RUN pip install -r /home/site/wwwroot/osci/requirements.txt

COPY __app__ /home/site/wwwroot
COPY osci /home/site/wwwroot/osci
COPY README.md /home/site/wwwroot
COPY LICENSE /home/site/wwwroot
COPY setup.py /home/site/wwwroot

WORKDIR /home/site/
RUN pip install -e wwwroot/

EXPOSE 80
