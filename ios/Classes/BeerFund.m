//
//  BeerFund.m
//  Dongsa
//
//  Created by Max Christian on 04/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "BeerFund.h"


@implementation BeerFund
@synthesize buttonDan;
@synthesize buttonMax;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)dealloc
{
    [buttonDan release];
    [buttonMax release];
    [super dealloc];
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

NSString* prodBokbunja = @"tc.max.dongsa.bokbunja";
NSString* prodSamadams = @"tc.max.dongsa.samadams";

- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = @"Donations";
    [self loadProductData];
}

- (void)loadProductData
{
    SKProductsRequest* request= [[SKProductsRequest alloc] initWithProductIdentifiers: 
                                 [NSSet setWithObjects:prodBokbunja, prodSamadams, nil]];
    request.delegate = self;
    [request start];
}

- (void)viewDidUnload
{
    [self setButtonDan:nil];
    [self setButtonMax:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (void)productsRequest:(SKProductsRequest *)request didReceiveResponse:(SKProductsResponse *)response
{
    NSArray* products = response.products;
    NSNumberFormatter *numberFormatter = [[NSNumberFormatter alloc] init];
    [numberFormatter setFormatterBehavior:NSNumberFormatterBehavior10_4];
    [numberFormatter setNumberStyle:NSNumberFormatterCurrencyStyle];

    for (int i=0; i<[products count]; i++)
    {
        SKProduct* product = [products objectAtIndex:i];
        UIButton* target = nil;
        
        if ([product.productIdentifier isEqualToString:prodBokbunja]) {
            target = buttonMax;
        } else if ([product.productIdentifier isEqualToString:prodSamadams]) {
            target = buttonDan;
        }
    
        if (target != nil)
        {
            [numberFormatter setLocale:product.priceLocale];
            NSString* formattedPrice = [numberFormatter stringFromNumber:product.price];
            NSString* title = [NSString stringWithFormat:@"%@ (%@)", product.localizedTitle, formattedPrice];
            target.enabled = YES;
            [target setTitle:title forState:UIControlStateNormal];
        }
    }

    [numberFormatter release];
    [request autorelease];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (IBAction)actionWebsite:(id)sender {
    [[UIApplication sharedApplication] openURL:[NSURL URLWithString:@"http://dongsa.net"]];
}

- (void)showPleaseWait:(UIButton*)button {
    [button setTitle:@"Please wait..." forState:UIControlStateNormal];
    button.enabled = NO;
}

- (IBAction)actionDan:(id)sender {
    if ([SKPaymentQueue canMakePayments])
    {
        [self showPleaseWait:sender];
        SKPayment *payment = [SKPayment paymentWithProductIdentifier:@"tc.max.dongsa.samadams"];
        [[SKPaymentQueue defaultQueue] addPayment:payment];
    }
}

- (IBAction)actionMax:(id)sender {
    if ([SKPaymentQueue canMakePayments])
    {
        [self showPleaseWait:sender];
        SKPayment *payment = [SKPayment paymentWithProductIdentifier:@"tc.max.dongsa.bokbunja"];
        [[SKPaymentQueue defaultQueue] addPayment:payment];
    }
}

@end
