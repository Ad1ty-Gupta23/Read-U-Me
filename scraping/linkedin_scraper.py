import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

def scrape_linkedin_jobs(job_titles, location="India"):
    """Scrapes LinkedIn job listings for the predicted job titles."""
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    if not os.path.exists(data_dir):
        print(f"Creating data directory at: {data_dir}")
        os.makedirs(data_dir)
    
    # 📌 Setup Selenium WebDriver with improved options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    
    # Add user agent to avoid detection
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    job_listings = []
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("WebDriver initialized successfully")
        
        for job_title in job_titles:
            print(f"Searching for: {job_title} in {location}")
            # Updated search URL to include location parameter for India
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
            
            try:
                driver.get(search_url)
                print(f"Navigated to: {search_url}")
                
                # Wait for job listings to load with increased timeout
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "base-card")))
                    print("Job listings loaded successfully")
                except TimeoutException:
                    print(f"Timeout waiting for job listings for {job_title}. Moving to next job title.")
                    continue
                
                # Extract job listings
                soup = BeautifulSoup(driver.page_source, "html.parser")
                jobs = soup.find_all("div", class_="base-card")
                
                print(f"Found {len(jobs)} job listings for {job_title} in {location}")
                
                for job in jobs[:5]:  # Increased to 5 results per job title
                    try:
                        title_elem = job.find("h3", class_="base-search-card__title")
                        company_elem = job.find("h4", class_="base-search-card__subtitle")
                        location_elem = job.find("span", class_="job-search-card__location")
                        
                        if title_elem and company_elem and location_elem:
                            title = title_elem.text.strip()
                            company = company_elem.text.strip()
                            location = location_elem.text.strip()
                            
                            job_listings.append({
                                "job_title_short": title.split(" ")[0],
                                "job_title": title,
                                "job_location": location,
                                "job_via": "LinkedIn",
                                "job_schedule_type": "Full-Time",  # Placeholder
                                "job_work_from_home": "No",  # Placeholder
                                "search_location": location,
                                "job_posted_date": "Recently Posted",  # Placeholder
                                "job_no_degree_mention": "Unknown",  # Placeholder
                                "job_health_insurance": "Unknown",  # Placeholder
                                "job_country": "India",
                                "salary_rate": "Not Provided",
                                "salary_year_avg": "Not Provided",
                                "salary_hour_avg": "Not Provided",
                                "company_name": company,
                                "job_skills": "Python, Machine Learning",  # Placeholder
                                "job_type_skills": "Software, Data Science"  # Placeholder
                            })
                            print(f"Added job: {title} at {company} in {location}")
                    except Exception as e:
                        print(f"Error extracting job details: {str(e)}")
                        continue
                
            except Exception as e:
                print(f"Error processing job title {job_title}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error initializing WebDriver: {str(e)}")
    finally:
        try:
            if 'driver' in locals():
                driver.quit()
                print("WebDriver closed successfully")
        except Exception as e:
            print(f"Error closing WebDriver: {str(e)}")
    
    # Save jobs to CSV with absolute path
    if job_listings:
        df = pd.DataFrame(job_listings)
        output_path = os.path.join(data_dir, "linkedin_jobs_india.csv")
        df.to_csv(output_path, index=False)
        print(f"✅ LinkedIn jobs from India scraped and saved to {output_path}!")
    else:
        print("⚠️ No job listings were found.")

if __name__ == "__main__":
    # You can specify more job titles here
    scrape_linkedin_jobs(["Data Scientist", "Machine Learning Engineer", "Software Engineer", "Data Analyst", "Frontend Developer"])
