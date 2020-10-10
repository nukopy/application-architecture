FROM node:14.6.0
LABEL maintainer "nukopy <pytwbf201830@gmail.com>"

WORKDIR /app

# install system packages
RUN apt-get update -y

# install npm packages
COPY ./package.json /app
COPY ./yarn.lock /app
RUN yarn install

# add src
COPY ./ /app

CMD yarn start