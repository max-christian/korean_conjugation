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
@synthesize tenseDescription;

- (void)dealloc
{
    [conjugatedVerb release];
    [tenseDescription release];
    [super dealloc];
}

@end
