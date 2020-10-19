#基于的基础镜像
FROM alpine:latest

#代码添加到code文件夹，后面可以通过进入容器中看的
# COPY ./ /irori

RUN apk update && apk add python3 && apk add py3-pip && \
apk add make automake gcc g++ subversion python3-dev && \
apk add curl bash openjdk8-jre-base && \
apk add jpeg-dev zlib-dev unzip screen nano git && \
rm -rf /var/cache/apk/* && \
pip3 install -U pip && \
pip3 install wheel && \
git clone https://github.com/voidf/bot_irori.git /irori && \
wget http://d0.ananas.chaoxing.com/download/aad7ee20c57d3b402b7f254b4f3373de -U "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36" -O env.zip && \
pip3 install -r /irori/requirements.txt && \
unzip env.zip && chmod +x /env/run.sh && cd /env

# 设置code文件夹是工作目录
WORKDIR /irori

ENV JAVA_HOME /usr/lib/jvm/default-jvm
ENV PATH ${PATH}:${JAVA_HOME}/bin

#当容器启动时，使用python3执行指定路径的py脚本
CMD ["python3", "config.py"]