# Human Activity Prediction App

### Problem Statement
Designing a service that predicts user activities like running, walking, sitting etc. from smartphone sensors data.


### Solution Proposed 
The solution model trains a linear SVM model to predict human activities

## Tech Stack Used
1. Python 
2. Pandas
3. AWS
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. Terraform


## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for some data storage. You also need AWS account to access S3, EC2 Services. You also need to have terraform installed and configured


## Project Architecture
![image](https://github.com/bsb4018/activity_pred_main_proj/blob/main/images/HLD_MODEL_PIPELINE.png)


### Step 1: Clone the repository
```bash
git clone https://github.com/bsb4018/activity_pred_main_proj.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -p venv python=3.8 -y
```

```bash
conda activate venv/
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### Step 4 - Create AWS Account and do the following get the following ids
```bash
Create three S3 bucket with unique names 
Goto activity/constant/s3_bucket.py and Replace the names accordingly
Create another S3 bucket with with any name "abc"
Goto infra/main.tf and replace the name under "aws_s3_bucket_acl" resource to "abc"
Get a note of the following
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION_NAME
```

### Step 5 - Create Mongo DB Atlas Cluster and Create the following 
```bash
Database with name "recsysdb"
collection with name "courses_tagwise"         
collection with name "course_name_id"
Get the MONGODB_URL
```

### Step 6 - Export the environment variable(LINUX) or Put in System Environments(WINDOWS)
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_REGION_NAME=<AWS_REGION_NAME>

export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.3gdw4s.mongodb.net/?retryWrites=true&w=majority"
```

### Step 7 - Start locally
```bash
python main.py
```

## Runing Through Docker

1. Check if the Dockerfile is available in the project directory

2. Build the Docker image
```
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID> --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> --build-arg AWS_REGION_NAME=<AWS_REGION_NAME> --build-arg MONGODB_URL=<MONGODB_URL> . 

```

3. Run the Docker image
```
docker run -d -p 8090:8090 <IMAGE_NAME>
```
