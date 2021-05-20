## Auto Scraper, an Image-Data Web Scraper

Auto Scraper can be used as either a CLI tool or can be imported as a package into your .ipynb/.py script.

It can download all images immediately, save image data in a .csv, or both. 

#### Function Call Example
`autoscrape(websites='./websites.json', output='output/', path='./chromedriver.exe', scrolls=1, mode='csv')`
#### CLI Call Example
`python autoscrape.py ./websites.json --output ./output/ --path ./chromedriver.exe -s 1 -m csv`


- `websites` Refers to the .JSON file used as a 'map' to direct your scraper. By default refers to a file called `websites.json`

- `output` Defines the location that your chosen output will be created in. By default refers to a folder called `output`

- `path` Refers to the browser driver of your choice that Selenium will use. By default refers to a local `chromedriver.exe`

- `scrolls` Useful for webpages with infinite scrolling, defines the number of times Auto Scraper will scroll before downloading the payload. By default set to 1 scroll.

- `mode` Specifies if the output is the raw images, the image data(link and alt text) in .csv form, or both. Defaults to `csv`

