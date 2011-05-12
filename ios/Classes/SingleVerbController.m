//
//  SingleVerbController.m
//  Dongsa
//
//  Created by Max Christian on 02/05/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "SingleVerbController.h"


@implementation SingleVerbController

@synthesize infinitive;
@synthesize conjugationName;
@synthesize webView;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        linkCount = 0;
    }
    return self;
}

- (void)dealloc
{
    self.infinitive = nil;
    self.conjugationName = nil;
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
    NSString *html = [NSString stringWithContentsOfFile:[[NSBundle mainBundle] pathForResource:@"ios" ofType:@"html"] 
											   encoding:NSUTF8StringEncoding error:nil];
	[webView loadHTMLString:html baseURL:[[NSBundle mainBundle] bundleURL]];
}

- (void)viewDidUnload
{
    [self setWebView:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (void)webViewDidFinishLoad:(UIWebView *)webView   
{
    NSString* javascript = [NSString stringWithFormat:@"fetch_conjugations('%@',true);", infinitive];
    [self.webView stringByEvaluatingJavaScriptFromString:javascript];
    javascript = [NSString stringWithFormat:@"show_conjugation_detail('%@');", conjugationName];
    [self.webView stringByEvaluatingJavaScriptFromString:javascript];
}

- (BOOL)webView:(UIWebView *)webView shouldStartLoadWithRequest:(NSURLRequest *)request navigationType:(UIWebViewNavigationType)navigationType
{
    if (++linkCount <= 1)
        return YES;
    else
    {
        [[UIApplication sharedApplication] openURL:[request URL]];
        return NO;
    }
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
