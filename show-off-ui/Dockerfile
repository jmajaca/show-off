FROM node:14-alpine as build-image

WORKDIR app

COPY . .

RUN yarn install && yarn "build:prod"

FROM nginx:alpine

COPY --from=build-image /app/build /bin/www

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000