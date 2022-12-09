terraform {
   backend "s3" {
    bucket = "bsb4018-s3-activitypred"
    key    = "terraform.tfstate"
    region = "ap-south-1"
  }
  required_providers {
    random = {
      source = "hashicorp/random"
      version = "3.4.3"
    }
    aws = {
      source = "hashicorp/aws"
      version = "4.45.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

module "sensor_model" {
  source = "./sensor_model_bucket"
}

module "sensor_ecr" {
  source = "./sensor_ecr"
}

module "sensor_ec2" {
  source = "./sensor_ec2"
}
