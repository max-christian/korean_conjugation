//
//  ResultViewController.h
//  Dongsa
//
//  Created by Max Christian on 22/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "VerbTableController.h"
#import "Conjugation.h"
#import "BeerFund.h"
#import "DongsaAppDelegate.h"

@interface ResultViewController : UIViewController <UITabBarDelegate, UIWebViewDelegate, VerbTableDelegate> {
    UITabBar *tabBar;
    UITabBarItem *tabPast;
    UITabBarItem *tabPresent;
    UITabBarItem *tabFuture;
    UITabBarItem *tabDonate;
    UITableView *verbTable;
    VerbTableController* verbTableController;
    UIWebView *webView;
    NSString* verbStem;
}

@property (nonatomic, retain) IBOutlet UITabBar *tabBar;
@property (nonatomic, retain) IBOutlet UITabBarItem *tabPast;
@property (nonatomic, retain) IBOutlet UITabBarItem *tabPresent;
@property (nonatomic, retain) IBOutlet UITabBarItem *tabFuture;
@property (nonatomic, retain) IBOutlet UITabBarItem *tabDonate;
@property (nonatomic, retain) IBOutlet UITableView *verbTable;
@property (nonatomic, retain) IBOutlet VerbTableController* verbTableController;
@property (nonatomic, retain) IBOutlet UIWebView *webView;
@property (nonatomic, retain) NSString* verbStem;

@end
