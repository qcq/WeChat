## 怎样启动这个客户端服务

1. 首先安装docker，请参照对应的docker官方文档
2. 安装python以及对应的第三方包
3. 安装对应的postgres实例，
4. 使用了tmux相关命令来管理控制台，防止控制台在关闭的时候，后台进程也会关闭的问题。
    tmux ls 在chuanqin账户下,
    ctrl+b   d  #dettach当前的控制台
    tmux attach -t  # attach到某一个控制台
    详细其他命令请参阅如下链接：
    https://www.cnblogs.com/liuguanglin/p/9290345.html
5. 启动主程序
    python /home/chuanqin/WeChat/com/qcq/main/main.py 80
6. 创建postgresql的docker容器
    docker run --name postgres -e POSTGRES_PASSWORD=root -d postgres
7. 连接postgres数据库，进行相应的数据操作，比如数据库创建，表创建，表删除等等命令。代码提供相应的sql语句。
    docker run -it --rm --link postgres:postgres postgres psql -h postgres -U postgres
    password root
8. 切换数据库（postgresql数据库的相关命令），具体的命令请查阅下边连接：
    https://www.cnblogs.com/liyasen/p/6611020.html
    \c ebook
    select * from pictures;     query the full picture