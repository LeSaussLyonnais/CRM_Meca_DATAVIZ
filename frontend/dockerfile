FROM node:16-alpine

WORKDIR /app/frontend/

COPY package*.json /app/frontend/
RUN npm install
RUN npm install chart.js@3.7.0
RUN npm install websocket


COPY . /app/frontend/

CMD ["npm", "start"]