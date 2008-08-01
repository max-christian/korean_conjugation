-module(korean_verb).

-compile(export_all).

merge(Character1, Character2) when is_binary(Character1) and is_binary(Character2)->
    SplitCharacter1 = hangul:split(Character1),
    SplitCharacter2 = hangul:split(Character2),
    case is_list(SplitCharacter1) of
        true -> 
            LeadString = lists:sublist(SplitCharacter1, length(SplitCharacter1) - 1),
            EndCharacter = lists:last(SplitCharacter1),
            NewEndString = merge(EndCharacter, SplitCharacter2),
            hangul:join(LeadString ++ NewEndString);
        false -> 
            hangul:join(merge(SplitCharacter1, SplitCharacter2))
    end;

% regulars that look irregular
merge({character, <<"ᄆ">>, <<"ㅣ">>, <<"ᆮ">>}=Mit, Character2) ->
    [Mit, Character2];

%TODO: hardcode irregular exceptions    

% 르 irregular
merge({character, Lead, <<"ㅗ">>, none}, {character, <<"ᄅ">>, <<"ㅡ">>, none}) ->
        [{character, Lead, <<"ㅗ">>, <<"ᆯ">>}, {character, <<"ᄅ">>, <<"ㅏ">>, none}];

% 드 irregular
merge({character, Lead, Vowel, <<"ᆮ">>}, {character, <<"ᄋ">>, _, _}=Character2) ->
    [{character, Lead, Vowel, <<"ᆯ">>}, Character2];

% ㅅ irregular
merge({character, Lead, Vowel, <<"ᆺ">>}, {character, _, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, Vowel, none}, {character, <<"ᄋ">>, <<"ㅏ">>, Padchim}];

% ㅂ irregular
merge({character, Lead, <<"ㅜ">>=Vowel, <<"ᆸ">>}, {character, <<"ᄋ">>, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, Vowel, none}, {character, <<"ᄋ">>, <<"ㅝ">>, Padchim}];

merge({character, Lead, Vowel, none}, {character, <<"ᄋ">>, <<"ㅡ">>, <<"ᆸ">>}) ->
    [{character, Lead, Vowel, <<"ᆸ">>}];

merge(Character, {character, <<"ᄋ">>, <<"ㅡ">>, <<"ᆸ">>}=Eup) ->
    [Character, Eup];

% vowel contractions
merge({character, Lead, <<"ㅐ">>, none}, {character, <<"ᄋ">>, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅐ">>, Padchim}];

merge({character, Lead, <<"ㅡ">>, none}, {character, <<"ᄋ">>, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅓ">>, Padchim}];

merge({character, Lead, <<"ㅜ">>, none}, {character, <<"ᄋ">>, <<"ㅓ">>, Padchim}) -> 
    [{character, Lead, <<"ㅝ">>, Padchim}];

merge({character, Lead, <<"ㅗ">>, none}, {character, <<"ᄋ">>, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, <<"ㅘ">>, Padchim}];

merge({character, Lead, <<"ㅚ">>, none}, {character, <<"ᄋ">>, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅙ">>, Padchim}];

merge({character, Lead, <<"ㅏ">>, none}, {character, <<"ᄋ">>, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, <<"ㅏ">>, Padchim}];

merge({character, Lead, <<"ㅡ">>, none}, {character, <<"ᄋ">>, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, <<"ㅏ">>, Padchim}];

merge({character, Lead, <<"ㅣ">>, none}, {character, <<"ᄋ">>, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅕ">>, Padchim}];

% 면 connective

merge({character, _, _, none}=Character, {character, <<"ᄆ">>, <<"ㅕ">>, <<"ᆫ">>}=Myun) ->
    [Character, Myun];

merge({character, _, _, _}=Character, {character, <<"ᄆ">>, <<"ㅕ">>, <<"ᆫ">>}=Myun) ->
    [Character, {character, <<"ᄋ">>, <<"ㅡ">>, none}, Myun];

merge(Character1, Character2) ->
    [Character1, Character2].

past_stem(Verb) when is_binary(Verb) ->
    SplitVerb = hangul:split(Verb),
    case is_list(SplitVerb) of
        true -> 
            LeadString = lists:sublist(SplitVerb, length(SplitVerb) - 1),
            EndCharacter = lists:last(SplitVerb),
            NewEndString = past_stem(EndCharacter),
            hangul:join(LeadString ++ NewEndString);
        false -> 
            hangul:join(past_stem(SplitVerb))
    end;

past_stem({character, _, <<"ㅗ">>, _}=Verb) ->
    merge(Verb, {character, <<"ᄋ">>, <<"ㅏ">>, <<"ᆻ">>});

past_stem({character, _, Vowel, _}=Verb) when Vowel =:= <<"ㅓ">> orelse Vowel =:= <<"ㅏ">> ->
    merge(Verb, {character, <<"ᄋ">>, Vowel, <<"ᆻ">>});
    
past_stem(Verb) ->
    merge(Verb, {character, <<"ᄋ">>, <<"ㅓ">>, <<"ᆻ">>}).

past_informal(Verb) ->
    merge(past_stem(Verb), <<"어">>).

past_formal(Verb) ->
    merge(past_informal(Verb), <<"요">>).

past_super_formal(Verb) ->
    merge(merge(merge(past_stem(Verb), <<"습">>), <<"니">>), <<"다">>).

present_simple(Verb) when is_binary(Verb) ->
    SplitVerb = hangul:split(Verb),
    case is_list(SplitVerb) of
        true -> 
            LeadString = lists:sublist(SplitVerb, length(SplitVerb) - 1),
            EndCharacter = lists:last(SplitVerb),
            NewEndString = present_simple(EndCharacter),
            hangul:join(LeadString ++ NewEndString);
        false -> 
            hangul:join(present_simple(SplitVerb))
    end;

present_simple(Verb) when is_binary(Verb) ->
    hangul:join(present_simple(hangul:split(Verb)));

present_simple({character, _, <<"ㅗ">>, _}=Verb) ->
    merge(Verb, {character, <<"ᄋ">>, <<"ㅏ">>, none});

present_simple({character, _, <<"ㅜ">>, _}=Verb) ->
    merge(Verb, {character, <<"ᄋ">>, <<"ㅓ">>, none});

present_simple({character, _, Vowel, _}=Verb) when Vowel =:= <<"ㅓ">> orelse Vowel =:= <<"ㅏ">> ->
    merge(Verb, {character, <<"ᄋ">>, Vowel, none}).


present_formal(Verb) ->
    merge(present_simple(Verb), <<"요">>).

propositive_informal(Verb) ->
    merge(Verb, <<"자">>).

propositive_super_formal(Verb) ->
    merge(merge(merge(Verb, <<"읍">>), <<"시">>), <<"다">>).

imperitive_polite(Verb) ->
    merge(merge(Verb, <<"세">>), <<"요">>).

main(_Args) ->  
    <<"워">> = merge(<<"우">>, <<"어">>),
    <<"나아">> = merge(<<"낫">>, <<"아">>),
    <<"봐">> = merge(<<"보">>, <<"아">>),
    <<"봤">> = merge(<<"보">>, <<"았">>),
    <<"바">> = merge(<<"브">>, <<"아">>),
    <<"려">> = merge(<<"리">>, <<"어">>),
    <<"렸">> = merge(<<"리">>, <<"었">>), 
    <<"셨">> = merge(<<"시">>, <<"었">>),
    <<"기다려">> = merge(<<"기다리">>, <<"어">>),
    <<"썼">> = merge(<<"쓰">>, <<"었">>),
    <<"됐">> = merge(<<"되">>, <<"었">>), 
    <<"몰라">> = merge(<<"모">>, <<"르">>),
    <<"들어">> = merge(<<"듣">>, <<"어">>),
    <<"추워">> = merge(<<"춥">>, <<"어">>),
    <<"믿어">> = merge(<<"믿">>, <<"어">>),
    
    <<"갑">> = merge(<<"가">>, <<"읍">>),
    
    % merging conjunctions
    <<"나면">> = merge(<<"나">>, <<"면">>),
    <<"웃으면">> = merge(<<"웃">>, <<"면">>),
    
    <<"갔">> = past_stem(<<"가">>),
    <<"읽었">> = past_stem(<<"읽">>),
    <<"먹었">> = past_stem(<<"먹">>),
    <<"봤">> = past_stem(<<"보">>),
    <<"왔">> = past_stem(<<"오">>),
    <<"기다렸">> = past_stem(<<"기다리">>),
    <<"추웠">> = past_stem(<<"춥">>),
    <<"꺼냈">> = past_stem(<<"꺼내">>),
    <<"구웠">> = past_stem(<<"굽">>),
    
    <<"갔어">> = past_informal(<<"가">>),
    <<"읽었어">> = past_informal(<<"읽">>),
    <<"먹었어">> = past_informal(<<"먹">>),
    <<"봤어">> = past_informal(<<"보">>),
    <<"왔어">> = past_informal(<<"오">>),
    <<"기다렸어">> = past_informal(<<"기다리">>),
    <<"추웠어">> = past_informal(<<"춥">>),
    <<"꺼냈어">> = past_informal(<<"꺼내">>),
    <<"구웠어">> = past_informal(<<"굽">>),
    
    <<"갔어요">> = past_formal(<<"가">>),
    
    <<"갔습니다">> = past_super_formal(<<"가">>),
    
    <<"가">> = present_simple(<<"가">>),
    <<"와">> = present_simple(<<"오">>),
    <<"추워">> = present_simple(<<"춥">>),
    <<"알아">> = present_simple(<<"알">>),
    
    <<"와요">> = present_formal(<<"오">>),
    <<"알아요">> = present_formal(<<"알">>),
    
    <<"가자">> = propositive_informal(<<"가">>),
    
    <<"갑시다">> = propositive_super_formal(<<"가">>),
    <<"먹읍시다">> = propositive_super_formal(<<"먹">>),
    
    <<"하세요">> = imperitive_polite(<<"하">>).
