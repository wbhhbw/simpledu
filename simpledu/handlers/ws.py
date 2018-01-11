import redis
import gevent
from flask import Blueprint

ws = Blueprint('ws', __name__, url_prefix='/ws')

# 创建redis连接
redis = redis.from_url('redis://127.0.0.1:6379')


class Chatroom(object):

    def __init__(self):
        self.clients = []
        # 初始化 pubsub 系统
        self.pubsub = redis.pubsub()
        # 订阅 chat 频道
        self.pubsub.subscribe('chat')

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        # 给每个客户端 client 发送消息data
        try:
            # python3 中收到的消息是二进制的，使用decode函数转化为字符串
            client.send(data.decode('utf-8'))
        except:
            # 发生错误可能是客户端已经关闭，移除该客户端
            self.clients.remove(client)

    def run(self):
        # 依次将接收到的消息再发给所有客户端
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    # 使用gevent异步发送
                    gevent.spawn(self.send, client, data)

    def start(self):
        # 异步执行run函数
        gevent.spawn(self.run)

# 初始化聊天室
chat = Chatroom()
# 异步启动聊天室
chat.start()

@ws.route('/send')
def inbox(ws): # 使用 flask-sockets，ws 链接对象会被被自动注入到路由处理函数
    while not ws.closed:
        message = ws.receive()

        if message:
            # 发送消息到 chat 频道
            redis.publish('chat', message)

@ws.route('/recv')
def outbox(ws):
    chat.register(ws)
    while not ws.closed:
        gevent.sleep(0.1)
