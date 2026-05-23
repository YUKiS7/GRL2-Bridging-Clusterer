FROM python:3.12.4

RUN pip3 install --upgrade pip
RUN pip3 install \
    jupyterlab \
    pandas \
    numpy \
    matplotlib \
    scikit-learn

RUN apt-get update && apt-get install -y software-properties-common npm
RUN npm install n -g && n stable

RUN jupyter lab --generate-config
RUN echo "c.LabApp.token = ''" >> $HOME/.jupyter/jupyter_lab_config.py
RUN echo "c.LabApp.password = u''" >> $HOME/.jupyter/jupyter_lab_config.py

CMD jupyter lab --allow-root --ip 0.0.0.0 --no-browser --port 8888
