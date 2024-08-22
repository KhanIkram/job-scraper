# job-scraper
This Python script automates job searches on SimplyHired using Selenium, ideal for job seekers who want to streamline their job-hunting process. 

An important thing to note about this job scraping automation python script. Eventually I will expand this code to alternate job search websites (Indeed, isecjobs, dice, etc...). Also will growing the list of job queries, maybe deploying an alternate AWS API gateway to combine using with Selenium.


### **Step 1: Install ChromeDriver**
Download and install ChromeDriver to match your installed version of Chrome. This step can be automated with the `webdriver_manager` package.

### **Step 2: Update Configuration**
Modify the `JOB_TITLES` list in the script to include the job titles you wish to search for.


## Usage

To run the script, execute the following command in your terminal:
```bash
python job_scraper.py
```
This command will launch a series of browser tabs, each targeting a specific job title, and will scrape the job listings.


## Features

- **Automated Job Search:** Automatically searches for job listings based on the provided titles.
- **User-Agent Rotation:** Uses random user-agent strings to prevent detection by the website.
- **CSV Export:** Saves job listings into a CSV file for easy management.
- **Multiple Tab Handling:** Opens multiple browser tabs to expedite the scraping process.

---


## Configuration

### **Job Titles:**
Modify the `JOB_TITLES` list in `job_scraper.py` to include specific job titles that align with your search criteria.

### **User-Agent Strings:**
The script rotates through a list of user-agent strings to mimic different browsers and reduce the likelihood of being blocked.

---


## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, create a feature branch, make your changes, and submit a pull request.

## Additional Resources

- **[Selenium Documentation](https://www.selenium.dev/documentation/)**
- **[SimplyHired](https://www.simplyhired.com/)**
