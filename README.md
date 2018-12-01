# WeChat Official Account Development
## Introduction

This is my own **Official Account** for server side program. which main purpose is to learn how to develop one functional and beautiful official Account which can provide below service in plan.

## The feature may be inclued

1. implement the e-book download platform, which can push e-book to kindle by email service.
2. E - book conversion function, which can conver the format between epub, mobi, txt .etc.
3. add one spider script which will grab e-books from other sites, which can enrich this Official Account.
4. this official account **杂感123**, which also contains my own articles. part of them written by myself, and I also upload some article which interesting and meaningful.

## The Task under plan

1. need add log system which can indicate the issue.[logging](https://www.cnblogs.com/yyds/p/6901864.html).**done**
2. add web spider to grab the e-book from other web site(outer site).
3. add docker, which can support redis or leveldb or mysql to store the data. **done by docker with postgres**
4. to the direction of **micro-service architecture** evolution. https://linux.cn/article-7584-1.html
5. need db as a bridge to communicte between threads, in current situation can use simple *shared data* to communicate with each other, should consider communicate **by DB or micro-service**.  in current stage, alreadt implements the code to store the data to database partly,
6. in final stage, I am considering packge whole project in one docker image, which can listening incoming message and reponse with outside, behind it exist others container service like database service .etc which can evolute to micro-service platform.

## Encountered Problem
1. because Tencent need the account to be verified to get more privilege to use more professional API(need money, I hate it), which limit the function of this official account. take upload media as example, with privilege can upload matrials in forever mode, without this feature the uploaded media can only 3 days available.

   *solution operation:*

   1. when get the picture, first to upload, then get the media_id, then give back the user wanted picture, but failed with the reason of take too much time, which cause **The Official Account is temporarily unavailable. Try again later.** display on Official Account.
   2. The reason of above issue --- Official Account will request in timeout of 5s, if server not response, Tencent will sent 3-request in sequence, which not in interval of 5s again. if not reponse with these 3 request, **The Official Account is temporarily unavailable. Try again later. ** will be display in Official Account, So code should reponse "success" for Tencent's request to avoid of 3-time-request.
   3. have to try the second way, start a thread in background with a cycle to upload media, then update corresponding media_id which list in code, then can solve this question.    
   4. **THIS METHOD SLOVED THIS QUESTION.**

2. try to use the containered database **postgres**, [this ariticle reference](./docker database Provide service.md) By contrast to traditional way to install indenpent database installer, such as mysql, redis, postgresql, which will take much more time to install and configure them, with the container can take more effect. such as extensible、scalable、flexible .etc

## The work under doing

1. set get_access_token as one single thread, which as single service to supply the **access_token**. *Done*
2. set another thread which in backgroud to upload the media in fixture cycle, then update the corresponing media_id of pictures. *Done*.
3. store the media data list in 2 into database. *Done.*

## Related Technologies

1. **Flask**
2. **Mysql**
3. **Redis**
4. **MessageQueue**, such as **RabbitMQ**
5. **multi-thread** or **multi-process**
6. **Restful-API**
7. **Micro-service**
8. **Docker**

## Note:

1. because I am new person to this area, so reference the below link code and doc as the base project code.
   https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1472017492_58YV5
2. if you really interested in my account**杂感123**, please follow it, and take an eye on this site's change.

# Reference

1. [微信公众平台，入门指引](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1472017492_58YV5)
2. [web.py](http://webpy.org/)
3. [Postgres](https://hub.docker.com/_/postgres/)
4. [micro-service](https://linux.cn/article-7584-1.html)