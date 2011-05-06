//
//  KoreanOnlyInput.m
//  Dongsa
//
//  Created by Max Christian on 01/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "KoreanOnlyInput.h"

@implementation KoreanOnlyInput

NSMutableCharacterSet* koreanUnicode; 

- (id)init
{
    self = [super init];
    if (self) {
        // From http://www.unicodemap.org/ :
        // 0x1100 - 0x11FF : Hangul Jamo (256)
        // 0x3130 - 0x318F : Hangul Compatibility Jamo (96)
        // 0xAC00 - 0xD7A3 : Hangul Syllables (11172)
        
        koreanUnicode = [[[NSMutableCharacterSet alloc] init] retain];
        NSRange range;
        
        range.location = 0x1100;
        range.length = 1 + 0x11FF - range.location;
        [koreanUnicode addCharactersInRange:range];

        range.location = 0x3130;
        range.length = 1 + 0x318F - range.location;
        [koreanUnicode addCharactersInRange:range];

        range.location = 0xAC00;
        range.length = 1 + 0xD7A3 - range.location;
        [koreanUnicode addCharactersInRange:range];
    }
    return self;
}
                                                                       
- (void)dealloc
{
    [koreanUnicode release];
    [super dealloc];
}
                                                                       
- (BOOL)textField:(UITextField*)textField shouldChangeCharactersInRange:(NSRange)range replacementString:(NSString*)string
{
    if ([string isEqualToString:@"\n"])
        return YES;
    
    BOOL shouldChange = YES;    
    for (int i=0; i<[string length]; i++)
    {
        if (![koreanUnicode characterIsMember:[string characterAtIndex:i]])
            shouldChange = NO;
    }
    
    if (!shouldChange)
    {
        AudioServicesPlaySystemSound(kSystemSoundID_Vibrate);
    }
    
    return shouldChange;
}

@end
