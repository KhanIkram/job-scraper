import time  # Module to manage time-related tasks, like delays
import random  # Module to generate random numbers or select random items from a list
import pandas as pd  # Pandas is a data manipulation library, useful for handling data frames and CSV files
from selenium import webdriver  # Selenium is a tool for automating web browsers
from selenium.webdriver.common.by import By  # Module to specify types of selectors (like ID, Class, CSS Selector)
from selenium.webdriver.support.ui import WebDriverWait  # Module to wait for a condition to occur before proceeding
from selenium.webdriver.support import expected_conditions as EC  # Module to define expected conditions to wait for
from selenium.webdriver.chrome.service import Service  # Service is used to manage the ChromeDriver service
from webdriver_manager.chrome import ChromeDriverManager  # This automatically manages ChromeDriver installation and updates

# List of job titles that we will search for on the job site
JOB_TITLES = [
    'junior security analyst'
]

# List of different User-Agent strings to mimic different browsers
# This helps in preventing the website from blocking our requests, thinking we're a bot
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'
]

# Function to create the URL needed for each job search query
# It replaces spaces in the job title with '+' to make the URL valid
def create_search_url(base_url, query):
    return f"{base_url}{query.replace(' ', '+')}"

# Function to scrape job listings from the job site
def scrape_jobs(base_url, job_titles):
    job_list = []  # List to store job details

    # Set up the WebDriver for Chrome
    options = webdriver.ChromeOptions()  # Create a ChromeOptions object to customize the browser
    # options.add_argument("--headless")  # This option runs the browser in the background without displaying it (disabled for debugging)
    options.add_argument("--no-sandbox")  # Disables the sandboxing feature (useful in certain environments)
    options.add_argument("--disable-dev-shm-usage")  # Fixes problems with limited shared memory on some systems
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")  # Randomly select a User-Agent string for each session

    # Set up the ChromeDriver service, which manages the actual browser automation
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)  # Initialize the Chrome WebDriver with the specified options

    # Open the first tab (starts with Google's homepage to establish a session)
    driver.get("https://www.google.com")
    main_window = driver.current_window_handle  # Save the main window handle for reference later

    # Loop through each job title in the list and open a new tab for each
    for i, title in enumerate(job_titles):
        if i > 0:
            driver.execute_script("window.open('');")  # Open a new blank tab
        driver.switch_to.window(driver.window_handles[i])  # Switch focus to the new tab
        url = create_search_url(base_url, title)  # Create the search URL for the current job title
        try:
            driver.get(url)  # Navigate to the job search URL
            print(f"Fetching URL: {url}")  # Log the URL being fetched for transparency
        except Exception as e:
            print(f"Error fetching {url}: {e}")  # If an error occurs, print it and move on to the next job title
            continue  # Skip to the next iteration of the loop

    # Now, we'll scrape the job data from each open tab
    for i, title in enumerate(job_titles):
        driver.switch_to.window(driver.window_handles[i])  # Switch focus to each tab one by one
        try:
            # Wait for the job cards to load on the page (up to 20 seconds)
            wait = WebDriverWait(driver, 20)  # Create a WebDriverWait object with a 20-second timeout
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="searchSerpJob"]')))  # Wait until job cards are present

            # Find all job cards on the page
            jobs = driver.find_elements(By.CSS_SELECTOR, '[data-testid="searchSerpJob"]')
            print(f"Found {len(jobs)} jobs for {title}")  # Print how many jobs were found for this title

            # Extract details from each job card
            for job in jobs:
                try:
                    # Extract job title, company name, location, and the link to the job posting
                    job_title = job.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobTitle"]').text.strip()
                    company = job.find_element(By.CSS_SELECTOR, '[data-testid="companyName"]').text.strip()
                    location = job.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobLocation"]').text.strip()
                    link = job.find_element(By.CSS_SELECTOR, '[data-testid="searchSerpJobTitle"] a').get_attribute('href')

                    # Append the extracted job details to the job list
                    job_list.append({
                        'Title': job_title,
                        'Company': company,
                        'Location': location,
                        'Link': link
                    })
                except Exception as e:
                    print(f"Error parsing job details for {title}: {e}")  # If there's an error parsing a job, print it and move on
                    continue  # Continue with the next job card

        except Exception as e:
            print(f"Error fetching jobs for {title}: {e}")  # If there's an error with the whole page, print it and move on
            continue  # Continue with the next job title

    driver.quit()  # Close the browser once all the scraping is done
    return job_list  # Return the list of job details

# Main script that runs when the file is executed
if __name__ == "__main__":
    BASE_URL = 'https://www.simplyhired.com/search?q='  # Base URL for job searches on SimplyHired

    # Call the scrape_jobs function with the base URL and list of job titles
    job_list = scrape_jobs(BASE_URL, JOB_TITLES)

    # If jobs were found, save them to a CSV file
    if job_list:
        df = pd.DataFrame(job_list)  # Convert the job list to a DataFrame
        df.to_csv('job_listings.csv', index=False)  # Save the DataFrame to a CSV file (without row indices)
        print("Job listings saved to job_listings.csv")  # Print a success message
    else:
        print("No job listings found")  # If no jobs were found, print a message
