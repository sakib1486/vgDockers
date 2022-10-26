FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

#RUN python -m pip install --upgrade pip
#RUN pip install -U crate geojson
#RUN pip install -U crate geojson pycorenlp git+https://github.com/cande1gut/RedditScore.git gensim tweet-preprocessor python-Levenshtein nltk
#RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-2.3.1/en_core_web_lg-2.3.1.tar.gz
#RUN python -m spacy download en_core_web_lg
#RUN python -m nltk.downloader vader_lexicon
#RUN pip install -U git+https://github.com/crazyfrogspb/RedditScore.git
#RUN python -c 'import stanza; stanza.download("en")'
#RUN [ "python", "-c", "import nltk; nltk.download('vader_lexicon')" ]

COPY ./app /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#EXPOSE 81

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "81"]

