FROM python:3.12

COPY ./ /code/app

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN python -m grpc_tools.protoc -I=./Protocol/proto/ --python_out=. --grpc_python_out=. --pyi_out=. user/user.proto
CMD ["python","main.py"]