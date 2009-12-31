#-*- coding: utf-8 -*-

from korean.conjugator import *

def test_type():
    assert verb_type(u'낫다')   == u'ㅅ 불규칙 동사 (irregular verb)'
    assert verb_type(u'모르다') == u'르 불규칙 동사 (irregular verb)'
    assert verb_type(u'까맣다') == u'ㅎ 불규칙 동사 (irregular verb)'
    assert verb_type(u'춥다')   == u'ㅂ 불규칙 동사 (irregular verb)'
    assert verb_type(u'캐묻다') == u'ㄷ 불규칙 동사 (irregular verb)'
    assert verb_type(u'알다')   == u'ㄹ 불규칙 동사 (irregular verb)'
    assert verb_type(u'가다')   == u'regular verb'

def test_conjugation():
    assert u'멍는다' in (x[2] for x in conjugation.perform(u'먹다'))

def test_base3():
    assert base3(u'돕다') == u'도우'

def test_merge():
    conjugation.reasons = []
    assert merge(u'오', u'아요') == u'와요'
    assert conjugation.reasons == [u'vowel contraction [ㅗ + ㅏ -> ㅘ] (오 + 아요 -> 와요)']
    assert merge(u'오', u'아') == u'와'
    assert merge(u'갔', u'면') == u'갔으면'
    assert merge(u'일어나', u'면') == u'일어나면'
    assert merge(u'맡', u'세요') == u'맡으세요'

def test_declarative_present():
    assert declarative_present_informal_low(u'민주적이다') == u'민주적이야'
    assert declarative_present_informal_high(u'민주적이다') == u'민주적이에요'
    # needed a random verb to test regularifying ㅅ :-)
    assert declarative_present_informal_low(u'귯') == u'규어'
    assert declarative_present_informal_low(u'귯', regular=True) == u'귯어'
    assert declarative_present_informal_low(u'치르다') == u'치러'
    assert declarative_present_informal_low(u'줍다') == u'주워'
    assert declarative_present_informal_low(u'동트다') == u'동터'
    assert declarative_present_informal_low(u'농트다') == u'농터'
    assert declarative_present_informal_low(u'엇다') == u'엇어'
    assert declarative_present_informal_low(u'푸다') == u'퍼'
    assert declarative_present_informal_low(u'깃다') == u'깃어'
    assert declarative_present_informal_low(u'그러다') == u'그래'
    assert declarative_present_informal_low(u'애긋다') == u'애긋어'
    assert declarative_present_informal_low(u'되묻다') == u'되물어'
    assert declarative_present_informal_low(u'밧다') == u'밧아'
    assert declarative_present_informal_low(u'힘닿다') == u'힘닿아'
    assert declarative_present_informal_low(u'용솟다') == u'용솟아'
    assert declarative_present_informal_low(u'쌓다') == u'쌓아'
    assert declarative_present_informal_low(u'파묻다', regular=True) == u'파묻어'
    assert declarative_present_informal_low(u'부르걷다') == u'부르걷어'
    assert declarative_present_informal_low(u'되묻다', regular=True) == u'되묻어'
    assert declarative_present_informal_low(u'뵙다') == u'봬'
    assert declarative_present_informal_low(u'쏟다') == u'쏟아'
    assert declarative_present_informal_low(u'묻잡다') == u'묻자와'
    assert declarative_present_informal_low(u'가로닫다') == u'가로달아'
    assert declarative_present_informal_low(u'동트다') == u'동터'
    assert declarative_present_informal_low(u'농트다') == u'농터'
    assert declarative_present_informal_low(u'농트다') == u'농터'
    assert declarative_present_informal_low(u'엇다') == u'엇어'
    assert declarative_present_informal_low(u'푸다') == u'퍼'
    assert declarative_present_informal_low(u'깃다') == u'깃어'
    assert declarative_present_informal_low(u'그러다') == u'그래'
    assert declarative_present_informal_low(u'애긋다') == u'애긋어'
    assert declarative_present_informal_low(u'되묻다') == u'되물어'
    assert declarative_present_informal_low(u'밧다') == u'밧아'
    assert declarative_present_informal_low(u'힘닿다') == u'힘닿아'
    assert declarative_present_informal_low(u'용솟다') == u'용솟아'
    assert declarative_present_informal_low(u'쌓다') == u'쌓아'
    assert declarative_present_informal_low(u'파묻다', regular=True) == u'파묻어'
    assert declarative_present_informal_low(u'부르걷다') == u'부르걷어'
    assert declarative_present_informal_low(u'되묻다', regular=True) == u'되묻어'
    assert declarative_present_informal_low(u'뵙다') == u'봬'
    assert declarative_present_informal_low(u'놓다') == u'놓아'
    #assert declarative_present_informal_low(u'요러다') == u'요래'
    assert declarative_present_informal_low(u'내솟다') == u'내솟아'
    assert declarative_present_informal_low(u'북돋다') == u'북돋아'
    assert declarative_present_informal_low(u'부르돋다') == u'부르돋아'
    assert declarative_present_informal_low(u'뒤묻다') == u'뒤묻어'
    assert declarative_present_informal_low(u'껴묻다') == u'껴묻어'
    assert declarative_present_informal_low(u'그러묻다') == u'그러묻어'
    assert declarative_present_informal_low(u'겉묻다') == u'겉묻어'
    assert declarative_present_informal_low(u'손쓰다') == u'손써'
    assert declarative_present_informal_low(u'따르다') == u'따라'
    assert declarative_present_informal_low(u'악쓰다') == u'악써'
    assert propositive_present_informal_low(u'꿰다') == u'꿰'
    assert declarative_present_informal_low(u'활걷다') == u'활걷어'
    assert declarative_present_informal_low(u'파묻다') == u'파물어'
    assert declarative_present_informal_low(u'캐묻다') == u'캐물어'
    assert declarative_present_informal_low(u'줄밑걷다') == u'줄밑걷어'
    assert declarative_present_informal_low(u'묻다') == u'물어'
    assert declarative_present_informal_low(u'예굽다') == u'예굽어'
    assert declarative_present_informal_low(u'에굽다') == u'에굽어'
    assert declarative_present_informal_low(u'치걷다') == u'치걷어'
    assert declarative_present_informal_low(u'욱걷다') == u'욱걷어'
    assert declarative_present_informal_low(u'설굳다') == u'설굳어'
    assert declarative_present_informal_low(u'내리벋다') == u'내리벋어'
    assert declarative_present_informal_low(u'내딛다') == u'내딛어'
    assert declarative_present_informal_low(u'굳다') == u'굳어'
    assert declarative_present_informal_low(u'흉업다') == u'흉어워'
    assert declarative_present_informal_low(u'빛접다') == u'빛저워'
    assert declarative_present_informal_low(u'바잡다') == u'바자워'
    #assert declarative_present_informal_low(u'허여멀겋다') == u'허여멀게'
    assert declarative_present_informal_low(u'켜다') == u'켜'
    assert declarative_present_informal_low(u'폐다') == u'폐'
    assert declarative_present_informal_low(u'서릊다') == u'서릊어'
    assert declarative_present_informal_low(u'홉뜨다') == u'홉떠'
    assert declarative_present_informal_low(u'접다') == u'접어'
    assert declarative_present_informal_low(u'업다') == u'업어'
    assert declarative_present_informal_low(u'뺏다') == u'뺏어'
    assert declarative_present_informal_low(u'겉약다') == u'겉약아'
    assert declarative_present_informal_low(u'흠뜯다') == u'흠뜯어'
    assert declarative_present_informal_low(u'수줍다') == u'수줍어'
    assert declarative_present_informal_low(u'이르다') == u'이르러'
    assert declarative_present_informal_low(u'엷푸르다') == u'엷푸르러'
    assert declarative_present_informal_low(u'덧묻다') == u'덧묻어'
    assert declarative_present_informal_low(u'묻다', regular=True) == u'묻어'
    assert declarative_present_informal_low(u'끄집다') == u'끄집어'
    assert declarative_present_informal_low(u'내리찧다') == u'내리찧어'
    assert declarative_present_informal_low(u'헐벗다') == u'헐벗어'
    assert declarative_present_informal_low(u'빼입다') == u'빼입어'
    assert declarative_present_informal_low(u'많다') == u'많아'
    assert declarative_present_informal_low(u'앗다') == u'앗아'
    assert declarative_present_informal_low(u'좋다') == u'좋아'
    assert declarative_present_informal_low(u'만들다') == u'만들어'
    assert declarative_present_informal_low(u'어떻다') == u'어때'
    assert declarative_present_informal_low(u'까맣다') == u'까매'
    assert declarative_present_informal_low(u'하얗다') == u'하얘'
    assert declarative_present_informal_low(u'잡') == u'잡아'
    assert declarative_present_informal_low(u'뽑') == u'뽑아'
    assert declarative_present_informal_low(u'입') == u'입어'
    assert declarative_present_informal_low(u'아프다') == u'아파'
    assert declarative_present_informal_low(u'하') == u'해'
    assert declarative_present_informal_low(u'가') == u'가'
    assert declarative_present_informal_low(u'오') == u'와'
    assert declarative_present_informal_low(u'피우') == u'피워'
    assert declarative_present_informal_low(u'듣') == u'들어'
    assert declarative_present_informal_low(u'춥') == u'추워'
    assert declarative_present_informal_low(u'낫') == u'나아'
    assert declarative_present_informal_low(u'알') == u'알아'
    assert declarative_present_informal_low(u'기다리') == u'기다려'
    assert declarative_present_informal_low(u'마르') == u'말라'
    assert declarative_present_informal_low(u'부르다') == u'불러'
    assert declarative_present_informal_low(u'되') == u'돼'
    assert declarative_present_informal_low(u'쓰') == u'써'
    assert declarative_present_informal_low(u'서') == u'서'
    assert declarative_present_informal_low(u'세') == u'세'
    assert declarative_present_informal_low(u'기다리다') == u'기다려'
    assert declarative_present_informal_low(u'굽다') == u'구워'
    assert declarative_present_informal_low(u'걷다') == u'걸어'
    assert declarative_present_informal_low(u'짓다') == u'지어'
    assert declarative_present_informal_low(u'웃다') == u'웃어'
    assert declarative_present_informal_low(u'걸다') == u'걸어'
    assert declarative_present_informal_low(u'깨닫다') == u'깨달아'
    assert declarative_present_informal_low(u'남다') == u'남아'
    assert declarative_present_informal_low(u'오르다') == u'올라'
    assert declarative_present_informal_low(u'돕다') == u'도와'
    assert declarative_present_informal_low(u'덥다') == u'더워'
    assert declarative_present_informal_low(u'푸르다') == u'푸르러'
    assert declarative_present_informal_low(u'번거롭다') == u'번거로워'
   
    assert declarative_present_informal_high(u'굽다', regular=True) == u'굽어요'
    assert declarative_present_informal_high(u'가다') == u'가요'

    assert declarative_present_formal_low(u'가다') == u'간다'
    assert declarative_present_formal_low(u'믿다') == u'믿는다'
    assert declarative_present_formal_low(u'걷다') == u'걷는다'
    assert declarative_present_formal_low(u'짓다') == u'짓는다'
    assert declarative_present_formal_low(u'부르다') == u'부른다'
    assert declarative_present_formal_low(u'살다') == u'산다'
    assert declarative_present_formal_low(u'오르다') == u'오른다'

    assert declarative_present_formal_high(u'가다') == u'갑니다'
    assert declarative_present_formal_high(u'좋다') == u'좋습니다'
    assert declarative_present_formal_high(u'믿다') == u'믿습니다'
    assert declarative_present_formal_high(u'걸다') == u'겁니다'
    assert declarative_present_formal_high(u'깨닫다') == u'깨닫습니다'
    assert declarative_present_formal_high(u'알다') == u'압니다'
    assert declarative_present_formal_high(u'푸르다') == u'푸릅니다'

def test_past_base():
    assert past_base(u'하') == u'했'
    assert past_base(u'가') == u'갔'
    assert past_base(u'기다리') == u'기다렸'
    assert past_base(u'기다리다') == u'기다렸'
    assert past_base(u'마르다') == u'말랐'
    assert past_base(u'드르다') == u'들렀'

def test_declarative_past():
    assert declarative_past_informal_low(u'푸다') == u'펐어'
    assert declarative_past_informal_low(u'뵙다') == u'뵀어'
    assert declarative_past_informal_low(u'쬐다') == u'쬈어'
    assert declarative_past_informal_low(u'하') == u'했어'
    assert declarative_past_informal_low(u'가') == u'갔어'
    assert declarative_past_informal_low(u'먹') == u'먹었어'
    assert declarative_past_informal_low(u'오') == u'왔어'

    assert declarative_past_informal_high(u'하다') == u'했어요'
    assert declarative_past_informal_high(u'가다') == u'갔어요'

    assert declarative_past_formal_low(u'가다') == u'갔다'

    assert declarative_past_formal_high(u'가다') == u'갔습니다'

def test_future_base():
    assert future_base(u'가다') == u'갈'
    assert future_base(u'가늘다') == u'가늘'
    assert future_base(u'좋다') == u'좋을'
    assert future_base(u'뵙다') == u'뵐'

def test_declarative_future():
    assert declarative_future_informal_low(u'끌어넣다') == u'끌어넣을 거야'
    assert declarative_future_informal_low(u'좁디좁다') == u'좁디좁을 거야'
    assert declarative_future_informal_low(u'가다') == u'갈 거야'
    assert declarative_future_informal_low(u'믿다') == u'믿을 거야'
    assert declarative_future_informal_low(u'알다') == u'알 거야'
    
    assert declarative_future_informal_high(u'하얗다') == u'하얄 거예요'
    assert declarative_future_informal_high(u'가다') == u'갈 거예요'
    assert declarative_future_informal_high(u'믿다') == u'믿을 거예요'
    assert declarative_future_informal_high(u'걷다') == u'걸을 거예요'
    assert declarative_future_informal_high(u'알다') == u'알 거예요'

    assert declarative_future_formal_low(u'가다') == u'갈 거다'
    assert declarative_future_formal_low(u'앉다') == u'앉을 거다'
    assert declarative_future_formal_low(u'알다') == u'알 거다'

    assert declarative_future_formal_high(u'가다') == u'갈 겁니다'
    assert declarative_future_formal_high(u'앉다') == u'앉을 겁니다'
    assert declarative_future_formal_high(u'알다') == u'알 겁니다'

    assert declarative_future_conditional_informal_low(u'가다') == u'가겠어'

    assert declarative_future_conditional_informal_high(u'가다') == u'가겠어요'

    assert declarative_future_conditional_formal_low(u'가다') == u'가겠다'

    assert declarative_future_conditional_formal_high(u'가다') == u'가겠습니다'

def test_inquisitive_present():
    assert inquisitive_present_informal_low(u'가다') == u'가?'
    assert inquisitive_present_informal_low(u'하다') == u'해?'

    assert inquisitive_present_informal_high(u'가다') == u'가요?'

    assert inquisitive_present_formal_low(u'가다') == u'가니?'
    assert inquisitive_present_formal_low(u'알다') == u'아니?'

    assert inquisitive_present_formal_high(u'가다') == u'갑니까?'
    assert inquisitive_present_formal_high(u'까맣다') == u'까맣습니까?'

def test_inquisitive_past():
    assert inquisitive_past_informal_low(u'가다') == u'갔어?'

    assert inquisitive_past_informal_high(u'가다') == u'갔어요?'

    assert inquisitive_past_formal_low(u'가다') == u'갔니?'

    assert inquisitive_past_formal_high(u'가다') == u'갔습니까?'

def test_imperative_present():
    assert imperative_present_informal_low(u'가다') == u'가'
    
    assert imperative_present_informal_high(u'가다') == u'가세요'
    assert imperative_present_informal_high(u'돕다') == u'도우세요'
    assert imperative_present_informal_high(u'걷다') == u'걸으세요'
    assert imperative_present_informal_high(u'눕다') == u'누우세요'
    assert imperative_present_informal_high(u'살다') == u'사세요'
    assert imperative_present_informal_high(u'걸다') == u'거세요'

    assert imperative_present_formal_low(u'가다') == u'가라'
    assert imperative_present_formal_low(u'굽다') == u'구워라'
    assert imperative_present_formal_low(u'살다') == u'살아라'
    assert imperative_present_formal_low(u'서') == u'서라'
    assert imperative_present_formal_low(u'뵙다') == u'봬라'

    assert imperative_present_formal_high(u'가다') == u'가십시오'
    assert imperative_present_formal_high(u'걷다') == u'걸으십시오'
    assert imperative_present_formal_high(u'돕다') == u'도우십시오'
    assert imperative_present_formal_high(u'알다') == u'아십시오'
    assert imperative_present_formal_high(u'눕다') == u'누우십시오'
    assert imperative_present_formal_high(u'뵙다') == u'뵈십시오'

def test_propositive_present():
    assert propositive_present_informal_low(u'가') == u'가'

    assert propositive_present_informal_high(u'가') == u'가요'

    assert propositive_present_formal_low(u'가') == u'가자'

    assert propositive_present_formal_high(u'가') == u'갑시다'
    assert propositive_present_formal_high(u'살') == u'삽시다'
    assert propositive_present_formal_high(u'눕다') == u'누웁시다'
    assert propositive_present_formal_high(u'돕다') == u'도웁시다'

def test_connectives():
    assert connective_if(u'낫') == u'나으면'
    assert connective_if(u'짓') == u'지으면'
    assert connective_if(u'짖') == u'짖으면'
    assert connective_if(u'가') == u'가면'
    assert connective_if(u'알') == u'알면'
    assert connective_if(u'살') == u'살면'
    assert connective_if(u'푸르다') == u'푸르면'
    assert connective_if(u'돕다') == u'도우면'
    
    assert connective_and(u'가다') == u'가고'

    assert nominal_ing(u'살다') == u'삶'
    assert nominal_ing(u'걷다') == u'걸음'
    assert nominal_ing(u'가져오다') == u'가져옴'
    assert nominal_ing(u'걷다') == u'걸음'
    assert nominal_ing(u'그렇다') == u'그럼'
    assert nominal_ing(u'까맣다') == u'까맘'
    assert nominal_ing(u'돕다') == u'도움'
