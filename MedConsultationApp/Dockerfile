# base image
FROM node:14

# set working dir
WORKDIR /app

# copy package .json
COPY package*.json /app

# install dependencies
RUN npm install --production

# copy app.js
COPY KonsultasiMedis.js /app

# expose port
EXPOSE 3000

# run app
CMD ["node", "src/app.js"]