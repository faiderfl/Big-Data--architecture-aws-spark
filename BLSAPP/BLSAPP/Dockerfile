 FROM artifactory.bancolombia.corp/devops/python
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install pytest-runner -i https://artifactory.bancolombia.corp/api/pypi/python-org/simple --trusted-host artifactory.bancolombia.corp
 RUN pip install -r requirements.txt -i https://artifactory.bancolombia.corp/api/pypi/python-org/simple --trusted-host artifactory.bancolombia.corp
 ADD . /code/
 CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
 EXPOSE 8000