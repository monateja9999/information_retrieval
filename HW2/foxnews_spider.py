import scrapy

class FoxNewsSpider(scrapy.Spider):
    name = 'foxnews_spider'
    allowed_domains = ['foxnews.com']  # Restrict crawling to foxnews.com
    start_urls = ['https://www.foxnews.com/']

    custom_settings = {
        'FEED_EXPORT_FIELDS': ['URL', 'Status'],
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'fetch_foxnews.csv',
        'CLOSESPIDER_ITEMCOUNT': 20000,  # Stop crawling after 20,000 items
    }

    def __init__(self):
        # Initialize statistics
        self.total_urls_extracted = 0
        self.unique_urls_within = set()
        self.unique_urls_outside = set()
        self.status_codes = {}
        self.file_sizes = {
            '<1KB': 0,
            '1KB~<10KB': 0,
            '10KB~<100KB': 0,
            '100KB~<1MB': 0,
            '>=1MB': 0,
        }
        self.successful_downloads = []  # Store successful downloads for the second CSV

    def start_requests(self):
        # Initialize visit_Foxnews.csv with headers
        with open('visit_foxnews.csv', 'w') as f:
            f.write('URL,Size (Bytes),# of Outlinks,Content Type\n')

        # Initialize urls_Foxnews.csv with headers
        with open('urls_foxnews.csv', 'w') as f:
            f.write('URL,Indicator\n')
            
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        # Log URL and status
        yield {
            'URL': response.url,
            'Status': response.status,
        }

        # Track status codes
        self.status_codes[response.status] = self.status_codes.get(response.status, 0) + 1

        # Gather metadata for 'visit_FoxNews.csv'
        content_length = int(response.headers.get('Content-Length', 0))
        content_type = response.headers.get('Content-Type', b'').decode('utf-8').split(';')[0]  # Remove charset

        # Categorize file sizes
        self.categorize_file_size(content_length)

        # Record successful downloads (only log content if status is 200)
        if response.status == 200:
            self.successful_downloads.append({
                'URL': response.url,
                'Size (Bytes)': content_length,
                '# of Outlinks': len(response.css('a::attr(href)').getall()),
                'Content Type': content_type,
            })

            # Write to visit_Foxnews.csv dynamically
            with open('visit_foxnews.csv', 'a') as f:
                f.write(f"{response.url},{content_length},{len(response.css('a::attr(href)').getall())},{content_type}\n")

        # Follow all links
        for href in response.css('a::attr(href)').getall():
            full_url = response.urljoin(href)
            self.total_urls_extracted += 1

            # Write to urls_Foxnews.csv
            if full_url.startswith('https://www.foxnews.com/'):
                indicator = 'OK'
                self.unique_urls_within.add(full_url)
                yield response.follow(full_url, self.parse)
            else:
                indicator = 'N_OK'
                self.unique_urls_outside.add(full_url)

            # Log every URL with its indicator (OK/N_OK)
            with open('urls_foxnews.csv', 'a') as f:
                f.write(f"{full_url},{indicator}\n")

    def categorize_file_size(self, content_length):
        """Categorize the file size into different ranges."""
        if content_length < 1024:
            self.file_sizes['<1KB'] += 1
        elif content_length < 10240:
            self.file_sizes['1KB~<10KB'] += 1
        elif content_length < 102400:
            self.file_sizes['10KB~<100KB'] += 1
        elif content_length < 1048576:
            self.file_sizes['100KB~<1MB'] += 1
        else:
            self.file_sizes['>=1MB'] += 1

    def close(self, reason):
        """Generate a summary report."""
        # Write the report file at the end of the crawl
        with open('CrawlerReport_foxnews.txt', 'w') as f:
            f.write(f"Name: Mona Teja Kurakula\n")
            f.write(f"News site crawled: https://www.foxnews.com/\n")
            f.write(f"Number of threads: 64\n\n")

            # Fetch statistics
            total_fetches = sum(self.status_codes.values())
            succeeded = self.status_codes.get(200, 0)
            failed_or_aborted = total_fetches - succeeded

            f.write(f"Fetch Statistics:\n")
            f.write(f"# fetches attempted: {total_fetches}\n")
            f.write(f"# fetches succeeded: {succeeded}\n")
            f.write(f"# fetches failed or aborted: {failed_or_aborted}\n\n")

            # Outgoing URLs
            f.write(f"Outgoing URLs:\n")
            f.write(f"Total URLs extracted: {self.total_urls_extracted}\n")
            f.write(f"# unique URLs extracted: {len(self.unique_urls_within) + len(self.unique_urls_outside)}\n")
            f.write(f"# unique URLs within News Site: {len(self.unique_urls_within)}\n")
            f.write(f"# unique URLs outside News Site: {len(self.unique_urls_outside)}\n\n")

            # Status codes
            f.write(f"Status Codes:\n")
            for status, count in self.status_codes.items():
                f.write(f"{status}: {count}\n")
            f.write("\n")

            # File sizes
            f.write(f"File Size Distribution:\n")
            for size_category, count in self.file_sizes.items():
                f.write(f"{size_category}: {count}\n")
