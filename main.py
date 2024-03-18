import csv
from Bot import Bot
from selenium.webdriver.common.by import By
from time import sleep
import itertools
import urllib
from selenium.common.exceptions import NoSuchElementException
import os
from random import shuffle


class StackScraper(Bot):
    def __init__(self, limit_per_role=50):
        super().__init__(verbose=True)
        self.limit_per_role = limit_per_role
        
        role_names = [
            "2D animator",
            "3D animator",
            "3D modeler",
            "Animation supervisor",
            "Animation technical director",
            "Animator",
            "Book designer",
            "Character designer",
            "Cinematic artist",
            "Compositor",
            "Concept artist",
            "Data analyst",
            "Data engineer",
            "Data scientist",
            "Document imaging specialist",
            "Environment artist",
            "Flash designer",
            "Game artist",
            "Food stylist",
            "Game designer",
            "Game developer",
            "Game director",
            "Game producer",
            "Graphic designer",
            "Illustrator",
            "Infographic artist",
            "Interaction designer",
            "Interactive designer",
            "Layout artist",
            "Level designer",
            "Matte painter",
            "Machine learning engineer",
            "Mobile application developer",
            "Modeling supervisor",
            "Motion graphic artist",
            "Multimedia artist",
            "New media specialist",
            "Senior web developer",
            "Sign designer",
            "Stop motion animator",
            "Storyboard artist",
            "Texture artist",
            "Technical artists",
            "User experience designer",
            "User interface designer",
            "User interaction designer",
            "Video game technical artist",
            "Visual development artist",
            "Visual designer",
            "Web designer",
            "Artificial intelligence specialist",
            "Bioinformatics software engineer",
            "Cisco Certified Internetwork Expert",
            "Clinical informatics director",
            "Computer forensics investigator",
            "Computer hardware engineer",
            "Computer science professor",
            "Computer support specialist",
            "Cybersecurity strategist",
            "Data architect",
            "Data scientist",
            "Data warehouse specialist",
            "Database analyst",
            "EDI systems analyst",
            "Electronics engineer",
            "Enterprise architect",
            "Ethical hacker",
            "Information architect",
            "Information technology consultant",
            "IT instructor",
            "IT operations analyst",
            "Java developer",
            "Lead software engineer",
            "Network administrator",
            "Network analyst",
            "Network architect",
            "Network designer",
            "Network engineer",
            "Network manager",
            "Nurse informaticist",
            "Quality assurance engineer",
            "Quality assurance manager",
            "Security administration",
            "Semiconductor process engineer",
            "Software architect",
            "Software developer",
            "Software engineer",
            "Software release manager",
            "Software tester",
            "Statistical programmer",
            "System administrator",
            "System analyst",
            "Systems architect",
            "Systems engineer",
            "Telecommunications engineer",
            "Telecommunication specialist",
            "Web developer",
            "Webmaster",
            "Business intelligence analyst",
            "eCommerce consultant",
            "Online media buyer",
            "Search engine optimization (SEO) specialist",
            "SEO analyst",
            "SEO consultant",
            "Web content manager",
            "Web editor",
            "Professional gamer",
            "Website administrator",
            "Computer support specialist",
            "Help desk analyst",
            "IT manager",
            "Cybersecurity specialist",
            "DevOps engineer",
            "Computer programmer"
        ]
        shuffle(role_names)
        self.driver.get("https://www.google.com")
        for role_name in role_names:
            self.get_all_jobs(role_name)
        

    def get_all_jobs(self, role_name):
        query = f"https://www.google.com/search?q={role_name}&ibp=htl;jobs#htivrt=jobs".replace(' ', '+')
        print(query)
        self.driver.get(query)
        sleep(1)

        try:
            self.load_all_listings(role_name)
        except Exception as e:
            print(f"Error getting job listings for {role_name}: {str(e)}")

    def load_all_listings(self, role_name):
        max_scroll_attempts = 5  # Set a limit to avoid an infinite loop
        scroll_attempt = 0

        while scroll_attempt < max_scroll_attempts:
            try:
                listings = self.driver.find_elements(By.XPATH, "//div[@class='PwjeAc']")
                if not listings:
                    break  # No listings found, exit the loop

                self.process_job_listings(listings, role_name)

                # Scroll down to trigger more job listings
                self.scroll_down()

                scroll_attempt += 1
                sleep(2)  # Adjust sleep time based on your page loading speed
            except Exception as e:
                print(f"Error getting job listings for {role_name}: {str(e)}")
                break

    def scroll_down(self):
        # Scroll down to trigger more job listings
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)  # Adjust sleep time based on your page loading speed

    def process_job_listings(self, listings, role_name):
        count = 0
        for idx, listing in enumerate(listings):
            self.scroll_into_view(listing)
            listing.click()
            sleep(0.5)

            try:
                job = self._get_job()
                self.save_job(job, role_name)
                count += 1
                print(f"Job {count} saved for {role_name}")
            except Exception as e:
                print(f"Error processing job for {role_name}: {str(e)}")
                continue
    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
    def _get_job(self):
        return {
            "id": self._get_job_id(),
            "title": self._get_title(),
            "company": self._get_company(),
            "description": self._get_job_description(),
            "link": self._get_link()
        }
        
    def _get_job_id(self):
        parsed_url = urllib.parse.urlparse(self.driver.current_url)
        job_id = urllib.parse.parse_qs(parsed_url.fragment)['htidocid'][0]
        return job_id
        
        
    def _get_job_description(self):
        job_container = self.driver.find_element(By.XPATH, '//div[@class="whazf bD1FPe"]')
        try:
            expand_description_button = job_container.find_element(By.XPATH, "div/div/div/div/div/div/div[@class='CdXzFe j4kHIf']")
            self.scroll_into_view(expand_description_button)
            expand_description_button.click()
        except NoSuchElementException:
            pass
        description = job_container.find_element(By.XPATH, ".//span[@class='HBvzbc']").text
        return description

    def _get_title(self):
        job_container = self.driver.find_element(By.XPATH, '//div[@class="whazf bD1FPe"]')
        description = job_container.find_element(By.XPATH, ".//h2[@class='KLsYvd']").text
        return description
    
    
    def _get_company(self):
        try:
            company_element = self.driver.find_element(By.XPATH, '//div[@class="whazf bD1FPe"]//div[@class="nJlQNd sMzDkb"]')
            company = company_element.text
            return company
        except NoSuchElementException:
            return "Company Not Found"
        
    def _get_link(self):
        job_container = self.driver.find_element(By.XPATH, '//div[@class="whazf bD1FPe"]')
        try:
            link_element = job_container.find_element(By.XPATH, './/a[contains(@class, "pMhGee") and contains(@class, "Co68jc") and contains(@class, "j0vryd")]')
            link = link_element.get_attribute("href")
            return link
        except NoSuchElementException:
            return ""


    def save_job(self, job, role_name):
        if self.verbose:
            print(f'Saving {role_name} job')

        folder_path = os.path.join("raw_data", role_name.replace(' ', '-'))
        os.makedirs(folder_path, exist_ok=True)

        file_name = f"{role_name.replace(' ', '_')}.csv"
        file_path = os.path.join(folder_path, file_name)

        data_to_write = [job["id"], job["title"], job["company"], job["description"], job["link"], role_name]

        # Check if the job already exists in the file
        job_exists = False
        if os.path.exists(file_path):
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader)  # Skip header row
                for row in csv_reader:
                    if row[:4] == data_to_write[:4]:  # Check if ID, Title, Company, and Description match
                        job_exists = True
                        break

        # If the job doesn't exist, append it to the CSV file
        if not job_exists:
            with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                if os.stat(file_path).st_size == 0:  # If file is empty, write header
                    csv_writer.writerow(["ID", "Title", "Company", "Description", "Link", "Career"])
                csv_writer.writerow(data_to_write)

        if self.verbose:
            print(f"Job ID {job['id']} saved in CSV as {file_name}")



if __name__ == '__main__':
    StackScraper()