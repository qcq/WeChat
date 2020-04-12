# 怎样启动这个客户端服务

1. 首先安装docker，请参照对应的docker官方文档
2. 安装python以及对应的第三方包
3. 安装对应的postgres实例，
4. 使用了tmux相关命令来管理控制台，防止控制台在关闭的时候，后台进程也会关闭的问题。
    tmux ls 在chuanqin账户下,
    ctrl+b   d  #dettach当前的控制台
    tmux attach -t  # attach到某一个控制台
    详细其他命令请参阅如下链接：
    https://www.cnblogs.com/liuguanglin/p/9290345.html
5. 创建postgresql的docker容器
    docker run --name postgres -e POSTGRES_PASSWORD=root -d postgres
6. 连接postgres数据库，进行相应的数据操作，比如数据库创建，表创建，表删除等等命令。代码提供相应的sql语句。
    docker run -it --rm --link postgres:postgres postgres psql -h postgres -U postgres
    password root
7. 如果不是第一次启动服务，比如服务器重启之后，相应的docker镜像还在，只需要执行如下命令即可：
    sudo docker start postgres(docker images的名字)
8. 启动主程序

    1. change path to /home/user/
    2. virtualenv wx
    3. source wx/bin/activate
    4. pip install -r ../WeChat requirsments.txt
    5. change path to /home/user/WeChat/com/qcq/main/
    6. sudo ~/wx/bin/python main.py 80
        1. the reason for *sudo* seems because, only root can create socket
        2. the reason for replacing *python* with *~/wx/bin/python*, becuase the python is not same under usual and root state.

9. 切换数据库（postgresql数据库的相关命令），具体的命令请查阅下边连接：
    https://www.cnblogs.com/liyasen/p/6611020.html
    \c ebook
    select * from pictures;     query the full picture
    select * from pg_tables where schemaname = 'public';      show all available tables in current database.
