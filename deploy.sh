#!/bin/bash

AWS_REGION="us-east-1"
AWS_ACCOUNT_ID="<aws_account_id>"
REPO_NAME="minha-lambda"
IMAGE_NAME="lambda-custom-python-lambda-dev"
IMAGE_TAG="latest"
LAMBDA_FUNCTION_NAME="minha-lambda-funcao"
LAMBDA_ROLE_ARN="arn:aws:iam::<aws_account_id>:role/seu-iam-role-para-lambda"

# Login no ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Cria o repositório caso não exista
aws ecr describe-repositories --repository-names $REPO_NAME --region $AWS_REGION >/dev/null 2>&1 || \
aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION

# Tag e push da imagem
docker tag $IMAGE_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG

# Cria ou atualiza a função Lambda
aws lambda get-function --function-name $LAMBDA_FUNCTION_NAME --region $AWS_REGION >/dev/null 2>&1

if [ $? -eq 0 ]; then
  echo "Atualizando função Lambda..."
  aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME --image-uri $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG --region $AWS_REGION
else
  echo "Criando função Lambda..."
  aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --package-type Image \
    --code ImageUri=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$IMAGE_TAG \
    --role $LAMBDA_ROLE_ARN \
    --region $AWS_REGION
fi

