FROM python:2.7.15-alpine

RUN apk add --no-cache chromium \ 
		chromium-chromedriver

COPY ./src/requirements.txt /

RUN pip install -r requirements.txt --no-cache-dir

COPY ./src /bodhi_app
WORKDIR /bodhi_app
EXPOSE 80 8000
ENTRYPOINT ["/bin/sh"]
CMD ["run.sh"]
