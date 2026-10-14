FROM python:3.12.4

RUN pip3 install pip==26.1.1
RUN pip3 install \
    jupyterlab==4.5.7 \
    pandas==3.0.3 \
    numpy==2.4.6 \
    matplotlib==3.10.9 \
    scikit-learn==1.8.0

RUN apt-get update && apt-get install -y software-properties-common npm
RUN npm install n@10.2.0 -g && n 24.15.0

RUN jupyter lab --generate-config
RUN echo "c.LabApp.token = ''" >> $HOME/.jupyter/jupyter_lab_config.py
RUN echo "c.LabApp.password = u''" >> $HOME/.jupyter/jupyter_lab_config.py

CMD jupyter lab --allow-root --ip 0.0.0.0 --no-browser --port 8888
