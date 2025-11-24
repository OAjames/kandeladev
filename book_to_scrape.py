"""
E-commerce Web Scraper - ETL Pipeline
Target: books.toscrape.com
Purpose: Extract book data, transform/clean it, and load to CSV
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import List, Dict
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BookScraperETL:
    """ETL Pipeline for scraping books from books.toscrape.com"""
    
    def __init__(self, base_url: str = "http://books.toscrape.com/catalogue/category/books_1"):
        self.base_url = base_url
        self.books_data = []
        
    def extract(self, max_pages: int = 49) -> List[Dict]:
        """
        EXTRACT Phase: Scrape book data from multiple pages
        
        Args:
            max_pages: Number of pages to scrape
            
        Returns:
            List of dictionaries containing raw book data
        """
        logger.info(f"Starting extraction from {self.base_url}")
        
        # Configure Chromium options
        chrome_options = Options()
        chrome_options.headless = False  # Show the browser window
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Initialize Selenium WebDriver with Chromium
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            for page_num in range(1, max_pages + 1):
                # Construct page URL
                if page_num == 1:
                    url = self.base_url + "/index.html"
                else:
                    url = self.base_url + f"/page-{page_num}.html"
                
                try:
                    logger.info(f"Scraping page {page_num}: {url}")
                    driver.get(url)
                    
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    books = soup.find_all('article', class_='product_pod')
                    
                    for book in books:
                        book_data = self._extract_book_details(book)
                        self.books_data.append(book_data)
                    
                    logger.info(f"Extracted {len(books)} books from page {page_num}")
                    
                    # Be respectful - add delay between requests
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"Error scraping page {page_num}: {e}")
                    continue
        finally:
            driver.quit()
        
        logger.info(f"Total books extracted: {len(self.books_data)}")
        return self.books_data
    
    def _extract_book_details(self, book_element) -> Dict:
        """Extract individual book details from HTML element"""
        
        # Title
        title = book_element.find('h3').find('a')['title']
        
        # Price
        price = book_element.find('p', class_='price_color').text
        
        # Availability
        availability = book_element.find('p', class_='instock availability').text.strip()
        
        # Rating
        rating_class = book_element.find('p', class_='star-rating')['class'][1]
        
        # Product URL
        product_url = book_element.find('h3').find('a')['href']
        
        return {
            'title': title,
            'price': price,
            'availability': availability,
            'rating': rating_class,
            'product_url': product_url
        }
    
    def transform(self) -> pd.DataFrame:
        """
        TRANSFORM Phase: Clean and standardize the extracted data
        
        Returns:
            Cleaned pandas DataFrame
        """
        logger.info("Starting data transformation")
        
        if not self.books_data:
            logger.warning("No data to transform")
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(self.books_data)
        
        # Clean price: Remove '£' and convert to float
        df['price_gbp'] = df['price'].str.replace('£', '').astype(float)
        
        # Convert rating to numeric
        rating_map = {
            'One': 1,
            'Two': 2,
            'Three': 3,
            'Four': 4,
            'Five': 5
        }
        df['rating_numeric'] = df['rating'].map(rating_map)
        
        # Clean availability: Extract just "In stock" or "Out of stock"
        df['in_stock'] = df['availability'].apply(
            lambda x: 'Yes' if 'In stock' in x else 'No'
        )
        
        # Extract stock quantity if available
        df['stock_quantity'] = df['availability'].apply(self._extract_stock_quantity)
        
        # Clean title: Remove extra whitespace
        df['title'] = df['title'].str.strip()
        
        # Create full product URL
        df['full_url'] = 'http://books.toscrape.com/catalogue/' + df['product_url'].str.replace('../../../', '')
        
        # Reorder columns
        df = df[[
            'title',
            'price_gbp',
            'rating',
            'rating_numeric',
            'in_stock',
            'stock_quantity',
            'full_url'
        ]]
        
        # Remove duplicates based on title
        initial_count = len(df)
        df = df.drop_duplicates(subset=['title'], keep='first')
        removed_duplicates = initial_count - len(df)
        
        if removed_duplicates > 0:
            logger.info(f"Removed {removed_duplicates} duplicate records")
        
        # Sort by rating and price
        df = df.sort_values(['rating_numeric', 'price_gbp'], ascending=[False, True])
        df = df.reset_index(drop=True)
        
        logger.info(f"Transformation complete. Final record count: {len(df)}")
        
        return df
    
    def _extract_stock_quantity(self, availability_text: str) -> int:
        """Extract numeric stock quantity from availability text"""
        match = re.search(r'\((\d+) available\)', availability_text)
        if match:
            return int(match.group(1))
        return 0
    
    def load(self, df: pd.DataFrame, filename: str = "books_data.csv") -> None:
        """
        LOAD Phase: Save cleaned data to CSV
        
        Args:
            df: Cleaned DataFrame
            filename: Output CSV filename
        """
        logger.info(f"Loading data to {filename}")
        
        if df.empty:
            logger.warning("No data to load")
            return
        
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            logger.info(f"Successfully saved {len(df)} records to {filename}")
            
            # Print summary statistics
            self._print_summary(df)
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def _print_summary(self, df: pd.DataFrame) -> None:
        """Print summary statistics of the scraped data"""
        print("\n" + "="*50)
        print("DATA SUMMARY")
        print("="*50)
        print(f"Total Books Scraped: {len(df)}")
        print(f"Average Price: £{df['price_gbp'].mean():.2f}")
        print(f"Price Range: £{df['price_gbp'].min():.2f} - £{df['price_gbp'].max():.2f}")
        print(f"Average Rating: {df['rating_numeric'].mean():.2f}/5")
        print(f"\nBooks in Stock: {(df['in_stock'] == 'Yes').sum()}")
        print(f"Books Out of Stock: {(df['in_stock'] == 'No').sum()}")
        print("\nRating Distribution:")
        print(df['rating'].value_counts().sort_index())
        print("="*50 + "\n")
    
    def run_pipeline(self, max_pages: int = 49, output_file: str = "books_data.csv") -> pd.DataFrame:
        """
        Execute the complete ETL pipeline
        
        Args:
            max_pages: Number of pages to scrape
            output_file: Output CSV filename
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("="*50)
        logger.info("STARTING ETL PIPELINE")
        logger.info("="*50)
        
        # EXTRACT
        self.extract(max_pages=max_pages)
        
        # TRANSFORM
        cleaned_df = self.transform()
        
        # LOAD
        self.load(cleaned_df, filename=output_file)
        
        logger.info("="*50)
        logger.info("ETL PIPELINE COMPLETED")
        logger.info("="*50)
        
        return cleaned_df


def main():
    """Main execution function"""
    
    # Initialize ETL pipeline
    scraper = BookScraperETL(
        base_url="http://books.toscrape.com/catalogue/category/books_1"
    )
    
    # Run the complete pipeline
    # Scrape 3 pages (approximately 60 books)
    df = scraper.run_pipeline(max_pages=49, output_file="books_data.csv")
    
    # Display first few records
    print("\nFirst 5 records:")
    print(df.head().to_string())
    
    # Optional: Display specific insights
    print("\n\nTop 5 Highest Rated Books:")
    top_rated = df.nsmallest(5, 'price_gbp')[['title', 'price_gbp', 'rating']]
    print(top_rated.to_string(index=False))


if __name__ == "__main__":
    main()