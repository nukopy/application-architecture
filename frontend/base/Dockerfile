FROM node:14.6.0
LABEL maintainer "nukopy <pytwbf201830@gmail.com>"

WORKDIR /app

# install system packages
RUN apt-get update -y

# install npm packages
COPY ./yarn.lock /app
RUN npm upgrade --global yarn && yarn install

# add src
COPY ./ /app

CMD ["yarn", "start"]