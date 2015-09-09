import hound
import emailFinderv2
import emailFinderv3
import Legion
import c_cubed
import c_4
import scrapers as s

def houndDown(legion_object, type_of_media, enough = []):
	if legion_object.type_of_entity == 'person':
		return hound.getPersonsSocialMedia(legion_object, type_of_media = type_of_media, enough = enough)
	return hound.getCompanysSocialMedia(legion_object, type_of_media = type_of_media)


def completeEntity(updated_legion, use_the_hounds = False):
	if use_the_hounds:
		to_find = ['company_linkedin', 'company_twitter']
		if updated_legion.type_of_entity == 'person':
			to_find = ['personal_linkedin', 'personal_twitter']
		for social_media in to_find:
			if social_media not in updated_legion.current_web_presences:
				newer_legion = houndDown(updated_legion, social_media)
				if newer_legion:
					updated_legion = newer_legion
	return updated_legion.complete()


def completeEmail(email, fuzzy = True, use_the_hounds = False, check_validity = True):
	valid = 'Unknown'
	if check_validity:
		valid = s.emailVerifier(email).getKBMetrics()[1]
	if valid == 'Invalid':
		return Legion.legion({'emails':[{'address':email, 'is_deliverable':'Invalid'}]}, scrapers = {})
	print valid
	return
	person = c_cubed.Scanner(email_to_find = email).ScanForSocialMedias()
	person = completeEntity(person, use_the_hounds = use_the_hounds)
	return person


def getEmail(legion_object, complete=False, use_the_hounds = False, want = ['personal', 'company']):
	if complete:
		person = completeEntity(legion_object, use_the_hounds = use_the_hounds)
	else:
		person = legion_object
	e = emailFinderv2.Emailgorithm(person, stop_if_matches = person, want = want)
	completed_legion = e.mainSearch()
	return completed_legion.complete()

def getEmail2(legion_object, complete=False, use_the_hounds = False, want = ['personal', 'company']):
	if complete:
		person = completeEntity(legion_object, use_the_hounds = use_the_hounds)
	else:
		person = legion_object
	e = emailFinderv3.Emailgorithm(person, want = want)
	completed_legion = e.mainSearch()
	return completed_legion.complete()


