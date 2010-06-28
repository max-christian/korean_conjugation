var conjugator = require('../conjugator'),
    assert     = require('assert'),
    sys        = require('sys');

var rule = conjugator.no_padchim_rule({'을': true, '습': true, '읍': true, '는': true, '음': true});
assert.deepEqual(rule('하', '습'), ['borrow padchim', '합']);

var rule = conjugator.vowel_contraction('ㅐ', 'ㅓ', 'ㅐ');
assert.deepEqual(rule('해', '어'), ['vowel contraction [ㅐ ㅓ -> ㅐ]', '해']);

assert.equal(conjugator.drop_l('갈', '아'), '가아');

assert.equal(conjugator.drop_l_and_borrow_padchim('갈', '습'), '갑');

assert.deepEqual(conjugator.dont_insert_eh('알', '면'), ['join', '알면']);

var rule = conjugator.insert_eh({'면': true, '세': true, '십': true});
assert.deepEqual(rule('갔', '면'), ['padchim + consonant -> insert 으', '갔으면']);

assert.deepEqual(conjugator.lm_merge('살', '음'), ['ㄹ + ㅁ -> ᆱ', '삶']);

assert.deepEqual(conjugator.merge('오', '아요'), '와요');
assert.deepEqual(conjugator.merge('오', '아'), '와');
assert.deepEqual(conjugator.merge('갔', '면'), '갔으면');
assert.deepEqual(conjugator.merge('맡', '세요'), '맡으세요');
//sys.puts(conjugator.reasons);
//assert.deepEqual(conjugator.reasons, ['vowel contraction [ㅗ + ㅏ -> ㅘ] (오 + 아요 -> 와요)']);
//
assert.equal(conjugator.after_last_space('시작을 하다'), '하다');

assert.equal(conjugator.is_s_irregular('내솟'), false);
assert.equal(conjugator.is_s_irregular('낫'), true);
assert.equal(conjugator.is_s_irregular('낫', true), false);

assert.equal(conjugator.is_l_irregular('알'), true);
assert.equal(conjugator.is_l_irregular('알', true), false);

assert.equal(conjugator.is_l_euh_irregular('아르'), true);
assert.equal(conjugator.is_l_euh_irregular('아르', true), false);

assert.equal(conjugator.is_h_irregular('가맣'), true);
assert.equal(conjugator.is_h_irregular('가맣', true), false);
assert.equal(conjugator.is_h_irregular('좋'), false);

assert.equal(conjugator.is_p_irregular('춥'), true);
assert.equal(conjugator.is_p_irregular('춥', true), false);

assert.equal(conjugator.is_d_irregular('묻'), true);
assert.equal(conjugator.is_d_irregular('묻', true), false);

assert.equal(conjugator.verb_type('낫다'), 'ㅅ 불규칙 동사 (irregular verb)');
assert.equal(conjugator.verb_type('모르다'), '르 불규칙 동사 (irregular verb)');
assert.equal(conjugator.verb_type('까맣다'), 'ㅎ 불규칙 동사 (irregular verb)');
assert.equal(conjugator.verb_type('춥다'), 'ㅂ 불규칙 동사 (irregular verb)');
assert.equal(conjugator.verb_type('캐묻다'), 'ㄷ 불규칙 동사 (irregular verb)');
assert.equal(conjugator.verb_type('알다'), 'ㄹ 불규칙 동사 (irregular verb)');
assert.equal(conjugator.verb_type('가다'), 'regular verb');

assert.equal(conjugator.base('알다'), '알');

assert.equal(conjugator.base2('알다'), '알');

assert.equal(conjugator.base2('곱다'), '고오');

assert.equal(conjugator.base2('아니'), '아니');

assert.equal(conjugator.base3('돕다'), '도우');

assert.equal(conjugator.declarative_present_informal_low('이르다', true), '일러');
assert.equal(conjugator.declarative_present_informal_low('이르다'), '이르러');
assert.equal(conjugator.declarative_present_informal_low('받다'), '받아');
assert.equal(conjugator.declarative_present_informal_low('주고 받다'), '주고 받아');
assert.equal(conjugator.declarative_present_informal_low('민주적이다'), '민주적이야');
// needed a random verb to test regularifying ㅅ :-)
assert.equal(conjugator.declarative_present_informal_low('귯'), '규어');
/*
assert declarative_present_informal_high(u'민주적이다') == u'민주적이에요'
*/
