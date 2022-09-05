FROM node:7.7.2-alpine
COPY package.json /
COPY package-lock.json /
WORKDIR /
RUN npm i
COPY index.js /
ENTRYPOINT ["node", "index.js"]