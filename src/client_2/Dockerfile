FROM node:16
WORKDIR /app
COPY package*.json /app
RUN npm install --save-dev
COPY . /app
CMD ["npm", "run", "dev"]