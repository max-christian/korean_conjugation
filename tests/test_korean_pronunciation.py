#-*- coding: utf-8 -*-

from korean_pronunciation import pronunciation

def test_pronunciation():
    for x, y in [(u'국물',    u'궁물'   ),
                 (u'격노하다', u'경노하다'),
                 (u'큌넷',    u'큉넷'),
                 (u'부엌문',  u'부엉문'),
                 (u'닫는',    u'단는'),
                 (u'묻몸',    u'문몸'),
                 (u'덧니',    u'던니'),
                 (u'했나',    u'핸나'),
                 (u'거짓말',  u'거진말'),
                 (u'국수',    u'국쑤')]:
        yield check_pronunciation, x, y 

def check_pronunciation(x, y):
    result = pronunciation(x)
    check = (u'pronunciation("%s") != "%s" (returned "%s")' % 
             (x, y, result)).encode('utf-8')
    assert pronunciation(x) == y, check
