# Something need to be improved

1. when the user request the ebook, should not paste the hyper-link in source code, may be put them into database or config.ini file, may be take four stage to finish this task.
    1. put the ebook link in config.ini
    2. put the hyper-link in database(postgresql) which hold in docker.
    3. dynamic to retrieve the hyper-link of ebook which user want, by the baidu net disk API, reference https://pan.baidu.com/union/document/
    4. for the short wait time consideration, one back thread can put the requested esource store in database, which can be used in second same request, the database can consider the **redis**, as the cache of this project.
2. becasue the Tencent not allowed no-paid user store the image longger than 3 days. so, we have to re-upload the picture when 3 days past, and can also upload new pictures which under the pictures path, current implementation will do this kind of operation every 60mins check, which may cause short time resource unavailable, should try to fix this.

    **may be can fixed by below way:**

    1. with the watchdog moudle https://pypi.org/project/watchdog/, get three kinds event:
        * when has new file created, upload to tencent, then added it to database with media id.
        * when file update, upload to tencent, then updated to database with media id.
        * when file delete, then delete it from database.
    2. another thread query the whole table of databse, get the olddest time file which closest to 3 days, then sleep (currenttime - timestamp of the file), also can consider sleep little than currenttime - timestamp, to make sure the file always avaliable, then update this file.
    3. thread in 2) query the whole database again, cycle all this setp.

    note: **add the eventbus like java, to decouple PicturePathHandler with Media**
3. code has no error deal, sepcifial for the reponse from BaiDu API

4. should add service which support indicate the system info, like uptime, cpu usage .etc, also can email the compressed logs to administer with email or others way.

5. should find one way to log the web.py log to standard logging file.
