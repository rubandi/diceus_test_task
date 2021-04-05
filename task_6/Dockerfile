FROM python:3.8.3

WORKDIR /app

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update \
    && apt-get -y install google-chrome-stable libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    && apt-get clean

RUN wget -q "https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip

ADD tests/ /app/
RUN pip install selenium pytest

CMD ["pytest", "test.py"]