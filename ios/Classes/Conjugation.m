//
//  Conjugation.m
//  Dongsa
//
//  Created by Max Christian on 28/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "Conjugation.h"


@implementation Conjugation
@synthesize tenseDescription;
@synthesize conjugatedVerb;

- (ConjugationCategory)category {
    if ([self.tenseDescription rangeOfString:@"[_\\b]past[_\\b]" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        return conjugationCategoryPast;
    }
    
    if ([self.tenseDescription rangeOfString:@"[_\\b]future[_\\b]" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        return conjugationCategoryFuture;
    }

    if ([self.tenseDescription rangeOfString:@"[_\\b]present[_\\b]" options:(NSCaseInsensitiveSearch+NSRegularExpressionSearch)].location != NSNotFound) {
        return conjugationCategoryPresent;
    }

    return conjugationCategoryOther;
}

- (NSComparisonResult)compare:(id)otherObject {
    return self.category > ((Conjugation*)otherObject).category;
}

@end
