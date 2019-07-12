//
//  AClassTestResource.m
//  AClassTest
//
//  Created by yuetianlu on 2019/7/12.
//

#import "AClassTest.h"

@implementation AClassTest

+ (UIImage *)imageNamed:(NSString *)imageName
{
    NSBundle *bundle = [NSBundle bundleForClass:[self class]];
    UIImage *image;
    if (bundle) {
        image = [UIImage imageNamed:imageName inBundle:bundle compatibleWithTraitCollection:nil];
    }
    return image?:[UIImage imageNamed:@""];
}

@end
