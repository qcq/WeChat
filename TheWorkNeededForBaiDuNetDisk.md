**This doc is for the develop with baidu netdisk**
1. for get the access_code of baidu api
    reference : https://developer.baidu.com/newwiki/dev-wiki/kai-fa-wen-dang.html?t=1557733846879
    go with it step by step,


## already finished:
1. already get the authorize code.
2. with the authorize code, get the access token


## need to do
1. because the authorize code need to operate on web, so has a way to store the access token, which effect 30 days,
2. also need to store the refresh token, which needed when to refresh the access token.




## solution
1. need to created one table of database or just store in redis
2. or take the way like the way to access code of wechat.