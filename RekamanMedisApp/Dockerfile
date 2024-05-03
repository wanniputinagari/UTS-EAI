# base image
FROM python:3.9

# set working dir
WORKDIR /app

# copy package 
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

# expose port
EXPOSE 4000

# run app
CMD ["python", "RekamanMedis.py"]