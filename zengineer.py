class Zengineer:
    def __init__(self, username, verbose = False, douglas_county = True, full_tld_search = False, open_links = False):
        self.bios = []
        self.ages = []
        self.vines = []
        self.emails = []
        self.events = []
        self.images = []
        self.domains = []
        self.genders = []
        self.bitcoins = []
        self.followers = []
        self.following = []
        self.locations = []
        self.companies = []
        self.usernames = []
        self.interests = []
        self.birthdays = []
        self.real_names = []
        self.public_keys = []
        self.verbose = verbose
        self.organizations = []
        self.header_images = []
        self.account_links = []
        self.finished_names = []
        self.usernames = [username]
        self.finished_usernames = []
        self.open_links = open_links
        self.douglas_county = douglas_county
        self.full_tld_search = full_tld_search
        self.out_file = open("output.log", "a")
    def scrape_github(self, username):
        self.log("Scraping GitHub")
        page = None
        try:
            page = urlopen("https://github.com/" + username)
            self.log("GitHub user " + username + " found")
        except HTTPError:
            self.log("GitHub user " + username + " not found")
            return False
        self.log("Processing GitHub Account")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        cards = soup.find_all("li", {"class" : "vcard-detail py-1 css-truncate css-truncate-target"})
        for card in cards:
            self.log("Scanning for companies")
            if "Organization" in card.attrs["aria-label"]:
                self.log("Adding company ")
                self.companies.append(card.contents[1].contents[0])
            self.log("Scanning for locations")
            if "location" in card.attrs["aria-label"]:
                self.log("Adding location")
                self.locations.append(card.contents[1])
            self.log("Scanning for emails")
            if "Email" in card.attrs["aria-label"]:
                self.log("Adding email")
                self.emails.append(card.contents[1].contents[0])
                self.usernames.append(card.contents[1].contents[0].split("@")[0].replace(" ","-"))
            self.log("Scanning for websites")
            if "website" in card.attrs["aria-label"]:
                self.log("Adding website")
                self.domains.append(card.contents[1].contents[0])
                self.usernames.append(card.contents[1].contents[0].replace("https://","").replace("http://","").replace("www.","").split(".")[0])
            self.log("Searching for events")
            if "since" in card.attrs["aria-label"]:
                self.log("Adding event")
                self.locations.append("Joined GitHub on " + card.contents[2].contents[0])
        self.log("Searching for GitHub biography")
        biosection = soup.find_all("div", {"class" : "user-profile-bio"})
        if len(biosection) > 0:
            self.log("Adding GitHub biography")
            self.bios.append(biosection[0].contents[0].contents[0])
        else:
            self.log("No GitHub biography found")
        self.log("Searching for GitHub avatar")
        avatar = soup.find_all("img", {"class" : "avatar rounded-2"})
        if len(avatar) > 0:
            self.log("Saving link to GitHub avatar")
            self.images.append(avatar[0].attrs['src'])
        else:
            self.log("No GitHub avatar found")
        self.log("Searching for real name")
        real_name = soup.find_all("div", {"class" : "vcard-fullname"})
        if len(real_name) > 0:
            self.log("Processing potential real name")
            try:
                self.real_names.append(real_name[0].contents[0])
            except IndexError:
                self.log("No real name")
    def scrape_etsy(self, username):
        self.log("Scraping Etsy")
        page = None
        try:
            page = urlopen("https://etsy.com/people/" + username)
            self.log("Etsy user " + username + " found")
        except HTTPError:
            self.log("Etsy user " + username + " not found")
            return False
        self.log("Processing Etsy Account")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        self.log("Searching for more usernames")
        real_name = soup.find_all("li", {"class" : "username wrap"})
        if len(real_name) > 0:
            self.log("Adding an username")
            self.usernames.append(soup.find_all("li", {"class" : "username wrap"})[0].contents[0].contents[0].replace(" ", "-"))
        self.log("Searching for locations")
        location = soup.find_all("li", {"class" : "location wrap"})
        if len(location) > 0:
            self.log("Adding location")
            self.locations.append(location[0].contents[0])
        alt_username = soup.find_all("span", {"class" : "shopname wrap "})
        self.log("Searching for more usernames")
        if len(alt_username) > 0:
            self.log("Adding username")
            self.usernames.append(alt_username[0].contents[1].contents[0].strip())
        else:
            self.log("No other usernames found")
        image = soup.find_all("img", {"class" : "user-avatar-circle-img user-avatar-external"})
        if len(image) > 0:
            self.images.append(image[0].attrs["src"])
    def scrape_keybase(self, username):
        self.log("Scraping Keybase")
        page = None
        try:
            page = urlopen("https://keybase.io/" + username)
            self.log("Keybase user " + username + "found")
        except HTTPError:
            self.log("No keybase account found")
            return False
        self.log("Interpreting Keybase page")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        self.log("Searching for public keys")
        evens = soup.find_all("span", {"class" : "even"})
        odds = soup.find_all("span", {"class" : "odd"})
        self.log("Assembling PGP public key")
        self.public_keys.append(evens[0].contents[0] + " " + odds[0].contents[0] + " " + evens[1].contents[0] + " " + odds[1].contents[0])
        media = soup.find_all("a", {"rel" : "me"})
        self.log("Collecting social media accounts")
        for medium in media:
            if "twitter.com" in medium.attrs["href"] or "github.com" in medium.attrs["href"] or "reddit.com" in medium.attrs["href"]:
                self.log("Adding social media account and username")
                self.account_links.append(medium.attrs["href"])
                self.usernames.append(medium.contents[0])
        self.log("Searching for bitcoin addresses")
        bitcoin = soup.find_all("a", {"class" : "currency-address view-currency-address"})
        if len(bitcoin) > 0:
            self.log("Adding username from bitcoin")
            self.usernames.append(bitcoin[0].attrs["data-username"])
            self.bitcoins.append(bitcoin[0].contents[0])
        else:
            self.log("No bitcoin found")
        self.log("Searching for Keybase biographies")
        bio = soup.find_all("div", {"class" : "bio"})
        if len(bio) > 0:
            self.log("Adding Keybase biography")
            self.bios.append(bio[0].contents[0].strip())
        else:
            self.log("No Keybase biography found")
        self.log("Searching for location")
        location = soup.find_all("div", {"class" : "location"})
        if len(location) > 0:
            self.log("Adding Keybase location")
            self.locations.append(location[0].contents[0].strip())
        else:
            self.log("No Keybase location found")
        avatar = soup.find_all("img", {"width" : "180", "height" : "180"})
        self.log("Searching for keybase image")
        if len(avatar) > 0:
            self.log("Adding Keybase image")
            self.images.append(avatar[0].attrs["src"])
        else:
            self.log("No Keybase image found")
    def scrape_twitter(self, username):
        self.log("Scraping Twitter")
        page = None
        try:
            page = urlopen("https://twitter.com/" + username)
            self.log("Twitter user " + username + " found")
        except HTTPError:
            self.log("Twitter user " + username + " not found")
            return False
        self.log("Interpreting Twitter page")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        name = soup.find_all("a", {"class" : "ProfileHeaderCard-nameLink"})
        self.log("Looking for real names")
        if len(name) > 0:
            self.log("Adding a real name from twitter")
            self.real_names.append(name[0].contents[0])
        else:
            self.log("No real name found from Twitter")
        self.log("Looking for Twitter join date")
        join = soup.find_all("span", {"class" : "ProfileHeaderCard-joinDateText"})
        if len(join) > 0:
            self.log("Adding Twitter join date")
            self.events.append("Joined Twitter at " + join[0].attrs["title"])
        else:
            self.log("No Twitter join date found")
        avatar = soup.find_all("img", {"class" : "ProfileAvatar-image u-bgUserColor"})
        self.log("Searching for Twitter avatar")
        if len(avatar) > 0:
            if "default_profile" not in avatar[0].attrs["src"]:
                self.log("Adding Twitter avatar")
                self.images.append(avatar[0].attrs["src"])
            else:
                self.log("No twitter avatar found")
        bios = soup.find_all("p", {"class" : "ProfileHeaderCard-bio"})
        if len(bios) > 0:
            self.log("Adding biography from Twitter")
            try:
                self.bios.append(bios[0].contents[0])
            except IndexError:
                pass
        else:
            self.log("No Twitter bio found")
        location = soup.find_all("span", {"class" : "ProfileHeaderCard-locationText"})
        if len(location) > 0:
            self.log("Adding location from Twitter")
            self.locations.append(location[0].contents[0].strip())
        else:
            self.log("No location found on Twitter")
        website = soup.find_all("span", {"class" : "ProfileHeaderCard-urlText"})[0].contents
        self.log("Searching for domain from Twitter")
        if len(website) > 1:
            self.log("Adding domain from Twitter")
            self.domains.append(website[1].attrs["title"])
            self.usernames.append(website[1].attrs["title"].replace("https://","").replace("http://","").replace("www.","").split(".")[0])
        else:
            self.log("No domains found on Twitter")
        outlinks = soup.find_all("a", {"target" : "_blank"})
        self.log("Searching for vine links")
        for outlink in outlinks:
            try:
                if "vine.co" in outlink.attrs["href"]:
                    self.account_links.append(outlink.attrs["href"])
                    self.vines.append(outlink.attrs["href"])
                else:
                    self.log("No vine account found")
            except KeyError:
                pass
    def scrape_flickr(self, username):
        self.log("Scraping Flickr")
        page = None
        try:
            page = urlopen("https://flickr.com/photos/" + username)
            self.log("Flickr user " + username + " found")
        except HTTPError:
            self.log("Flickr user " + username + " not found")
            return False
        self.log("Interpreting Flickr page")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        self.log("Looking for real names")
        rname = soup.find_all("h1", {"class" : "truncate"})
        if len(rname) > 0:
            self.log("Adding real names")
            self.usernames.append(rname[0].contents[0].strip())
        else:
            self.log("No real name found")
    def scrape_aboutme(self, username):
        self.log("Scraping AboutMe")
        page = None
        try:
            page = urlopen("https://about.me/" + username)
            self.log("AboutMe user " + username + " found")
        except HTTPError:
            self.log("AboutMe user " + username + " not found")
            return False
        self.log("Interpreting AboutMe page")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        image = soup.find_all("div", {"class", "image"})
        if len(image) > 0:
            self.log("Added AboutMe image")
            self.images.append(image[0].attrs["style"].split(")")[0].split("(")[1])
        else:
            self.log("No AboutMe image found")
        name = soup.find_all("h1", {"class" : "name"})
        if len(name) > 0:
            self.real_names.append(name[0].contents[0])
            self.log("Adding real name from AboutMe")
        else:
            self.log("No real names from AboutMe")
        bios = soup.find_all("section", {"class" : "bio short-bio"})
        if len(bios) > 0:
            self.log("Added biography from AboutMe")
            self.bios.append(bios[0].contents[0].contents[0].contents[0])
        else:
            self.log("No biography from AboutMe")
        socials = soup.find_all("a", {"class" : "social-link"})
        for social in socials:
            self.account_links.append(social.attrs["href"])
            if "twitter.com" in social.attrs["href"] or "youtube.com" in social.attrs["href"] or "instagram.com" in social.attrs["href"]:
                self.usernames.append(social.attrs["href"].split("/")[-1])
            elif "flickr.com" in social.attrs["href"]:
                if "/" in social.attrs["href"][:-1]:
                    self.usernames.append(social.attrs["href"].split("/")[-2])
    def scrape_youtube(self, username):
        self.log("Scraping YouTube")
        page = None
        try:
            page = urlopen("https://youtube.com/user/" + username)
            self.log("YouTube user " + username + " found")
        except HTTPError:
            self.log("YouTube user " + username + " not found")
            return False
        self.log("Interpreting YouTube page")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        avatar = soup.find_all("img", {"class" : "channel-header-profile-image"})
        if len(avatar) > 0:
            self.log("Adding YouTube avatar")
            self.images.append(avatar[0].attrs["src"])
        else:
            self.log("No Youtube avatar found")
        self.real_names.append(soup.find("title").contents[0].split("-")[0].strip())
    def scrape_deivant(self, username):
        self.log("Scraping DeviantArt")
        page = None
        try:
            page = urlopen("http://" + username + ".deviantart.com")
            self.log("DeviantArt user " + username + " found")
        except HTTPError:
            self.log("DeviantArt user " + username + " not found")
            return False
        self.log("Interpreting DeviantArt page")
        soup = BeautifulSoup(page.read().decode("UTF-8"), "lxml")
        reals = soup.find_all("strong", {"class" : "realname"})
        self.log("Searching for realnames")
        if len(reals) > 0:
            self.log("Added real name from DeviantArt")
            self.real_names.append(reals[0].contents[0])
        else:
            self.log("No real name found on DeviantArt")
    def scrape_douglas(self, name):
        chrome_options = ChromeOptions()
        prefs = {"download.default_directory" : getcwd().replace("\\\\", "/")}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = Chrome(executable_path = "chromedriver.exe", chrome_options = chrome_options)
        self.log("Navigating to Douglas County Assessor")
        driver.get("http://douglascone.wgxtreme.com/?d=1")
        self.log("Navigating to advanced tabs")
        driver.find_elements_by_class_name("x-tab-right")[2].click()
        inputElement = driver.find_element_by_name("owner_name_searchA")
        self.log("Typing name")
        inputElement.send_keys(name)
        sleep(4)
        self.log("Searching")
        try:
            driver.find_element_by_xpath("//*[@id='ext-gen311']").click()
        except NoSuchElementException:
            driver.find_element_by_xpath("//*[@id='ext-gen300']").click()
        sleep(4)
        self.log("Processing source code")
        s = driver.page_source
        soup = BeautifulSoup(s, "lxml")
        potentials = soup.find_all("div", {"class" : "x-grid3-cell-inner"})
        found = False
        names = []
        addresses = []
        self.log("Interating over potential names")
        for n in range(len(potentials)):
            if n % 8 is 1:
                names.append(potentials[n].contents[0])
            elif n % 8 is 2:
                addresses.append(potentials[n].contents[0])
        close = []
        for x in range(len(names)):
            y = self.narrow(names[x], addresses[x])
            if y < 20:
                close.append(names[x])
        matches = []
        self.log("Finding name")
        for clos in close:
            matches.append(driver.find_element_by_xpath("//*[(text()='" + clos + "')]"))
        for match in matches:
            match.click()
            self.log("Selecting entry")
            sleep(4)
            download_pdf = driver.find_element_by_class_name("tb_pdf").click()
            sleep(4)
            self.log("Downloading and checking pdf")
            if not getsize("output.pdf") > 0:
                remove("output.pdf")
            else:
                try:
                    rename("output.pdf", name + ".pdf")
                except FileExistsError:
                    remove(name + ".pdf")
                    rename("output.pdf", name + ".pdf")
                self.pdf_results.append(name + ".pdf")
                found = True
        driver.close()
        self.finished_names.append(name)
        return found
    def narrow(self, name, address):
        self.log("Creating new profile")
        chrome_options2 = ChromeOptions()
        prefs2 = {"download.default_directory" : getcwd().replace("\\\\","/")}
        chrome_options2.add_experimental_option("prefs", prefs2)
        self.log("Creating new driver")
        driver2 = Chrome(executable_path = "chromedriver.exe", chrome_options = chrome_options2)
        self.log("Finding home")
        driver2.get("https://www.google.com/maps/place/" + address.replace(" ", "+"))
        sleep(3)
        self.log("Selecting home image")
        driver2.find_element_by_class_name("widget-pane-section-header-hero").click()
        sleep(6)
        self.log("Minimizing menu")
        driver2.find_element_by_class_name("widget-expand-button-label").click()
        sleep(2)
        self.log("Maximizing window")
        driver2.maximize_window()
        sleep(1)
        self.log("Saving screenshot")
        driver2.save_screenshot("house.png")
        self.header_images.append("file:///" + getcwd().replace("\\", "/").replace("//", "/") + "/house.png")
        driver2.get("https://www.google.com/maps/dir/" + address.replace(" ", "+") + ",+Omaha,+NE/Millard+West+High+School,+5710+South+176th+Avenue,+Omaha,+NE+68135")
        sleep(3)
        self.log("Processing webpage source code")
        s = driver2.page_source
        soup = BeautifulSoup(s, "lxml")
        times = soup.find_all("div", {"class" : "widget-pane-section-directions-trip-duration"})
        time_ints = []
        returns = []
        self.log("Finding shortest travel time")
        for time in times:
            try:
                time_ints.append(int(time.contents[1].contents[0].replace(" min", "")))
            except IndexError:
                time_ints.append(int(time.contents[0].replace(" min", "")))
        driver2.close()
        return min(time_ints)
    def scan(self):
        for username in self.usernames:
            if username not in self.finished_usernames:
                self.log("Checking for domains")
                if self.full_tld_search:
                    self.log("Searching all TLDs")
                    self.find_domains(username)
                else:
                    self.log("Searching common TLDs")
                    self.find_common_domains(username)
                global urlopen, HTTPError, BeautifulSoup, Request, Chrome, ChromeOptions, getcwd, sleep, getsize, rename, remove, system, NoSuchElementException
                from urllib.request import urlopen, Request
                from urllib.error import HTTPError
                from bs4 import BeautifulSoup
                self.scrape_github(username)
                self.scrape_etsy(username)
                self.scrape_keybase(username)
                self.scrape_twitter(username)
                self.scrape_flickr(username)
                self.scrape_aboutme(username)
                self.scrape_youtube(username)
                self.scrape_deivant(username)
                from selenium.webdriver import Chrome, ChromeOptions
                from selenium.common.exceptions import NoSuchElementException
                from os import getcwd, rename, remove, system
                from os.path import getsize
                from time import sleep
                import sys
                if self.douglas_county is True:
                    for name in list(set(self.real_names)):
                        if name not in self.finished_names:
                            found = False
                            if len(name.split(" ")) is 2:
                                found = self.scrape_douglas(name)
                            if found is not True:
                                self.scrape_douglas(name.split(" ")[-1])
                self.finished_usernames.append(username)
        self.display()
    def log(self, message):
        if self.verbose is True:
            os.system("echo -ne ' Checking: " + currentDomain + "  \r'")
            self.out_file.write(message + "\n")
    def find_domains(self, name):
        from Data import all_tlds, default_ips
        from socket import gethostbyname, gaierror
        for extension in all_tlds:
            self.log("Checking " + extension + " domains")
            ip = None
            try:
                ip = gethostbyname(name + extension)
                if ip not in default_ips:
                    self.log("Adding domain: " + "http://www." + name + extension)
                    self.domains.append("http://www." + name + extension)
                else:
                    self.log("Domain " + name + extension + " is unregistered")
            except gaierror:
                self.log("Domain " + name + extension + " is broken")
    def display(self):
        y = open("output.html", "w")
        y.write("\n")
        y.close()
        q = open("output.html", "a")
        q.write("<!DOCTYPE html><html><head><title>" + self.usernames[0] + "</title></head><body style='text-align:center;'><h2>Images</h2>")
        if len(self.images) > 0:
            for image in list(set(self.images)):
                q.write("<img height='200' width='200' src='" + image + "' alt='Image unavailable' />")
        if len(self.header_images) > 0:
            for header_image in list(set(self.header_images)):
                q.write("<br><img width='1200' height='500' src='" + header_image + "' />")
        if len(self.domains) > 0:
            q.write("<hr><h2>Domains</h2>")
            for domain in list(set(self.domains)):
                q.write("<p>" + domain + "</p>")
        if len(self.real_names) > 0:
            q.write("<hr><h2>Names</h2>")
            for name in list(set(self.real_names)):
                q.write("<p>" + name + "</p>")
        if len(self.companies) > 0:
            q.write("<hr><h2>Companies</h2>")
            for company in list(set(self.companies)):
                q.write("<p>" + company + "</p>")
        if len(self.locations) > 0:
            q.write("<hr><h2>Locations</h2>")
            for location in list(set(self.locations)):
                q.write("<p>" + location + "</p>")
        if len(self.emails) > 0:
            q.write("<hr><h2>Emails</h2>")
            for email in list(set(self.emails)):
                q.write("<p>" + email + "</p>")
        if len(self.public_keys) > 0:
            q.write("<hr><h2>PGP Keys</h2>")
            for key in list(set(self.public_keys)):
                q.write("<p>" + key + "</p>")
        if len(self.bitcoins) > 0:
            q.write("<hr><h2>Bitcoin Addresses</h2>")
            for bitcoin in list(set(self.bitcoins)):
                q.write("<p>" + bitcoin + "</p>")
        if len(self.ages) > 0:
            q.write("<hr><h2>Ages</h2>")
            for age in list(set(self.ages)):
                q.write("<p>" + age + "</p>")
        if len(self.genders) > 0:
            q.write("<hr><h2>Genders</h2>")
            for gender in list(set(self.genders)):
                q.write("<p>" + gender + "</p>")
        if len(self.birthdays) > 0:
            q.write("<hr><h2>Birthdays</h2>")
            for birthday in list(set(self.birthdays)):
                q.write("<p>" + birthday + "</p>")
        if len(self.events) > 0:
            q.write("<hr><h2>Events</h2>")
            for event in list(set(self.events)):
                q.write("<p>" + event + "</p>")
        if len(self.account_links) > 0:
            q.write("<hr><h2>Links</h2>")
            for account in list(set(self.account_links)):
                q.write("<p>" + account + "</p>")
        if len(self.bios) > 0:
            q.write("<hr><h2>Biographies</h2>")
            for bio in list(set(self.bios)):
                q.write("<p>" + bio + "</p>")
        q.close()
        import webbrowser
        for account in self.account_links:
            webbrowser.open(account)
    def find_common_domains(self, name):
        from Data import common_tlds, default_ips
        from socket import gethostbyname, gaierror
        for extension in common_tlds:
            self.log("Checking " + extension + " comains")
            ip = None
            try:
                ip = gethostbyname(name + extension)
                if ip not in default_ips:
                    self.log("Adding domain: " + "http://www." + name + extension)
                    self.domains.append("http://www." + name + extension)
                else:
                    self.log("Domain " + name + extension + " is unregistered")
            except gaierror:
                self.log("Domain " + name + extension + " is broken")
import argparse
b = argparse.ArgumentParser(description = "Collects social engineering data on an username", epilog = "Written by Thomas Gerot, Millard West Computer Science Club", prefix_chars = "-")
b.add_argument("-d", "--douglas", help = "Search the Douglas County Assesor", action = "store_true")
b.add_argument("-f", "--full", help = "Checks against every TLD", action = "store_true")
b.add_argument("-l", "--links", help = "Open links to discovered accounts", action = "store_true")
b.add_argument("-v", "--verbose", help = "Increases how wordy the program's output will be", action = "store_true")
c = b.add_argument_group("required arguments")
c.add_argument("-u", "--username", help = "The username to look for", required = True)
a = b.parse_args()
zen = Zengineer(a.username, a.verbose, a.douglas, a.full, a.links)
zen.scan()
