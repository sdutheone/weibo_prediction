#!/usr/bin/env python
# -*- coding: utf-8 -*-

events = [
        {
           'name': "Anshun incident",
           'category': 'Social',
           'time': '2010-01-12 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Anshun incident",
           },
        {
           'name': "Bohai bay oil spill",
           'category': 'Disaster',
           'time': '2011-06-04 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Bohai bay oil spill",
           },
        {
           'name': "case of running fast car in Heibei University",
           'category': 'Social',
           'time': '2010-10-16 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/case of running fast car in Heibei University",
           },
        {
           'name': "Chaozhou riot",
           'category': 'Social',
           'time': '2011-06-06 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Chaozhou riot",
           },
        {
           'name': "China Petro chemical Co. Ltd",
           'category': 'Social',
           'time': '2011-04-14 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/China Petro chemical Co. Ltd",
           },
        {
           'name': "Chongqing gang trials",
           'category': 'Social',
           'time': '2009-07-10 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Chongqing gang trials",
           },
        {
           'name': "death of Muammar Gaddafi",
           'category': 'Politics',
           'time': '2011-10-20 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/death of Muammar Gaddafi",
           },
        {
           'name': "death of Steve Jobs",
           'category': 'IT',
           'time': '2011-10-05 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/death of Steve Jobs",
           },
        {
           'name': "Death of Wang Yue",
           'category': 'Social',
           'time': '2011-10-13 00:00:00',
           'usage': 'Test',
           'path': "/mnt/data2/Death of Wang Yue",
           },
        {
           'name': "Deng Yujiao incident",
           'category': 'Social',
           'time': '2009-05-10 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Deng Yujiao incident",
           },
        {
           'name': "earthquake of Yunnan Yingjiang",
           'category': 'Disaster',
           'time': '2011-03-10 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/earthquake of Yunnan Yingjiang",
           },
        {
           'name': "family violence of Li Yang",
           'category': 'Social',
           'time': '2011-09-01 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/family violence of Li Yang",
           },
        {
           'name': "Foxconn worker falls to death",
           'category': 'Social',
           'time': '2010-01-23 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Foxconn worker falls to death",
           },
        {
           'name': "Fuzhou bombings",
           'category': 'Social',
           'time': '2011-05-26 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Fuzhou bombings",
           },
        {
           'name': "Gansu school bus crash",
           'category': 'Disaster',
           'time': '2011-11-16 00:00:00',
           'usage': 'Test',
           'path': "/mnt/data2/Gansu school bus crash",
           },
        {
           'name': "Guo Meimei",
           'category': 'Social',
           'time': '2011-06-21 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Guo Meimei",
           },
        {
           'name': "House prices",
           'category': 'NationalEvents',
           'time': '2010-04-17 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/House prices",
           },
        {
           'name': "incident of self-burning at Yancheng, Jangsu",
           'category': 'Social',
           'time': '2010-01-26 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/incident of self-burning at Yancheng, Jangsu",
           },
        {
           'name': "individual income tax threshold rise up to 3500",
           'category': 'NationalEvents',
           'time': '2011-06-30 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/individual income tax threshold rise up to 3500",
           },
        {
           'name': "iphone4s release",
           'category': 'IT',
           'time': '2011-10-14 00:00:00',
           'usage': 'Test',
           'path': "/mnt/data2/iphone4s release",
           },
        {
           'name': "Japan Earthquake",
           'category': 'Disaster',
           'time': '2011-03-11 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Japan Earthquake",
           },
        {
           'name': "Li Na win French Open in tennis",
           'category': 'Sports',
           'time': '2011-06-04 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Li Na win French Open in tennis",
           },
        {
           'name': "line 10 of Shanghai-Metro pileup",
           'category': 'Disaster',
           'time': '2011-09-27 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/line 10 of Shanghai-Metro pileup",
           },
        {
           'name': "mass suicide at Nanchang Bridge",
           'category': 'Social',
           'time': '2011-08-04 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/mass suicide at Nanchang Bridge",
           },
        {
           'name': "Motorola was acquisitions by Google",
           'category': 'IT',
           'time': '2011-08-15 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Motorola was acquisitions by Google",
           },
        {
           'name': "protests of Wukan",
           'category': 'Social',
           'time': '2011-09-21 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/protests of Wukan",
           },
        {
           'name': "Qian Yunhui",
           'category': 'Social',
           'time': '2010-12-25 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Qian Yunhui",
           },
        {
           'name': "Qianxi riot",
           'category': 'Social',
           'time': '2011-08-11 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Qianxi riot",
           },
        {
           'name': "Shanghai government's urban management officers attack migrant workers in 2011",
           'category': 'Social',
           'time': '2011-04-13 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Shanghai government's urban management officers attack migrant workers in 2011",
           },
        {
           'name': "Shanxi",
           'category': 'Social',
           'time': '2010-03-17 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Shanxi",
           },
        {
           'name': "Shenzhou-8 launch successfully",
           'category': 'NationalEvents',
           'time': '2011-11-01 00:00:00',
           'usage': 'Test',
           'path': "/mnt/data2/Shenzhou-8 launch successfully",
           },
        {
           'name': "Spain Series A League",
           'category': 'Sports',
           'time': '2009-08-28 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Spain Series A League",
           },
        {
           'name': "Tang Jun educatioin qualification fake",
           'category': 'Social',
           'time': '2010-07-01 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Tang Jun educatioin qualification fake",
           },
        {
           'name': "the death of Kim Jongil",
           'category': 'Politics',
           'time': '2011-12-17 00:00:00',
           'usage': 'Test',
           'path': "/mnt/data2/the death of Kim Jongil",
           },
        {
           'name': "the death of Osama Bin Laden",
           'category': 'Politics',
           'time': '2011-05-02 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/the death of Osama Bin Laden",
           },
        {
           'name': "Tiangong-1 launch successfully",
           'category': 'NationalEvents',
           'time': '2011-09-29 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Tiangong-1 launch successfully",
           },
        {
           'name': "Wenzhou train collision",
           'category': 'Disaster',
           'time': '2011-07-23 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Wenzhou train collision",
           },
        {
           'name': "Windows Phone release",
           'category': 'IT',
           'time': '2010-10-11 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Windows Phone release",
           },
        {
           'name': "Xiaomi release",
           'category': 'IT',
           'time': '2011-08-16 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Xiaomi release",
           },
        {
           'name': "Yao Jiaxin murder case",
           'category': 'Social',
           'time': '2010-10-20 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Yao Jiaxin murder case",
           },
        {
           'name': "Yao Ming retire",
           'category': 'Sports',
           'time': '2011-07-20 00:00:00',
           'usage': 'Test',
           'path': "/mnt/data2/Yao Ming retire",
           },
        {
           'name': "Yihuang self-immolation incident",
           'category': 'Social',
           'time': '2010-09-10 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Yihuang self-immolation incident",
           },
        {
           'name': "Yushu earthquake",
           'category': 'Disaster',
           'time': '2010-04-14 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Yushu earthquake",
           },
        {
           'name': "Zhili disobey tax official violent",
           'category': 'Politics',
           'time': '2010-02-01 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Zhili disobey tax official violent",
           },
        {
           'name': "Zhouqu landslide",
           'category': 'Disaster',
           'time': '2010-08-07 00:00:00',
           'usage': 'Train',
           'path': "/mnt/data2/Zhouqu landslide",
           },]

zhang2012 = {
        'outdirname': '/mnt/exps/zhang2012',
        'timeunit': 60,
        'm': 2 * 24 * 60,
        'n': 30,
        'pm': 2 * 60,
        'simthreshold': 0.8,
        'errthreshold': 0.05
        }
