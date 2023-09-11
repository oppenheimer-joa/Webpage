# myapp/management/commands/fetch_images.py

import boto3  # S3를 사용하기 위한 라이브러리
import requests  # HTTP 요청을 보내기 위한 라이브러리
from posts.models import ExternalImageModel

# 영화 상세정보 가져오기
def fetch_movie_details():
    from configparser import ConfigParser
    import fastparquet
    import pandas as pd

    parser = ConfigParser()
    parser.read("/Users/kimdohoon/git/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access,
    aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/')
    
    combined_df = None

    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_stream = s3_object['Body'].read()
        
        df = fastparquet.ParquetFile(BytesIO(parquet_stream)).to_pandas()
        
        if combined_df is None:
            combined_df = df
        else:
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    image_urls = []
    image_base_url = 'https://image.tmdb.org/t/p/original' 
    for idx, row in combined_df.iterrows():
        # movie_id = row['movie_id']
        # movie_nm = row['movie_nm']
        poster_path = f"{image_base_url}{row['poster_path']}"
        image_urls.append(poster_path)

    return image_urls


if __name__ == "__main__":

    # 영화 상세정보를 가져올 movie_id
    movie_id = 'your_movie_id'

    # 영화 상세정보 가져오기
    image_urls = fetch_movie_details(movie_id)

    # 생성된 이미지 URL을 ExternalImageModel에 추가
    for url in image_urls:
        ExternalImageModel.objects.create(image_url=url)
        print(f'Successfully added image from {url}')

