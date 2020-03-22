# based on https://gist.githubusercontent.com/kmmanoj/d1e256469379a24beffb6e0a9aab76c3/raw/ccd69a745bb30e88ed5f89e1248312e24ab51481/dockerfile
FROM python:alpine
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "backend:app"]
