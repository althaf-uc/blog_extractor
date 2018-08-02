from bs4 import BeautifulSoup
import re

from datetime import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblogsite.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from blogs.models import log
from datetime import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblogsite.settings")

import argparse
import inspect

ERR_CODE = {'ERROR': 1, 'WARNING': 2,'INFO':3,'DEBUG':4}


class  parseBase:
    
    def __init__(self,my_blogs_div,run_id,ex_id):
        self.blogs_div=my_blogs_div
        self.post_title=''
        self.run_id=run_id
        self.ex_id=ex_id

    def create_log(self,severity1,msg,fn_name):
        l=log()
        l.run_id=self.run_id
        l.severity_id=severity1
        l.log_message=msg
        l.extractor_id=self.ex_id
        l.function_name=fn_name    
        l.save()    

    def parse_date(self):
        header=self.blogs_div.find_all("h2",class_="date-header")[0]
        return header.string

    def parse_title(self):                                
        try:
            #if title tag present
            title=self.blogs_div.find("h3",class_="post-title entry-title")
            title_string=title.a.string
            return title_string
        except AttributeError as err:
            try:
                # if title not present getting first sentence of body which is in differnt tags
                body=self.blogs_div.find("div",class_="post-body entry-content")
                title_string=''        
                title_string=title_string+body.contents[0]    
                title_string=title_string+body.contents[1].text
                title_string=title_string+body.contents[2]
                title_string=title_string+body.contents[3].text
                title_string=title_string+body.contents[4]
                title_string = re.sub('\n', '', title_string)
                
                self.create_log(ERR_CODE['INFO'],"'Attribute error':Title tag not present for post '"+title_string+"'.",inspect.stack()[0][3])
                    #print 'log created'
                return title_string
            except TypeError as err:
                # if title not present getting first sentence of body which is under span tag
                
 
                title_string=''        
                body=self.blogs_div.find("div",class_="post-body entry-content")
                title_string=body.span.string
                title_string = re.sub('\n', '', title_string)
                self.post_title=title_string
                
                self.create_log(ERR_CODE['INFO'],"'Attribute error': Title tag not present for post '"+title_string+"'.",inspect.stack()[0][3])
                return title_string


    def parse_content(self):
        body=self.blogs_div.find_all("div",class_="post-body entry-content")[0]
        content=''
        for string in body.stripped_strings:
            content=content+repr(string)

        content = re.sub('..a0', '', content)
        content = re.sub('\'u\'|u\'', ' ',content)
        content = re.sub('\'\Z', ' ', content)
        return content
    
    def parse_author_name(self):    
        

        footer=self.blogs_div.find("div",class_="post-footer")
        try:
            author_string=''
            author_string=author_string+footer.find("span",class_="fn").string
            return author_string
        except:
            self.create_log(ERR_CODE['INFO'],"Attribute error:No footer tag present for post: '"+self.post_title+"'.",inspect.stack()[0][3])
            return 'error'

    def parse_post_time(self):
        footer=self.blogs_div.find("div",class_="post-footer")
        try:
            footer_string=''    
            footer_string=footer_string+footer.find("abbr",class_="published").string
            return footer_string
        except:
            self.create_log(ERR_CODE['INFO'],"Attribute error:No footer tag present for post: '"+self.post_title+"'.",inspect.stack()[0][3])
            return 'error'

    def parse_comments(self):
        try:
            comment=self.blogs_div.find_all("span",class_="post-comment-link")
            comment_count=1
            com_str=''            
            for com in comment:                
                com=com.string.replace('\n','')
                com=com.strip()
                if com:
                    com_str=com_str+'comment :'+comment_count+'\n'
                    comment_count=comment_count+1    
            return com_str        
        except:
            self.create_log(ERR_CODE['INFO'],"Attribute error:No cooment tag present for post: '"+self.post_title+"'.",inspect.stack()[0][3])
            return 'error'















                    
