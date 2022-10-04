FROM nginx:lastest
LABEL contributers="Team E-kuzo"

RUN mkdir /etc/live
RUN mkdir /app
WORKDIR /app


#static 파일들 들어가 있는 디렉토리
# COPY ./build ./build

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/nginx.conf

COPY live/. /etc/live/.


EXPOSE 80
EXPOSE 443

CMD ["nginx","-g","daemon off;"]