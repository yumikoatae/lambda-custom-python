FROM public.ecr.aws/lambda/python:3.12

WORKDIR /var/task

# Copia todo o código da aplicação (inclui o requirements.txt)
COPY src/ ./

# Agora sim: instala os pacotes dentro da própria pasta da app
RUN pip3 install -r requirements.txt -t .

# Substitui o bootstrap padrão da AWS
COPY src/runtime/bootstrap.py /var/runtime/bootstrap
RUN chmod +x /var/runtime/bootstrap

# Script de entrada que decide se roda dev ou prod
COPY docker/python3/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

