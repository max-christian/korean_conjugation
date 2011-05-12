//
//  NativeInterfaceController.m
//  Dongsa
//
//  Created by Max Christian on 20/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import "NativeInterfaceController.h"


@implementation NativeInterfaceController
@synthesize enclosingTextField;
@synthesize verbField;

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
    [verbField release];
    [verbField release];
    [verbField release];
    [enclosingTextField release];
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
    if (verbField.delegate == nil)
        verbField.delegate = [[KoreanOnlyInput alloc] init];
    [verbField becomeFirstResponder];
}

- (void)viewDidUnload
{
    [verbField.delegate release];
    [verbField release];
    verbField = nil;
    [self setVerbField:nil];
    [self setVerbField:nil];
    [self setEnclosingTextField:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    // Return YES for supported orientations
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (IBAction)verbFieldChanged:(id)sender {
    // enable or disable clear button in enclosingTextField
    if ([verbField.text length] == 0)
        enclosingTextField.text = @"";
    else
        enclosingTextField.text = @" ";
}

- (IBAction)enclosingTextFieldChanged:(id)sender {
    // clear button was pressed
    verbField.text = @"";
}

- (IBAction)verbFieldSubmit:(id)sender {
    ResultViewController* rvc = [[ResultViewController alloc] init];
    rvc.verbStem = verbField.text;
    [self.navigationController pushViewController:rvc animated:YES];
    [rvc release];
}

- (void) viewWillAppear:(BOOL)animated
{
    [self.navigationController setNavigationBarHidden:YES animated:animated];
    [super viewWillAppear:animated];
}

- (void) viewWillDisappear:(BOOL)animated
{
    [self.navigationController setNavigationBarHidden:NO animated:animated];
    [super viewWillDisappear:animated];
}

@end
