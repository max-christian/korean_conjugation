//
//  VerbTableController.h
//  Dongsa
//
//  Created by Max Christian on 22/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "CustomVerbCell.h"
#import "Conjugation.h"
#import "SingleVerbController.h"

@protocol VerbTableDelegate;

@interface VerbTableController : UITableViewController {
    NSMutableArray* conjugations;
    NSPredicate* conjugationFilter;
    id <VerbTableDelegate> delegate;
}

@property (nonatomic, retain) NSMutableArray* conjugations;
@property (nonatomic, retain) NSPredicate* conjugationFilter;
@property (nonatomic, retain) id <VerbTableDelegate> delegate;

@end

@protocol VerbTableDelegate
- (void) verbTable:(VerbTableController*)controller didSelectConjugation:(NSString*)conjugationName verb:(NSString*)conjugatedVerb;
@end
