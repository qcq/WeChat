## 怎样启动这个客户端服务

1. 首先安装docker，请参照对应的docker官方文档
2. 安装python以及对应的第三方包
3. 安装对应的postgres实例，
tmux ls 在chuanqin账户下
ctrl+b   d
tmux attach -t 
python /home/chuanqin/WeChat/com/qcq/main/main.py 80
docker run --name postgres -e POSTGRES_PASSWORD=root -d postgres
docker run -it --rm --link postgres:postgres postgres psql -h postgres -U postgres
password root

\c ebook

select * from pictures;     query the full picture
