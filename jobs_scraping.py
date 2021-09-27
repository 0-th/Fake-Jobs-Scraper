# https://realpython.github.io/fake-jobs/
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_soup(page_url: str):
  """
  Generate the soup object for any url in the program

  input:
      :param page_url: input page_url
  returns:
      - page_soup: BeautifulSoup object from parsing the html page
  """
  # get response object returned from the HTTP GET request
  page_response = requests.get(url=page_url)
  # get the html of the page as a string
  page_html = page_response.text
  # parse the html string
  page_soup = BeautifulSoup(page_html, 'lxml')

  return page_soup


def get_job_descr(job_descr_link: str):
  """
  Get the job description from another page.
  input:
      :param job_descr_link: link to the page containing the job description text
  returns:
      - job_descr: string object containing the job description
  """
  # generate site soup
  descr_soup = get_soup(page_url=job_descr_link)
  # get the description text
  job_descr = descr_soup.find(name='div', class_='content').p.text
  return job_descr


def get_job_info(soup, all_jobs_info):
  """
  Get the job title, company name, location, data posted and the job description

  input:
      :param soup: BeautifulSoup object
  returns:
      - job_info: a dictionary containing information about the job
  """
  # for each job posted in the job listing page
  print(f'[+]Scraping jobs')
  for jobs in soup.find_all(name='div', class_='column'):
    # dictionary to store jobs information
    job_info = {}

    # get the job title and add it to a dictionary
    job_title = jobs.find(name='h2', class_='title').text
    job_info['job_title'] = job_title
    # get the company name and add it to a dictionary
    company_name = jobs.find(name='h3', class_='subtitle').text
    job_info['company_name'] = company_name
    # get the location and add it to a dictionary
    location = jobs.find(name='p', class_='location').text
    location = location.strip()
    job_info['location'] = location
    # get the date posted and add it to a dictionary
    date_posted = jobs.find(name='p', class_='is-small').time.text
    job_info['date_posted'] = date_posted
    # get the link to job_description
    job_descr_link = jobs.find_all(name='a', class_='card-footer-item')[-1]['href']
    # get the job description and add it to a dictionary
    job_descr = get_job_descr(job_descr_link=job_descr_link)
    job_info['job_description'] = job_descr

    print(f'[+]Found {job_title} job...')
    # append the job_info for a job to a list
    all_jobs_info.append(job_info)
  print(f'[+]Done searching')


def conv_to_csv(jobs_info_list: list):
  """
  Stores the list of dictionaries containing the info about the jobs to a csv file.
  input:
      :param jobs_info_list: list of dictionaries containing job information
  """
  headers = ['Job Title', 'Company', 'Location', 'Date', 'Description']
  # convert the jobs_info_list to a pandas DataFrame
  jobs_df = pd.DataFrame(jobs_info_list, columns=headers)
  print(f'[+]Writing job to jobs.csv')
  csv_file = open('jobs.csv', 'w+')
  # write DataFrame to csv file
  jobs_df.to_csv(csv_file, index=False)
  csv_file.close()
  print(f'[+]Closing file')


def main():
  # generate soup object
  url = "https://realpython.github.io/fake-jobs"
  site_soup = get_soup(page_url=url)

  print(f"================={url}=================")
  # list to store all the jobs_info dictionaries
  all_jobs_list = []
  # get the job_info and append to the list above
  get_job_info(soup=site_soup, all_jobs_info=all_jobs_list)

  # write the data to a csv file
  conv_to_csv(jobs_info_list=all_jobs_list)
  print('==================DONE==================')

start_time = time.time()
main()
print(f"{time.time() - start_time} seconds")
