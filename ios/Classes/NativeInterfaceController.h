//
//  NativeInterfaceController.h
//  Dongsa
//
//  Created by Max Christian on 20/04/2011.
//  Copyright 2011 Max Christian. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "NoInputTextField.h"
#import "ResultViewController.h"
#import "KoreanOnlyInput.h"

@interface NativeInterfaceController : UIViewController {
    UITextField *verbField;
    NoInputTextField *enclosingTextField;
}

@property (nonatomic, retain) IBOutlet UITextField *verbField;
@property (nonatomic, retain) IBOutlet NoInputTextField *enclosingTextField;

- (IBAction)verbFieldChanged:(id)sender;
- (IBAction)enclosingTextFieldChanged:(id)sender;
- (IBAction)verbFieldSubmit:(id)sender;

@end
