//
//  Conjugation.m
//  Dongsa
//
//  Created by Max Christian on 28/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "Conjugation.h"


@implementation Conjugation
@synthesize conjugationName;
@synthesize conjugatedVerb;
@synthesize category;

-(void) setConjugationName:(NSString *)newName
{
    if (conjugationName != newName)
    {
        [newName retain];
        [conjugationName release];
        conjugationName = newName;
    }
    
    if ([self.conjugationName rangeOfString:@"\\bpast\\b" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        category = conjugationCategoryPast;
    } else if ([self.conjugationName rangeOfString:@"\\bfuture\\b" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        category = conjugationCategoryFuture;
    } else if ([self.conjugationName rangeOfString:@"\\bpresent\\b" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        category = conjugationCategoryPresent;
    } else {
        category = conjugationCategoryOther;
    }
}

- (NSComparisonResult)compare:(id)otherObject {
    return self.category > ((Conjugation*)otherObject).category;
}

- (void)dealloc
{
    self.conjugatedVerb = nil;
    self.conjugationName = nil;
    [super dealloc];
}

@end
