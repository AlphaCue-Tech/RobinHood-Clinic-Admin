# Dockerfile
FROM python:3.9-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log


# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/RobinHoodAdmin
COPY requirements.txt start-server.sh /opt/app/
COPY .pip_cache /opt/app/pip_cache/
COPY . /opt/app/RobinHoodAdmin/
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app

# start server
EXPOSE 8020
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]

#https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-applicationssss
#https://semaphoreci.com/community/tutorials/dockerizing-a-python-django-web-application

#docker build --no-cache  -t robinhood .
#docker build --no-cache -t robinhood -f robinhood .
#docker run -it -p 8020:8020 -e DJANGO_SUPERUSER_USERNAME=xian -e DJANGO_SUPERUSER_PASSWORD=xian -e DJANGO_SUPERUSER_EMAIL=admin@example.com robinhood

#waitress-serve --listen=*:8000 RobinHoodAdmin.wsgi:application


# Docker A-Z project
#https://subscription.packtpub.com/book/web-development/9781838987428/1/ch01lvl1sec18/working-with-docker-containers-for-django-gunicorn-nginx-and-postgresql