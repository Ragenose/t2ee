FROM node:13.6.0

# install chrome for protractor tests
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update && apt-get install -yq google-chrome-stable

# set working directory
WORKDIR /webpage

COPY . /webpage
RUN npm install
RUN npm install -g @angular/cli@7.3.9

CMD ng serve --host webpage --port 4201 --disableHostCheck true