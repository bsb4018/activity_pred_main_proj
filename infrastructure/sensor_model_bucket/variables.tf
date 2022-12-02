variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "model" {
  type    = string
  default = "activity-model"
}

variable "aws_account_id" {
  type    = string
  default = "487410058179"
}

variable "force_destroy_bucket" {
  type    = bool
  default = true
}
