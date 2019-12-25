# Wordpress spider

So python. Much crawling. 

Recursively crawls /wp-content/uploads pages for given domains 
and saves .php files. 

## Installation

Wordpress crawler uses next packages:
```
pip install scrapy
pip install logging
```


## Usage

Initial links for crawling are stored in the 'input/links.txt'.
Both 'http://www.example.com' and 'example.com' formats are allowed.

Open the terminal into a root project folder, namely 'wordpress' 
that contains another 'wordpress' folder.

Type in the command below:
```
scrapy crawl wordpress -o <filename.csv>
```

This will save all the output to a csv file. Make sure filename.csv 
doesn't exist or is empty before starting the spider lest the new data will 
be append to primarily written to the file. 

