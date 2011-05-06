//
//  BeerFund.h
//  Dongsa
//
//  Created by Max Christian on 04/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <StoreKit/StoreKit.h>

@interface BeerFund : UIViewController <SKProductsRequestDelegate> 
{
    UIButton *buttonDan;
    UIButton *buttonMax;
}

@property (nonatomic, retain) IBOutlet UIButton *buttonDan;
@property (nonatomic, retain) IBOutlet UIButton *buttonMax;

- (IBAction)actionWebsite:(id)sender;
- (IBAction)actionDan:(id)sender;
- (IBAction)actionMax:(id)sender;
- (void)productsRequest:(SKProductsRequest *)request didReceiveResponse:(SKProductsResponse *)response;
- (void)loadProductData;
- (void)showPleaseWait:(UIButton*)button;

@end
