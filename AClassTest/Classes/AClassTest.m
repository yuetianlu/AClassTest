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
    UIImage *image;
    NSBundle *mainBundle = [NSBundle bundleForClass:[self class]];
    
    // Check to see if the resource bundle exists inside the top level bundle
    NSBundle *resourcesBundle = [NSBundle bundleWithPath:[mainBundle pathForResource:@"AClassTest" ofType:@"bundle"]];
    
    if (resourcesBundle == nil) {
        resourcesBundle = mainBundle;
    }
    if (resourcesBundle) {
        image = [UIImage imageNamed:imageName inBundle:resourcesBundle compatibleWithTraitCollection:nil];
    }
    return image?:[UIImage imageNamed:@""];
}

@end
