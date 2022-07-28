# Latest plugin updated by @youtubeslgeekshow

# This file is part of Uvindu Bro - Donents.LK Bot  (Telegram Bot)
# Thank you for your codes 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Apache License 2.0 License as
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License 2.0 License for more details.

# You should have received a copy of the Apache License 2.0 License
# along with this program.  If not, see <https://www.apache.org/licenses/LICENSE-2.0/>.


from telethon import TelegramClient, events
import requests
from Hermione.conf import get_str_key
from Hermione import telethn as tbot

def Al(indexx):
    print(indexx)
    r = requests.get('https://www.doenets.lk/result/service/AlResult/{0}'.format(indexx))
    print(r.text)
    jsondata = json.loads(r.text)
    alexamination    = str(jsondata['examination'])
    alyear           = str(jsondata['year'])
    alname           = str(jsondata['name'])
    alindex          = str(jsondata['indexNo'])
    alnic            = str(jsondata['nic'])
    aldrank          = str(jsondata['districtRank'])
    alirank          = str(jsondata['islandRank'])
    alzscore         = str(jsondata['zScore'])
    alstream         = str(jsondata['stream'])
    alsyllabus       = str(jsondata['studentInfo'][2]['value'])
    sub1name         = str(jsondata['subjectResults'][0]['subjectName'])
    sub1result       = str(jsondata['subjectResults'][0]['subjectResult'])
    sub2name         = str(jsondata['subjectResults'][1]['subjectName'])
    sub2result       = str(jsondata['subjectResults'][1]['subjectResult'])
    sub3name         = str(jsondata['subjectResults'][2]['subjectName'])
    sub3result       = str(jsondata['subjectResults'][2]['subjectResult'])
    sub4name         = str(jsondata['subjectResults'][3]['subjectName'])
    sub4result       = str(jsondata['subjectResults'][3]['subjectResult'])
    sub5name         = str(jsondata['subjectResults'][4]['subjectName'])
    sub5result       = str(jsondata['subjectResults'][4]['subjectResult'])

    textt = str(

        '<b>' + alexamination + ' ' + alyear  + '</b>' + '\n' + '\n' +
        'Index No. = ' + '<b>' + alindex + '</b>' + '\n' +
        'Name = '  + '<b>' + alname + '</b>' + '\n' +  'NIC = '  + '<b>' + alnic + '</b>' + '\n' + 
        'District Rank = '  + '<b>' + aldrank + '</b>' + '\n' +  'Island Rank = '  + '<b>' + alirank + '</b>' + '\n' +
        'Z Score = '  + '<b>' + alzscore + '</b>' + '\n' +   'Stream = '  + '<b>' + alstream + '</b>' + '\n' +
        'Syllabus = '  + '<b>' + alsyllabus + '</b>' + '\n' + '\n' + 
        '<u>' + 'Exam Results' + '</u>' +  '\n' + '\n' +  sub1name + ' = ' + '<b>' + sub1result + '</b>' + '\n' + 
        sub2name + ' = '  + '<b>' + sub2result + '</b>' + '\n' +  sub3name + ' = '  + '<b>' + sub3result + '</b>' + '\n' + 
        sub4name + ' = '  + '<b>' + sub4result + '</b>' + '\n' +  sub5name + ' = '  + '<b>' + sub5result + '</b>' + '\n' + '\n' +
        '✅ All the Data Verified by the Government' + '\n' +'~ @HermioneSlBot 🇱🇰 ')

    return textt


def Ol(olindexx):
    print(olindexx)
    r = requests.get('https://www.doenets.lk/result/service/OlResult/{0}'.format(olindexx))
    print(r.text)
    jsondata = json.loads(r.text)
    olexamination    = str(jsondata['examination'])
    olyear           = str(jsondata['year'])
    olname           = str(jsondata['name'])
    olindex          = str(jsondata['indexNo'])
    olnic            = str(jsondata['nic'])
    sub1name         = str(jsondata['subjectResults'][0]['subjectName'])
    sub1result       = str(jsondata['subjectResults'][0]['subjectResult'])
    sub2name         = str(jsondata['subjectResults'][1]['subjectName'])
    sub2result       = str(jsondata['subjectResults'][1]['subjectResult'])
    sub3name         = str(jsondata['subjectResults'][2]['subjectName'])
    sub3result       = str(jsondata['subjectResults'][2]['subjectResult'])
    sub4name         = str(jsondata['subjectResults'][3]['subjectName'])
    sub4result       = str(jsondata['subjectResults'][3]['subjectResult'])
    sub5name         = str(jsondata['subjectResults'][4]['subjectName'])
    sub5result       = str(jsondata['subjectResults'][4]['subjectResult'])
    sub6name         = str(jsondata['subjectResults'][5]['subjectName'])
    sub6result       = str(jsondata['subjectResults'][5]['subjectResult'])
    sub7name         = str(jsondata['subjectResults'][6]['subjectName'])
    sub7result       = str(jsondata['subjectResults'][6]['subjectResult'])
    sub8name         = str(jsondata['subjectResults'][7]['subjectName'])
    sub8result       = str(jsondata['subjectResults'][7]['subjectResult'])
    sub9name         = str(jsondata['subjectResults'][8]['subjectName'])
    sub9result       = str(jsondata['subjectResults'][8]['subjectResult'])

    textt = str(

         '<b>' + olexamination + ' ' + olyear  + '</b>' + '\n' + '\n' +
         'Index No. = ' + '<b>' + olindex + '</b>' + '\n' +
         'Name = '  + '<b>' + olname + '</b>' + '\n' +  'NIC = '  + '<b>' + olnic + '</b>' + '\n' + '\n' + '\n' + 
         '\n' +
         '\n' +  sub1name + ' = ' + '<b>' + sub1result + '</b>' + '\n' + 
         sub2name + ' = '  + '<b>' + sub2result + '</b>' + '\n' +  sub3name + ' = '  + '<b>' + sub3result + '</b>' + '\n' + 
         sub4name + ' = '  + '<b>' + sub4result + '</b>' + '\n' +  sub5name + ' = '  + '<b>' + sub5result + '</b>' + '\n' +  
         sub6name + ' = '  + '<b>' + sub6result + '</b>' + '\n' +  sub7name + ' = '  + '<b>' + sub7result + '</b>' + '\n' + 
         sub8name + ' = '  + '<b>' + sub8result + '</b>' + '\n' +  sub9name + ' = '  + '<b>' + sub9result + '</b>' + '\n' + '\n' +
         '✅ All the Data Verified by the Government' + '\n' +'~ @HermioneSlBot 🇱🇰 ')
         
    return textt



def G5(g5indexx):
    print(g5indexx)
    r = requests.get('https://www.doenets.lk/result/service/GvResult/{0}'.format(g5indexx))
    print(r.text)
    jsondata = json.loads(r.text)
    G5examination  = str(jsondata['examination'])
    G5year         = str(jsondata['year'])
    G5name         = str(jsondata['name'])
    G5drank        = str(jsondata['districtRank'])
    G5irank        = str(jsondata['islandRank'])
    G5index        = str(jsondata['indexNo'])
    G5marks        = str(jsondata['subjectResults'][0]['subjectResult'])
    G5cutoffmarks  = str(jsondata['studentInfo'][4]['value'])

    textt = str(
         '<b>' + G5examination + ' ' + G5year  + '</b>' + '\n' + '\n' +
         'Index No. = ' + '<b>' + G5index + '</b>' + '\n' +
         'Name = '  + '<b>' + G5name + '</b>' + '\n' + 'District Rank = '  + '<b>' + G5drank + '</b>' + '\n' +  'Island Rank = '  + '<b>' + G5irank + '</b>' + '\n' + '\n' + '\n' +
         '<u>' + 'Exam Results' + '</u>' +  '\n' + '\n' +
         'Marks = ' + G5marks + '\n' + 'District / Medium Cut off Mark = ' + G5cutoffmarks + '\n' + '\n' +
         '✅ All the Data Verified by the Government' + '\n' +'~ @HermioneSlBot 🇱🇰 ')

    return textt

# AL result Command

@tbot.on(events.NewMessage(pattern="/al (.*)"))
async def ALresult(event):
    indexx=str(event.raw_text).split(' ')
    print(indexx)
    await event.respond(Al(indexx[1]),parse_mode='html')
    raise events.StopPropagation


#Ol Result Command

@tbot.on(events.NewMessage(pattern="/ol (.*)"))
async def OLresult(event):
    olindexx=str(event.raw_text).split(' ')
    print(olindexx)
    await event.respond(Ol(olindexx[1]),parse_mode='html')
    raise events.StopPropagation


#Grade 5 Scholarship Command

@tbot.on(events.NewMessage(pattern="/g5 (.*)"))
async def G5result(event):
    g5indexx=str(event.raw_text).split(' ')
    print(g5indexx)
    await event.respond(G5(g5indexx[1]),parse_mode='html')
    raise events.StopPropagation
    
#©UvinduBro
    
    
