//
//  CustomVerbCell.h
//  Dongsa
//
//  Created by Max Christian on 22/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface CustomVerbCell : UITableViewCell {
    UILabel *conjugatedVerb;
    UILabel *conjugationName;
}

@property (nonatomic, retain) IBOutlet UILabel *conjugatedVerb;
@property (nonatomic, retain) IBOutlet UILabel *conjugationName;

@end
