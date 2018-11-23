

# 连接在docker中运行的PostgreSQL数据库

## 背景描述

随着容器化进程的加速，相比于传统虚拟机存在的巨大优势，分布式云计算的兴起，以docker为代表的容器化技术解决方案越来越流行。作为一种不算新兴技术的技术，毕竟docker所用到的技术在早很多年就存在，只是docker的出现让这些技术真正的组合在了一起，并开始发挥效用。docker相比于虚拟机的解决方案使用更少的宿主机资源，可扩展性更加优秀，相比于单独的软件安装，出现的问题更少，更容易部署。

尤其是在当前微服务架构以及云计算当道的时代下，docker更有其发挥长处的舞台。

## 问题描述

在开发个人微信公众号**杂感123**（欢迎关注）的功能逐渐完善的过程中。开始需要在项目中需要数据库来存储数据，以及作为多线程之间的一种解耦方法，初步计划从一下几种方式中做出选择。

1. 安装单独的数据库，比如mysql，redis，或者Postgres，leveldb。
2. 安装上述数据库的docker版本。

后来考虑到安装独立软件的复杂性，就采用了方案2，最开始本来想安装mysql的docker，但是发现[web.py](http://webpy.org)使用的连接mysql的驱动[MySQLdb](https://sourceforge.net/projects/mysql-python/files/)安装不上，原因是太老了，很久没有更新过了。于是，选择了docker版本的postgres。

但是在用独立的python脚本连接docker版本的postgres的时候出现了问题。本博客的主要目的就是解决单独的脚本，如何成功连接容器内的数据库。

## 环境设置

1. 今年双十一的时候购买了最便宜的阿里云，单核2G，40G硬盘空间，三年300块。当然普通的Linux环境也可以测试这个功能。需要注意的是，阿里云默认占用80端口号，阿里云盾占用了这个端口，所使用的web.py框架需要这个端口，[关闭阿里云盾](https://www.feiniaomy.com/post/155.html)。本博客默认使用了阿里云服务器。

2. 首先，更新一下服务器，安装对应的软件

   1. 更新服务器（我的服务器实例是centos）。

      ```shell
      yum update
      yum install *
      ```

   2. 安装python2.7(服务器默认安装)。

      ```
      yum install python***(Google)
      ```

   3. 安装[pip](https://pip.pypa.io/en/stable/installing/)

   4. 安装web.py，用于连接Postgres的测试。

      ```shell
      pip install web.py
      ```

   5. 创建python测试脚本所在目录

      ```shell
      mkdir wx
      ```

   6. 安装docker版本的[Postgres](https://hub.docker.com/_/postgres/)读一读doc，直接安装。

      ```
      # start a postgres instance命令来自上述的链接，下边的命令意思是用docker运行了一个Postgres实例，容器的名字叫做some-postgres（可修改），密码是mysecretpassword（可修改），默认简历的数据库是postgres，默认的用户名是postgres，默认暴露的端口是127.0.0.1
      docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
      ```

   7. 安装对应的python驱动。

      ```shell
      pip install psycopg2
      ```

   8. 在上述wx目录下写如下脚本

      ```python
      # sql.py
      try:
          connection = psycopg2.connect(user = "postgres",
                                        password = "root",
                                        host = "127.0.0.1",
                                        port = "5432",
                                        database = "postgres")
      
          cursor = connection.cursor()
          # Print PostgreSQL Connection properties
          print ( connection.get_dsn_parameters(),"\n")
      
          # Print PostgreSQL version
          cursor.execute("SELECT version();")
          record = cursor.fetchone()
          print("You are connected to - ", record,"\n")
      except (Exception, psycopg2.Error) as error :
          print ("Error while connecting to PostgreSQL", error)
      finally:
          #closing database connection.
              if(connection):
                  cursor.close()
                  connection.close()
                  print("PostgreSQL connection is closed")
      ```

   ## 问题诊断

   用上述的脚本运行，得到结果如下：

   ```
   python sql.py
   ```

   ```shell
   /usr/lib64/python2.7/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
     """)
   ('Error while connecting to PostgreSQL', OperationalError('could not connect to server: Connection refused\n\tIs the server running on host "127.0.0.1" and accepting\n\tTCP/IP connections on port 5432?\n',))
   Traceback (most recent call last):
     File "sql.py", line 22, in <module>
       if(connection):
   NameError: name 'connection' is not defined
   ```

    前半部分的psycopg2-binary可以不予以关注，只是告诉我们这个驱动以后可能不叫这个名字了，我们暂且不管，毕竟现在可以用。

   后边逐渐诊断，发现问题在于，postgres的IP不是localhost，而是docker分配的某一个IP。

   那么，问题变成了，docker用的IP是什么呢？

   ```shell
   docker ps
   ```

   ```shell
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                 NAMES
   81bac6277944        postgres            "docker-entrypoint..."   18 hours ago        Up 18 hours         5432/tcp              postgres
   ```

   可以注意到上边运行的容器实例，注意我的本机容器的名字是**postgres**。

   需要查看一下这个容器实例的信息：

   ```
   docker inspect postgres
   ```

   ```shell
    "NetworkSettings": {
               "Bridge": "",
               "SandboxID": "131fea24669611632eb4fdceb4c475c246a7e5ffa25746defd3c4ab45d93d55f",
               "HairpinMode": false,
               "LinkLocalIPv6Address": "",
               "LinkLocalIPv6PrefixLen": 0,
               "Ports": {
                   "5432/tcp": null
               },
               "SandboxKey": "/var/run/docker/netns/131fea246696",
               "SecondaryIPAddresses": null,
               "SecondaryIPv6Addresses": null,
               "EndpointID": "5d2a5af617dc56c11f95b874cd6e61a5f410d00b20c62e4ec1c12d13057c6234",
               "Gateway": "172.17.0.1",
               "GlobalIPv6Address": "",
               "GlobalIPv6PrefixLen": 0,
               "IPAddress": "172.17.0.4",
               "IPPrefixLen": 16,
               "IPv6Gateway": "",
               "MacAddress": "02:42:ac:11:00:04",
               "Networks": {
                   "bridge": {
                       "IPAMConfig": null,
                       "Links": null,
                       "Aliases": null,
                       "NetworkID": "e91322f0782411ef7fdb56da968e30b8c0d19c95894f8fef993431c197660239",
                       "EndpointID": "5d2a5af617dc56c11f95b874cd6e61a5f410d00b20c62e4ec1c12d13057c6234",
                       "Gateway": "172.17.0.1",
                       "IPAddress": "172.17.0.4",
                       "IPPrefixLen": 16,
                       "IPv6Gateway": "",
                       "GlobalIPv6Address": "",
                       "GlobalIPv6PrefixLen": 0,
                       "MacAddress": "02:42:ac:11:00:04"
                   }
               }
           }
   ```

   可以注意到IPAddress这个字段，这个字段标明了当前这个实例的网络相关参数，需要将上述的127.0.0.1参数换成**172.17.0.4**，这个参数需要根据实际的docker实例运行的实际参数进行设置，将参数更该之后运行上述sql.py脚本。

   ```shell
   [root@izm5eezkmfgg9tyd15gha9z wx]# python sql.py
   /usr/lib64/python2.7/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
     """)
   ({'tty': '', 'sslcompression': '0', 'dbname': 'postgres', 'options': '', 'host': '172.17.0.4', 'target_session_attrs': 'any', 'user': 'postgres', 'sslmode': 'prefer', 'port': '5432', 'krbsrvname': 'postgres'}, '\n')
   ('You are connected to - ', ('PostgreSQL 11.1 (Debian 11.1-1.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit',), '\n')
   PostgreSQL connection is closed
   ```

    可以注意到，python脚本链接docker的postgres成功。


