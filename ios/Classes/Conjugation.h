//
//  Conjugation.h
//  Dongsa
//
//  Created by Max Christian on 28/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <Foundation/Foundation.h>

typedef enum {
    conjugationCategoryPast,
    conjugationCategoryPresent,
    conjugationCategoryFuture,
    conjugationCategoryOther
} ConjugationCategory;

@interface Conjugation : NSObject {
    NSString* conjugatedVerb;
    NSString* conjugationName;
    ConjugationCategory category;
}

- (NSComparisonResult)compare:(id)otherObject;

@property (nonatomic, retain) NSString* conjugatedVerb;
@property (nonatomic, retain) NSString* conjugationName;
@property (nonatomic, readonly) ConjugationCategory category;

@end
