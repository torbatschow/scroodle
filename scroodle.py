import mechanize
from bs4 import BeautifulSoup
import cookielib
import getpass


#get a table with all sessions, resource names and resource URLs out of a course page soup
def extract_course_resources(coursepagesoup):
    sessionssoup = []
    for i in coursepagesoup.find_all('li', class_='section main clearfix'):
        sessionssoup.append(i)
    sessions = []
    for item in sessionssoup:
        resource_titles = []
        resource_links = []
        session = []
        for i in item.find_all(class_='modtype_resource'):
            resource_titles.append(i.get_text())
            for a in i.find_all('a', href=True):
                resource_links.append(a['href'])
        session.append(item.find('h3', class_='sectionname').get_text())
        session.append(resource_titles)
        session.append(resource_links)
        sessions.append(session)
    return sessions


#Find courses from moodle dash board soup, generate var courses with names and urls
def extract_courses(moodlesoup):
    return ([i.encode(formatter=None)[i.encode(formatter=None).find('title=\"') + 7:
    i.encode(formatter=None).find('\"><img alt=\"\" class=\"smallicon')]
                for i in moodlesoup.find_all('li', class_='type_course')],
               [i.encode(formatter=None)[i.encode(formatter=None).find('role=\"treeitem\"><a href=\"') + 25:
               i.encode(formatter=None).find('\" id=\"label')]
                for i in moodlesoup.find_all('li', class_='type_course')])


#Initialize Browser
br = mechanize.Browser()

#Enable CookieJar
cj = cookielib.CookieJar()
br.set_cookiejar(cj)

#Set browser options
br.set_handle_equiv( True )
br.set_handle_gzip( True )
br.set_handle_redirect( True )
br.set_handle_referer( True )
br.set_handle_robots( False )
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]

#Open log-in URL
br.open("https://moodle.hertie-school.org/login/index.php")

#Get login data
username = raw_input('Enter your username: ')
password = getpass.getpass('Enter your password: ')

#Fill in log-in form and log in
br.form = list(br.forms())[0] # use when form is unnamed
br.form['username'] = username
br.form['password'] = password

#Log in and find courses
courses = extract_courses(BeautifulSoup(br.submit()))

#open first course and get all resource links
br.open(courses[1][0])
resources = extract_course_resources(BeautifulSoup(br.response()))

#show resources output
for p in resources:
    print(p)