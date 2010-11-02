//
//  DongsaAppDelegate.h
//  Dongsa
//
//  Created by Max on 31/10/2010.
//  (C) 2010 Max C - licensed under the AGPL 3.0
//

#import <UIKit/UIKit.h>

@class DongsaViewController;

@interface DongsaAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    DongsaViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet DongsaViewController *viewController;

@end

