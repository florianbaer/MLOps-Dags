import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from datetime import date
import re
import tkinter as tk
from tkinter import simpledialog

# Load OpenAI API key from .env file
dotenv_path = r"C:/Users/hidbe/VSCodeProjects/JobAssistance/.env"
load_dotenv(dotenv_path)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), )


# Visit a webpage and return its soup object or None if not found
def visit_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        print("Webpage found:", soup.title.text)
        return soup
    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve page {url}: {e}")
        return None


def get_page_amount(search_term):
    soup = visit_page(f"https://www.jobs.ch/de/stellenangebote/?page=1&source=home&term={search_term}")

    if not soup:
        return 0

    match = re.search(r'[\d\s.\u202f]+', soup.title.text)
    if match:
        # Remove any whitespace characters (including non-breaking spaces) and dots
        cleaned_number = re.sub(r'[\s.\u202f]', '', match.group())
        total_jobs = int(cleaned_number)
    else:
        total_jobs = 0

    return total_jobs // 20


# Find job listing URLs from the main job search page
def extract_job_links(soup):
    links = []
    try:
        job_container = soup.find('div', class_='d_flex flex-d_column h_100% w_100%')
        job_articles = job_container.find_all("article") if job_container else []

        for job in job_articles:
            link = "https://www.jobs.ch" + job.find("a", {"data-cy": "job-link"}).get('href')
            links.append(link)
            print(link)
    except AttributeError as e:
        print(f"Error extracting job links: {e}")
    return links


# Extract and format job data from an individual job page
def extract_job_data(soup, url):
    try:
        job_data = {
            "URL": url,
            "Titel": soup.title.text.split(' - ')[0],
            "Firma": soup.find("div", {"data-cy": "vacancy-logo"}).find('img').get('alt') if soup.find("div", {
                "data-cy": "vacancy-logo"}) else None,
            "Logo": soup.find("div", {"data-cy": "vacancy-logo"}).find('img').get('src').replace("48x0",
                                                                                                 "500x0") if soup.find(
                "div", {"data-cy": "vacancy-logo"}) else None
        }

        # This here is missing (4 fields)
        # Extract additional fields from the job listing
        info_list = soup.find('ul',
                              class_='li-t_none pl_s0 mb_s0 mt_s0 d_grid gap_s16 grid-tc_[auto] sm:grid-tc_[1fr_1fr] md:grid-tc_[1fr] pb_s24')
        if info_list:
            for item in info_list.find_all('li'):
                text_content = item.get_text().replace("\n", "").strip()
                if ":" in text_content:  # Only proceed if a colon is present
                    key, value = text_content.split(":", 1)  # Split only on the first ":"
                    job_data[key.strip()] = value.strip()
                else:
                    print(f"Warning: Unrecognized format for field: '{text_content}'")

        # Perform GPT analysis
        job_description = soup.find('main', class_='grid-area_jobAd w_100%').get_text(separator=" ")
        job_data.update(extract_gpt_analysis(job_description))

        job_data["Text"] = job_description
        return json.dumps(job_data, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error extracting data from {url}: {e}")
        return None


# # Use GPT to analyze the job description for additional fields
# def extract_gpt_analysis(description_text):
#     prompt = """
#     Extract the following fields from this job description:
#     - Benefits
#     - Requirements
#     - Responsibilities
#
#     Return the result as a JSON object with this format:
#     {
#       "Benefits": "...",
#       "Requirements": "...",
#       "Responsibilities": "..."
#     }
#     """
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": prompt},
#                 {"role": "user", "content": description_text}
#             ],
#             temperature=0.7,
#             max_tokens=1024,
#             top_p=1
#         )
#         # Parse the JSON response from the assistant's reply
#         completion = json.loads(response.choices[0].message.content)
#         return completion
#     except Exception as e:
#         print(f"Error in GPT analysis: {e}")
#         return {"Benefits": "", "Requirements": "", "Responsibilities": ""}


# Write job data to a file
def write_job_data(filename, job_data):
    with open(filename, 'a', encoding='utf-8', errors='ignore') as file:
        file.write(job_data + "\n\n\n")


# Main function to execute the scraping and data extraction
def main():
    # Filename to store job data
    filename = f"{date.today()}_Jobs_CH.txt"

    root = tk.Tk()
    root.withdraw()  # Hide the root window
    search_term = simpledialog.askstring("Input", "Enter the job search term:")
    if not search_term:
        print("No search term entered. Exiting.")
        exit()

    page_amount = get_page_amount(search_term)

    for page_number in range(page_amount - 1):
        print("Page: ", page_number, "of ", page_amount - 1, " Pages")
        main_page_url = f"https://www.jobs.ch/de/stellenangebote/?page={page_number}&source=home&term={search_term}"
        soup = visit_page(main_page_url)

        if not soup:
            continue  # Skip this page if it couldn't be loaded

        # Get all job links from this page
        job_links = extract_job_links(soup)

        # Extract data for each job link
        for link in job_links:
            job_soup = visit_page(link)
            if job_soup:
                job_data = extract_job_data(job_soup, link)
                if job_data:
                    write_job_data(filename, job_data)


if __name__ == "__main__":
    main()
