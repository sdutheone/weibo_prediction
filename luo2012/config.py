 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

SPLIT_TRAIN_TWEETS_BY_UID = {
        'infilenames': [
            '/mnt/data2/Sports/Li Na win French Open in tennis',
            '/mnt/data2/Sports/Spain Series A League',
            '/mnt/data2/Disaster/Bohai bay oil spill',
            '/mnt/data2/Disaster/earthquake of Yunnan Yingjiang',
            '/mnt/data2/Disaster/Japan Earthquake',
            '/mnt/data2/Disaster/line 10 of Shanghai-Metro pileup',
            '/mnt/data2/Disaster/Wenzhou train collision',
            '/mnt/data2/Disaster/Yushu earthquake',
            '/mnt/data2/Disaster/Zhouqu landslide',
            '/mnt/data2/Politics/death of Muammar Gaddafi',
            '/mnt/data2/Politics/the death of Osama Bin Laden',
            '/mnt/data2/Politics/Zhili disobey tax official violent',
            '/mnt/data2/IT/death of Steve Jobs',
            '/mnt/data2/IT/Motorola was acquisitions by Google',
            '/mnt/data2/IT/Windows Phone release',
            '/mnt/data2/IT/Xiaomi release',
            '/mnt/data2/NationalEvents/House prices',
            '/mnt/data2/NationalEvents/individual income tax threshold rise up to 3500',
            '/mnt/data2/NationalEvents/Tiangong-1 launch successfully',
            '/mnt/data2/Social/Anshun incident',
            '/mnt/data2/Social/case of running fast car in Heibei University',
            '/mnt/data2/Social/Chaozhou riot',
            '/mnt/data2/Social/China Petro chemical Co. Ltd',
            '/mnt/data2/Social/Chongqing gang trials',
            '/mnt/data2/Social/Deng Yujiao incident',
            '/mnt/data2/Social/family violence of Li Yang',
            '/mnt/data2/Social/Foxconn worker falls to death',
            '/mnt/data2/Social/Fuzhou bombings',
            '/mnt/data2/Social/Guo Meimei',
            '/mnt/data2/Social/incident of self-burning at Yancheng, Jangsu',
            '/mnt/data2/Social/mass suicide at Nanchang Bridge',
            '/mnt/data2/Social/protests of Wukan',
            '/mnt/data2/Social/Qian Yunhui',
            '/mnt/data2/Social/Qianxi riot',
            "/mnt/data2/Social/Shanghai government's urban management officers attack migrant workers in 2011",
            '/mnt/data2/Social/Shanxi',
            '/mnt/data2/Social/Tang Jun educatioin qualification fake',
            '/mnt/data2/Social/Yao Jiaxin murder case',
            '/mnt/data2/Social/Yihuang self-immolation incident'
            ],
        'outdirname': '/mnt/data2/ByUid/Train'
        }

SPLIT_TEST_TWEETS_BY_UID = {
        'infilenames': [
            '/mnt/data2/Sports/Yao Ming retire',
            '/mnt/data2/Disaster/Gansu school bus crash',
            '/mnt/data2/Politics/the death of Kim Jongil',
            '/mnt/data2/IT/iphone4s release',
            '/mnt/data2/NationalEvents/Shenzhou-8 launch successfully',
            '/mnt/data2/Social/Death of Wang Yue'],
        'outdirname': '/mnt/data2/ByUid/Test'
        }


EXTRACT_TRAIN_TWEETS_BY_LIFESPAN = {
        'indirname': '/mnt/data2/ByUid/Train',
        'outdirname': '/mnt/data2/ByUidExtracted/Train',
        'lifespan': 3 * 24 * 60 * 60
        }

EXTRACT_TEST_TWEETS_BY_LIFESPAN = {
        'indirname': '/mnt/data2/ByUid/Test',
        'outdirname': '/mnt/data2/ByUidExtracted/Test',
        'lifespan': 3 * 24 * 60 * 60
        }


CHECK_USER_OVERLAP = {
        'indirname1': '/mnt/data2/ByUidExtracted/Train',
        'indirname2': '/mnt/data2/ByUidExtracted/Test'
        }
