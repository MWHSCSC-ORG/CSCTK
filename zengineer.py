# TODO Add followers and following
# TODO Find organization names
class Zengineer:
    def __init__(self, username, verbose = False, douglas_county = True, full_tld_search = False, open_links = False, webpage_output = True):
        self.bios = []
        self.ages = []
        self.vines = []
        self.emails = []
        self.events = []
        self.images = []
        self.domains = []
        self.bitcoins = []
        self.followers = []
        self.following = []
        self.locations = []
        self.companies = []
        self.usernames = []
        self.interests = []
        self.birthdays = []
        self.real_names = []
        self.pdf_results = []
        self.public_keys = []
        self.verbose = verbose
        self.organizations = []
        self.header_images = []
        self.account_links = []
        self.usernames = [username]
        self.finished_usernames = []
        self.open_links = open_links
        self.webpage_output = webpage_output
        self.douglas_county = douglas_county
        self.full_tld_search = full_tld_search
        self.out_file = open("output/output.log", "a")
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
            self.images.append([avatar[0].attrs['src'], "GitHub Avatar"])
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
            self.locations.append(location[0].contents[0])
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
    def scrape_youtube(self, username):
        self.log("Scraping ACCOUNT")
        # page = urlopen("OOOOOOO")
    def scrape_deivant(self, username):
        self.log("Scraping ACCOUNT")
        # page = urlopen("OOOOOOO")
    def scrape_myspace(self, username):
        self.log("Scraping ACCOUNT")
        # page = urlopen("OOOOOOO")
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
                global urlopen, HTTPError, BeautifulSoup, Request
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
                self.scrape_myspace(username)
                self.finished_usernames.append(username)
    def log(self, message):
        if self.verbose is True:
            print(message)
        self.out_file.write(message + "\n")
    def find_domains(self, name):
        from Data import all_tlds, default_ips
        from socket import gethostbyname, gaierror
        for extension in all_tlds:
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
zen = Zengineer("tom")
zen.scan()
