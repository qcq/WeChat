# This doc is for the develop with baidu netdisk

1. for get the access_code of baidu api
    reference : https://developer.baidu.com/newwiki/dev-wiki/kai-fa-wen-dang.html?t=1557733846879
    go with it step by step,

## already finished:

1. already get the authorize code.
2. with the authorize code, get the access token
3. when the access token invalid, can refresh the access token.

## need to do

1. because the authorize code need to operate on web, so has a way to store the access token, which effect 30 days,**done**
2. also need to store the refresh token, which needed when to refresh the access token. **done**
3. search if exist the file which user typed, then create the share link to user, then sent back to user. **done**
4. may be exist many files, should thought one way to display them all, or do something others. **done**
5. should add code to deal with error reponse from wx and baidu.

## solution

1. need to created one table of database or just store in redis
2. or take the way like the way to access code of wechat.

actual: store the info into postgresql of one table.

3. for point 4 has a solution below *draft*:
define prioritiy like below: take below as algorithm as the draft.
    a. first try to find the file which complete match the search words, which include filename + suffix, if found this kind of file, just return the result. if has no search result return null.
    b. if has no suffix, order the result with the shorter at the before.
    c. if the order is same, take the order ['azw3, mobi, pdf, txt'].
    d. return the list of the first one, or let the user input the para to define how many result can return.

check the baidu net disk api, which seems can share more files together, so no need to fliter files.

actual: share all the file(not include the folder) with filter for mobi, azw3, epub and limit to 1000.


----

## image one scenario

user request one book, type in the book, will happen below:

1. use the baidu api to search this book.
    https://pan.baidu.com/union/document/basic#搜索文件
2. get the result, if the file non-exist, can tell the user corresponding file non-exist, or tell the user will try to get this file after, and wirte down the file.
3. if the file exist, should get the dlink of this file.
    https://pan.baidu.com/union/document/basic#文件操作
4. with the urllib2.reponse.geturl(), return this url to user, so user can download by self.

**NOTE:**

1. exist one problem, search if exist the file then get the dlink will cost too long, which will cause wx timeout, and the zaTan123 can not direct sent the message to user in time. so, has to split the producre to 2 step, first tell the user has or has not, then tell the user how to get this.
2. another solution, when search out the file with fsid, then create one share, with possword. which will also cause time cost too long, may be will be fine. This method proved works fine.
3. query all the file, has limitaion, create one thread to create share in backgroud, but has limit, which cause everyday can only create 10000 share, so has create share with forever, but create all the share may take very long.

```shell
https://pan.baidu.com/union/document/openLink#创建外链
单个用户每分钟创建外链上限: 20
单个用户每小时创建外链上限: 300
单个用户每天创建外链上限: 10000
```
