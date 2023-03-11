FROM python
COPY . /app
WORKDIR /app
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt
RUN sed -i "s@http://\(deb\|security\).debian.org@https://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN apt update && apt install redis -y && apt install cron -y
EXPOSE 8000
CMD python3 ./manage.py runserver 0.0.0.0:8000