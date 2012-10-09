#!/usr/bin/env python3.2
import sys
import os
import re
from ftplib import FTP
from myftpdata import *

#fetch jpg in path1
#ln to path2

def hlinkimage(path1,path2):
	os.chdir(path2)
	for dirpath,dirnames,filenames in os.walk(path1):
		for file in filenames:
			sf=file.split('.')[1]
			print(sf)
			if sf=='jpg':
				fullpath=os.path.join(dirpath,file)
				try:
					os.link(fullpath,file)
				except:
					pass
#comic_list:it's a file which have comic_list and episode
def index_update(argv):
	clist=[('dg',argv),('cat',1)]
	f=open('module/index','r')
	fcombine=open('html/index.html','w')
	tab=r'	'*6
	trtab=r'	'*5
	s=f.read()
	for li in clist:
		addline=''
		fn=li[0]
		n=li[1]
		for i in range(1,n+1):
			if i%20==0:
				name=fn+'%03d'%i+r'.html'
				addline=addline+tab+r'<td><a href="'+name+r'">'+str(i)+r'</a></td>\n'+trtab+r'</tr>\n'+trtab+r'<tr>\n'
			else:
				name=fn+r'%03d'%i+r'.html'
				addline=addline+tab+r'<td><a href="'+name+'">'+str(i)+'</a></td>\n'
		pattern=r'{{'+fn+r'}}'
		s=re.sub(pattern,addline,s)
	fcombine.write(s)
	f.close()
	fcombine.close()
#module: module name
#episode:comic episode, number
def comicsite_update(module,episode):
	htmlname='module/'+module
	f=open(htmlname,'r')
	#head f:format
	fepisode='%03d'%episode
	fprev='%03d'%int(episode-1)
	fnext='%03d'%int(episode+1)
	newf='html/'+module+fepisode+'.html'
	prevf=module+fprev+'.html'
	nextf=module+fnext+'.html'
	newf=open(newf,'w')
	pattern=r'{{episode}}'
	replace=module+str(episode)
	s=re.sub(pattern,replace,f.read())
	pattern=r'{{prev}}'
	replace=r'<a href="'+prevf+r'"><li class="prev">prev</li></a>'
	s=re.sub(pattern,replace,s)
	print(os.path.exists('html/'+nextf))
	if os.path.exists('html/'+nextf)==True:
		pattern=r'{{next}}'
		replace=r'<a href="'+nextf+r'"><li class="next">next</li></a>'
		s=re.sub(pattern,replace,s)
	else:
		s=re.sub(r'{{next}}',r'',s)
	newf.write(s)

#url is ftp url
#valuse is dictionary:key is : 'usr' and 'pwd'(password)
#urldir: object directory in the server
#lcpath:the dir that upload files belong
#mfn:all filename
#sfn:sub filename
def ftpupload(url,values,urldir,lcpath):
	ftp=FTP(url,values['usr'],values['pwd'])
	#if mfn==None and sfn!=None:
	os.chdir(lcpath)
	for dirpath,dirnames,filenames in os.walk(lcpath):
		'''
		for f in filenames:
			try:
				sf=f.split('.')[1]
			except:
				continue
			if sf==sfn:
				print('upload %s'%lcpath+'/'+f)
				try:
					ftp.storbinary('STOR '+urldir+'/'+f,open(f,'rb'))
				except:
					print('upload fail')
				print('finished')
			else:
				pass
		'''
		if dirnames=='image':
			continue
		for f in filenames:
			try:
				if f.split('.')[1]=='css':
					print('upload to:'+'STOR '+urldir+'/css/'+f)
					ftp.storbinary('STOR '+urldir+'/css/'+f,open('css/'+f,'rb'))
				elif f.split('.')[1]=='js':
					print('upload to:''STOR '+urldir+'/'+f)
					ftp.storbinary('STOR '+urldir+'/javascript/'+f,open('javascript/'+f,'rb'))
				elif f.split('.')[1]=='html':
					print('upload to:'+'STOR '+urldir+'/'+f)
					ftp.storbinary('STOR '+urldir+'/'+f,open(f,'rb'))
				else:
					continue
				print('finished')
			except:
				print('upload fail')
	print('all finished')
	'''
	elif mfn!=None:
		os.chdir(lcpath)
		print('connect server')
		try:
			ftp.storbinary('STOR '+urldir+'/'+fn,open(mfn,'rb'))
		except:
			print('upload fail')
		print('finished')

	else:
		print('please input mfn or sfn')
	'''
if __name__=='__main__':
	'''
	#update html
	index_update(int(sys.argv[1]))
	for i in range(1,int(sys.argv[1])+1):
		comicsite_update('dg',i)
	comicsite_update('cat',1)
	'''
	#ftp upload
	myftpdata=myftpdata()
	url=myftpdata.geturl()
	values=myftpdata.getvalues()
	urldir=myftpdata.geturldir()
	lcpath=os.getcwd()+'/html'
	ftpupload(url,values,urldir,lcpath)

