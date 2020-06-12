#adapted from https://github.com/heroku-examples/python-miniconda
FROM heroku/miniconda

# Grab requirements.txt.
ADD requirements.txt 

# Install dependencies
RUN pip install -qr requirements.txt

# Add our code
ADD ./ /opt/
WORKDIR /opt/

RUN conda install scikit-learn

CMD gunicorn --bind 0.0.0.0:$PORT wsgi


