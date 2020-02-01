# WeChat Official Account Development

## Introduction

This is my own **Official Account** for server side program. which main purpose is to learn how to develop one functional and beautiful official Account which can provide below service in plan. I give it a name **ZaTan123**.

## The feature may be inclued

1. implement the e-book download platform, which can push e-book to kindle by email service.
2. E - book conversion function, which can conver the format between epub, mobi, txt .etc.
3. add one spider script which will grab e-books from other sites, which can enrich this Official Account.
4. this official account **杂感123**, which also contains my own articles. part of them written by myself, and I also upload some article which interesting and meaningful.
5. also can provide picture service, which put the picture under pictures path, this will upload the picture auto behavior. **Doing**

## The Task under plan

1. need add log system which can indicate the issue.[logging](https://www.cnblogs.com/yyds/p/6901864.html).**done**
2. add web spider to grab the e-book from other web site(outer site).
3. add docker, which can support redis or leveldb or mysql to store the data. **done by docker with postgres**
4. to the direction of **micro-service architecture** evolution. https://linux.cn/article-7584-1.html
5. need db as a bridge to communicte between threads, in current situation can use simple *shared data* to communicate with each other, should consider communicate **by DB or micro-service**.  in current stage, already implements the code to store the data to database partly,
6. in final stage, I am considering packge whole project in one docker image, which can listening incoming message and reponse with outside, behind it exist others container service like database service .etc which can evolute to micro-service platform.

## Encountered Problem

1. because Tencent need the account to be verified to get more privilege to use more professional API(need money, I hate it), which limit the function of this official account. take upload media as example, with privilege can upload matrials in forever mode, without this feature the uploaded media can only 3 days available.

   *solution operation:*

   1. when get the picture, first to upload, then get the media_id, then give back the user wanted picture, but failed with the reason of take too much time, which cause **The Official Account is temporarily unavailable. Try again later.** display on Official Account.
   2. The reason of above issue --- Official Account will request in timeout of 5s, if server not response, Tencent will sent 3-request in sequence, which not in interval of 5s again. if not reponse with these 3 request, **The Official Account is temporarily unavailable. Try again later. ** will be display in Official Account, So code should reponse "success" for Tencent's request to avoid of 3-time-request.
   3. have to try the second way, start a thread in background with a cycle to upload media, then update corresponding media_id which list in code, then can solve this question.
   4. **THIS METHOD SLOVED THIS QUESTION.**

   note: **right now store the media id into database**

2. try to use the containered database **postgres**, [this ariticle reference](./docker database Provide service.md) By contrast to traditional way to install independent database installer, such as mysql, redis, postgresql, which will take much more time to install and configure them, with the container can take more effect. such as extensible、scalable、flexible .etc

3. when load web.py application under linux in un-root user, which will occur: [socket.error: No socket could be created](https://stackoverflow.com/questions/8115330/why-wont-web-py-let-me-run-a-server-on-port-80), stack over flow, suggest with sudo, in sudo will print ImportError: No module named com.qcq.handles.url_mapping, which becasue the sudo can not take the corresponding env from original user.
becasue not wrapped the project with **setuptools**. so want to import the module, according to the python doc, should set PYTHONPATH environment variable, [slove this question](http://ghoulich.xninja.org/2017/05/09/how-to-find-env-variables-when-exec-sudo-commands/),

    1. edit /etc/profile, add **export PYTHONPATH=/home/user/WeChat**
    2. edit the /etc/sudoers, add **Defaults env_keep+="PYTHONPATH"**

## The work under doing

1. set get_access_token as one single thread, which as single service to supply the **access_token**. *Done*
2. set another thread which in backgroud to upload the media in fixture cycle, then update the corresponing media_id of pictures. *Done*.
3. store the media data list into into database. *Done.*
4. need the mail system which can email out from email server, such as *163*. *Done.*
5. need spider script, which work in dameon mode to grab the e-book.
6. reference the TODO.md

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

## Reference

1. [微信公众平台，入门指引](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1472017492_58YV5)
2. [web.py](http://webpy.org/)
3. [Postgres](https://hub.docker.com/_/postgres/)
4. [micro-service](https://linux.cn/article-7584-1.html)
5. [watchdog](https://pypi.org/project/watchdog/)
6. [pyeventbus](https://github.com/n89nanda/pyeventbus)[other](https://pypi.org/project/pyeventbus/0.5/)
7. [tmux](https://segmentfault.com/a/1190000007427965)