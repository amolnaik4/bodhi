FROM alpine:latest


RUN apk add --no-cache python \
		python-dev \
		py-pip \
		chromium \ 
		chromium-chromedriver

COPY . /bodhi_app
WORKDIR /bodhi_app
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 80 8000
ENTRYPOINT ["/bin/sh"]
CMD ["run.sh"]
