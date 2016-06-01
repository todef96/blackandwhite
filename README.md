# blackandwhite
An information comparison tool.

Scrapes a list of websites for two set lists of keywords and returns the headline results in two set output files.

For Example, You could use blackandwhite to:
- Track how one particular news conglomerate or organisation reports the news on two opposing themes, ie; two political parties.

Usage:
1. blackandwhite.py source_websites.csv keywords_black.csv keywords_white.csv
2. Source websites contain your list of webstes, keywords_black contain one theme of keywords, whilst keywords_white contain another. These items should be comma delimited. Populate your source file and opposing keywords before running. Eg. One set of keywords could be Republican Party related whilst the other are Democrat related.
3. Output results write a keywords particular output as a .JSON file which are datestamped eg "blackfile_datetimeyear.json"

Example of output being used live: http://northofmoltke.com/blackandwhite/
