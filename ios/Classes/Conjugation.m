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

- (ConjugationCategory)category {
    if ([self.conjugationName rangeOfString:@"\\bpast\\b" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        return conjugationCategoryPast;
    }
    
    if ([self.conjugationName rangeOfString:@"\\bfuture\\b" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        return conjugationCategoryFuture;
    }

    if ([self.conjugationName rangeOfString:@"\\bpresent\\b" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        return conjugationCategoryPresent;
    }

    return conjugationCategoryOther;
}

- (NSComparisonResult)compare:(id)otherObject {
    return self.category > ((Conjugation*)otherObject).category;
}

@end
