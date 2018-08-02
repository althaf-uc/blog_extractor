from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
from datetime import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblogsite.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from blogs.models import author,post,post_content,additional_information,severity,log,same_post,extractor,run_info,refresh_post,blogs_import,json_post
import re

from datetime import datetime
from datetime import timedelta 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblogsite.settings")
from blogs.models import author,post,post_content,additional_information
import argparse
import inspect
from parse_base import *
import django
django.setup()

parser = argparse.ArgumentParser()
parser.add_argument("extractor_id",type=int)
parser.add_argument("run_id",type=int)
args = parser.parse_args()




ERR_CODE = {'ERROR': 1, 'WARNING': 2,'INFO':3,'DEBUG':4}

def create_log(severity1,msg,fn_name,exid,rid):
        l=log()
        r1=run_info.objects.get(id=rid)
        
        l.run_id=r1.id
        l.severity_id=severity1
        
        l.log_message=msg
        l.extractor_id=exid
        l.function_name=fn_name    
        l.save()    

def main(args):
    parser = argparse.ArgumentParser()


    parser.add_argument("extractor_id",type=int)
    parser.add_argument("run_id",type=int)
    args = parser.parse_args()
    rid=args.run_id
    titles=''
    contents=''
    authors=''
    dates=''
    times=''
    comments=''
    
    blog_count=0
    run1=run_info.objects.get(id=args.run_id)

    ex=extractor.objects.get(id=args.extractor_id)
    dirpath = os.getcwd()
    filename='myblogs.html'
    file_path=dirpath+'/'+filename
    try:
        f = urlopen('http://blog.python.org/',timeout=3)
        create_log(ERR_CODE['WARNING'],"connecting to 'http://blog.python.org/'",inspect.stack()[0][3],ex.id,rid)
    except :#urllib.URLError:        
        create_log(ERR_CODE['ERROR'],"Extraction of posts is not possible in website due to connection issues",inspect.stack()[0][3],ex.id,rid)
        run1.run_status='Failed'        
        run1.save()
        exit()   
      
    file1= open("myblogs.html", "a")




    if ex.extractor_type.extractor_style=='NORMAL':    
        
        if ex.year!=0:        
            create_log(ERR_CODE['INFO'],"extracting posts of the year: "+str(ex.year),inspect.stack()[0][3],ex.id,rid)
        if ex.no_of_pages!=0:        
            create_log(ERR_CODE['INFO'],"extracting first '"+str(ex.no_of_pages)+"' pages.",inspect.stack()[0][3],ex.id,rid)
        if ex.no_of_blogs!=0:        
            create_log(ERR_CODE['INFO'],"extracting first '"+str(ex.no_of_blogs)+"' blogs.",inspect.stack()[0][3],ex.id,rid)
        n_o_p=22
        max_blog=200
        if ex.no_of_pages!=0 and ex.year==0:
            n_o_p=ex.no_of_pages
        elif ex.no_of_blogs!=0 and ex.year==0:
            max_blog=ex.no_of_blogs
        elif ex.year==0:
            max_blog=0
            n_o_p=0
        for k in range(n_o_p):
            html_doc= f.read()
            
            #file1.write(html_doc)
            soup = BeautifulSoup(html_doc, 'html.parser')

            blogs_div1=soup.find_all("div",class_="date-outer")

    
            for i in range(len(blogs_div1)):
                
                blog_count=blog_count+1
                if blog_count>max_blog:
                    break
                a=author()
                p=post_content()
                c=additional_information()
                pp=post()
                
                my_parser=parseBase(blogs_div1[i],run1.id,args.extractor_id)
                #print 'post:'+str(i+1)
                dates=my_parser.parse_date()
                titles=my_parser.parse_title()
                contents=my_parser.parse_content()
                authors=my_parser.parse_author_name()
                times=my_parser.parse_post_time()
                comments=my_parser.parse_comments()
                flag=0
                if authors=='error' or times=='error':
                    flag=1    
                



                cur_year = datetime.strptime(dates, "%A, %B %d, %Y").year
                ex=extractor.objects.get(id=args.extractor_id)
                if cur_year<ex.year :
                
                    run1.run_status='Success'        
                    run1.save()    
                    exit()

                if ex.year !=0 and ex.year!=cur_year:
                    print ('post of different year')
                elif  flag==0 :
                    file1.write(str(blogs_div1[i]))
                    try:
                        #print 'updating'                        
                        a=author.objects.get(author_name=authors)                        
                        tit=post.objects.get(title=titles,author_id=a.id)    
            
                        con=post_content.objects.get(id=tit.post_content_id)
                        try:
                                 con.content=contents
                                 con.save()
                        except:
                                 con.content='content not supported'
                                 con.save()
                                
                        try:                        
                                                            
                                con1=additional_information.objects.get(id=tit.comments_id)
                        
                                if comments:
                                    con1.comments=comments                
                                    con1.save()                            
                                
                                else:
                                    #print tit.comments
                                    tit.comments=None
                                    tit.save()
                                    con1.delete()

                        except:
                                con=additional_information()
                                if comments:
                                    con.comments=comments                
                                    con.save()
                                    tit.comments=con    
                                    create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: No comments earlier for post: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)                                    
                                
                    




                        struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                        struct_time1 = datetime.strptime(times, "%I:%M %p")


                        tit.post_date=struct_time.strftime('%Y-%m-%d')
                        tit.post_time=struct_time1.strftime('%H:%M:%S')
                        tit.file_path=file_path

                        tit.save()
                        create_log(ERR_CODE['INFO'],"post already present for title: '"+titles+"' updaing its details",inspect.stack()[0][3],ex.id,rid)    
            
                

                
                    except:
                    
                        create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: Earlier there is no posts with title: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)
                        s=same_post()
                        #print'insertinng'
                        prev_posts=post.objects.filter(title=titles)
                        if len(prev_posts)>0:
                            msg='same title found \nTitle: '+titles+'\nAuthor name: '+authors+'\n previously written by:\n'
                            authors_list=''
                            post_ids=''
                            for ever_post in prev_posts:
                                post_ids=post_ids+str(ever_post.id)+', '
                                au=author.objects.get(id=ever_post.author_id)
                                msg=msg+au.author_name+', '
                                authors_list=authors_list+au.author_name+', '
                            create_log(ERR_CODE['ERROR'],msg,inspect.stack()[0][3])
                    
                            s.title=titles
                            s.old_author=authors_list
                            s.new_author=authors
                            s.old_post_id=post_ids
                    
                    
        
                        try:                     
                            a.author_name=authors
                            a.save()
                            
                        except:
                            #print'trying to insert duplicate author'
                            create_log(ERR_CODE['INFO'],"Integrity error: author already present as '"+authors+"'.",inspect.stack()[0][3],ex.id,rid)
                                
       
                        try:
                            p.content=contents
                            p.save()
                        except:
                            p.content='content not supported'
                            p.save()
                                
                      
                        if comments:
                            c.comments=comments                
                            c.save()

                        a=author.objects.get(author_name=authors)
                        #print a.author_name
                
                        struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                        struct_time1 = datetime.strptime(times, "%I:%M %p")
                        pp.title=titles
                        pp.post_date=struct_time.strftime('%Y-%m-%d')
                        pp.post_time=struct_time1.strftime('%H:%M:%S')
                        pp.file_path=file_path
                        pp.author_id=a.id
                        pp.post_content_id=p.id
        
                        if c.comments:
                            pp.comments_id=c.id
                        print (dates)
                        pp.save()
                        if len(prev_posts)>0:
                            s.new_post_id=pp.id
                            s.save()
                        
                        json_post.objects.create(datas={'author':authors,'title':titles,'date':struct_time.strftime('%Y-%m-%d'),'content': contents})

    
        
            try:
                next_blog_tag=soup.find("span",id="blog-pager-older-link")
                f = urlopen(next_blog_tag.a['href'],timeout=3)
            except:
                create_log(ERR_CODE['ERROR'],"unable to open the link or link to next page not present",inspect.stack()[0][3],ex.id,rid)                    
                break
            if blog_count>max_blog:
                break

        run1.run_status='Success'        
        run1.save()    

        #os.system(str1)
        
    elif ex.extractor_type.extractor_style=='INCREMENTAL':
        
        create_log(ERR_CODE['INFO'],"extracting '"+str(ex.no_of_pages)+"' pages starting from '"+str(ex.start_page)+"'.",inspect.stack()[0][3],ex.id,rid)
    
        n_o_p=ex.no_of_pages+ex.start_page-1
        s_p=ex.start_page

        for k in range(n_o_p):
            html_doc= f.read()
            #file1.write(html_doc)
            soup = BeautifulSoup(html_doc, 'html.parser')
            if k>=s_p-1:
                blogs_div1=soup.find_all("div",class_="date-outer")
            
                for i in range(len(blogs_div1)):
    
    
                    a=author()
                    p=post_content()
                    c=additional_information()
                    pp=post()
                    
                    my_parser=parseBase(blogs_div1[i],run1.id,args.extractor_id)
                    #print 'post:'+str(i+1)
                    dates=my_parser.parse_date()
                    titles=my_parser.parse_title()
                    contents=my_parser.parse_content()
                    authors=my_parser.parse_author_name()
                    times=my_parser.parse_post_time()
                    comments=my_parser.parse_comments()
                    flag=0
                    if authors=='error' or times=='error':
                        flag=1 

        
                    if  flag==0:
                        file1.write(str(blogs_div1[i]))
                        try:
                            #print 'updating'                        
                            a=author.objects.get(author_name=authors)                        
                            tit=post.objects.get(title=titles,author_id=a.id)                        
                            con=post_content.objects.get(id=tit.post_content_id)
                            
                            try:
                                 con.content=contents
                                 con.save()
                            except:
                                 con.content='content not supported'
                                 con.save()
                                
                            try:                        
                                                            
                                con1=additional_information.objects.get(id=tit.comments_id)
                        
                                if comments:
                                    con1.comments=comments                
                                    con1.save()                            
                                
                                else:
                                    #print tit.comments
                                    tit.comments=None
                                    tit.save()
                                    con1.delete()

                            except:
                                con=additional_information()
                                if comments:
                                    con.comments=comments                
                                    con.save()
                                    tit.comments=con    
                                    create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: No comments earlier for post: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)                                    
                                
                    

                            struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                            struct_time1 = datetime.strptime(times, "%I:%M %p")

    
                            tit.post_date=struct_time.strftime('%Y-%m-%d')
                            tit.post_time=struct_time1.strftime('%H:%M:%S')
                            tit.file_path=file_path
        
                            tit.save()
                            create_log(ERR_CODE['INFO'],"post already present for title: '"+titles+"' updaing its details",inspect.stack()[0][3],ex.id,rid)
                        except:
                            create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: Earlier there is no posts with title: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)
                            s=same_post()
                            #print'insertinng'
                            prev_posts=post.objects.filter(title=titles)
                            if len(prev_posts)>0:
                                msg='same title found \nTitle: '+titles+'\nAuthor name: '+authors+'\n previously written by:\n'
                                authors_list=''
                                post_ids=''
                                for ever_post in prev_posts:
                                    post_ids=post_ids+str(ever_post.id)+', '
                                    au=author.objects.get(id=ever_post.author_id)
                                    msg=msg+au.author_name+', '
                                    authors_list=authors_list+au.author_name+', '
                                create_log(ERR_CODE['ERROR'],msg,inspect.stack()[0][3],ex.id,rid)
                            
                                s.title=stitles
                                s.old_author=authors_list
                                s.new_author=authors
                                s.old_post_id=post_ids                
                            try:                     
                                a.author_name=authors
                                a.save()
                            except:
                                #print'trying to insert duplicate author'
                                create_log(ERR_CODE['INFO'],"Integrity error: author already present as '"+authors+"'.",inspect.stack()[0][3],ex.id,rid)
                                    
                                         
                            try:
                                p.content=contents
                                p.save()
                            except:
                                p.content='content not supported'
                                p.save()
                                
                
        
                            if comments:
                                c.comments=comments                
                                c.save()

                            a=author.objects.get(author_name=authors)
                            
                            struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                            struct_time1 = datetime.strptime(times, "%I:%M %p")
                            pp.title=titles
                            pp.post_date=struct_time.strftime('%Y-%m-%d')
                            pp.post_time=struct_time1.strftime('%H:%M:%S')
                            pp.file_path=file_path
                            pp.author_id=a.id
                            pp.post_content_id=p.id
            
                            if c.comments:
                                pp.comments_id=c.id

                            pp.save()
                            if len(prev_posts)>0:
                                s.new_post_id=pp.id
                                s.save()
                                                
            try:
                next_blog_tag=soup.find("span",id="blog-pager-older-link")
                f = urlopen(next_blog_tag.a['href'],timeout=3)
            except:
                break
    
                
        ex.start_page=s_p+ex.no_of_pages
        ex.save()    
        run1.run_status='Success'        
        run1.save()        




        
    elif ex.extractor_type.extractor_style=='DATE RANGE':
        create_log(ERR_CODE['INFO'],"extracting posts from '"+str(ex.start_date)+"'to '"+str(ex.end_date)+"'.",inspect.stack()[0][3],ex.id,rid)
        end_date1=ex.start_date + timedelta(days=ex.days_to_extract)  
        start_date1=ex.start_date - timedelta(days=ex.days_to_negate)  
        #self.start_date1=self.ex.start_date
        if ex.end_date!=None:
            end_date1=ex.end_date
        while True:
            html_doc= f.read()
            #file1.write(html_doc)
            soup = BeautifulSoup(html_doc, 'html.parser')
            blogs_div1=soup.find_all("div",class_="date-outer")
            for i in range(len(blogs_div1)):
                blog_count=blog_count+1                
                a=author()
                p=post_content()
                c=additional_information()
                pp=post()
                
                my_parser=parseBase(blogs_div1[i],run1.id,args.extractor_id)
                #print 'post:'+str(i+1)
                dates=my_parser.parse_date()
                titles=my_parser.parse_title()
                contents=my_parser.parse_content()
                authors=my_parser.parse_author_name()
                times=my_parser.parse_post_time()
                comments=my_parser.parse_comments()
                flag=0
                if authors=='error' or times=='error':
                    flag=1 


                cur_date = datetime.strptime(dates, "%A, %B %d, %Y").date()
                
                if cur_date<start_date1:
                    run1.run_status='Success'        
                    run1.save()    
                    exit()
                if  flag==0 and cur_date<=end_date1:
                    file1.write(str(blogs_div1[i]))
                    try:
                        #print 'updating'                        
                        a=author.objects.get(author_name=authors)                        
                        tit=post.objects.get(title=titles,author_id=a.id)    
        
                        con=post_content.objects.get(id=tit.post_content_id)
                        try:
                                 con.content=contents
                                 con.save()
                        except:
                                 con.content='content not supported'
                                 con.save()
                        try:                        
                                                            
                                con1=additional_information.objects.get(id=tit.comments_id)
                        
                                if comments:
                                    con1.comments=comments                
                                    con1.save()                            
                                
                                else:
                                    #print tit.comments
                                    tit.comments=None
                                    tit.save()
                                    con1.delete()

                        except:
                                con=additional_information()
                                if comments:
                                    con.comments=comments                
                                    con.save()
                                    tit.comments=con    
                                    create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: No comments earlier for post: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)                                    
                                
                    


                        struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                        struct_time1 = datetime.strptime(times, "%I:%M %p")
    


                        tit.post_date=struct_time.strftime('%Y-%m-%d')
                        tit.post_time=struct_time1.strftime('%H:%M:%S')
                        tit.file_path=file_path
                        tit.save()    
                        create_log(ERR_CODE['INFO'],"post already present for title: '"+titles+"' updaing its details",inspect.stack()[0][3],ex.id,rid)                    
                    except:
                        s=same_post()
                        create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: Earlier there is no posts with title: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)
                        #print'insertinng'
                        prev_posts=post.objects.filter(title=titles)
                        if len(prev_posts)>0:
                            msg='same title found \nTitle: '+titles+'\nAuthor name: '+authors+'\n previously written by:\n'
                            authors_list=''
                            post_ids=''
                            for ever_post in prev_posts:
                                post_ids=post_ids+str(ever_post.id)+', '
                                au=author.objects.get(id=ever_post.author_id)
                                msg=msg+au.author_name+', '
                                authors_list=authors_list+au.author_name+', '
                            create_log(ERR_CODE['ERROR'],msg,inspect.stack()[0][3],ex.id,rid)
                
                            s.title=titles
                            s.old_author=authors_list
                            s.new_author=authors2018
                            s.old_post_id=post_ids    
                        try:                     
                            a.author_name=authors
                            a.save()
                        except:
                            #print'trying to insert duplicate author'
                            create_log(ERR_CODE['INFO'],"Integrity error: author already present as '"+authors+"'.",inspect.stack()[0][3],ex.id,rid)
                                    
                        try:
                            p.content=contents
                            p.save()
                        except:
                            p.content='content not supported'
                            p.save()
                                
                
                

                        if comments:
                            c.comments=comments                
                            c.save()

                        a=author.objects.get(author_name=authors)
                    
                        struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                        struct_time1 = datetime.strptime(times, "%I:%M %p")
                        pp.title=titles
                        pp.post_date=struct_time.strftime('%Y-%m-%d')
                        pp.post_time=struct_time1.strftime('%H:%M:%S')
                        pp.file_path=file_path
                        pp.author_id=a.id
                        pp.post_content_id=p.id        
                        if c.comments:
                            pp.comments_id=c.id
                        pp.save()
                        if len(prev_posts)>0:
                            s.new_post_id=pp.id
                            s.save()
        
            try:
                next_blog_tag=soup.find("span",id="blog-pager-older-link")
                f = urlopen(next_blog_tag.a['href'],timeout=3)
            except:
                break
                create_log(ERR_CODE['ERROR'],"unable to open the link or link to next page not present",inspect.stack()[0][3],ex.id,rid)

            

        

    elif ex.extractor_type.extractor_style=='REFRESH BLOG':
        r_posts=list()        
        start_date=datetime.now().date()
        ref_ids=refresh_post.objects.all()
        for ref in ref_ids:        
            r_posts.append(ref.post_id)
    
    
        for abc in r_posts:
            try:
                pos=post.objects.get(id=abc)
                if start_date>=pos.post_date:
                    start_date=pos.post_date
            except:
                create_log(ERR_CODE['ERROR'],"ObjectNotFound: The post for paricular post id: "+str(abc)+" is not found",inspect.stack()[0][3],ex.id,rid)
                ref=refresh_post.objects.get(post_id=abc)
                ref.delete()
        while True:
            html_doc= f.read()
            #file1.write(html_doc)
            soup = BeautifulSoup(html_doc, 'html.parser')
            blogs_div1=soup.find_all("div",class_="date-outer")
            for i in range(len(blogs_div1)):
                blog_count=blog_count+1                
                a=author()
                p=post_content()
                c=additional_information()
                pp=post()
                
                my_parser=parseBase(blogs_div1[i],run1.id,args.extractor_id)
                #print 'post:'+str(i+1)
                dates=my_parser.parse_date()
                titles=my_parser.parse_title()
                contents=my_parser.parse_content()
                authors=my_parser.parse_author_name()
                times=my_parser.parse_post_time()
                comments=my_parser.parse_comments()
                flag=0
                if authors=='error' or times=='error':
                    flag=1 


                cur_date = datetime.strptime(dates, "%A, %B %d, %Y").date()
        
                if cur_date<start_date:                        
                    run1.run_status='Success'        
                    run1.save()                    
                    exit()
                
                auth=author.objects.filter(author_name=authors)
                
                postcur=list()
                if len(auth)>0:
                    post_cur=post.objects.filter(title=titles,author_id=auth[0].id)
                if len(post_cur)>0:
                    post_cur=post_cur[0]
                    if  flag==0 and post_cur.id in r_posts:
                            file1.write(str(blogs_div1[i]))
                        
                            #print 'updating'                        
                            a=author.objects.get(author_name=authors)                        
                            tit=post.objects.get(title=titles,author_id=a.id)    
                        
        
                            con=post_content.objects.get(id=tit.post_content_id)
                            try:
                                 con.content=contents
                                 con.save()
                            except:
                                 con.content='content not supported'
                                 con.save()
                            try:                        
                                                            
                                con1=additional_information.objects.get(id=tit.comments_id)
                        
                                if comments:
                                    con1.comments=comments                
                                    con1.save()                            
                                
                                else:
                                    #print tit.comments
                                    tit.comments=None
                                    tit.save()
                                    con1.delete()

                            except:
                                con=additional_information()
                                if comments:
                                    con.comments=comments                
                                    con.save()
                                    tit.comments=con    
                                    create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: No comments earlier for post: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)                                    
                                
                    



                            struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                            struct_time1 = datetime.strptime(times, "%I:%M %p")


                            tit.post_date=struct_time.strftime('%Y-%m-%d')
                            tit.post_time=struct_time1.strftime('%H:%M:%S')
                            tit.file_path=file_path
                            tit.save()    
                            ref=refresh_post.objects.get(post_id=post_cur.id)
                            create_log(ERR_CODE['INFO'],"Refreshing the post '"+titles+"' written by: '"+authors+"'.",inspect.stack()[0][3],ex.id,rid)                
                            ref.delete()                
                    
            try:
                next_blog_tag=soup.find("span",id="blog-pager-older-link")
                f = urlopen(next_blog_tag.a['href'],timeout=3)
            except:
                break
                create_log(ERR_CODE['ERROR'],"unable to open the link or link to next page not present",inspect.stack()[0][3],ex.id,rid)
        
            

                
    
    elif ex.extractor_type.extractor_style=='BLOGS IMPORT':
        imp_posts=blogs_import.objects.all()
        start_date=datetime.now().date()
        titles_imp=list()
        for ref in imp_posts:        
            titles_imp.append(ref.title)                    
            if start_date>=ref.post_date:
                start_date=ref.post_date
        while True:
            html_doc= f.read()
            #file1.write(html_doc)
            soup = BeautifulSoup(html_doc, 'html.parser')
            blogs_div1=soup.find_all("div",class_="date-outer")
            for i in range(len(blogs_div1)):
                blog_count=blog_count+1                
                a=author()
                p=post_content()
                c=additional_information()
                pp=post()
                
                my_parser=parseBase(blogs_div1[i],run1.id,args.extractor_id)
                #print 'post:'+str(i+1)
                dates=my_parser.parse_date()
                titles=my_parser.parse_title()
                contents=my_parser.parse_content()
                authors=my_parser.parse_author_name()
                times=my_parser.parse_post_time()
                comments=my_parser.parse_comments()
                flag=0
                if authors=='error' or times=='error':
                    flag=1 
            
                cur_date=datetime.strptime(dates, "%A, %B %d, %Y").date()
            
                if cur_date<start_date:
                    imp=blogs_import.objects.all()
                    #print cur_date
                    #print start_date
                    #print titles
                    for res1 in imp:
                        create_log(ERR_CODE['ERROR'],"Title: '"+res1.title+"' not present before that particular date",inspect.stack()[0][3],ex.id,rid)
                        res1.delete()
                    run1.run_status='Success'        
                    run1.save()    
                
                    exit()
                for k in range(len(titles_imp)):
                    titles_imp[k]=titles_imp[k].replace(u'\xa0', u' ')
                
                titles1=titles.replace(u'\xa0', u' ')
                if  flag==0 and titles1 in titles_imp:
                    file1.write(str(blogs_div1[i]))
                    try:    
                    
                        #print 'updating'                        
                        a=author.objects.get(author_name=authors)                        
                        tit=post.objects.get(title=titles,author_id=a.id)    
    
                        con=post_content.objects.get(id=tit.post_content_id)
                        try:
                                 con.content=contents
                                 con.save()
                        except:
                                 con.content='content not supported'
                                 con.save()
                        try:                        
                                                            
                                con1=additional_information.objects.get(id=tit.comments_id)
                        
                                if comments:
                                    con1.comments=comments                
                                    con1.save()                            
                                
                                else:
                                    #print tit.comments
                                    tit.comments=None
                                    tit.save()
                                    con1.delete()
                         
                        except:
                                con=additional_information()
                                if comments:
                                    con.comments=comments                
                                    con.save()
                                    tit.comments=con    
                                    create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: No comments earlier for post: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)                                    
                                
                    

                        struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                        struct_time1 = datetime.strptime(times, "%I:%M %p")
                        tit.post_date=struct_time.strftime('%Y-%m-%d')
                        tit.post_time=struct_time1.strftime('%H:%M:%S')
                        tit.file_path=file_path
                        tit.save()
                        create_log(ERR_CODE['INFO'],"Refreshing the post '"+titles+"' written by: '"+authors+"'.",inspect.stack()[0][3],ex.id,rid)    
                        create_log(ERR_CODE['INFO'],"post already present for title: '"+titles+"' updaing its details",inspect.stack()[0][3],ex.id,rid)                    
                    except:
                        create_log(ERR_CODE['INFO'],"ObjectDoesNotExist: Earlier there is no posts with title: '"+titles+"'.",inspect.stack()[0][3],ex.id,rid)
                        s=same_post()
                        #print'insertinng'
                        prev_posts=post.objects.filter(title=titles)
                        if len(prev_posts)>0:
                            msg='same title found \nTitle: '+titles+'\nAuthor name: '+authors+'\n previously written by:\n'
                            authors_list=''
                            post_ids=''
                            for ever_post in prev_posts:
                                post_ids=post_ids+str(ever_post.id)+', '
                                au=author.objects.get(id=ever_post.author_id)
                                msg=msg+au.author_name+', '
                                authors_list=authors_list+au.author_name+', '
                            create_log(ERR_CODE['ERROR'],msg,inspect.stack()[0][3],ex.id,rid)
            
                            s.title=titles
                            s.old_author=authors_list
                            s.new_author=authors
                            s.old_post_id=post_ids    
                        try:                     
                            a.author_name=authors
                            a.save()
                        except:
                            #print'trying to insert duplicate author'
                            create_log(ERR_CODE['INFO'],"Integrity error: author already present as '"+authors+"'.",inspect.stack()[0][3],ex.id,rid)
                                
                                     
                        try:
                            p.content=contents
                            p.save()
                        except:
                            p.content='content not supported'
                            p.save()
                                
                    
                        if comments:
                            c.comments=comments                
                            c.save()

                        a=author.objects.get(author_name=authors)
                
                        struct_time = datetime.strptime(dates, "%A, %B %d, %Y")
                        struct_time1 = datetime.strptime(times, "%I:%M %p")
                        pp.title=titles
                        pp.post_date=struct_time.strftime('%Y-%m-%d')
                        pp.post_time=struct_time1.strftime('%H:%M:%S')
                        pp.file_path=file_path
                        pp.author_id=a.id
                        pp.post_content_id=p.id        
                        if c.comments:
                            pp.comments_id=c.id
                        pp.save()
                        if len(prev_posts)>0:
                            s.new_post_id=pp.id
                            s.save()

                    rab=blogs_import.objects.get(title=titles1)
                    rab.delete()        
            try:
                next_blog_tag=soup.find("span",id="blog-pager-older-link")
                f =urlopen(next_blog_tag.a['href'],timeout=3)
            except:    
                create_log(ERR_CODE['ERROR'],"unable to open the link or link to next page not present",inspect.stack()[0][3],ex.id,rid)                    
                break
        run1.run_status='Success'        
        run1.save()    
    
        
    



    return 0

if __name__ == '__main__':
    import sys
    try:
        sys.exit(main(sys.argv))
    except Exception as err:
        print (err)
        run1=run_info.objects.get(id=args.run_id)
        run1.run_status='Failed'        
        run1.save()
        exit()   
      




