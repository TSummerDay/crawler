from wechatpy import WeChatClient
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply
from flask import Flask, request
import xmltodict
from wechatmp import WechatMP
from utils.serialization import load_config
from website.zlibrary import ZLibrary

app = Flask(__name__)
# 全局 微信公众号对象

client = WeChatClient('wxf1773544d081d5a1', '75b01a385ca4bea81d1d53da39826a42', access_token="OFLZdDWAG2M7pcKU4")
mp = WechatMP(Token="OFLZdDWAG2M7pcKU4",appId='wxf1773544d081d5a1', secret='75b01a385ca4bea81d1d53da39826a42')

config = load_config()
zlib = ZLibrary(config)
zlib.open_page()
zlib.login()
# 用于微信服务器验证的路由
@app.route('/', methods=['GET'])
def wechat_server_validation():
    signature = request.values.get('signature')
    timestamp = request.values.get('timestamp')
    nonce = request.values.get('nonce')
    echo_str = request.values.get('echostr')
    
    try:
        check_signature(token='OFLZdDWAG2M7pcKU4', signature=signature, timestamp=timestamp, nonce=nonce)
    except InvalidSignatureException:
        return "Invalid signature"
    return echo_str

# 监听用户消息的路由
@app.route('/', methods=['POST'])
def wechat_message_handling():
    msg = xmltodict.parse(request.data).get('xml')
    msgType = msg.get('MsgType')
    reply = mp.replyText(msg, "妹妹好")
    print(msg)
    if msgType == 'text':
        reply = crawler(msg['Content'])
    return xmltodict.unparse(reply)

def crawler(message, search_type='book',file_type='pdf'):
    zlib.search(message, search_type)
    zlib.find_book(message, file_type)
    zlib.download(message, file_type)
    return "ok"

def upload_file(file_path):
    with open(file_path,'rb') as f:
        media = client.material.add("file", f)
        return media['media_id']
    
def send_file_to_user(openid, media_id):
    client.message.send_image(openid,media_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
