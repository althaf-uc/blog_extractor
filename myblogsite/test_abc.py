#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sys
import re
from bs4 import BeautifulSoup

import parse_base
from parse_base import parseBase

import pytest

myblogstag='<div class="date-outer"><h2 class="date-header"><span>Tuesday, June 12, 2018</span></h2><div class="date-posts"><div class="post-outer"><div class="post hentry"><a name="7832107410943607536"></a><h3 class="post-title entry-title"><a href="https://pythoninsider.blogspot.com/2018/06/python-370rc1-and-366rc1-now-available.html">Python 3.7.0rc1 and 3.6.6rc1 now available for testing</a></h3><div class="post-header"><div class="post-header-line-1"></div></div><div class="post-body entry-content">Python <b><a href="https://www.python.org/downloads/release/python-370rc1/" target="_blank">3.7.0rc1</a></b> and <b><a href="https://www.python.org/downloads/release/python-366rc1/" target="_blank">3.6.6rc1</a></b> are now available. 3.7.0rc1 is the <b>final planned release preview</b> of <b>Python 3.7</b>, the next feature release of Python. 3.6.6rc1 is the<b> release preview</b> of the next maintenance release of <b>Python 3.6</b>, the current release of Python. Assuming no critical problems are found prior to <b>2018-06-27</b>, the <b>scheduled release dates for 3.7.0 and 3.6.6,</b> no code changes are planned between these release candidates and the final releases. These release candidates are intended to give you the opportunity to test the new features and bug fixes in 3.7.0 and 3.6.6 and to prepare your projects to support them. We strongly encourage you to test your projects and report issues found to <a href="https://bugs.python.org/" target="_blank">bugs.python.org</a> as soon as possible. Please keep in mind that these are preview releases and, thus, their use is not recommended for production environments.  <i>Attention macOS users</i>: there is now a new installer variant for macOS 10.9+ that includes a built-in version of Tcl/Tk 8.6. This variant will become the default version when 3.7.0 releases.  Check it out!<br/><br/>You can find these releases and more information here:<br/><div style="margin: 0px;">   <a href="https://www.python.org/downloads/release/python-370rc1/" target="_blank">https://www.python.org/downloads/release/python-370rc1/</a><br/><div>   <a href="https://www.python.org/downloads/release/python-366rc1/" target="_blank">https://www.python.org/downloads/release/python-366rc1/</a></div><div><div style="margin: 0px;"><div><br/></div></div></div><div></div></div><div style="clear: both;"></div></div><div class="post-footer"><div class="post-footer-line post-footer-line-1"><span class="post-author vcard">Posted by<span class="fn">Ned Deily</span></span><span class="post-timestamp">at<a class="timestamp-link" href="https://pythoninsider.blogspot.com/2018/06/python-370rc1-and-366rc1-now-available.html" rel="bookmark" title="permanent link"><abbr class="published" title="2018-06-12T16:26:00-04:00">4:26 PM</abbr></a></span><span class="post-comment-link"> </span><span class="post-icons"></span><div class="post-share-buttons"><a class="goog-inline-block share-button sb-email" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=email" target="_blank" title="Email This"><span class="share-button-link-text">Email This</span></a><a class="goog-inline-block share-button sb-blog" href="https://www.blogger.comsharepost.gblogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=blog"onclick=\'window.open(this.href, "_blank", "height=270,width=475"); return false;\' target="_blank" title="BlogThis!"><span class="share-button-link-text">BlogThis!</span></a><a class="goog-inline-block share-button sb-twitter" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=twitter" target="_blank" title="Share to Twitter"><span class="share-button-link-text">Share to Twitter</span></a><a class="goog-inline-block share-button sb-facebook" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=facebook" onclick=\'window.open(this.href, "_blank", "height=430,width=640"); return false;\' target="_blank" title="Share to Facebook"><span class="share-button-link-text">Share to Facebook</span></a><a class="goog-inline-block share-button sb-pinterest" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=pinterest" target="_blank" title="Share to Pinterest"><span class="share-button-link-text">Share to Pinterest</span></a><div class="goog-inline-block google-plus-share-container"><g:plusone annotation="inline" href="http://pythoninsider.blogspot.com/2018/06/python-370rc1-and-366rc1-now-available.html" size="medium" source="blogger:blog:plusone" width="300"></g:plusone></div></div></div><div class="post-footer-line post-footer-line-2"><span class="post-labels">Labels:<a href="https://pythoninsider.blogspot.com/search/label/releases" rel="tag">releases</a></span></div><div class="post-footer-line post-footer-line-3"><span class="post-location"></span></div></div></div></div></div></div>'

myblogstag_exception='<div class="date-outer"><h2 class="date-header"><span>Tuesday, June 12, 2018</span></h2><div class="date-posts"><div class="post-outer"><div class="post hentry"><a name="7832107410943607536"></a><h3 class="post-title entry-title"><a href="https://pythoninsider.blogspot.com/2018/06/python-370rc1-and-366rc1-now-available.html">Python 3.7.0rc1 and 3.6.6rc1 now available for testing</a></h3><div class="post-header"><div class="post-header-line-1"></div></div><div class="post-body entry-content">Python <b><a href="https://www.python.org/downloads/release/python-370rc1/" target="_blank">3.7.0rc1</a></b> and <b><a href="https://www.python.org/downloads/release/python-366rc1/" target="_blank">3.6.6rc1</a></b> are now available. 3.7.0rc1 is the <b>final planned release preview</b> of <b>Python 3.7</b>, the next feature release of Python. 3.6.6rc1 is the<b> release preview</b> of the next maintenance release of <b>Python 3.6</b>, the current release of Python. Assuming no critical problems are found prior to <b>2018-06-27</b>, the <b>scheduled release dates for 3.7.0 and 3.6.6,</b> no code changes are planned between these release candidates and the final releases. These release candidates are intended to give you the opportunity to test the new features and bug fixes in 3.7.0 and 3.6.6 and to prepare your projects to support them. We strongly encourage you to test your projects and report issues found to <a href="https://bugs.python.org/" target="_blank">bugs.python.org</a> as soon as possible. Please keep in mind that these are preview releases and, thus, their use is not recommended for production environments.  <i>Attention macOS users</i>: there is now a new installer variant for macOS 10.9+ that includes a built-in version of Tcl/Tk 8.6. This variant will become the default version when 3.7.0 releases.  Check it out!<br/><br/>You can find these releases and more information here:<br/><div style="margin: 0px;">   <a href="https://www.python.org/downloads/release/python-370rc1/" target="_blank">https://www.python.org/downloads/release/python-370rc1/</a><br/><div>   <a href="https://www.python.org/downloads/release/python-366rc1/" target="_blank">https://www.python.org/downloads/release/python-366rc1/</a></div><div><div style="margin: 0px;"><div><br/></div></div></div><div></div></div><div style="clear: both;"></div></div><div class="post-footer"><div class="post-footer-line post-footer-line-1"><span class="post-author vcard">Posted by</span><span class="post-timestamp">at<a class="timestamp-link" href="https://pythoninsider.blogspot.com/2018/06/python-370rc1-and-366rc1-now-available.html" rel="bookmark" title="permanent link"></a></span><span class="post-comment-link"></span><span class="post-icons"></span><div class="post-share-buttons"><a class="goog-inline-block share-button sb-email" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=email" target="_blank" title="Email This"><span class="share-button-link-text">Email This</span></a><a class="goog-inline-block share-button sb-blog" href="https://www.blogger.comsharepost.gblogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=blog"onclick=\'window.open(this.href, "_blank", "height=270,width=475"); return false;\' target="_blank" title="BlogThis!"><span class="share-button-link-text">BlogThis!</span></a><a class="goog-inline-block share-button sb-twitter" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=twitter" target="_blank" title="Share to Twitter"><span class="share-button-link-text">Share to Twitter</span></a><a class="goog-inline-block share-button sb-facebook" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=facebook" onclick=\'window.open(this.href, "_blank", "height=430,width=640"); return false;\' target="_blank" title="Share to Facebook"><span class="share-button-link-text">Share to Facebook</span></a><a class="goog-inline-block share-button sb-pinterest" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=7832107410943607536&amp;target=pinterest" target="_blank" title="Share to Pinterest"><span class="share-button-link-text">Share to Pinterest</span></a><div class="goog-inline-block google-plus-share-container"><g:plusone annotation="inline" href="http://pythoninsider.blogspot.com/2018/06/python-370rc1-and-366rc1-now-available.html" size="medium" source="blogger:blog:plusone" width="300"></g:plusone></div></div></div><div class="post-footer-line post-footer-line-2"><span class="post-labels">Labels:<a href="https://pythoninsider.blogspot.com/search/label/releases" rel="tag">releases</a></span></div><div class="post-footer-line post-footer-line-3"><span class="post-location"></span></div></div></div></div></div></div>'

my_blog_title1='<div class="date-outer"><h2 class="date-header"><span>Wednesday, June 27, 2018</span></h2><div class="date-posts"><div class="post-outer"><div class="post hentry"><a name="2856959947997709845"></a><div class="post-header"><div class="post-header-line-1"></div></div><div class="post-body entry-content">Python <b><a href="https://www.python.org/downloads/release/python-370/" target="_blank">3.7.0</a></b> is now available (and so is <a href="https://www.python.org/downloads/release/python-366/" target="_blank">3.6.6</a>)!<br/><br/><div><div>On behalf of the Python development community and the Python 3.7 release team, we are pleased to announce the availability of <b>Python 3.7.0</b>. Python 3.7.0 is the newest feature release of the Python language, and it contains many new features and optimizations. You can find Python 3.7.0 here:</div><div><a href="https://www.python.org/downloads/release/python-370/">https://www.python.org/downloads/release/python-370/</a></div><div><br/></div><div>Most third-party distributors of Python should be making 3.7.0 packages available soon.</div><div><br/></div><div>See the <a href="https://docs.python.org/3.7/whatsnew/3.7.html" target="_blank">What’s New In Python 3.7</a> document for more information about features included in the 3.7 series.  Detailed information about the changes made in 3.7.0 can be found in its <a href="https://docs.python.org/3.7/whatsnew/changelog.html#python-3-7-0-final" target="_blank">change log</a>.  Maintenance releases for the 3.7 series will follow at regular intervals starting in July of 2018.</div><div><br/></div><div>We hope you enjoy Python 3.7!</div><div><br/></div><div>P.S. We are also happy to announce the availability of <b>Python 3.6.6</b>, the next maintenance release of Python 3.6:</div><div><a href="https://www.python.org/downloads/release/python-366/">https://www.python.org/downloads/release/python-366/</a></div><div><br/></div><div>Thanks to all of the many volunteers who help make Python Development and these releases possible!  Please consider supporting our efforts by volunteering yourself or through organization contributions to the <a href="https://www.python.org/psf/" target="_blank">Python Software Foundation</a>.</div></div><div><br/></div><div style="clear: both;"></div></div><div class="post-footer"><div class="post-footer-line post-footer-line-1"><span class="post-author vcard">Posted by<span class="fn">Ned Deily</span></span><span class="post-timestamp">at<a class="timestamp-link" href="https://pythoninsider.blogspot.com/2018/06/python-3.html" rel="bookmark" title="permanent link"><abbr class="published" title="2018-06-27T20:00:00-04:00">8:00 PM</abbr></a></span><span class="post-comment-link"></span><span class="post-icons"></span><div class="post-share-buttons"><a class="goog-inline-block share-button sb-email" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=2856959947997709845&amp;target=email" target="_blank" title="Email This"><span class="share-button-link-text">Email This</span></a><a class="goog-inline-block share-button sb-blog" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=2856959947997709845&amp;target=blog" onclick=\'window.open(this.href, "_blank", "height=270,width=475"); return false;\' target="_blank" title="BlogThis!"><span class="share-button-link-text">BlogThis!</span></a><a class="goog-inline-block share-button sb-twitter" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=2856959947997709845&amp;target=twitter" target="_blank" title="Share to Twitter"><span class="share-button-link-text">Share to Twitter</span></a><a class="goog-inline-block share-button sb-facebook" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=2856959947997709845&amp;target=facebook" onclick=\'window.open(this.href, "_blank", "height=430,width=640"); return false;\' target="_blank" title="Share to Facebook"><span class="share-button-link-text">Share to Facebook</span></a><a class="goog-inline-block share-button sb-pinterest" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=2856959947997709845&amp;target=pinterest" target="_blank" title="Share to Pinterest"><span class="share-button-link-text">Share to Pinterest</span></a><div class="goog-inline-block google-plus-share-container"><g:plusone annotation="inline" href="http://pythoninsider.blogspot.com/2018/06/python-3.html" size="medium" source="blogger:blog:plusone" width="300"></g:plusone></div></div></div><div class="post-footer-line post-footer-line-2"><span class="post-labels">Labels:<a href="https://pythoninsider.blogspot.com/search/label/releases" rel="tag">releases</a></span></div><div class="post-footer-line post-footer-line-3"><span class="post-location"></span></div></div></div></div></div></div>'



my_blog_title2='<div class="date-outer"><h2 class="date-header"><span>Sunday, February 4, 2018</span></h2><div class="date-posts"><div class="post-outer"><div class="post hentry"><a name="4641934383113037916"></a><div class="post-header"><div class="post-header-line-1"></div></div><div class="post-body entry-content"><span style="background-color: white; color: #111111; font-family: &quot;arial&quot; , &quot;tahoma&quot; , &quot;helvetica&quot; , &quot;freesans&quot; , sans-serif; font-size: 13px; line-height: 17.29px;">Python 3.5.5 and Python 3.4.8 are now available.</span><br><span style="background-color: white; color: #111111; font-family: &quot;arial&quot; , &quot;tahoma&quot; , &quot;helvetica&quot; , &quot;freesans&quot; , sans-serif; font-size: 13px; line-height: 17.29px;"><br></span><span style="background-color: white; color: #111111; font-family: &quot;arial&quot; , &quot;tahoma&quot; , &quot;helvetica&quot; , &quot;freesans&quot; , sans-serif; font-size: 13px; line-height: 17.29px;"><a href="https://www.python.org/downloads/release/python-355/">You can&nbsp;download Python 3.5.5 here,</a>&nbsp;and&nbsp;<a href="https://www.python.org/downloads/release/python-348/">you can&nbsp;download Python 3.4.8 here.</a></span><div style="clear: both;"></div></div><div class="post-footer"><div class="post-footer-line post-footer-line-1"><span class="post-author vcard">Posted by<span class="fn">Larry Hastings</span></span><span class="post-timestamp">at<a class="timestamp-link" href="https://blog.python.org/2018/02/python-3.html" rel="bookmark" title="permanent link"><abbr class="published" title="2018-02-04T19:36:00-05:00">7:36 PM</abbr></a></span><span class="post-comment-link"></span><span class="post-icons"></span><div class="post-share-buttons"><a class="goog-inline-block share-button sb-email" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=4641934383113037916&amp;target=email" target="_blank" title="Email This"><span class="share-button-link-text">Email This</span></a><a class="goog-inline-block share-button sb-blog" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=4641934383113037916&amp;target=blog" onclick="window.open(this.href, &quot;_blank&quot;, &quot;height=270,width=475&quot;); return false;" target="_blank" title="BlogThis!"><span class="share-button-link-text">BlogThis!</span></a><a class="goog-inline-block share-button sb-twitter" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=4641934383113037916&amp;target=twitter" target="_blank" title="Share to Twitter"><span class="share-button-link-text">Share to Twitter</span></a><a class="goog-inline-block share-button sb-facebook" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=4641934383113037916&amp;target=facebook" onclick="window.open(this.href, &quot;_blank&quot;, &quot;height=430,width=640&quot;); return false;" target="_blank" title="Share to Facebook"><span class="share-button-link-text">Share to Facebook</span></a><a class="goog-inline-block share-button sb-pinterest" href="https://www.blogger.com/share-post.g?blogID=3941553907430899163&amp;postID=4641934383113037916&amp;target=pinterest" target="_blank" title="Share to Pinterest"><span class="share-button-link-text">Share to Pinterest</span></a><div class="goog-inline-block google-plus-share-container"><div id="___plusone_0" style="text-indent: 0px; margin: 0px; padding: 0px; background: transparent; border-style: none; float: none; line-height: normal; font-size: 1px; vertical-align: baseline; display: inline-block; width: 32px; height: 20px;"><iframe ng-non-bindable="" frameborder="0" hspace="0" marginheight="0" marginwidth="0" scrolling="no" style="position: static; top: 0px; width: 32px; margin: 0px; border-style: none; left: 0px; visibility: visible; height: 20px;" tabindex="0" vspace="0" width="100%" id="I0_1532680583914" name="I0_1532680583914" src="https://apis.google.com/u/0/se/0/_/+1/fastbutton?usegapi=1&amp;source=blogger%3Ablog%3Aplusone&amp;size=medium&amp;width=300&amp;annotation=inline&amp;hl=en&amp;origin=https%3A%2F%2Fblog.python.org&amp;url=http%3A%2F%2Fpythoninsider.blogspot.com%2F2018%2F02%2Fpython-3.html&amp;gsrc=3p&amp;jsh=m%3B%2F_%2Fscs%2Fapps-static%2F_%2Fjs%2Fk%3Doz.gapi.en.BtYqSUsc058.O%2Fam%3DwQ%2Frt%3Dj%2Fd%3D1%2Frs%3DAGLTcCNOI37dC7_PJcPPGxvKQtW4KDVetg%2Fm%3D__features__#_methods=onPlusOne%2C_ready%2C_close%2C_open%2C_resizeMe%2C_renderstart%2Concircled%2Cdrefresh%2Cerefresh&amp;id=I0_1532680583914&amp;_gfid=I0_1532680583914&amp;parent=https%3A%2F%2Fblog.python.org&amp;pfname=&amp;rpctoken=19088511" data-gapiattached="true" title="G+"></iframe></div></div></div></div><div class="post-footer-line post-footer-line-2"><span class="post-labels"></span></div><div class="post-footer-line post-footer-line-3"><span class="post-location"></span></div></div></div></div></div></div>'





myblogstag1=BeautifulSoup(myblogstag, 'html.parser')
myblogstag_exception=BeautifulSoup(myblogstag_exception, 'html.parser')
my_blog_title1=BeautifulSoup(my_blog_title1, 'html.parser')
my_blog_title2=BeautifulSoup(my_blog_title2, 'html.parser')

my_parser=parseBase(myblogstag1,1,2)
my_parser_exception=parseBase(myblogstag_exception,1,2)	
my_parser_title1=parseBase(my_blog_title1,1,2)
my_parser_title2=parseBase(my_blog_title2,1,2)


def dummylog(a,b,c,d):
	pass

def test_parse_author_name(monkeypatch):

	
	monkeypatch.setattr(parseBase, "create_log", dummylog)


	assert my_parser.parse_author_name()=='Ned Deily'


def test_parse_title(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser.parse_title()=='Python 3.7.0rc1 and 3.6.6rc1 now available for testing'

def test_parse_title_1(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser_title1.parse_title()=='Python 3.7.0 is now available (and so is 3.6.6)!'

def test_parse_title_2(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser_title2.parse_title()=='Python 3.5.5 and Python 3.4.8 are now available.'

def test_parse_author_exception(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser_exception.parse_author_name()=='error'



def test_parse_date(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser.parse_date()=='Tuesday, June 12, 2018'

def test_parse_time(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser.parse_post_time()=='4:26 PM'
def test_parse_time_exception(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser_exception.parse_post_time()=='error'


def test_parse_comments(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser.parse_comments()==''
def test_parse_comments_exception(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser_exception.parse_comments()=='error'

def test_parse_contents(monkeypatch):
	monkeypatch.setattr(parseBase, "create_log", dummylog)
	assert my_parser.parse_content().replace('\'\'',' ').strip().replace('\'','')=="Python''3.7.0rc1''and''3.6.6rc1''are now available. 3.7.0rc1 is the''final planned release preview''of''Python 3.7'', the next feature release of Python.3.6.6rc1 is the''release preview''of the next maintenance release of''Python 3.6'', the current release of Python. Assuming no critical problems are found prior to''2018-06-27'', the''scheduled release dates for 3.7.0 and 3.6.6,''no code changes are planned between these release candidates and the final releases.These release candidates are intended to give you the opportunity to test the new features and bug fixes in 3.7.0 and 3.6.6 and to prepare your projects to support them. We strongly encourage you to test your projects and report issues found to''bugs.python.org''as soon as possible. Please keep in mind that these are preview releases and, thus, their use is not recommended for production environments.''AttentionmacOS users'': there is now a new installer variant for macOS 10.9+ that includes a built-in version of Tcl/Tk 8.6. This variant will become the default version when 3.7.0 releases. Check it out!''You can find these releases and more information here:''https://www.python.org/downloads/release/python-370rc1/''https://www.python.org/downloads/release/python-366rc1/ ".replace('\'\'',' ').strip()



	
