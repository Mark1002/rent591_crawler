# rent591 scrapy web scrawler

install package
```
pip -r install requirements.txt
```

set up mongoDB (need docker/docker-compose before install)
```
> cd db
> docker-compose up -d
```

start scrapy web crawler
```
> cd crawlers/rent_591
> scrapy crawl rent591
```

Restful API format
```
get /rent?<parameter1=value>&<parameter2=value>...&<parameterN=value>
```
API parameter
```
'sex_limit':    number (0: male | 1: female | 2: no limit)
'phone_number': string (09XX-XXX-XXX)
'city':         string (台北市 | 新北市)
'renter_sex':   number (0: male | 1: female)
'home_owner':   number (0: not home owner | 1: home owner)
'first_name':   string (張,黃....else)
```
API response
```
{
    "data": [
        {
            "city": "台北市",
            "house_id": 7227694,
            "house_recent": "分租套房",
            "house_type": "公寓",
            "phone_number": "0987-097-311",
            "renter": "詹小姐",
            "renter_sex": 1,
            "renter_type": "屋主",
            "sex_limit": 2
        },...
    ]
}
```

reference
1. https://ithelp.ithome.com.tw/articles/10191506
