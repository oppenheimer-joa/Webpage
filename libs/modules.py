import configparser, boto3


def create_s3client():
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    access = config.get("AWS", "S3_ACCESS")
    secret = config.get("AWS", "S3_SECRET")

    # s3 client 생성
    s3 = boto3.client('s3', aws_access_key_id=access,
                      aws_secret_access_key=secret)

    return s3

