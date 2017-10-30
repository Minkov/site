FROM jeffersfp/xenial-python2

RUN apt-get update
RUN apt install -y curl
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash
RUN apt-get install -y python-dev python-pip python-setuptools python-mysqldb nodejs ruby-full fonts-lmodern apt-utils libmysqlclient-dev gettext
RUN apt install -y git
RUN apt-get clean

RUN useradd --user-group --home /usr/src django
RUN chown django:django -R /usr/src

RUN pip install virtualenv

USER django
RUN mkdir -p /usr/src/env
RUN virtualenv /usr/src/env

RUN /usr/src/env/bin/pip install --upgrade pip
RUN /usr/src/env/bin/pip install mysql-python

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN /usr/src/env/bin/pip install -r requirements.txt
RUN /usr/src/env/bin/pip install mysql-python mysqlclient websocket-client


ADD . /usr/src/app

USER root
RUN chown django:django -R /usr/src

RUN gem install sass compass
RUN npm install -g pleeease-cli

USER django

ENV DJANGO_SETTINGS_MODULE=dmoj.settings

#RUN	echo "yes" | /usr/src/env/bin/python manage.py collectstatic

EXPOSE 8000
CMD /usr/src/env/bin/python manage.py runserver 0.0.0.0:8000
