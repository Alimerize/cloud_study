provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  # ЭТИ СТРОКИ ГОВОРЯТ: "НЕ ХОДИ В НАСТОЯЩИЙ AMAZON ЗА ПРОВЕРКАМИ"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3  = "http://localhost:4566"
    sts = "http://localhost:4566" # Добавили еще этот эндпоинт для тишины
  }
}

resource "aws_s3_bucket" "my_future_bucket" {
  bucket = "success-storage-2026"
}

resource "aws_s3_bucket" "my_archive_bucket" {
    bucket = "archive-storage-2026"
}
