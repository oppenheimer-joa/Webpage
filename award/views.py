from django.shortcuts import render
from configparser import ConfigParser
import boto3
import pandas as pd
from io import BytesIO
import pyarrow.parquet as pq
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_award_list(festa_name):
    parser = ConfigParser()
    # parser.read('/home/neivekim76/config/config.ini')
    parser.read("./config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    s3 = boto3.client('s3', aws_access_key_id=access,
    aws_secret_access_key=secret)
    
    prefix = f'imdb/all/parquet/festa_name={festa_name}/'
    bucket = 'sms-warehouse'
    # S3 버킷에서 객체 목록 가져오기
    objects = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    # 빈 DataFrame 생성
    combined_df = pd.DataFrame()

    # 각 객체(파일)에 대해 반복
    for obj in objects.get('Contents', []):  # 만약 'Contents'가 없으면 빈 리스트를 반환
        file_key = obj.get('Key', '')  # 파일의 S3 키를 가져옴
        if file_key.endswith('.parquet'):  # parquet 파일만 처리
            s3_object = s3.get_object(Bucket=bucket, Key=file_key)
            parquet_stream = s3_object['Body'].read()
            table = pq.read_table(BytesIO(parquet_stream))
            df = table.to_pandas()
            combined_df = pd.concat([combined_df, df])
    award_list = combined_df.to_dict('records')
    
    # year 컬럼에서 중복을 제거한 후 리스트로 변환
    years = combined_df['year'].drop_duplicates().tolist()
    years = sorted(years, reverse=True)
    return award_list, years

def award_list(request):
    academy, academy_years = get_award_list('academy')
    cannes, cannes_years = get_award_list('cannes')
    venice, venice_years = get_award_list('venice')
    busan, busan_years = get_award_list('busan')
    context = {'academy': academy, 'academy_years': academy_years, 'cannes': cannes, 'cannes_years': cannes_years, 'venice': venice, 'venice_years': venice_years, 'busan': busan, 'busan_years': busan_years}
    
    return render(request, 'award/award_list.html', context)
    

def award_detail(request, festa_name, year):
    award_list, years = get_award_list(festa_name)
    specific_year_awards = [award for award in award_list if award['year'] == str(year)]
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 (Paginator(people_list, 5))
    paginator = Paginator(specific_year_awards, 20)
    # 초기 시작 페이지 설정
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
        
    if festa_name == 'academy':
        festa = 'ACADEMY'
    elif festa_name == 'cannes':
        festa = 'CANNES'
    elif festa_name == 'venice':
        festa = 'VENICE'
    elif festa_name == 'busan':
        festa = 'BUSAN'

    context = {'award':specific_year_awards, 'festa_name':festa, 'year':year, 'pages':pages}
    
    return render(request, 'award/award_detail.html', context)