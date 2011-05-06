//
//  NoInputTextField.m
//  Dongsa
//
//  Created by Max Christian on 22/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "NoInputTextField.h"


@implementation NoInputTextField

// Prevent the control from ever gaining focus,
// so that only the clear button works:
- (BOOL)canBecomeFirstResponder {
    return NO;
}

@end
