//
//  DonationObserver.h
//  Dongsa
//
//  Created by Max Christian on 04/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <StoreKit/StoreKit.h>
#import "BeerFund.h"

@interface DonationObserver : NSObject <SKPaymentTransactionObserver> 
{
    BeerFund* beerFund;
}

@property (nonatomic, assign) BeerFund* beerFund;

- (void) paymentQueue:(SKPaymentQueue *)queue updatedTransactions:(NSArray *)transactions;
- (void) completeTransaction: (SKPaymentTransaction *)transaction;
- (void) restoreTransaction: (SKPaymentTransaction *)transaction;
- (void) failedTransaction: (SKPaymentTransaction *)transaction;
- (void) recordTransaction: (SKPaymentTransaction *)transaction;
- (void) restoreInterface;

@end
