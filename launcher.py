import requests
import hashlib
import base64
import struct
import os
import getpass
from Crypto.Cipher import AES
from urllib.parse import quote

loginformurl = 'http://hon.mgame.com/common/login_mgame.mgame?returnUrl=http://hon.mgame.com/'
loginsendurl = 'https://sign.mgame.com/login/login_action_pub_type_b.mgame?tu=http://hon.mgame.com/'
loginsendurl2 = 'https://sign.mgame.com/login/login_action.mgame'
launchurl = 'http://gstart.mgame.com/launch/launch_ghost.mgame?goUrl=ghost'

_encboxseed = '7d6e17cd885ec27e36fda16e7af947c171f73ce7b6a92ddd36ca0e732625a638'
__mkeyallbox__ = "s9n9b5t8c4e2k2a2v0c5v7d1h3q3i7w8q8w9i9c2z6v6z5w9c3i1b3v4r8n2d4t1c0f1a8h2n4a0y6m2q0u6e6j4z6x0t9q5b8g6a5p8b8e6b4t1i4n4l8g6s7s4w3o2f4t9h7k6x2a2t8n9m7j5w3d4a9k2s3r6f2p1o3u1f6h6u1o3v7m5d5x5r9w2f1c5v9e5x3b9p9w5t8k0z9m3e1z2f9a6g8b5c5v3i7k9e4u8w8c3m7j4u6f0p0j4m7m4o5p7u9o1i9r3n2n4y5v7i6y9o1i0n2a3f4m7a4l2g6z6s4s3m0p1m5m5n3f4x1e8c6l2m0b1g2g3z0p6g5w6x6y4f9q3w6n6n1h3l5d2d1z4w1g2o7f7y1y1r0b6y0f2l6j1m1j7g1n5j6d1b9p9r2f3o4i9j1q2g5f7w1k4g0h4r3a0a4x8h7b2u1f6p9o2j5s3f7g8g1c2z2m3s6j1u1s2j1u3c2u4f4r1l9o0v4b5x7m1e6u5e9m2m1m0d4d8u9h0g6r0q8w6v4o9v6t9j2p8r4q4f4k1p0a9h4c8n1a2v1e1g5m8k3s9f5g1g1o0r8p1y4r2f4b5g1u7m0r0c6g1h4l4m7v6f6x1s4h0c7v1l3q8a8r2c1s2r7t6x8d5k7d3a1j7g5u2o0q9h8r0z4a7b7y4l4z6j0h8f7s3u2d9k4m8k4l9t5p5f2x7f0j1x2j7a9m3f5t5z9m2x9w3g5t0o1d4l3u6g0s5s5l7q2f1p5r7c3o9c8a2u9o5x5h5p0a8q8m1d8p4a7y2a7h2p4y0i9y5c7i2c6u7t1d5g9j7o3y1g9k8y5a7c1r1q0w3t5t6n6i7g9k8u7a9o7y2h0m6n1i9e6a4g2f0w9o2h4t5l3t5i7y4l3f6l7d7n9c8x9g7t1e7l3k2o7q2j0u5i5d2q9v9v4o5j2r6c5b5j2l1q9f6g1z7v0t8l7f4k0k1l0v0z4d7a1e4v2p9k8u5g9v1y4w6d1o2o2c3u7f6"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

def pad(s):
    return s + chr(16-len(s)%16).encode()*(16-len(s)%16)
def unpad(s): # for debugging
    return s[:-ord(s[len(s)-1:])]
def encodeURIComponent(s):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent
    NotEscaped = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.!~*\'()'
    return ''.join(map(lambda x:x if x in NotEscaped else quote(x), s))
    
def md5_mgame(s):
    return hashlib.md5(s.encode('utf-8')).digest()

def setcjhkey(ctype):
    global _encboxseed
    global __mkeyallbox__
    _hkey1 = ''
    _hkey2 = ''
    for i in range(32):
        _sekey = ord(_encboxseed[i])
        _hkey1 = _hkey1 + __mkeyallbox__[_sekey]
        _sekey = ord(_encboxseed[i+32])
        _hkey2 = _hkey2 + __mkeyallbox__[_sekey]
    if ctype == 1:
        return md5_mgame(_hkey1)
    else:
        return md5_mgame(_hkey2)

def getlogindata(id, pw):
    key = setcjhkey(1)
    iv = setcjhkey(2)
    uidencode = encodeURIComponent(id)
    upwdencode = encodeURIComponent(pw)
    uidencdata = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(uidencode.encode('utf-8')))
    upwdencdata = AES.new(key, AES.MODE_CBC, iv).encrypt(pad(upwdencode.encode('utf-8')))
    upwddecdata = unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(upwdencdata))
    return (base64.b64encode(uidencdata), base64.b64encode(upwdencdata))

def launch(mgid, mgpw):
    global _encboxseed
    global user_agent
    global loginformurl
    global loginsendurl
    global loginsendurl2
    global launchurl
    
    sess = requests.Session()
    headers = {'User-Agent': user_agent}
    loginform = sess.get(loginformurl, headers=headers).text
    loginformlines = loginform.splitlines()
    _encboxseed = loginformlines[9].split("'")[-2]
    _mgamelogindata3 = loginformlines[18].split('"')[-2]
    _mgamelogindata1, _mgamelogindata2 = getlogindata(mgid, mgpw)
    headers = {'User-Agent': user_agent, 'Referer':loginformurl}
    data = {'mgamelogindata1': _mgamelogindata1,
            'mgamelogindata2': _mgamelogindata2,
            'mgamelogindata3': _mgamelogindata3,
            'lt':'4', 'tu':'http://hon.mgame.com/', 'ru':'http://hon.mgame.com/',
            'x':'0', 'y':'0'}
    sendform = sess.post(loginsendurl, data=data, headers=headers).text
    headers = {'User-Agent': user_agent, 'Referer':loginsendurl}
    data['loginparamgood'] = sendform.splitlines()[15].split('"')[-2]
    data['mac_addr'] = ''
    data['pc_name'] = ''
    sess.post(loginsendurl2, headers=headers, data=data)
    launchhtml = sess.get('http://gstart.mgame.com/launch/launch_ghost.mgame?goUrl=ghost').text
    try:
        launcharg = launchhtml.splitlines()[6].split("'")[-2]
        os.system('MStartPro.exe '+launcharg)
        print('Launch Success')
        return True
    except Exception as ex:
        print('Failed to Launch')
        return False

if __name__ == '__main__':
    success = False
    while not success:
        ID = input('ID : ')
        PW = getpass.getpass('PW : ')
        success = launch(ID, PW)