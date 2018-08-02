from django.http import HttpResponse
from blogs.models import author,post,post_content,additional_information,extractor,log,run_info,run_version
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import os
import time
import inspect

ERR_CODE = {'ERROR': 1, 'WARNING': 2,'INFO':3,'DEBUG':4}

def create_log(severity1,msg,fn_name,xid,rid):
		l=log()
		l.run_id=rid
		l.severity_id=severity1
		l.log_message=msg
		l.extractor_id=xid
		l.function_name=fn_name	
		l.save()	


def index(request,ex_id):
	
	ex=extractor.objects.get(id=ex_id)
	str3=len(post.objects.all())
	
	runv=run_version.objects.filter(extractor_id=ex.id,no_of_pages=ex.no_of_pages,no_of_blogs=ex.no_of_blogs,start_page=ex.start_page,start_date=ex.start_date,year=ex.year,end_date=ex.end_date,days_to_extract=ex.days_to_extract,days_to_negate=ex.days_to_negate)
   



	if len(runv)>0 and ex.duplicate_allowed==False and ex.extractor_type.extractor_style!='REFRESH BLOG' and ex.extractor_type.extractor_style!='BLOGS IMPORT':
		r=run_info()
		r.extractor_id=ex_id
		r.run_status='Stopped'
		r.save()
		#create_log(ERR_CODE['INFO'],"Extractor starts now",inspect.stack()[0][3],ex_id,r.id)

	else:
		
		runv2=run_version(no_of_pages=ex.no_of_pages,no_of_blogs=ex.no_of_blogs,start_page=ex.start_page,start_date=ex.start_date,year=ex.year,end_date=ex.end_date,days_to_extract=ex.days_to_extract,days_to_negate=ex.days_to_negate)
		runv2.extractor_id=ex.id		
		runv2.save()		
		r=run_info()
		r.extractor_id=ex_id
		r.run_version_id=runv2.id
		r.run_status='Running'
		r.save()
		str1='python3.6 '+ex.file_path+' '+str(ex_id)+' '+str(r.id)
		create_log(ERR_CODE['INFO'],"Extractor starts now",inspect.stack()[0][3],ex_id,r.id)

		os.system(str1)
	#return HttpResponse(str(str3)+' posts are updated and posts are added  '+'<a href="http://127.0.0.1:8000/admin/blogs/post/" class="button" type="button">click here</button></a>'+' to see the posts')
	
	
	

	
	return HttpResponseRedirect('http://127.0.0.1:8000/admin/blogs/run_info/?id='+str(r.id))

	#return HttpResponse("sdssd")

