//
//  KoreanOnlyInput.h
//  Dongsa
//
//  Created by Max Christian on 01/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <AudioToolbox/AudioToolbox.h>

@interface KoreanOnlyInput : NSObject <UITextFieldDelegate>
{
    NSMutableCharacterSet* koreanUnicode; 
}

@end
