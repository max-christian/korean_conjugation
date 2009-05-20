#-*- coding: utf-8 -*-

from korean_conjugator import *

def test_base3():
    assert base3(u'돕다') == u'도우'

def test_merge():
    assert merge(u'오', u'아요') == u'와요'
    assert merge(u'오', u'아') == u'와'
    assert merge(u'갔', u'면') == u'갔으면'
    assert merge(u'일어나', u'면') == u'일어나면'
    assert merge(u'맡', u'세요') == u'맡으세요'

def test_declarative_present():
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

    assert declarative_present_informal_high(u'가다') == u'가요'

    assert declarative_present_formal_low(u'가다') == u'간다'
    assert declarative_present_formal_low(u'믿다') == u'믿는다'
    assert declarative_present_formal_low(u'걷다') == u'걷는다'
    assert declarative_present_formal_low(u'짓다') == u'짓는다'
    assert declarative_present_formal_low(u'부르다') == u'부른다'
    assert declarative_present_formal_low(u'살다') == u'산다'
    assert declarative_present_formal_low(u'오르다') == u'오른다'

    assert declarative_present_formal_high(u'가다') == u'갑니다'
    assert declarative_present_formal_high(u'믿다') == u'믿습니다'
    assert declarative_present_formal_high(u'걸다') == u'겁니다'
    assert declarative_present_formal_high(u'깨닫다') == u'깨닫습니다'
    assert declarative_present_formal_high(u'알다') == u'압니다'

def test_past_base():
    assert past_base(u'하') == u'했'
    assert past_base(u'가') == u'갔'
    assert past_base(u'기다리') == u'기다렸'
    assert past_base(u'기다리다') == u'기다렸'
    assert past_base(u'마르다') == u'말랐'
    assert past_base(u'드르다') == u'들렀'

def test_declarative_past():
    assert declarative_past_informal_low(u'하') == u'했어'
    assert declarative_past_informal_low(u'가') == u'갔어'
    assert declarative_past_informal_low(u'먹') == u'먹었어'
    assert declarative_past_informal_low(u'오') == u'왔어'

    assert declarative_past_informal_high(u'하다') == u'했어요'
    assert declarative_past_informal_high(u'가다') == u'갔어요'

    assert declarative_past_formal_low(u'가다') == u'갔다'

    assert declarative_past_formal_high(u'가다') == u'갔습니다'

def test_declarative_future():
    assert declarative_future_informal_low(u'가다') == u'갈 거야'
    assert declarative_future_informal_low(u'믿다') == u'믿을 거야'
    assert declarative_future_informal_low(u'알다') == u'알 거야'

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

    assert imperative_present_formal_high(u'가다') == u'가십시오'
    assert imperative_present_formal_high(u'걷다') == u'걸으십시오'
    assert imperative_present_formal_high(u'돕다') == u'도우십시오'
    assert imperative_present_formal_high(u'알다') == u'아십시오'
    assert imperative_present_formal_high(u'눕다') == u'누우십시오'

def test_propositive_present():
    assert propositive_present_informal_low(u'가') == u'가'

    assert propositive_present_informal_high(u'가') == u'가요'

    assert propositive_present_formal_low(u'가') == u'가자'

    assert propositive_present_formal_high(u'가') == u'갑시다'
    assert propositive_present_formal_high(u'살') == u'삽시다'
    assert propositive_present_formal_high(u'눕다') == u'누웁시다'

def test_connectives():
    assert connective_if(u'낫') == u'나으면'
    assert connective_if(u'짓') == u'지으면'
    assert connective_if(u'짖') == u'짖으면'
    assert connective_if(u'가') == u'가면'
    assert connective_if(u'알') == u'알면'
    assert connective_if(u'살') == u'살면'

    assert connective_and(u'가다') == u'가고'

    assert nominal_ing(u'살다') == u'삶'
    assert nominal_ing(u'걷다') == u'걸음'
    assert nominal_ing(u'가져오다') == u'가져옴'
    assert nominal_ing(u'걷다') == u'걸음'

