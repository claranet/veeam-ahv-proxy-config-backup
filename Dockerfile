FROM python:3.9-alpine

LABEL version="1.0.0" \
      author="Martin Weber <martin.weber@de.clara.net>"

ENV PROXY_HOSTNAME="" \
    PROXY_USERNAME="veeam" \
    PROXY_PASSWORD="" \
    BACKUP_PASSWORD="" \
    OUT_DIR="/backup"

WORKDIR /usr/src/app

COPY entrypoint.sh /
COPY ./backup.py ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

VOLUME [ "/backup" ]

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ ]
