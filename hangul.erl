-module(hangul).

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
    <<"몰">> = join([{character, <<"ᄆ">>, <<"ㅗ">>, <<"ᆯ">>}]).
