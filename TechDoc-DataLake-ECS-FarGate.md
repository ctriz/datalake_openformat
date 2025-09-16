

# Running PySpark + Hudi on AWS ECS Fargate

This document captures the high level steps to package a PySpark + Hudi app into a Docker container, deploy it to AWS ECS Fargate, and validate execution

## Package Python Code as a Wheel

-   Organize source code under a Python package (`hudi_app/`).
    
-   Add a `setup.py` with `entry_points` for scripts (`hudi_trips_cow`, `hudi_trips_mor`).
    
-   Build the wheel:

    pip install --upgrade build    python -m build

Output: `.whl` in `dist/`.

## Build and Verify Docker Image
-   Base image: `bitnami/spark:3.5.0`.
-   Copy the `.whl` and install it inside container.
-   Add Hudi bundle JAR into Spark jars path.
-   Example local test:
   
## Push to Amazon ECR

Create an ECR repo:

    aws ecr create-repository --repository-name hudi-ecs

Authenticate & Push

     aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 		 <acct>.dkr.ecr.us-east-1.amazonaws.com
     
     docker tag hudi-ecs:latest <acct>.dkr.ecr.us-east-1.amazonaws.com/hudi-ecs:latest docker push  <acct>.dkr.ecr.us-east-1.amazonaws.com/hudi-ecs:latest

Create ECS Cluster

     aws ecs create-cluster --cluster-name hudi-cluster

Define ECS Task
 
    {
          "family": "hudi-task",
          "networkMode": "awsvpc",
          "requiresCompatibilities": ["FARGATE"],
          "cpu": "2048",
          "memory": "8192",
          "executionRoleArn": "arn:aws:iam::<acct>:role/ecsTaskExecutionRoleHudi",
          "taskRoleArn": "arn:aws:iam::<acct>:role/ecsTaskRoleHudi",
          "containerDefinitions": [
            {
              "name": "hudi-job",
              "image": "<acct>.dkr.ecr.us-east-1.amazonaws.com/hudi-ecs:latest",
              "essential": true,
              "entryPoint": ["python", "-m"],
              "command": ["hudi_trips_cow"],
              "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                  "awslogs-group": "/ecs/hudi",
                  "awslogs-region": "us-east-1",
                  "awslogs-stream-prefix": "hudi"
                }
              }
            }
          ]
        }

Register it:

    aws ecs register-task-definition --cli-input-json file://task-def.json

## Networking Setup (VPC + Public Subnet)

-   Ensure:
    
    -   Subnet has **Auto-assign Public IP = Enabled**.
        
    -   Internet Gateway is attached to VPC.
        
    -   Security group allows egress (0.0.0.0/0) and ingress (optional, for debugging).

## Run Task

     aws ecs run-task \   --cluster hudi-cluster \   --launch-type FARGATE
     \   --enable-execute-command \   --network-configuration
     "awsvpcConfiguration={subnets=[subnet-xxxx],securityGroups=[sg-xxxx],assignPublicIp=ENABLED}"
     \   --task-definition hudi-task

## Validate

Check Task Status

       aws ecs describe-tasks --cluster hudi-cluster --tasks <task-arn>

Check logs:

 `aws logs tail /ecs/hudi --follow`



