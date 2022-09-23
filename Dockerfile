FROM python:3.9-alpine
ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV}
   # PIPENV_DOTENV_LOCATION=config/.env

# Creating folders, and files for a project:
COPY . /code
WORKDIR /code
RUN apk update
RUN apk add --no-cache \
   build-base \
   g++ \
   cairo-dev \
   pango-dev \
   nodejs \
   npm

# js install
RUN npm run build --prefix /code/apps/ticketscraping/js 

# python install
RUN pip install pipenv
RUN pipenv install $(test "$DJANGO_ENV" == production || echo "--dev") --deploy --system --ignore-pipfile

# start the server
CMD ["gunicorn", "tmtracker.wsgi:application", "-b", "0.0.0.0:8080", "--log-file=/log/message.log"]
