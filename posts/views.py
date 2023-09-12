def main(request):
    from django.shortcuts import render, redirect
    user = request.user
    is_authenticated = user.is_authenticated
    print('user:', user)
    print('is_authenticated:', is_authenticated)

    if not is_authenticated:
        return redirect('/users/login')

    return render(request, 'posts/main.html')

def external_image_detail(request, pk):
    from django.shortcuts import render
    from .models import ExternalImageModel
    from configparser import ConfigParser
    import boto3
    import pandas as pd
    import pyarrow.parquet as pq
    from io import BytesIO

    parser = ConfigParser()
    parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access,
    aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/')
    
    combined_df = pd.DataFrame()
    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        if file_path.find('parquet') == -1:
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_stream = s3_object['Body'].read()
        table = pq.read_table(BytesIO(parquet_stream))
        df = table.to_pandas()
        new_df = pd.concat([combined_df, df])

    row = new_df[new_df['id'] == pk]
    try:
        movie_id = row['id'].tolist()[0]
        movie_nm = row['name'].tolist()[0]
        movie_dt = row['scripts'].tolist()[0]
        movie_gr = row['genre'].tolist()[0]
        poster_path_str = row['profile_img'].tolist()[0]
    except:
        movie_id = "No Data for This Movie ID."
        movie_nm = "No Data for This Movie Name."
        movie_dt = "There is no data for this movie id. You can search for other movies."
        movie_gr = "ERROR"
        poster_path = "No Data"
    try: 
        poster_path = f"https://image.tmdb.org/t/p/original{poster_path_str}"
        ExternalImageModel.objects.create(image_url=poster_path)
    except: 
        pass
    
    try:
        external_image = ExternalImageModel.objects.get(pk=pk).image_url
        print(external_image)
    except:
        external_image = "https://image.tmdb.org/t/p/original/9Yg7DZE4ip2Yl0K2BUm6hAd8iRK.jpg"
        # external_image = "https://image.tmdb.org/t/p/original/1.jpg"

    context = {
        'movie_id' : movie_id,
        'movie_nm' : movie_nm,
        'movie_dt' : movie_dt,
        'movie_gr' : movie_gr,
        'external_image' : external_image
    }

    return render(request, 'posts/external_image_detail.html', context)
