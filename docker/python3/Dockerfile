# Dockerfile para imagem AWS Lambda Python customizada
#
# Esta imagem:
# - Usa a imagem base oficial AWS Lambda Python 3.12.
# - Copia o código da aplicação para o diretório padrão /var/task.
# - Instala as dependências Python dentro da pasta da aplicação.
# - Substitui o bootstrap padrão da AWS Lambda por um bootstrap customizado,
#   permitindo controle avançado do runtime.
# - Usa um script entrypoint (/entrypoint.sh) para decidir se executa:
#     * O servidor Flask para testes locais (modo DEV, via variável LAMBDA_ENV=dev).
#     * Ou o runtime oficial da AWS Lambda (modo PROD, padrão).
#
# Com isso, esta imagem é uma solução única e flexível para:
# - Desenvolvimento local e testes com servidor HTTP.
# - Implantação na AWS Lambda via container, para produção.
#
# Essa abordagem simplifica o ciclo de desenvolvimento e implantação,
# evitando a necessidade de imagens separadas para cada ambiente.

FROM public.ecr.aws/lambda/python:3.12
# Usa a imagem oficial AWS Lambda Python 3.12 como base

WORKDIR /var/task
# Define o diretório de trabalho padrão (onde o Lambda espera o código)

COPY src/ ./
# Copia todo o seu código-fonte da pasta src para /var/task

RUN pip3 install -r requirements.txt -t .
# Instala as dependências Python localmente dentro da pasta da aplicação (/var/task)

COPY src/runtime/bootstrap.py /var/runtime/bootstrap
# Substitui o bootstrap padrão da AWS Lambda pelo seu custom bootstrap.py

RUN chmod +x /var/runtime/bootstrap
# Dá permissão de execução para o bootstrap customizado

COPY docker/python3/entrypoint.sh /entrypoint.sh
# Copia o script entrypoint.sh que controla como o container inicia (dev/prod)

RUN chmod +x /entrypoint.sh
# Dá permissão de execução para o script entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
# Define o entrypoint para que o container execute o script ao iniciar

