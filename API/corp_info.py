import requests, json, math

# 총 데이터 개수 추출
url = 'http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getAffiliate'
params ={'serviceKey': 'MGlX8jT2jARU535Ywm/oJG192i6N5Bj/xpb8RpxuKOU2o8LihjzxJPC0O0xg6RVZtBL/NvfSaBzhHUJK22CHXQ==',
         'pageNo': '1', 'numOfRows': '1', 'resultType': 'json'}
response = requests.get(url, params=params)
res = response.json()
count = int(res['response']['body']['totalCount'])
loop_count = math.trunc(count/1000) + 1


lst = []
for i in range(1, loop_count+1):
    try:
        url = 'http://apis.data.go.kr/1160100/service/GetCorpBasicInfoService/getAffiliate'
        params = {'serviceKey': 'MGlX8jT2jARU535Ywm/oJG192i6N5Bj/xpb8RpxuKOU2o8LihjzxJPC0O0xg6RVZtBL/NvfSaBzhHUJK22CHXQ==',
                  'pageNo': i, 'numOfRows': '1000', 'resultType': 'json'}
        response = requests.get(url, params=params)
        res = response.json()
        stat = res['response']['body']['items']['item']
        lst.extend(stat)
        print(f'{i}페이지 완료')
    except:
        print(f'{i}번째 페이지에서 데이터 수집이 멈췄습니다.')
        num = i
        break

with open('corp_info.json', 'w', encoding='utf-8') as f:
    json.dump(lst, f, indent=4, sort_keys=True, ensure_ascii=False)

