>概要
>>采用了tornado基本框架,写业务逻辑
>>部署采用supervisor管理服务进行部署
>>前端加nginx做反向代理+负载均衡

>功能描述
>>1.端口连通性检测
>>2.远程命令执行
>>3.远程文件上传

>本地调试启动方式
>> python main.py --port=8000 或者 python main.py  默认监听8000端口


>Supervisor的配置范例(需要根据实际的情况进行调整配置)

```
# 为了方便管理，增加一个tornado组
[group:tornados]
programs=tornado-0,tornado-1,tornado-2

# 分别定义三个tornado的进程配置
[program:tornado-0]
# 进程要执行的命令
command={virual_env}/bin/python main.py --port=8020
directory={prog_dir}
user=jackson
# 自动重启
autorestart=true
redirect_stderr=true
# 日志路径
stdout_logfile={prog_dir}/log/tornado0.log
loglevel=info

[program:tornado-1]
command={virtual_env}/bin/python main.py --port=8021
directory={prog_dir}
user=jackson
autorestart=true
redirect_stderr=true
stdout_logfile={proj_dir}/log/tornado1.log
loglevel=info

[program:tornado-2]
command={virtual_env}/bin/python main.py --port=8022
directory={prog_dir}
user=jackson
autorestart=true
redirect_stderr=true
stdout_logfile={prog_dir}/log/tornado2.log
loglevel=info

```

>Nginx配置范例

```
upstream tornados{
    server 127.0.0.1:8020;
    server 127.0.0.1:8021;
    server 127.0.0.1:8022;
}

proxy_next_upstream error;
server {
    listen 80;
    server_name www.tornado.cc;

    # 静态文件直接由Nginx处理
    location /static/{
        alias /opt/src/img/;
        expires 24h;
    }
    location /{
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        # 把请求方向代理传给tornado服务器，负载均衡
        proxy_pass http://tornados;
    }
}
```