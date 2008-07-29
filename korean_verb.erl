-module(korean_verb).

-compile(export_all).

% lead = 1 + int [ (Hangul codepoint − 44032)/588 ]

lead(Character) ->
    {ok, [Base]} = utf8:from_binary(<<"ᄀ">>),
    {ok, [X]} = utf8:from_binary(Character),
    CodePoint = 1 + trunc((X - 44032) / 588) + Base - 1,
    {ok, Lead} = utf8:to_binary([CodePoint]),
    {lead, Lead, CodePoint}.

% vowel = 1 + mod (Hangul codepoint − 44032 − tail, 588) / 28

vowel(Character) ->
    {ok, [Base]} = utf8:from_binary(<<"ㅏ">>),
    {ok, [X]} = utf8:from_binary(Character),
    {padchim, _, PadchimCodePoint} = padchim(Character),
    {ok, [PadchimBase]} = utf8:from_binary(<<"ᆨ">>),
    PadchimOffset = PadchimCodePoint - PadchimBase + 1,
    CodePoint = trunc(((X - 44032 - PadchimOffset) rem 588) / 28) + Base,
    {ok, Vowel} = utf8:to_binary([CodePoint]),
    {vowel, Vowel, CodePoint}.

% padchim = mod (Hangul codepoint − 44032, 28)

padchim(Character) ->
    {ok, [Base]} = utf8:from_binary(<<"ᆨ">>),
    {ok, [X]} = utf8:from_binary(Character),
    CodePoint = (X - 44032) rem 28 + Base - 1,
    {ok, Padchim} = utf8:to_binary([CodePoint]),
    case CodePoint of
        4519 -> {padchim, none, 4519};
        _ -> {padchim, Padchim, CodePoint}
    end.

join([H|Tail], Acc) ->
    {ok, [CodePoint]} = utf8:from_binary(join(H)),
    join(Tail, [CodePoint|Acc]);
    
join([], Acc) ->
    {ok, Str} = utf8:to_binary(lists:reverse(Acc)),
    Str.

join(Characters) when is_list(Characters) ->
    join(Characters, []);

join({character, Lead, Vowel, Padchim}) ->
    {ok, [LeadBase]} = utf8:from_binary(<<"ᄀ">>),
    {ok, [VowelBase]} = utf8:from_binary(<<"ㅏ">>),
    {ok, [PadchimBase]} = utf8:from_binary(<<"ᆨ">>),
    {ok, [LeadPoint]} = utf8:from_binary(Lead),
    {ok, [VowelPoint]} = utf8:from_binary(Vowel),
    PadchimPoint = case Padchim of
        none -> 
            {ok, [X]} = utf8:from_binary(<<"ᆨ">>),
            X - 1;
        _ -> 
            {ok, [X]} = utf8:from_binary(Padchim),
            X
    end,
    LeadOffset = LeadPoint - LeadBase,
    VowelOffset = VowelPoint - VowelBase,
    PadchimOffset = PadchimPoint - PadchimBase,
    CodePoint = PadchimOffset + (VowelOffset) * 28 + (LeadOffset) * 588 + 44032 + 1,
    {ok, Character} = utf8:to_binary([CodePoint]),
    Character.

split([H|Tail], Acc) ->
    {ok, Character} = utf8:to_binary([H]),
    split(Tail, [split(Character)|Acc]);

split([], Acc) ->
    lists:reverse(Acc).

split(Character) ->
    {ok, Utf8} = utf8:from_binary(Character),
    case length(Utf8) of
        1 ->
            {lead, Lead, _} = lead(Character),
            {vowel, Vowel, _} = vowel(Character),
            {padchim, Padchim, _} = padchim(Character),
    
            {character, Lead, Vowel, Padchim};
        _ -> 
            split(Utf8, [])
    end.

merge(Character1, Character2) when is_binary(Character1) and is_binary(Character2)->
    SplitCharacter1 = split(Character1),
    SplitCharacter2 = split(Character2),
    case is_list(SplitCharacter1) of
        true -> 
            LeadString = lists:sublist(SplitCharacter1, length(SplitCharacter1) - 1),
            EndCharacter = lists:last(SplitCharacter1),
            NewEndString = merge(EndCharacter, SplitCharacter2),
            join(LeadString ++ NewEndString);
        false -> 
            join(merge(SplitCharacter1, SplitCharacter2))
    end;

% regulars that look irregular
merge({character, <<"ᄆ">>, <<"ㅣ">>, <<"ᆮ">>}=Mit, Character2) ->
    [Mit, Character2];

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

% vowel contractions
merge({character, Lead, <<"ㅐ">>, none}, {character, _, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅐ">>, Padchim}];

merge({character, Lead, <<"ㅡ">>, none}, {character, _, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅓ">>, Padchim}];

merge({character, Lead, <<"ㅜ">>, none}, {character, _, <<"ㅓ">>, Padchim}) -> 
    [{character, Lead, <<"ㅝ">>, Padchim}];

merge({character, Lead, <<"ㅗ">>, none}, {character, _, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, <<"ㅘ">>, Padchim}];

merge({character, Lead, <<"ㅚ">>, none}, {character, _, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅙ">>, Padchim}];

merge({character, Lead, <<"ㅏ">>, none}, {character, _, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, <<"ㅏ">>, Padchim}];

merge({character, Lead, <<"ㅡ">>, none}, {character, _, <<"ㅏ">>, Padchim}) ->
    [{character, Lead, <<"ㅏ">>, Padchim}];

merge({character, Lead, <<"ㅣ">>, none}, {character, _, <<"ㅓ">>, Padchim}) ->
    [{character, Lead, <<"ㅕ">>, Padchim}];

% 면 connective

merge({character, _, _, none}=Character, {character, <<"ᄆ">>, <<"ㅕ">>, <<"ᆫ">>}=Myun) ->
    [Character, Myun];

merge({character, _, _, _}=Character, {character, <<"ᄆ">>, <<"ㅕ">>, <<"ᆫ">>}=Myun) ->
    [Character, {character, <<"ᄋ">>, <<"ㅡ">>, none}, Myun];

merge(Character1, Character2) ->
    [Character1, Character2].

past_stem(Verb) when is_binary(Verb) ->
    SplitVerb = split(Verb),
    case is_list(SplitVerb) of
        true -> 
            LeadString = lists:sublist(SplitVerb, length(SplitVerb) - 1),
            EndCharacter = lists:last(SplitVerb),
            NewEndString = past_stem(EndCharacter),
            join(LeadString ++ NewEndString);
        false -> 
            join(past_stem(SplitVerb))
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

main(_Args) ->
    {padchim, <<"ᆭ">>, 4525} = padchim(<<"않">>),
    {padchim, none, 4519} = padchim(<<"아">>),
    
    {vowel, <<"ㅝ">>, _} = vowel(<<"워">>),
    {vowel, <<"ㅚ">>, _} = vowel(<<"외">>),
    {vowel, <<"ㅣ">>, _} = vowel(<<"인">>),
    {vowel, <<"ㅐ">>, _} = vowel(<<"앤">>),
    {vowel, <<"ㅏ">>, _} = vowel(<<"낫">>),
    
    {lead, <<"ᄂ">>, _} = lead(<<"난">>),
    {lead, <<"ᄀ">>, _} = lead(<<"간">>),
    {lead, <<"ᄈ">>, _} = lead(<<"빨">>),
    
    {character, <<"ᄂ">>, <<"ㅏ">>, <<"ᆺ">>} = split(<<"낫">>),
    {character, <<"ᄂ">>, <<"ㅝ">>, <<"ᆯ">>} = split(<<"눨">>),
    <<"눨">> = join({character, <<"ᄂ">>, <<"ㅝ">>, <<"ᆯ">>}),
    <<"눠">> = join({character, <<"ᄂ">>, <<"ㅝ">>, none}),
    <<"낫">> = join({character, <<"ᄂ">>, <<"ㅏ">>, <<"ᆺ">>}),
    <<"몰">> = join([{character, <<"ᄆ">>, <<"ㅗ">>, <<"ᆯ">>}]),
    
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
    
    <<"갔어요">> = past_formal(<<"가">>).
