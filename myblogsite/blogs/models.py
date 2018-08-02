from django.db import models
from django_mysql.models import JSONField

class author(models.Model):
    author_name = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.author_name


class additional_information(models.Model):
    comments = models.TextField()
    def __str__(self):
        return self.comments


class post_content(models.Model):
    content = models.TextField()
    def __str__(self):
        return self.content
    

class post(models.Model):
    author = models.ForeignKey(author, on_delete=models.CASCADE)
    post_content = models.ForeignKey(post_content, on_delete=models.CASCADE)
    comments = models.ForeignKey(additional_information,null=True,blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    post_date=models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    post_time=models.TimeField()
    file_path = models.CharField(max_length=100)
    def __str__(self):
        return self.title
    class Meta:
    	unique_together = ('author', 'title',)
class mypost(post):
	class Meta:
       		proxy = True

	
class extractor_type(models.Model):
		extractor_style=models.CharField(max_length=20)
		def __str__(self):
        		return self.extractor_style
class refresh_post(models.Model):
	post_id=models.IntegerField()
	created_date = models.DateTimeField(auto_now_add=True)
class extractor(models.Model):
	extractor_type=models.ForeignKey(extractor_type, on_delete=models.CASCADE)	
	file_path = models.CharField(max_length=250)
	extractor_name=models.CharField(max_length=100)
	no_of_pages=models.IntegerField(default=0)
	no_of_blogs=models.IntegerField(default=0)
	start_page=models.IntegerField(default=0)
	days_to_extract=models.IntegerField(default=0)
	days_to_negate=models.IntegerField(default=0)
	start_date=models.DateField(null=True,blank=True)
	year=models.IntegerField(default=0)
	end_date=models.DateField(null=True,blank=True)	
	duplicate_allowed=models.BooleanField(default=False)

	def __str__(self):
        	return self.extractor_name

class severity(models.Model):
	severity_name=models.CharField(max_length=10)
	def __str__(self):
        	return self.severity_name
class run_version(models.Model):
	no_of_pages=models.IntegerField()
	no_of_blogs=models.IntegerField()
	start_page=models.IntegerField()
	start_date=models.DateField(null=True,blank=True)
	year=models.IntegerField()
	end_date=models.DateField(null=True,blank=True)	
	days_to_extract=models.IntegerField()
	days_to_negate=models.IntegerField()
	extractor=models.ForeignKey(extractor, on_delete=models.CASCADE)
	def __str__(self):
        	return str(self.id)

class run_info(models.Model):
	extractor=models.ForeignKey(extractor, on_delete=models.CASCADE)
	run_time= models.DateTimeField(auto_now_add=True)
	run_status=models.CharField(max_length=20)
	run_version=models.ForeignKey(run_version,null=True, on_delete=models.CASCADE)
	def __str__(self):
        	return str(self.id)

class log(models.Model):
	severity=models.ForeignKey(severity, on_delete=models.CASCADE)
	log_message=models.CharField(max_length=200)
	log_time= models.DateTimeField(auto_now_add=True)
	extractor=models.ForeignKey(extractor, on_delete=models.CASCADE)
	run=models.ForeignKey(run_info, on_delete=models.CASCADE)
	function_name=models.CharField(max_length=20)

class same_post(models.Model):
	title=models.CharField(max_length=100)
	old_author=models.CharField(max_length=100)
	new_author=models.CharField(max_length=30)
	old_post_id=models.CharField(max_length=30)
	new_post_id=models.IntegerField()
	created= models.DateTimeField(auto_now_add=True)
class blogs_import(models.Model):
	title = models.CharField(max_length=100)
	post_date=models.DateField()
	created_date = models.DateTimeField(auto_now_add=True)
class json_post(models.Model):
    datas =  JSONField()
	




