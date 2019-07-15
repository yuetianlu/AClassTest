//
//  TLViewController.m
//  AClassTest
//
//  Created by yuetianlu_kyy@163.com on 07/10/2019.
//  Copyright (c) 2019 yuetianlu_kyy@163.com. All rights reserved.
//

#import "TLViewController.h"
#import "ATest.h"
#import "AClassTest.h"

@interface TLViewController ()

@end

@implementation TLViewController

- (void)viewDidLoad
{
    [super viewDidLoad];
    [ATest showA];
    [ATest showA2];
    UIImageView *imageView = [[UIImageView alloc] init];
    imageView.image = [AClassTest imageNamed:@"arrow_down"];
    imageView.frame = CGRectMake(100, 100, 20, 20);
    [self.view addSubview:imageView];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

@end
