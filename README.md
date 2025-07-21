# Adevinta Microservice

A minimal microservice to expose a Bert Sequence Classification.


---

## Introduction

This project demonstrates a simple microservice that initializes and consumes a classification model.

The project is managed using Poetry and contains the following:
* **/src**: contains all app code
* **/tests**: contains all app tests
* **Dockerfile**: used to build the docker image
* **app-deployment.yaml and app-service.yaml**: necessary file to deploy to kubernetes

App carachteristics:
* **App dependencies**: managed using depenency injection
* **Code style**: Black, Isort and PyLint
* **Testing**: 94% with pytest 


---

## Local Setup

If you want to run the application locally, follow the next steps:

1. **Install Poetry** (if not already installed):
   ```
   pipx install poetry==2.1.3
   ```

2. **Initialize project** Copy all files inside a folder and install the project
    ```
    poetry install
    ```
3. **Start the app locally**: The app can be initialized locally running the following command
    ```
    poetry run uvicorn src.entrypoints.cli:app --host 0.0.0.0 --reload
    ```
    Now you can access to http://127.0.0.1:8000/docs# and see the API docs.

4. **Call the API** To predict a text sentiment, you can interact with the Swagger interface or can make an API call using curl
    ```
    curl -X 'POST' \
    'http://127.0.0.1:8000/predict_sentiment' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "text": "I love my new phone, I would by it again for sure!"
    }'
    ```

## Build Docker image

1. **Build Docker image**: The docker image can be build running the following command:
    ```
    docker build -t your-image .
    ```
2. **Run docker image**: Run image to ensure the app is correctly working:
    ```
    docker run -p 8000:8000 your-image
    ```

## Image deployment on EKS


1. **Push image to your repository**: Make the image available by pushing it to your desired Container repository, such as AWS ECR.

2. **Create your cluster**: If your cluster is not created yet, create it. For instance, use this command:
    ```
    eksctl create cluster \
    --name fastapi-cluster \
    --region <your-region> \
    --nodes 2 \
    --node-type t3.medium \
    --managed
    ```


3. **Deploy to EKS using Kubernetes**: Run the following commands, wait for the load balancer to be created and the microservice will be deployed.
    ```
    kubectl apply -f app-deployment.yaml
    kubectl apply -f app-service.yaml
    ```

## AWS considerations
 * Be aware of the security groups of your cluster and Application Load Balancer the app is not reachable
 * 

