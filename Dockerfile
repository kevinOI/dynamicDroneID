# syntax=docker/dockerfile:1

FROM node:18-alpine
WORKDIR /app
copy . .
RUN yarn install --production
CMD 
