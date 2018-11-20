# WeChat Official Account
## Introduction

This is my own **Official Account** for server side program. which main purpose is to learn how to develop one functional and beautiful official Acoount which can provide below service in plan.

## The feature may be inclued

1. implement the e-book download platform, which can push e-book to kindle by email.
2. E - book conversion function, which can conver the format between epub, mobi, txt etc.
3. add one spider script which will grab e-books from other sites, which can enrich this Official Account.
4. this official account **杂感123**, which also contains my own articles. part of them written by myself, and I also upload some article which interesting or meaningful.

## The Task under plan

1. need add log system which can indicate the issue.
2. add web spider to grab the e-book from other web site(outer site).
3. add docker, which can support redis or leveldb or mysql to store the data. 
4. to the direction of micro-service architecture evolution.


## Note:
1. because I am new person to this area, so reference the below link code and doc.
   https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1472017492_58YV5
2. if you really interested in my account**杂感123**, please follow it, and take an eye on this site's change.

## Encountered Problem
1. because Tencent need the account to be verified to get more privilege to use more professional API(need money, I hate it), which limit the function of this official account. take upload media as example, with privilege can upload matrials in forever mode, without this the upload media can only keep 3 days for it.

   operation:

   1. when get the picture, first to upload, then get the media_id, then give back the user wanted picture, but failed with the reason of take too much time, which cause **The Official Account is temporarily unavailable. Try again later.**
   2. have to try the second way, start a thread in background with a cycle to upload media, then update corresponding media_id which list in code, then can solve this question.

## The work under doing

1. set get_access_token as one single thread, which as single service to supply the **access_token**.
2. set another thread which in backgroud to upload the media in fixture cycle, then update the corresponing media_id of pictures.