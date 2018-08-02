from blogs.models import author,post,post_content,additional_information,extractor,severity,log,same_post,extractor_type,refresh_post,blogs_import,log,run_info,mypost,run_version,json_post
from django import urls
from django.utils.safestring import mark_safe
from django.utils.html import format_html
#from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib import messages, admin
from django.db.models.functions import Lower

VIEW_URL='http://127.0.0.1:8000/extractor/'

class extractorAdmin(admin.ModelAdmin):

    list_display=('extractor_name','ex_style','start_page','no_of_pages','no_of_blogs','start_date','end_date','year','days_to_extract','days_to_negate','duplicate_allowed','get_extractor','get_logs','get_runs','get_versions')
    
    def get_extractor(self, obj):
        run_program_url=VIEW_URL+str(obj.id)
        if obj.no_of_pages!=0:
            obj.no_of_blogs=0    
        return format_html('<a href="%s" class="button" type="button"">RUN</button>' % run_program_url)
    get_extractor.allow_tags = True
    get_extractor.short_description = 'View Logs'
        

    
    def get_logs(self, obj):
        url_for_logs='http://127.0.0.1:8000/admin/blogs/log/?extractor_id='+str(obj.id)    
        return format_html('<a href="%s" class="button" type="button"">GET LOGS</button>' % url_for_logs)

    get_logs.allow_tags = True
    get_logs.short_description = 'View Logs'
    def get_runs(self, obj):
        url_for_logs='http://127.0.0.1:8000/admin/blogs/run_info/?extractor_id='+str(obj.id)    
        return format_html('<a href="%s" class="button" type="button"">Run Info</button>' % url_for_logs)

    get_runs.allow_tags = True
    get_runs.short_description = 'View Runs'
    def get_versions(self, obj):
            url_for_logs='http://127.0.0.1:8000/admin/blogs/run_version/?extractor_id='+str(obj.id)    
            return format_html('<a href="%s" class="button" type="button"">Run Versions</button>' % url_for_logs)

    get_versions.allow_tags = True
    get_versions.short_description = 'View Run Versions'


    def ex_style(self,obj):
        return obj.extractor_type.extractor_style
    ex_style.short_description = 'Extractor style'
    def message_user(self, *args):
        pass
    def save_model(self, request, obj, form, change):
        if obj.no_of_pages != 0 and obj.no_of_blogs!=0:
            obj.no_of_blogs=0
            messages.error(request, "scince no of pages is not equal to '0' no of blogs is setting to zero")
        if obj.extractor_type.extractor_style=='NORMAL':
            obj.start_page=0
            obj.start_date=None
            obj.end_date=None
            if obj.year!=0:
                obj.no_of_blogs=0
                obj.no_of_pages=0
            obj.days_to_extract=0
            obj.days_to_negate=0
        if obj.extractor_type.extractor_style=='INCREMENTAL':
            obj.no_of_blogs=0
            obj.year=0
            obj.start_date=None
            obj.end_date=None
            obj.days_to_extract=0
            obj.days_to_negate=0
        if obj.extractor_type.extractor_style=='DATE RANGE':
            obj.no_of_blogs=0
            obj.no_of_pages=0
            obj.year=0
            obj.start_page=0
            if obj.end_date!=None:
                obj.days_to_extract=0
                obj.days_to_negate=0
    
        if obj.extractor_type.extractor_style=='REFRESH BLOG':
            obj.no_of_blogs=0
            obj.no_of_pages=0
            obj.year=0
            obj.start_page=0
            obj.start_date=None
            obj.end_date=None
            obj.year=0
            obj.days_to_extract=0
            obj.days_to_negate=0
        if obj.extractor_type.extractor_style=='BLOGS IMPORT':
            obj.no_of_blogs=0
            obj.no_of_pages=0
            obj.year=0
            obj.start_page=0
            obj.start_date=None
            obj.end_date=None
            obj.year=0
            obj.days_to_extract=0
            obj.days_to_negate=0
        
            
        messages.success(request,'The extractor "'+obj.extractor_name+'" was changed successfully.')
        super(extractorAdmin,self).save_model(request, obj, form, change)
        
            
    
class postAdmin(admin.ModelAdmin):
    actions=['delete_relatives']
    def delete_relatives(modeladmin, request, queryset):
        for obj in queryset:
            abc=post_content.objects.get(id=obj.post_content_id)
            aut=author.objects.get(id=obj.author_id)
            abc.delete()
            pos=post.objects.filter(author_id=aut.id)
            if len(pos)==0:
                aut.delete()

                
    delete_relatives.short_description = "Delete selected with content and author"    
    list_display=('title','post_date','post_time','file_path','author_link','post_link','comment_link','created_date','last_updated')
    list_filter = ['post_date']
    def get_ordering(self, request):
        return [('-last_updated')]
    def author_link(self, obj):
        return obj.author.author_name
    author_link.short_description = 'Author Name'    

    def post_link(self, obj):
        return obj.post_content
    post_link.short_description = 'Blog'

    def comment_link(self, obj):
        if obj.comments:        
           return obj.comments.comments
        else:
            return None
    comment_link.short_description = 'Comments'
    


class exAdmin(admin.ModelAdmin):
    
    list_display=('id','extractor_style')
    
class severityAdmin(admin.ModelAdmin):
    
    list_display=('id','severity_name')
 
    

    
class sameAdmin(admin.ModelAdmin):
    list_display=('title','old_author','new_author','old_post_id','new_post_id','created')
class refreshAdmin(admin.ModelAdmin):
    list_display=('id','post_id','created_date')
class importAdmin(admin.ModelAdmin):
    list_display=('title','post_date','created_date')

class runverAdmin(admin.ModelAdmin):




    list_display=('id','extractor','start_page','no_of_pages','no_of_blogs','start_date','end_date','year','days_to_extract','days_to_negate')
	

class runAdmin(admin.ModelAdmin):
                
                
    
    list_display=('extractor','run_time','run_status','get_logs','get_versions')
    def get_logs(self, obj):
        url_for_logs='http://127.0.0.1:8000/admin/blogs/log/?run_id='+str(obj.id)    
        return format_html('<a href="%s" class="button" type="button"">Get Logs</button>' % url_for_logs)
    get_logs.allow_tags = True
    get_logs.short_description = 'View Logs'
    def get_versions(self, obj):
        if obj.run_version!=None:
            url_for_logs='http://127.0.0.1:8000/admin/blogs/run_version/?id='+str(obj.run_version.id)    
            return format_html('<a href="%s" class="button" type="button"">Run Version</button>'  % url_for_logs)

    get_versions.allow_tags = True
    get_versions.short_description = 'View Run Versions'
    
class logAdmin(admin.ModelAdmin):
    
    

    list_display=('log_time','extractor_link','run','severity_link','function_name','log_message')
    list_filter=['severity']

    def severity_link(self, obj):
        return obj.severity.severity_name

    severity_link.short_description = 'Severity Name'    
    def extractor_link(self, obj):
        return obj.extractor.extractor_name
    extractor_link.short_description = 'Extractor Name'   
    
class jsonAdmin(admin.ModelAdmin):

    list_display=('json_data',)
    def json_data(self, obj):
        my_str='<a> {{<br>'
        for key in obj.datas:
            my_str=my_str+'%s : %s<br> ' %(key,obj.datas[key])            
        my_str=my_str+'</a>}}'
        return format_html(my_str)
    json_data.allow_tags = True

admin.site.register(blogs_import,importAdmin)
admin.site.register(refresh_post,refreshAdmin)
admin.site.register(same_post,sameAdmin)
admin.site.register(author)
admin.site.register(log,logAdmin)
admin.site.register(extractor_type,exAdmin)
admin.site.register(severity,severityAdmin)
admin.site.register(post,postAdmin)
#admin.site.register(mypost)
admin.site.register(post_content)
admin.site.register(run_info,runAdmin)
admin.site.register(run_version,runverAdmin)
admin.site.register(json_post,jsonAdmin)

admin.site.register(additional_information)
admin.site.register(extractor,extractorAdmin) 




