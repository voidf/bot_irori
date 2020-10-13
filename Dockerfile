#基于的基础镜像
FROM alpine:latest

RUN mkdir /irori && \
sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
apk update && apk add python3 && apk add py3-pip && \
apk add make automake gcc g++ subversion python3-dev && \
apk add curl bash openjdk8-jre-base && \
apk add jpeg-dev zlib-dev && \
rm -rf /var/cache/apk/* && \
pip3 install -U pip && \
pip3 install wheel && \
wget https://github.com/iTXTech/mirai-console-loader/releases/download/v1.0.0/mirai-console-loader-1.0.0.zip && \
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

#代码添加到code文件夹，后面可以通过进入容器中看的
COPY ./ /irori

# 设置code文件夹是工作目录
WORKDIR /irori

ENV JAVA_HOME /usr/lib/jvm/default-jvm
ENV PATH ${PATH}:${JAVA_HOME}/bin

#当容器启动时，使用python3执行指定路径的py脚本
CMD ["python3", "irori.py"]