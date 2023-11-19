import os, marko, glob, re
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


class Database:

	@staticmethod
	def get_tags(file):
	    tags = list(map(lambda x: x[0],re.findall(r'#(.*?)([\. ]|$)',file)))
	    if (re.search(r'/- ',file)):
	        tags.append('_stbd')
	    return tags		

	def __init__(self):

		NOTES_DIR = str(settings.BASE_DIR) + "/_external/content/db3/files/"
		files = glob.glob(str(NOTES_DIR) + '**/*.txt', recursive=True)

		df = pd.DataFrame(data=files,columns=['file'])
		df['file'] = df['file'].str.replace(NOTES_DIR,'')
		df['tags'] = df['file'].apply(self.get_tags)

		self.df = df[df.apply(lambda x: False if '_pi' in x['tags'] else True,axis=1)]

	def __tag_counts(self):
		tag_counts = pd.Series([item for sublist in self.df['tags'] for item in sublist]).value_counts().to_frame(name='count').reset_index()
		tag_counts = tag_counts.rename(columns={'index':'tag'})
		return tag_counts

	def basic_tag_counts(self):
		tag_counts = self.__tag_counts()
		return tag_counts[~tag_counts.tag.str.contains('^_')]

	def special_tag_counts(self):
		tag_counts = self.__tag_counts()
		print(tag_counts)
		return tag_counts[tag_counts.tag.str.contains('^_')]


def index(request):

	db = Database()

	files = glob.glob(str(settings.BASE_DIR) + '/_external/content/preview/**/*.txt', recursive=True)

	bodies = []

	for file in files:
		f = open(file,'r')
		f.read()

		bodies.append(f.read())
		break


	body = marko.convert("\n".join(bodies))

	context = {
	    "special_tag_counts": db.special_tag_counts(),
	    "basic_tag_counts": db.basic_tag_counts(),
	    "body": 'yo'
	}

	# return HttpResponse("Hello, world. You're at some page, bruh." + str(settings.BASE_DIR))	
	return render(request, "db.html", context)

