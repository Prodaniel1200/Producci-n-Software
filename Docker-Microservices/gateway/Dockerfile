<<<<<<< HEAD
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY build/ /usr/share/nginx/html
=======
FROM devopsfaith/krakend:2.6

COPY krakend.json /etc/krakend/krakend.json

EXPOSE 8080

CMD ["run", "-c", "/etc/krakend/krakend.json"]
>>>>>>> 8fab604 (dockerfile corregido de auth para azure)
