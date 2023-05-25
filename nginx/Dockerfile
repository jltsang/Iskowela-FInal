FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template
RUN envsubst '8000 5005' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/nginx.conf
