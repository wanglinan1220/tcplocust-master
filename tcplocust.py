#!/usr/bin/env python
"""Locust对TCP长连接进行压力的测试脚本示例。

本脚本通过TCP长连接发送简单的数据给被测服务器(Ping)，并接收被测服务器返回的数据(Pong)。
脚本通过记录请求发送的时间，以及成功接收服务器响应数据的时间，计算请求的响应时间。
如果有任何异常抛出，则记录异常信息。
用户可以在脚本中设置一些Locust的参数，如最小等待时间、最大等待时间，以及被测的服务器地址等。

用户可以在此基础上进行扩展，编写适合实际业务场景的测试脚本。

执行脚本：
locust -f tcplocust.py

如果脚本是本地启动的话，可以访问：
http://localhost:8089
进行参数设置，执行测试任务以及查看测试结果。

关于使用Locust进行压力测试的更多信息，请访问Locust官网https://locust.io
"""

import time
import socket
from locust import user, TaskSet, task, events,between


class SocketClient(object):

    def __init__(self):
        # 仅在新建实例的时候创建socket.
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __getattr__(self, name):
        conn = self._socket
        def wrapper(*args, **kwargs):
            # 根据后面做的业务类，不同的方法做不同的处理
            if name == "connect":
                try:
                    conn.connect(args[0])
                except Exception as e:
                    print(e)
            elif name == "send":
                print(' '.join(hex(ord(i)) for i in args[0]))
                conn.sendall(args[0])
                data = conn.recv(1024)
                print(data)
            elif name == "close":
                conn.close()
        return wrapper

class UserBehavior(TaskSet):
    def on_start(self):
        # 该方法每用户启动时调用进行连接打开
        self.client.connect((self.locust.host, self.locust.port))
    def on_stop(self):
        # 该方法当程序结束时每用户进行调用，关闭连接
        self.client.close()

    @task()
    def sendAddCmd(self):
        #
        data= "Calling sayHello over binary protocol"
        start_time = time.time()
        # 接下来做实际的网络调用，并通过request_failure和request_success方法分别统计成功和失败的次数以及所消耗的时间
        try:
            self.client.send(data)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="earthtest", name="add", response_time=total_time, response_length=0, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="earthtest", name="add", response_time=total_time, response_length=0)


class SocketUser(SocketClient):
    # 目标地址
    host = "123.57.201.215"
    # 目标端口
    port = 18883
    task_set = UserBehavior
    wait_time = between(0.1, 1)
