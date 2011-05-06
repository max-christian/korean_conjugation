//
//  DongsaAppDelegate.h
//  Dongsa
//
//  Created by Max on 31/10/2010.
//  (C) 2010 Max C - licensed under the AGPL 3.0
//

#import <UIKit/UIKit.h>
#import "DonationObserver.h"

#define NATIVE_INTERFACE

@class DongsaViewController;

@interface DongsaAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    DonationObserver* donationObserver;

#ifdef HTML_INTERFACE
    DongsaViewController *viewController;
#endif
    
#ifdef NATIVE_INTERFACE
    UINavigationController* navigationController;
#endif
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, assign) DonationObserver* donationObserver;

#ifdef HTML_INTERFACE
@property (nonatomic, retain) IBOutlet DongsaViewController *viewController;
#endif

#ifdef NATIVE_INTERFACE
@property (nonatomic, retain) IBOutlet UINavigationController *navigationController;
#endif

@end

