import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

outfile = open('apple_job_list.csv', 'w')
wd = webdriver.Firefox()
n=0 #Page Number
while True:
	#When you apply filter, then you can get url including query. Let's sweep the current page number at the end of url.
	filter_url = 'https://jobs.apple.com/us/search?#location&t=0&sb=req_open_dt&so=1&j=HDWEG&lo=1*953*USA&pN='
	url = filter_url + str(n)
	print(url)
	wd.get(url)
	time.sleep(10)
	WebDriverWait(wd, 10).until(
		EC.visibility_of_element_located((By.CLASS_NAME, "searchresult")))

# And grab the page HTML source
	html_page = wd.page_source

# Now you can use html_page as you like
	from bs4 import BeautifulSoup
	soup = BeautifulSoup(html_page, "html.parser")

# if we have 'searchresult error' class, then stop.
# if we have 'searchresult' class, then parse its sub elements and print to the file as a string.
	rows_error = soup.find_all('tr', {'class': 'searchresult error'})
	rows = soup.find_all('tr', {'class': 'searchresult'})
	if rows_error:
		break
	else:
		for row in rows:
			tds = row.find_all('td')
			title = tds[0].p.a.get_text()
			function = tds[1].p.get_text()
			location = tds[2].p.get_text()
			date = tds[3].p.get_text()
			outfile.write(title+ '\t'+function+'\t'+location+'\t'+date+'\n')
		n=n+1

outfile.close()
wd.close()
