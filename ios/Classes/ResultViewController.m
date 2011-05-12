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
    }
    return self;
}

- (void)dealloc
{
    tabBar.delegate = nil;
    [tabBar release];
    [tabPast release];
    [tabPresent release];
    [tabFuture release];
    [tabDonate release];
    verbTable.delegate = nil;
    verbTable.dataSource = nil;
    [verbTable release];
    verbTableController.delegate = nil;
    [verbTableController release];
    webView.delegate = nil;
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
    regular = false;
    self.title = [NSString stringWithFormat:@"%@다", verbStem];
    tabBar.selectedItem = tabPresent;
    verbTableController = [[VerbTableController alloc] init];
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
        self.tabBar.selectedItem = tabPresent;
        [self tabBar:self.tabBar didSelectItem:(self.tabBar.selectedItem)];
    }
    
    [verbTable reloadData];
}

- (void)webViewDidFinishLoad:(UIWebView *)webView
{
    [self loadConjugations];
}

- (void)loadConjugations
{
    NSString* infinitive = [NSString stringWithFormat:@"%@다", verbStem]; 
    NSString* jScript = [NSString stringWithFormat:@"fetch_conjugations('%@',%@);", infinitive, regular? @"true":@"false"];
    NSString* retVal = [self.webView stringByEvaluatingJavaScriptFromString:jScript];
    
    [verbTableController.conjugations removeAllObjects];
    
    for (NSString* line in [retVal componentsSeparatedByString:@"\n"]) {
        if ([line length] > 0)
        {
            NSArray* components = [line componentsSeparatedByString:@","];
            Conjugation* conjugation = [[Conjugation alloc] init];
            conjugation.conjugationName = [components objectAtIndex:0];
            conjugation.conjugatedVerb = [components objectAtIndex:1];
            [verbTableController.conjugations addObject:conjugation];
            [conjugation release];
        }
    }
    
    [verbTableController.conjugations sortUsingSelector:@selector(compare:)];
    [verbTable reloadData];
    
    retVal = [self.webView stringByEvaluatingJavaScriptFromString:@"both_regular_and_irregular();"];
    if ([retVal isEqualToString:@"true"]) {
        if (!addedUIForDualForm)
            [self addUIForDualForm];
        [self setUIForForm];
    }
}

- (void)addUIForDualForm 
{
    // Replace titleView
    CGRect headerTitleSubtitleFrame = CGRectMake(0, 0, 140, 44);    
    UIView* _headerTitleSubtitleView = [[[UILabel alloc] initWithFrame:headerTitleSubtitleFrame] autorelease];
    _headerTitleSubtitleView.backgroundColor = [UIColor clearColor];
    _headerTitleSubtitleView.autoresizesSubviews = YES;
    
    CGRect titleFrame = CGRectMake(0, 2, 140, 24);  
    UILabel *titleView = [[[UILabel alloc] initWithFrame:titleFrame] autorelease];
    titleView.backgroundColor = [UIColor clearColor];
    titleView.font = [UIFont boldSystemFontOfSize:20];
    titleView.textAlignment = UITextAlignmentCenter;
    titleView.textColor = [UIColor whiteColor];
    titleView.shadowColor = [UIColor darkGrayColor];
    titleView.shadowOffset = CGSizeMake(0, -1);
    titleView.adjustsFontSizeToFitWidth = YES;
    [_headerTitleSubtitleView addSubview:titleView];
    
    CGRect subtitleFrame = CGRectMake(0, 24, 140, 44-24);   
    UILabel *subtitleView = [[[UILabel alloc] initWithFrame:subtitleFrame] autorelease];
    subtitleView.backgroundColor = [UIColor clearColor];
    subtitleView.font = [UIFont systemFontOfSize:13];
    subtitleView.textAlignment = UITextAlignmentCenter;
    subtitleView.textColor = [UIColor lightGrayColor];
    subtitleView.shadowColor = [UIColor darkGrayColor];
    subtitleView.shadowOffset = CGSizeMake(0, -1);
    subtitleView.adjustsFontSizeToFitWidth = YES;
    [_headerTitleSubtitleView addSubview:subtitleView];
    
    _headerTitleSubtitleView.autoresizingMask = (UIViewAutoresizingFlexibleLeftMargin |
                                                 UIViewAutoresizingFlexibleRightMargin |
                                                 UIViewAutoresizingFlexibleTopMargin |
                                                 UIViewAutoresizingFlexibleBottomMargin);
    
    self.navigationItem.titleView = _headerTitleSubtitleView;
    
    UIBarButtonItem *regularButton = [[UIBarButtonItem alloc] initWithTitle:@"" 
                                                                      style:UIBarButtonItemStyleBordered target:self action:@selector(switchVerbForm:)];      
    self.navigationItem.rightBarButtonItem = regularButton;
    [regularButton release];
    addedUIForDualForm = true;
}

- (void)setUIForForm 
{
    UIView* headerTitleSubtitleView = self.navigationItem.titleView;
    UILabel* titleView = [headerTitleSubtitleView.subviews objectAtIndex:0];
    UILabel* subtitleView = [headerTitleSubtitleView.subviews objectAtIndex:1];
    assert((titleView != nil) && (subtitleView != nil) && ([titleView isKindOfClass:[UILabel class]]) && ([subtitleView isKindOfClass:[UILabel class]]));
    titleView.text = [NSString stringWithFormat:@"%@다", verbStem];
    subtitleView.text = regular? @"Regular Form":@"Irregular Form";
    
    UIBarButtonItem* button = self.navigationItem.rightBarButtonItem;
    button.title = regular? @"Irregular":@"Regular";
}

- (void)switchVerbForm:(id)sender {
	regular = !regular;
    [self loadConjugations];
}

- (void)verbTable:(VerbTableController *)controller didSelectConjugation:(NSString *)conjugationName verb:(NSString*)conjugatedVerb
{
    SingleVerbController* detailViewController = [[SingleVerbController alloc] init];
    detailViewController.infinitive = [NSString stringWithFormat:@"%@다", verbStem];
    detailViewController.conjugationName = conjugationName;
    detailViewController.title = conjugatedVerb;
    detailViewController.regular = regular;
    [self.navigationController pushViewController:detailViewController animated:YES];
    [detailViewController release];
}

@end
