#-*- coding: utf-8 -*-

from korean_pronunciation import pronunciation

def test_pronunciation():
    for x, y in [(u'국물',       u'궁물'),
                 (u'격노하다',   u'경노하다'),
                 (u'큌넷',       u'큉넫'),
                 (u'부엌문',     u'부엉문'),
                 (u'닫는',       u'단는'),
                 (u'묻몸',       u'문몸'),
                 (u'덧니',       u'던니'),
                 (u'했나',       u'핸나'),
                 (u'거짓말',     u'거진말'),
                 (u'국수',       u'국쑤'),
                 (u'북한',       u'부칸'),
                 (u'그렇다',     u'그러타'),
                 (u'받이',       u'바지'),
                 (u'같이',       u'가치'),
                 (u'젖니',       u'전니'),
                 (u'낮말',       u'난말'),
                 (u'옻나무',     u'온나무'),
                 (u'옻물',       u'온물'),
                 (u'맡는',       u'만는'),
                 (u'낱말',       u'난말'),
                 (u'놓는',       u'논는'),
                 (u'놓말',       u'논말'),
                 (u'굽는',       u'굼는'),
                 (u'업무',       u'엄무'),
                 (u'엎는',       u'엄는'),
                 (u'그렇게',     u'그러케'),
                 (u'걷하',       u'거타'),
                 (u'급하다',     u'그파다'),
                 (u'낳부',       u'나푸'),
                 (u'맞히다',     u'마치다'),
                 (u'놓지마',     u'노치마'),
                 (u'그렇지',     u'그러치'),
                 (u'역량',       u'영냥'),
                 (u'선릉',       u'설릉'),
                 (u'암루',       u'암누'),
                 (u'강력',       u'강녁'),
                 (u'잡록',       u'잠녹'),
                 (u'앉아',       u'안자'),
                 (u'잃어버리다', u'이러버리다'),
                 (u'앉는',       u'안는'),
                 (u'닮다',       u'담다'),
                 (u'닮아',       u'달마'),
                 (u'못하다',     u'모타다'),
                 (u'학교',       u'학꾜'),
                 (u'손이',       u'소니'),
                 (u'산에',       u'사네'),
                 (u'돈을',       u'도늘'),
                 (u'문으로',     u'무느로'),
                 (u'좋은',       u'조은'),
                 (u'낳다',       u'나타'),
                 (u'옷',         u'옫'),
                 (u'앞',         u'압'),
                 (u'요?',        u'요?'),
                 (u'있습니다',   u'이씀니다')]:
        yield check_pronunciation, x, y 

def check_pronunciation(x, y):
    result = pronunciation(x)
    check = (u'pronunciation("%s") != "%s" (returned "%s")' % 
             (x, y, result)).encode('utf-8')
    assert pronunciation(x) == y, check
