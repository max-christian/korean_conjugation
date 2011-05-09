//
//  CustomVerbCell.m
//  Dongsa
//
//  Created by Max Christian on 22/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "CustomVerbCell.h"

@implementation CustomVerbCell
@synthesize conjugatedVerb;
@synthesize conjugationName;

- (void)dealloc
{
    [conjugatedVerb release];
    [conjugationName release];
    [super dealloc];
}

@end
