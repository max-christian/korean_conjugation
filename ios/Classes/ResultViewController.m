//
//  ResultViewController.m
//  Dongsa
//
//  Created by Max Christian on 22/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "ResultViewController.h"

@implementation ResultViewController

@synthesize tabBar;
@synthesize tabPast;
@synthesize tabPresent;
@synthesize tabFuture;
@synthesize tabDonate;
@synthesize verbTable;
@synthesize verbTableController;
@synthesize webView;
@synthesize verbStem;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
        verbTableController = [[VerbTableController alloc] init];
    }
    return self;
}

- (void)dealloc
{
    [tabBar release];
    [tabPast release];
    [tabPresent release];
    [tabFuture release];
    [tabDonate release];
    [verbTable release];
    [verbTableController release];
    [webView release];
    [super dealloc];
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

- (void)viewDidLoad
{
    [super viewDidLoad];
    self.title = [NSString stringWithFormat:@"%@다", verbStem];
    tabBar.selectedItem = tabPresent;
    verbTable.delegate = verbTableController;
    verbTable.dataSource = verbTableController;
    verbTableController.delegate = self;
    [self tabBar:tabBar didSelectItem:(tabBar.selectedItem)];
	NSString *html = [NSString stringWithContentsOfFile:[[NSBundle mainBundle] pathForResource:@"ios" ofType:@"html"] 
											   encoding:NSUTF8StringEncoding error:nil];
	[webView loadHTMLString:html baseURL:[[NSBundle mainBundle] bundleURL]];
}

- (void)viewDidUnload
{
    [self setTabBar:nil];
    [self setTabPast:nil];
    [self setTabPresent:nil];
    [self setTabFuture:nil];
    [self setTabDonate:nil];
    [self setVerbTable:nil];
    [self setVerbTableController:nil];
    [self setWebView:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)tabBar:(UITabBar *)tabBar didSelectItem:(UITabBarItem *)item
{
    if (item == tabPast) {
        verbTableController.conjugationFilter = [NSPredicate predicateWithBlock:^BOOL(id evaluatedObject, NSDictionary *bindings) {
            Conjugation* c = evaluatedObject;
            return c.category == conjugationCategoryPast;
        }];
    } else if (item == tabPresent) {
        verbTableController.conjugationFilter = [NSPredicate predicateWithBlock:^BOOL(id evaluatedObject, NSDictionary *bindings) {
            Conjugation* c = evaluatedObject;
            return c.category == conjugationCategoryPresent || c.category == conjugationCategoryOther;
        }];
    } else if (item == tabFuture) {
        verbTableController.conjugationFilter = [NSPredicate predicateWithBlock:^BOOL(id evaluatedObject, NSDictionary *bindings) {
            Conjugation* c = evaluatedObject;
            return c.category == conjugationCategoryFuture;
        }];
    } else if (item == tabDonate) {
        BeerFund* beerFund = [[BeerFund alloc] init];
        DongsaAppDelegate* appDelegate = [UIApplication sharedApplication].delegate;
        appDelegate.donationObserver.beerFund = beerFund;
        
        [self.navigationController pushViewController:beerFund animated:YES];
        [beerFund release];
    }
    
    [verbTable reloadData];
}

- (void)webViewDidFinishLoad:(UIWebView *)webView
{
    NSString* jScript = [NSString stringWithFormat:@"fetch_conjugations('%@다');", verbStem];
    NSString* retVal = [self.webView stringByEvaluatingJavaScriptFromString:jScript];
     
    [verbTableController.conjugations removeAllObjects];
    
    for (NSString* line in [retVal componentsSeparatedByString:@"\n"]) {
        if ([line length] > 0)
        {
            NSArray* components = [line componentsSeparatedByString:@","];
            Conjugation* conjugation = [[Conjugation alloc] init];
            conjugation.tenseDescription = [components objectAtIndex:0];
            conjugation.conjugatedVerb = [components objectAtIndex:1];
            [verbTableController.conjugations addObject:conjugation];
        }
    }
    
    [verbTableController.conjugations sortUsingSelector:@selector(compare:)];
    [verbTable reloadData];
}

- (void)verbTable:(VerbTableController *)controller didSelectConjugation:(NSString *)tenseDescription verb:(NSString*)conjugatedVerb
{
    SingleVerbController* detailViewController = [[SingleVerbController alloc] init];
    detailViewController.infinitive = [NSString stringWithFormat:@"%@다", verbStem];
    detailViewController.tenseDescription = tenseDescription;
    detailViewController.title = conjugatedVerb;
    [self.navigationController pushViewController:detailViewController animated:YES];
    [detailViewController release];
}

@end
