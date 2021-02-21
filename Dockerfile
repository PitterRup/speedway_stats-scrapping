FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade ipython
RUN ipython profile create
RUN echo "c.InteractiveShell.colors = 'Neutral'" >> /root/.ipython/profile_default/ipython_config.py
RUN echo "c.InteractiveShell.color_info = True" >> /root/.ipython/profile_default/ipython_config.py
RUN echo "c.TerminalInteractiveShell.colors = 'Neutral'" >> /root/.ipython/profile_default/ipython_config.py

COPY . .

CMD [ "python", "manage.py", "-c", "api.config", "runserver", "-h", "0.0.0.0", "-p", "5000", "-d"]
