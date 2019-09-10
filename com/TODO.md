## something need to be improved
1. when the user request the ebook, should not paste the hyper-link in source code,
    may be put them into database or config.ini file, may be take four stage to finish
    this task.
    1). put the ebook link in config.ini
    2). put the hyper-link in database(postgresql) which hold in docker.
    3). dynamic to retrieve the hyper-link of ebook which user want, by the baidu net disk
        API, reference https://pan.baidu.com/union/document/
    4). for the short wait time consideration, one back thread can put the requested
        resource store in database, which can be used in second same request, the database
        can consider the **redis**, as the cache of this project.
2. becasue the Tencent can not allow no-paid user store the image longger than 3 days.
    so, we have to re-upload the picture when 3 days past, and can also upload new
    pictures which under the pictures path, current implementation will do this kind
    of operation every 60mins check, which may cause short time resource unavailable, should
    try to fix this.