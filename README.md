# blackandwhite
An information comparison tool.

Scrapes a list of websites for two set lists of keywords and returns the headline results in two set output files.

For Example, You could use blackandwhite to:
- Track how one particular news conglomerate or organisation reports the news on two opposing themes, ie; two political parties.

Usage:
- blackandwhite.py source_websites.csv keywords_black.csv keywords_white.csv
- Source websites contain your list of webstes, keywords_black contain one theme of keywords, whilst keywords_white contain another. These items should be comma delimited. Populate your source file and opposing keywords before running. Eg. One set of keywords could be Republican Party related whilst the other are Democrat related.
- Output results write a keywords particular output as a .JSON file which are datestamped eg "blackfile_datetimeyear.json"

Example of output being used live: http://northofmoltke.com/blackandwhite/

#Disclaimer

Please note, this scraper is written 'to do the right thing'. Although I've included multithreading it is purposely set to only run a single thread/queue with a 5sec delay to mimic an average user/human opening a bunch of bookmarks one after the other. I encourage that it be used in this way at all times. 
