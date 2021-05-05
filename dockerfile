FROM postgres

ENV APP /app
WORKDIR $APP
ADD requirements.txt .
ADD res /root/res
ADD dist/VMIntelligence-1.0.1-py2.py3-none-any.whl .
ADD startup.sh .
RUN chmod 755 startup.sh
RUN ./startup.sh