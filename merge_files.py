#!/usr/bin/python


import csv
import glob, os, sys
import codecs
import datetime
import operator

days = set()
keywords = set()

keywords_clicks = {}
keywords_impres = {}
keywords_ctr = {}
keywords_avg_cpc = {}
keywords_cost = {}
keywords_avg_pos = {}

# write to file
def write_to_file(keywords, days, data, fw):
    for kw in keywords:
        new_row = [kw]
        for day in days:
            new_row.append(data[kw][day])
        fw.writerow(new_row)

# take a list of all files
filearray = glob.glob("Keyword*.csv")

# loop through all files and gather data
for filename in filearray:
    f=codecs.open(filename,"rb","utf-16")
    csvread=csv.reader(f,delimiter='\t')
    day = ''
    for row in csvread:
        if len(row) < 2:
            day = row[0][row[0].find('(')+1:row[0].find(')')]
            days.add(day)
        elif row[0] == 'enabled':
            kw = row[1]
            keywords.add(kw)
            
            if not keywords_clicks.has_key(kw):
                keywords_clicks[kw] = dict()
            clicks = row[4]
            keywords_clicks[kw][day] = clicks
            
            if not keywords_impres.has_key(kw):
                keywords_impres[kw] = dict()
            immpr = row[5]
            keywords_impres[kw][day] = immpr
            
            if not keywords_ctr.has_key(kw):
                keywords_ctr[kw] = dict()
            ctr = row[6].replace('%', '')
            keywords_ctr[kw][day] = ctr
            
            if not keywords_avg_cpc.has_key(kw):
                keywords_avg_cpc[kw] = dict()
            avg_cpc = row[7]
            keywords_avg_cpc[kw][day] = avg_cpc
            
            if not keywords_cost.has_key(kw):
                keywords_cost[kw] = dict()
            cost = row[8]
            keywords_cost[kw][day] = cost
            
            if not keywords_avg_pos.has_key(kw):
                keywords_avg_pos[kw] = dict()
            avg_pos = row[9]
            keywords_avg_pos[kw][day] = avg_pos
    
keywords_arr = list(keywords)

dates = list(days)
dates.sort(key=lambda d: datetime.datetime.strptime(d, '%b %d, %Y'))

f = open('merged.csv', 'wb')
fw = csv.writer(f, delimiter=';', quoting=csv.QUOTE_ALL)

first_row = dates[:]
first_row.insert(0, '')
fw.writerow(first_row)

fw.writerow(['Clicks'])
write_to_file(keywords_arr, dates, keywords_clicks, fw)

fw.writerow(['Cost'])
write_to_file(keywords_arr, dates, keywords_cost, fw)

fw.writerow(['Avg CPC'])
write_to_file(keywords_arr, dates, keywords_avg_cpc, fw)

fw.writerow(['Impressions'])
write_to_file(keywords_arr, dates, keywords_impres, fw)

fw.writerow(['CTR'])
write_to_file(keywords_arr, dates, keywords_ctr, fw)

fw.writerow(['Avg_pos'])
write_to_file(keywords_arr, dates, keywords_avg_pos, fw)

f.close()
