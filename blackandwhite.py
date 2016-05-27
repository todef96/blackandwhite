import mechanize
import cookielib
from bs4 import BeautifulSoup
import random
import time
import json
from threading import Thread
import Queue
import csv
import argparse

def run(websites_file,kw_black,kw_white):
    tmp_list = []
    with open(websites_file, 'rb') as csvfile:
        csvr = csv.reader(csvfile, delimiter=',')
        for row in csvr:
            tmp_list.append(row)
    list_of_websites = [item for sublist in tmp_list for item in sublist]
    # persistant dictionaries
    white_file = {}
    black_file = {}
    thread_queue(list_of_websites, black_file, white_file,kw_black,kw_white)

def scrape_web(i,q, dict1, dict2,kw_black,kw_white):
    # Keep our queue looping.
    while True:
        current_url = q.get()
        print current_url
        # We mix up the user-agents to avoid looking like a bot.
        user_agents = ['Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',\
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',\
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',\
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',\
            'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; de-de) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16',\
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)']
        cj = cookielib.CookieJar()
        br = mechanize.Browser()
        br.set_cookiejar(cj)
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', random.choice(user_agents))]
        br.open(current_url)
        time.sleep(5)
        website_responses = br.response().read()
        soup = BeautifulSoup(website_responses, 'html.parser')
        keyword_lookup(q, soup, current_url, dict1, dict2, kw_black, kw_white)

def keyword_lookup(q, input_soup, source, black_file, white_file,kw_black,kw_white):
    print 'running keyword lookup'
    # CSV parse arg files.
    tmp_list_b = []
    tmp_list_w = []
    with open(kw_black, 'rb') as csvfile:
        csvr = csv.reader(csvfile, delimiter=',')
        for row in csvr:
            tmp_list_b.append(row)
    keyword_black = [item for sublist in tmp_list_b for item in sublist]
    with open(kw_white, 'rb') as csvfile:
        csvr = csv.reader(csvfile, delimiter=',')
        for row in csvr:
            tmp_list_w.append(row)
    keyword_white = [item for sublist in tmp_list_w for item in sublist]
    # name for JSON buffer keys
    source_tmp = source.split('.')
    source_name = source_tmp[1]
    # we lookup and copy headlines to buffer.
    for headline in input_soup.find_all('a',href=True):
        headline_found = False
        for word in keyword_black:
            if headline_found == False:
                if word in headline.text:
                    try:
                        print headline.text
                        black_file[source_name + '.com.au' + '-' + str(time.time())] = headline.text
                    except:
                        pass
                    headline_found = True
        for word in keyword_white:
            if headline_found == False:
                if word in headline.text:
                    try:
                        print headline.text
                        white_file[source_name + '.com.au' + '-' + str(time.time())] = headline.text
                    except:
                        pass
                    headline_found = True
    if q.empty():
        make_json_file(black_file, white_file)
    q.task_done()


def make_json_file(black_file, white_file):
    # we get our file names from current date/time.
    time_date = time.asctime()
    temp = time_date.replace(':','_').split()
    file_name = ''.join(temp)
    black = 'blackfile_' + file_name + '.json'
    white = 'whitefile_' + file_name + '.json'
    # write blackfile
    print 'building: ',black
    with open(black, 'w') as outfile:
        json.dump(black_file, outfile)
    # write whitefile
    print 'building: ',white
    with open(white, 'w') as outfile:
        json.dump(white_file, outfile)
    # write csv file list. NOTE: this should append and not re-write.
    print 'building archive list...'
    fd = open('archive_list.csv','a')
    fd.write(white + ',')
    fd.write(black + ',')
    fd.close()

def thread_queue(list_of_websites, dict1, dict2, kw_black, kw_white):
    num_threads = 1
    enclosed_q = Queue.Queue()

    for i in range(num_threads):
        d = Thread(target=scrape_web, args=(i,enclosed_q, dict1, dict2,kw_black,kw_white))
        d.setDaemon(True)
        d.start()

    # this adds the urls to the Queue.
    for url in list_of_websites:
        enclosed_q.put(url)

    enclosed_q.join()
    print '----------DONE----------'

if __name__ == "__main__":
    #setup args
    parser = argparse.ArgumentParser()
    parser.add_argument('websites', help='This should be a .CSV file containing your websites')
    parser.add_argument('kw_black', help='This should be a .CSV file containing all your keywords for the blackfile')
    parser.add_argument('kw_white', help='This should be a .CSV file containing all your keywords for the whitefile')
    args = parser.parse_args()
    run(args.websites,args.kw_black,args.kw_white)