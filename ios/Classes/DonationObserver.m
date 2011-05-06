//
//  DonationObserver.m
//  Dongsa
//
//  Created by Max Christian on 04/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "DonationObserver.h"

@implementation DonationObserver

@synthesize beerFund;

- (void)paymentQueue:(SKPaymentQueue *)queue updatedTransactions:(NSArray *)transactions
{
    for (SKPaymentTransaction *transaction in transactions)
    {
        switch (transaction.transactionState)
        {
            case SKPaymentTransactionStatePurchased:
                [self completeTransaction:transaction];
                break;
            case SKPaymentTransactionStateFailed:
                [self failedTransaction:transaction];
                break;
            case SKPaymentTransactionStateRestored:
                [self restoreTransaction:transaction];
            default:
                break;
        }
    }
}

- (void) completeTransaction: (SKPaymentTransaction *)transaction
{
    [self recordTransaction: transaction];
    // Remove the transaction from the payment queue.
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}

- (void) restoreTransaction: (SKPaymentTransaction *)transaction
{
    [self recordTransaction: transaction];
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}

- (void) failedTransaction: (SKPaymentTransaction *)transaction
{
    [self restoreInterface];
    if (transaction.error.code != SKErrorPaymentCancelled)
    {
        UIAlertView *alert = [[[UIAlertView alloc] initWithTitle:@"Error" message:@"Sorry, donation failed." delegate:self cancelButtonTitle:@"OK" otherButtonTitles:nil] autorelease];
        [alert show];
    }
    [[SKPaymentQueue defaultQueue] finishTransaction: transaction];
}

- (void) recordTransaction: (SKPaymentTransaction *)transaction
{
    [self restoreInterface];
    UIAlertView *alert = [[[UIAlertView alloc] initWithTitle:@"Bottoms up!" message:@"Thanks for your donation, please feel free to buy a round!" delegate:self cancelButtonTitle:@"OK" otherButtonTitles:nil] autorelease];
    [alert show];
}

- (void) restoreInterface
{
    // refresh the button, which has been changed to "Please wait" and disabled
    [beerFund loadProductData];
}

@end
