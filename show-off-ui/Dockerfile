FROM node:14-alpine

WORKDIR app

COPY . .

RUN yarn install && yarn build && yarn global add serve

EXPOSE 3000

CMD serve -s build:prod