def dataframe_confirm(dataframe, column):
    # try : return_value = dataframe.iloc[0][column]
    try : return_value = dataframe[column].values[0]
    except Exception as e :
        print(e)
        return_value = "ERROR"
    return return_value


# home


def home(request):
    from django.shortcuts import render, redirect
    
    user = request.user
    is_authenticated = user.is_authenticated
    print('user:', user)
    print('is_authenticated:', is_authenticated)

    return render(request, 'posts/DEMO-start.html')


# main


def main(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    context = {
        'user' : user
    }
    return render(request, 'posts/DEMO-main.html', context)


# about


def about(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-about.html')


def outline(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-about-outline.html')


def team(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-about-team.html')

def release(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-about-release.html')

def api(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-about-api.html')


# help


def help(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-help.html')

def faq(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-help-faq.html')

def qna(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-help-qna.html')

def inq(request):
    from django.shortcuts import render, redirect
    from django.core.mail import EmailMessage

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-help-inq.html')


# email

def send_email(request):
    from django.core.mail import send_mail
    from django.shortcuts import render
    from django.http import HttpResponse

    if request.method == 'POST':
        first_name = request.POST.get('leadCapFirstName')
        last_name = request.POST.get('leadCapLastName')
        email = request.POST.get('leadCapEmail')
        company = request.POST.get('leadCapCompany')

        # 이메일 내용 작성
        message = f'이름: {first_name} {last_name}\n이메일 주소: {email}\n문의 사항: {company}'

        try:
            # 이메일 전송
            send_mail('문의 사항', message, email, ['nichijou52@naver.com'])
            return HttpResponse('이메일이 성공적으로 전송되었습니다.')
        except Exception as e:
            return HttpResponse('이메일 전송에 실패하였습니다.')

    return render(request, 'posts/DEMO-help-inq.html')  # Replace 'your_template.html' with your actual template name



# document


def document(request):
    from django.shortcuts import render, redirect

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    return render(request, 'posts/DEMO-document.html')


# dir


def directory(request):
    from django.shortcuts import render, redirect
    from .forms import SearchForm
    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')
    
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            search_term = form.cleaned_data['search_term']

            if category == 'title':
                return redirect(f'/movie/?type={category}&search={search_term}')
            elif category == 'people':
                return redirect(f'/people/?search={search_term}')
    else:
        form = SearchForm()

    context = {
        'user' : user,
        'form' : form
    }

    return render(request, 'posts/DEMO-dir.html', context)
    

# movie


def movie_detail(request, pk):
    from django.shortcuts import render, get_object_or_404, redirect
    from .models import ExternalImageModel
    from configparser import ConfigParser
    import boto3
    import json
    import pandas as pd
    import pyarrow.parquet as pq
    from io import BytesIO
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


    parser = ConfigParser()
    parser.read("./config/config.ini")
    # parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/2023-07-')
    
    combined_df = pd.DataFrame()
    for obj in objects.get('Contents', []):  # 만약 'Contents'가 없으면 빈 리스트를 반환
        file_key = obj.get('Key', '')  # 파일의 S3 키를 가져옴
        if file_key.endswith('.parquet'):  # parquet 파일만 처리
            s3_object = s3.get_object(Bucket='sms-warehouse', Key=file_key)
            parquet_stream = s3_object['Body'].read()
            table = pq.read_table(BytesIO(parquet_stream))
            df = table.to_pandas()
            combined_df = pd.concat([combined_df, df])

    # for obj in objects.get('Contents'):
    #     file_path = f"s3://sms-warehouse/{obj.get('Key')}"
    #     if file_path.find('parquet') == -1:
    #         continue
    #     s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
    #     parquet_stream = s3_object['Body'].read()
    #     table = pq.read_table(BytesIO(parquet_stream))
    #     df = table.to_pandas()
    #     new_df = pd.concat([combined_df, df])

    row = combined_df[combined_df['id'] == pk]
    print(row['backdrop_path'])

    movie_id = dataframe_confirm(row, 'id')
    movie_nm = dataframe_confirm(row, 'original_title')
    movie_dt = dataframe_confirm(row, 'overview')
    movie_gr = dataframe_confirm(row, 'genres')
    poster_path_str = dataframe_confirm(row, 'posters')
    date = dataframe_confirm(row, 'release_date')
    backdrop_path_str = dataframe_confirm(row, 'backdrop_path')
    cast = dataframe_confirm(row, 'cast')
    crew = dataframe_confirm(row, 'crew')
    
    # json_path = "/home/neivekim76/demo/json/genre.json"
    # with open(json_path, 'r') as file:
    #     data = json.load(file)
    # json_genre = data["genres"]

    # genre_string = ""
    # for genre_id in movie_gr:
    #     for genre_reference in json_genre:
    #         if genre_id == genre_reference['id']:
    #             genre_string += f"{genre_reference['name']}, "

    try: 
        url_poster = f"https://image.tmdb.org/t/p/original{poster_path_str}"
    except Exception as e: 
        url_poster = "https://image.tmdb.org/t/p/original/9Yg7DZE4ip2Yl0K2BUm6hAd8iRK.jpg"


    try: 
        url_backdrop = f"https://image.tmdb.org/t/p/original{backdrop_path_str}"
    except Exception as e: 
        url_backdrop = "https://image.tmdb.org/t/p/original/9Yg7DZE4ip2Yl0K2BUm6hAd8iRK.jpg"

    # 출연진 가져오기
    objects_credit = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB_people_test/')
    
    people_details = pd.DataFrame(columns=[
        'id', 'date_gte', 'name', 'known_for_department', 'profile_img', 'birth', 'death'
    ])

    # 각 객체(파일)에 대해 반복
    for obj in objects_credit.get('Contents', []):  # 만약 'Contents'가 없으면 빈 리스트를 반환
        file_key = obj.get('Key', '')  # 파일의 S3 키를 가져옴
        if file_key.endswith('.parquet'):  # parquet 파일만 처리
            s3_object = s3.get_object(Bucket='sms-warehouse', Key=file_key)
            parquet_stream = s3_object['Body'].read()
            table = pq.read_table(BytesIO(parquet_stream))
            df = table.to_pandas()
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        
    # 중복된 'id'를 가진 행 제거 (처음 발견되는 것만 남김)
    people_details.drop_duplicates(subset=['id'], keep='first', inplace=True)
    
    cast_list = people_details[people_details['id'].isin(cast)].to_dict('records')
    cast_paginator = Paginator(cast_list, 12)
    crew_list = people_details[people_details['id'].isin(crew)].to_dict('records')
    crew_paginator = Paginator(crew_list, 12)
    cast_page = request.GET.get('cast_page', 1)
    crew_page = request.GET.get('crew_page', 1)
    print(cast_list)
    print(crew_list)
    
    try:
        cast_pages = cast_paginator.page(cast_page)
    except (PageNotAnInteger, EmptyPage):
        cast_pages = cast_paginator.page(1)

    try:
        crew_pages = crew_paginator.page(crew_page)
    except (PageNotAnInteger, EmptyPage):
        crew_pages = crew_paginator.page(1)
    
    
    context = {
        'movie_id' : movie_id,
        'movie_nm' : movie_nm,
        'movie_dt' : movie_dt,
        #'movie_gr' : genre_string[:-2],
        'poster' : url_poster,
        'external_image' : url_backdrop,
        'date' : date,
        'cast' : cast_pages,
        'crew' : crew_pages
    }

    return render(request, 'posts/DEMO-movie-detail.html', context)


# box
def rank_change_to_string(rank_change):
    if rank_change >= 100:
        return 'New'
    elif rank_change > 0:
        return f'▲ {rank_change}'
    elif rank_change < 0:
        return f'▼ {abs(rank_change)}'
    elif rank_change == 0:
        return '-'
    
def boxoffice(request):
    from django.shortcuts import render, get_object_or_404, redirect
    from .models import ExternalImageModel
    from configparser import ConfigParser
    import boto3
    import json
    import pandas as pd
    import pyarrow.parquet as pq
    from io import BytesIO
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    from datetime import datetime, timedelta
    
    # request GET
    year = request.GET.get('year', '2023')
    month = request.GET.get('month', '08')
    date = request.GET.get('date', '31')
    area = request.GET.get('area', '0105001')
    
    now_date = f"{year}-{month}-{date}"
    now_date_dt = datetime.strptime(now_date,"%Y-%m-%d")
    yesterday = now_date_dt - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%d")

    # s3 연동
    parser = ConfigParser()
    parser.read("config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix=f'kobis/{year}/boxOffice_{month}/loc_code={area}')


    ##
    area_code = {'0105001':'서울시','105002':'경기도','0105003':'강원도','0105004':'충청북도','0105005':'충청남도',
                 '0105006':'경상북도','0105007':'경상남도','0105008':'전라북도','0105009':'전라남도','0105010':'제주도',
                 '0105011':'부산시','0105012':'대구시','0105013':'대전시','0105014':'울산시','0105015':'인천시','0105016':'광주시',
                 '0105017':'세종시'}

    box_details = pd.DataFrame(columns=['date', 'rank', 'movie_nm', 'movie_open', 'sales_amount', 'sales_share',
       'sales_inten', 'sales_change', 'sales_acc', 'audi_cnt', 'audi_inten',
       'audi_change', 'audi_acc', 'scrn_cnt', 'show_cnt'])

    box_details_before = pd.DataFrame(columns=['date', 'rank', 'movie_nm', 'movie_open', 'sales_amount', 'sales_share',
       'sales_inten', 'sales_change', 'sales_acc', 'audi_cnt', 'audi_inten',
       'audi_change', 'audi_acc', 'scrn_cnt', 'show_cnt'])

    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        if (file_path.find('parquet') == -1):
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_data = BytesIO(s3_object['Body'].read())
        parquet_table = pq.read_table(parquet_data)
        parquet_df = parquet_table.to_pandas()
        box_details = pd.concat([box_details, parquet_df], ignore_index=True)
    
    box_details_today = box_details[box_details['date'] == f"{year}-{month}-{date}"]

    if date == "01":
        nowdate = datetime.strptime(f"{year}{month}{date}", "%Y%m%d")
        yesterday = nowdate - timedelta(days=1)
        year_bf = yesterday.strftime("%Y")
        month_bf = yesterday.strftime("%m")
        date_bf = yesterday.strftime("%d")
        yesterday.strftime("%Y-%m-%d")
        objects_before = s3.list_objects_v2(Bucket='sms-warehouse', Prefix=f'kobis/{year_bf}/boxOffice_{month_bf}/loc_code={area}')

        
        for obj in objects_before.get('Contents'):
            file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
            if (file_path.find('parquet') == -1):
                continue
            s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
            parquet_data = BytesIO(s3_object['Body'].read())
            parquet_table = pq.read_table(parquet_data)
            parquet_df = parquet_table.to_pandas()
            box_details_before = pd.concat([box_details_before, parquet_df], ignore_index=True)

        box_details_before = box_details_before[box_details_before['date'] == f"{year_bf}-{month_bf}-{date_bf}"]
        # box_details_today = pd.concat([box_details_today, box_details_before], ignore_index=True)
    else :
        box_details_before = box_details[box_details['date'] == f"{yesterday}"]

    box_details_today = pd.merge(box_details_today, box_details_before[['movie_nm','rank']], on='movie_nm', how='left')
    box_details_today['rank_y'] = box_details_today['rank_y'].fillna('1000') # 신작의 전날 순위값 1000등으로 대체
    box_details_today[['rank_x','rank_y']]  = box_details_today[['rank_x','rank_y']].astype(int)
    box_details_today['rank_change'] = box_details_today['rank_y'] - box_details_today['rank_x']
    box_details_today['rank_change'] = box_details_today['rank_change'].apply(rank_change_to_string)
    box_details_today[['rank_x','rank_y', 'rank_change']]  = box_details_today[['rank_x','rank_y', 'rank_change']].astype(str)
    box_details_today = box_details_today.rename(columns={'rank_x':'rank'})
    print(box_details_today)
    # box_rank_change['rank_change'] = box_details_today['rank_y'] - box_details_today['rank']
    # box_rank_change = box_rank_change.fillna('1000')
    # box_rank_change[['rank_x','rank_y']] = box_rank_change[['rank_x','rank_y']].astype(int)
    # box_rank_change['rank_change'] = box_rank_change['rank_y'] - box_rank_change['rank_x']
    # box_rank_change['rank_change'] = box_rank_change['rank_change'].apply(rank_change_to_string)
    # box_details_today['rank_change'] = box_rank_change['rank_change']
    # # box_rank_change = box_rank_change.astype(int)


    return render(request, 'posts/DEMO-boxoffice.html',{'box_details':box_details_today,
                                                        'year':year,
                                                        'month':month,
                                                        'date':date,
                                                        'area':area_code[area]})
    
