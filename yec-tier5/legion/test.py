import growth_scrapers
import scrapers
import emailFinderv2
import growth_scrapers
from Legion import legion
import master

# l = legion({'web_presence':{'personal_twitter':{'url':'prof_oz'}}}).complete().information
# print l

# print growth_scrapers.scanGoogleForLinkedin(search_dict = {'keywords':'inside sales manager', 'location': 'austin'})

# a = growth_scrapers.scanTwitter(scraper_dict = {'keywords':'founder'},  limit = 1)
# print len(a)
# print a[0]

print master.completeEmail('a.asallen@gmail.com', use_the_hounds = True)

# print len(a)
# for b in a:
# 	print b
	# l = legion(b, scrapers = {})
	# completed_person = master.getEmail(l, complete = True, use_the_hounds = True).information
	# print completed_person
