FROM node:14-alpine

WORKDIR app

COPY . .

EXPOSE 3000

RUN yarn build
RUN yarn global add serve

CMD serve -s build