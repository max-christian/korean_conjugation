//
//  DongsaViewController.m
//  Dongsa
//
//  Created by Max on 31/10/2010.
//  (C) 2010 Max C - licensed under the AGPL 3.0
//

#import "DongsaViewController.h"

@implementation DongsaViewController

@synthesize webView;

// Implement viewDidLoad to do additional setup after loading the view, typically from a nib.
- (void)viewDidLoad {
    [super viewDidLoad];
	
	NSString *html = [NSString stringWithContentsOfFile:[[NSBundle mainBundle] pathForResource:@"index" ofType:@"html"] 
											   encoding:NSUTF8StringEncoding error:nil];
	[webView loadHTMLString:html baseURL:[[NSBundle mainBundle] bundleURL]];
}

/*
// Override to allow orientations other than the default portrait orientation.
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation {
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}
*/

- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
}

- (void)viewDidUnload {
	// Release any retained subviews of the main view.
	// e.g. self.myOutlet = nil;
}

- (void)dealloc {
    [super dealloc];
}

@end
