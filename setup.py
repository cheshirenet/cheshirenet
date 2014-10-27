from distutils.core import setup
import distutils.cmd
import sys,os,unicodedata
from distutils.command.build import build as _build

class build(_build):
	def run(self):
		for t in ["female","male","surname"]:
				self.genmarkov("namegen",t)
		_build.run(self)
	def genmarkov(self,dirname,varname):
		infile=open(dirname+"/"+varname+".names")
		outfile=open(dirname+"/"+varname+"_hash.py","w")
		self.x={}
		for line in infile: 
			l=unicodedata.normalize("NFKD",line.strip().decode("utf-8")).encode("ascii","ignore").lower()
			a = ' ';
			b = l[0]
			for i in l[1:]:
				self.addchar(a,b,i)
				a=b
				b=i
			self.addchar(a,b,' ')
		print >>outfile,varname, '=',repr(self.x)
	def addchar(self,a,b,c):
		if not a in self.x:
			self.x[a]={}
		if not b in self.x[a]:
			self.x[a][b]=""
		self.x[a][b]+=c
class MyTests(distutils.cmd.Command):
	user_options=[]
	def initialize_options(self):
		pass
	def finalize_options(self):
		pass
	def run(self):
		self.run_command("build")
		import glob
		lib=glob.glob(os.getcwd()+"/build/*")[0]
		sys.path.insert(0,lib)
		print >>sys.stderr,"Using %s for tested modules"%(lib)
		import unittest
		result=unittest.TextTestResult(sys.stdout,True,True)
		suite= unittest.defaultTestLoader.discover("./tests")
		print "Discovered %d test cases"%suite.countTestCases()
		result.buffer=True
		suite.run(result)
		print ""
		if not result.wasSuccessful():
			if len(result.errors):
				print "============ Errors disovered ================="
				for r in result.errors:
					print r[0],":",r[1]
			
			if len(result.failures):
				print "============ Failures disovered ================="
				for r in result.failures:
					print r[0],":",r[1]
			sys.exit(1)
		else:
			print "All tests successful"

setup(
	name="cheshirenet",
	version="0.1.0",
	description="Network without a medium is like a smile without a cat",
	author="Victor Wagner",
	author_email="vitus@wagner.pp.ru",
	url="https://github.com/ctypescrypto/ctypescrypto",
	packages=["cheshirenet","namegen"],
	cmdclass={"test":MyTests,"build":build}
)

