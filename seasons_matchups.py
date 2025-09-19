# Dictionary for 1st round playoff matchups from 2000-2023
from datetime import date

NBA_SEASONS = {
    '2000-2001': {'start': date(2000, 10, 31), 'end': date(2001, 4, 18)},
    '2001-2002': {'start': date(2001, 10, 30), 'end': date(2002, 4, 17)},
    '2002-2003': {'start': date(2002, 10, 29), 'end': date(2003, 4, 16)},
    '2003-2004': {'start': date(2003, 10, 28), 'end': date(2004, 4, 14)},
    '2004-2005': {'start': date(2004, 11, 2), 'end': date(2005, 4, 20)},
    '2005-2006': {'start': date(2005, 11, 1), 'end': date(2006, 4, 19)},
    '2006-2007': {'start': date(2006, 10, 31), 'end': date(2007, 4, 18)},
    '2007-2008': {'start': date(2007, 10, 30), 'end': date(2008, 4, 16)},
    '2008-2009': {'start': date(2008, 10, 28), 'end': date(2009, 4, 15)},
    '2009-2010': {'start': date(2009, 10, 27), 'end': date(2010, 4, 14)},
    '2010-2011': {'start': date(2010, 10, 26), 'end': date(2011, 4, 13)},
    '2011-2012': {'start': date(2011, 12, 25), 'end': date(2012, 4, 26)},
    '2012-2013': {'start': date(2012, 10, 30), 'end': date(2013, 4, 17)},
    '2013-2014': {'start': date(2013, 10, 29), 'end': date(2014, 4, 16)},
    '2014-2015': {'start': date(2014, 10, 28), 'end': date(2015, 4, 15)},
    '2015-2016': {'start': date(2015, 10, 27), 'end': date(2016, 4, 13)},
    '2016-2017': {'start': date(2016, 10, 25), 'end': date(2017, 4, 12)},
    '2017-2018': {'start': date(2017, 10, 17), 'end': date(2018, 4, 11)},
    '2018-2019': {'start': date(2018, 10, 16), 'end': date(2019, 4, 10)},
    '2019-2020': {'start': date(2019, 10, 22), 'end': date(2020, 9, 28)},
    '2020-2021': {'start': date(2020, 12, 22), 'end': date(2021, 7, 22)},
    '2021-2022': {'start': date(2021, 10, 19), 'end': date(2022, 4, 10)},
    '2022-2023': {'start': date(2022, 10, 18), 'end': date(2023, 4, 9)},
}

PLAYOFF_MATCHUPS = {
    '2000-2001':{
        'East':['sixers', 'pacers', 
                'hornets', 'heat', 
                'raptors', 'knicks',
                  'bucks', 'magic'
        ],
        'West':["spurs","timberwolves",
    "lakers","blazers",
    "kings","suns",
    "mavericks","jazz"
 ]
    },
    '2001-2002':{
        'East':['celtics','sixers',
                'hornets','magic',
                'pistons','raptors',
                'nets','pacers'
        ],
        'West':['mavericks','timberwolves',
                'lakers','blazers',
                'kings','jazz',
                'spurs','supersonics'
        ]
    },
    '2002-2003':{
        'East':['celtics', 'pacers',
        'pistons', 'magic',
        'nets', 'bucks',
        'sixers', 'hornets'

        ],
        'West':['mavericks', 'blazers',
        'lakers', 'timberwolves',
        'kings', 'jazz',
        'spurs', 'suns']
    },
    '2003-2004':{
        'East':['pistons', 'bucks',
 'pacers', 'celtics',
 'heat', 'hornets',
 'nets', 'knicks'],
        'West':['lakers', 'rockets',
 'timberwolves', 'nuggets',
 'kings', 'mavericks',
 'spurs', 'grizzlies']
    },
    '2004-2005':{
        'East':['pistons', 'sixers',
 'pacers', 'celtics',
 'heat', 'nets',
 'wizards', 'bulls'],
        'West':['mavericks', 'rockets',
 'suns', 'grizzlies',
 'spurs', 'nuggets',
 'supersonics', 'kings']

    },
    '2005-2006':{
        'East':['cavaliers', 'wizards',
 'pistons', 'bucks',
 'heat', 'bulls',
 'nets', 'pacers'],
        'West':['mavericks', 'grizzlies',
 'clippers', 'nuggets',
 'suns', 'lakers',
 'spurs', 'kings']
    },
    '2006-2007':{
        'East':['bulls', 'heat',
 'cavaliers', 'wizards',
 'pistons', 'magic',
 'nets', 'raptors']
,
        'West':['warriors', 'mavericks',
 'suns', 'lakers',
 'spurs', 'nuggets',
 'jazz', 'rockets']
    },
    '2007-2008':{
        'East':['celtics', 'hawks',
 'cavaliers', 'wizards',
 'pistons', 'sixers',
 'magic', 'raptors'],
        'West':['lakers', 'nuggets',
 'hornets', 'mavericks',
 'spurs', 'suns',
 'jazz', 'rockets']

    },
    '2008-2009':{
        'East':['hawks', 'heat',
 'celtics', 'bulls',
 'cavaliers', 'pistons',
 'magic', 'sixers']
,
        'West':['mavericks', 'spurs',
 'nuggets', 'hornets',
 'rockets', 'blazers',
 'lakers', 'jazz']

    },
    '2009-2010':{
        'East':['hawks', 'bucks',
 'celtics', 'heat',
 'cavaliers', 'bulls',
 'magic', 'bobcats']
,
        'West':['lakers', 'thunder',
 'suns', 'blazers',
 'spurs', 'mavericks',
 'jazz', 'nuggets']

    },
    '2010-2011':{
        'East':['hawks', 'magic',
 'celtics', 'knicks',
 'bulls', 'pacers',
 'heat', 'sixers']
,
        'West':['hawks', 'magic',
 'celtics', 'knicks',
 'bulls', 'pacers',
 'heat', 'sixers']

    },
    '2011-2012':{
        'East':['celtics', 'hawks',
 'pacers', 'magic',
 'heat', 'knicks',
 'sixers', 'bulls']
,
        'West':['clippers', 'grizzlies',
 'lakers', 'nuggets',
 'thunder', 'mavericks',
 'spurs', 'jazz']

    },
    '2012-2013':{
        'East':['bulls', 'nets',
 'pacers', 'hawks',
 'heat', 'bucks',
 'knicks', 'celtics']
,
        'West':['warriors', 'nuggets',
 'grizzlies', 'clippers',
 'thunder', 'rockets',
 'spurs', 'lakers']

    },
    '2013-2014':{
        'East':['nets', 'raptors',
 'pacers', 'hawks',
 'heat', 'bobcats',
 'wizards', 'bulls']
,
        'West':['clippers', 'warriors',
 'thunder', 'grizzlies',
 'blazers', 'rockets',
 'spurs', 'mavericks']
    },
    '2014-2015':{
        'East':['hawks', 'nets',
 'bulls', 'bucks',
 'cavaliers', 'celtics',
 'wizards', 'raptors']
,
        'West':['warriors', 'pelicans',
 'rockets', 'mavericks',
 'clippers', 'spurs',
 'grizzlies', 'blazers']

    },
    '2015-2016':{
        'East':['hawks', 'celtics',
 'cavaliers', 'pistons',
 'heat', 'hornets',
 'raptors', 'pacers']
,
        'West':['warriors', 'rockets',
 'thunder', 'mavericks',
 'blazers', 'clippers',
 'spurs', 'grizzlies']

    },
    '2016-2017':{
        'East':['celtics', 'bulls',
 'cavaliers', 'pacers',
 'raptors', 'bucks',
 'wizards', 'hawks']
,
        'West':['warriors', 'blazers',
 'rockets', 'thunder',
 'spurs', 'grizzlies',
 'jazz', 'clippers']

    },
    '2017-2018':{
        'East':['celtics', 'bucks',
 'cavaliers', 'pacers',
 'sixers', 'heat',
 'raptors', 'wizards']
,
        'West':['warriors', 'spurs',
 'rockets', 'timberwolves',
 'pelicans', 'blazers',
 'jazz', 'thunder']

    },
    '2018-2019':{
        'East':['celtics', 'pacers',
 'bucks', 'pistons',
 'sixers', 'nets',
 'raptors', 'magic']
,
        'West':['nuggets', 'spurs',
 'warriors', 'clippers',
 'rockets', 'jazz',
 'blazers', 'thunder']

    },
    '2019-2020':{
        'East':['celtics', 'sixers',
 'heat', 'pacers',
 'bucks', 'magic',
 'raptors', 'nets']
,
        'West':['nuggets', 'jazz',
 'rockets', 'thunder',
 'clippers', 'mavericks',
 'lakers', 'blazers']
    },
    '2020-2021':{
        'East':['hawks', 'knicks',
 'nets', 'celtics',
 'bucks', 'heat',
 'sixers', 'wizards']
,
        'West':['nuggets', 'blazers',
 'clippers', 'mavericks',
 'suns', 'lakers',
 'jazz', 'grizzlies']

    },
    '2021-2022':{
        'East':['celtics', 'nets',
 'heat', 'hawks',
 'bucks', 'bulls',
 'sixers', 'raptors']
,
        'West':['mavericks', 'jazz',
 'warriors', 'nuggets',
 'grizzlies', 'timberwolves',
 'suns', 'pelicans']

    },
    '2022-2023':{
        'East':['celtics', 'hawks',
 'heat', 'bucks',
 'knicks', 'cavaliers',
 'sixers', 'nets']
,
        'West':['nuggets', 'timberwolves',
 'warriors', 'kings',
 'lakers', 'grizzlies',
 'suns', 'clippers']

    }
}