 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

TESTFILENAME = '/mnt/data2/Yao Ming retire'

SELECT_TOP_N_TWEETS_CONFIGS = {
    'Sports': {
        'infilenames': [#'/mnt/data2/Sports/Yao Ming retire',
                        '/mnt/data2/Sports/Li Na win French Open in tennis',
                        '/mnt/data2/Sports/Spain Series A League'],
        'eventtimes': [#'2011-07-20 14:00:00',
                       '2011-06-04 23:00:00',
                       '2009-08-28 00:00:00'],
        'unittime': 60,
        'm': 3 * 24 * 60,
        'n': 10,
        'outfilename': '/mnt/exps/zhang2012/Sports.curves'
        },
    'Disaster': {
        'infilenames': ['/mnt/data2/Disaster/Bohai bay oil spill',
                        '/mnt/data2/Disaster/earthquake of Yunnan Yingjiang',
                        #'/mnt/data2/Disaster/Gansu school bus crash',
                        '/mnt/data2/Disaster/Japan Earthquake',
                        '/mnt/data2/Disaster/line 10 of Shanghai-Metro pileup',
                        '/mnt/data2/Disaster/Wenzhou train collision',
                        '/mnt/data2/Disaster/Yushu earthquake',
                        '/mnt/data2/Disaster/Zhouqu landslide'],
        'eventtimes': ['2011-06-04 00:00:00',
                       '2011-03-10 00:00:00',
                       #'2011-11-16 00:00:00',
                       '2011-03-11 00:00:00',
                       '2011-09-27 00:00:00',
                       '2010-04-14 00:00:00',
                       '2010-08-07 00:00:00'
                       ],
        'unittime': 60,
        'm': 3 * 24 * 60,
        'n': 30,
        'outfilename': '/mnt/exps/zhang2012/Disaster.curves'
        },
    'Politics': {
        'infilenames': ['/mnt/data2/Politics/death of Muammar Gaddafi',
                        #'/mnt/data2/Politics/the death of Kim Jongil',
                        '/mnt/data2/Politics/the death of Osama Bin Laden',
                        '/mnt/data2/Politics/Zhili disobey tax official violent'],
        'eventtimes': ['2011-10-20 00:00:00',
                       #'2011-12-17 00:00:00',
                       '2011-05-02 00:00:00',
                       '2010-02-01 00:00:00'
                       ],
        'unittime': 60,
        'm': 3 * 24 * 60,
        'n': 60,
        'outfilename': '/mnt/exps/zhang2012/Politics.curves'
        },
    'IT': {
        'infilenames': ['/mnt/data2/IT/death of Steve Jobs',
                        #'/mnt/data2/IT/iphone4s release',
                        '/mnt/data2/IT/Motorola was acquisitions by Google',
                        '/mnt/data2/IT/Windows Phone release',
                        '/mnt/data2/IT/Xiaomi release'],
        'eventtimes': ['2011-10-05 00:00:00',
                       #'2011-10-14 00:00:00',
                       '2011-08-15 00:00:00',
                       '2010-10-11 00:00:00',
                       '2011-08-16 00:00:00'],
        'unittime': 60,
        'm': 3 * 24 * 60,
        'n': 20,
        'outfilename': '/mnt/exps/zhang2012/IT.curves'
        },
    'NationalEvents': {
        'infilenames': ['/mnt/data2/NationalEvents/House prices',
                        '/mnt/data2/NationalEvents/individual income tax threshold rise up to 3500',
                        #'/mnt/data2/NationalEvents/Shenzhou-8 launch successfully',
                        '/mnt/data2/NationalEvents/Tiangong-1 launch successfully'],
        'eventtimes': ['2010-04-17 00:00:00',
                       '2011-06-30 00:00:00',
                       #'2011-11-01 00:00:00',
                       '2011-09-29 00:00:00'],
        'unittime': 60,
        'm': 3 * 24 * 60,
        'n': 200,
        'outfilename': '/mnt/exps/zhang2012/NationalEvents.curves'
        },
    'Social': {
        'infilenames': ['/mnt/data2/Social/Anshun incident',
                        '/mnt/data2/Social/case of running fast car in Heibei University',
                        '/mnt/data2/Social/Chaozhou riot',
                        '/mnt/data2/Social/China Petro chemical Co. Ltd',
                        '/mnt/data2/Social/Chongqing gang trials',
                        #'/mnt/data2/Social/Death of Wang Yue',
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
                        '/mnt/data2/Social/Yihuang self-immolation incident'],
        'eventtimes': ['2010-01-12 00:00:00',
                       '2010-10-16 00:00:00',
                       '2011-06-06 00:00:00',
                       '2011-04-14 00:00:00',
                       '2009-07-10 00:00:00',
                       #'2011-10-13 00:00:00',
                       '2009-05-10 00:00:00',
                       '2011-09-01 00:00:00',
                       '2010-01-23 00:00:00',
                       '2011-05-26 00:00:00',
                       '2011-06-21 00:00:00',
                       '2010-01-26 00:00:00',
                       '2011-08-04 00:00:00',
                       '2011-09-21 00:00:00',
                       '2010-12-25 00:00:00',
                       '2011-08-11 00:00:00',
                       '2011-04-13 00:00:00',
                       '2010-03-17 00:00:00',
                       '2010-07-01 00:00:00',
                       '2010-10-20 00:00:00',
                       '2010-09-10 00:00:00'],
        'unittime': 60,
        'm': 3 * 24 * 60,
        'n': 120,
        'outfilename': '/mnt/exps/zhang2012/Social.curves'
        }
    }

GET_TEST_CURVES_CONFIGS = [
        {
            'infilename': '/mnt/data2/Sports/Yao Ming retire',
            'eventtime': '2011-07-20 14:00:00',
            'unittime': 60,
            'm': 3 * 24 * 60,
            'outfilename': '/mnt/exps/zhang2012/Yao Ming retire.curves'
            },
        {
            'infilename': '/mnt/data2/Disaster/Gansu school bus crash',
            'eventtime': '2011-11-16 00:00:00',
            'unittime': 60,
            'm': 3 * 24 * 60,
            'outfilename': '/mnt/exps/zhang2012/Gansu school bus crash.curves'
            },
        {
            'infilename': '/mnt/data2/Politics/the death of Kim Jongil',
            'eventtime': '2011-12-17 00:00:00',
            'unittime': 60,
            'm': 3 * 24 * 60,
            'outfilename': '/mnt/exps/zhang2012/the death of Kim Jongil.curves'
            },
        {
            'infilename': '/mnt/data2/IT/iphone4s release',
            'eventtime': '2011-10-14 00:00:00',
            'unittime': 60,
            'm': 3 * 24 * 60,
            'outfilename': '/mnt/exps/zhang2012/iphone4s release.curves'
            },
        {
            'infilename': '/mnt/data2/NationalEvents/Shenzhou-8 launch successfully',
            'eventtime': '2011-11-01 00:00:00',
            'unittime': 60,
            'm': 3 * 24 * 60,
            'outfilename': '/mnt/exps/zhang2012/Shenzhou-8 launch successfully.curves'
            },
        {
            'infilename': '/mnt/data2/Social/Death of Wang Yue',
            'eventtime': '2011-10-13 00:00:00',
            'unittime': 60,
            'm': 3 * 24 * 60,
            'outfilename': '/mnt/exps/zhang2012/Death of Wang Yue.curves'
            },

        ]

PREDICT_RTNUMS_CONFIGS = [
        {
            'infilename1': '/mnt/exps/zhang2012/Sports.curves',
            'infilename2': '/mnt/exps/zhang2012/Yao Ming retire.curves',
            'simthreshold': 0.9,
            'errthreshold': 0.3,
            'm': 180,
            'outfilename': '/mnt/exps/zhang2012/Yao Ming retire.results'
            },
        {
            'infilename1': '/mnt/exps/zhang2012/Disaster.curves',
            'infilename2': '/mnt/exps/zhang2012/Gansu school bus crash.curves',
            'simthreshold': 0.9,
            'errthreshold': 0.3,
            'm': 180,
            'outfilename': '/mnt/exps/zhang2012/Gansu school bus crash.results'
            },
        {
            'infilename1': '/mnt/exps/zhang2012/Politics.curves',
            'infilename2': '/mnt/exps/zhang2012/the death of Kim Jongil.curves',
            'simthreshold': 0.9,
            'errthreshold': 0.3,
            'm': 180,
            'outfilename': '/mnt/exps/zhang2012/the death of Kim Jongil.results'
            },
        {
            'infilename1': '/mnt/exps/zhang2012/IT.curves',
            'infilename2': '/mnt/exps/zhang2012/iphone4s release.curves',
            'simthreshold': 0.9,
            'errthreshold': 0.3,
            'm': 180,
            'outfilename': '/mnt/exps/zhang2012/iphone4s release.results'
            },
        {
            'infilename1': '/mnt/exps/zhang2012/NationalEvents.curves',
            'infilename2': '/mnt/exps/zhang2012/Shenzhou-8 launch successfully.curves',
            'simthreshold': 0.9,
            'errthreshold': 0.3,
            'm': 180,
            'outfilename': '/mnt/exps/zhang2012/Shenzhou-8 launch successfully.results'
            },
        {
            'infilename1': '/mnt/exps/zhang2012/Social.curves',
            'infilename2': '/mnt/exps/zhang2012/Death of Wang Yue.curves',
            'simthreshold': 0.9,
            'errthreshold': 0.3,
            'm': 180,
            'outfilename': '/mnt/exps/zhang2012/Death of Wang Yue.results'
            },

        ]

CALC_PRECISION = {
        'infilenames': ['/mnt/exps/zhang2012/Yao Ming retire.results',
                        '/mnt/exps/zhang2012/Gansu school bus crash.results',
                        '/mnt/exps/zhang2012/the death of Kim Jongil.results',
                        '/mnt/exps/zhang2012/iphone4s release.results',
                        '/mnt/exps/zhang2012/Shenzhou-8 launch successfully.results',
                        '/mnt/exps/zhang2012/Death of Wang Yue.results']
        }

CHECK_OVERLAPS = {
        'test': [
            '/mnt/exps/zhang2012/Yao Ming retire.curves',
            '/mnt/exps/zhang2012/Gansu school bus crash.curves',
            '/mnt/exps/zhang2012/the death of Kim Jongil.curves',
            '/mnt/exps/zhang2012/iphone4s release.curves',
            '/mnt/exps/zhang2012/Shenzhou-8 launch successfully.curves',
            '/mnt/exps/zhang2012/Death of Wang Yue.curves'],
        'top': [
            '/mnt/exps/zhang2012/Sports.curves',
            '/mnt/exps/zhang2012/Disaster.curves',
            '/mnt/exps/zhang2012/Politics.curves',
            '/mnt/exps/zhang2012/IT.curves',
            '/mnt/exps/zhang2012/NationalEvents.curves',
            '/mnt/exps/zhang2012/Social.curves'
            ],
        'all': [
            '/mnt/exps/zhang2012/Yao Ming retire.curves',
            '/mnt/exps/zhang2012/Gansu school bus crash.curves',
            '/mnt/exps/zhang2012/the death of Kim Jongil.curves',
            '/mnt/exps/zhang2012/iphone4s release.curves',
            '/mnt/exps/zhang2012/Shenzhou-8 launch successfully.curves',
            '/mnt/exps/zhang2012/Death of Wang Yue.curves',
            '/mnt/exps/zhang2012/Sports.curves',
            '/mnt/exps/zhang2012/Disaster.curves',
            '/mnt/exps/zhang2012/Politics.curves',
            '/mnt/exps/zhang2012/IT.curves',
            '/mnt/exps/zhang2012/NationalEvents.curves',
            '/mnt/exps/zhang2012/Social.curves'
            ]
        }
