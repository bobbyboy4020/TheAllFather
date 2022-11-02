#The All Together
from datetime import date
setAutoWaitTimeout(20)    #give program time to wait for the slow report program
Settings.MoveMouseDelay = 0.0   #mouse instant movement
reportSaveLoc = r"C:\Users\hkarn\Documents\PDF\FreshReports\Nov 1 - Nov 18"
jobCodes = []
choice = ""

def CopyClip():
	type('c', KeyModifier.CTRL)
	sleep(0.6)
	return Env.getClipboard() #copies clipboard to return
def CopyJobCodes():
	#grabs assigned jobs from Tracking
	jobCodes = []
	clicker = Screen(1).find(Pattern("JobsCheck.png").similar(0.65).targetOffset(-82,72)) #Location on second monitor to click 3 times to select all jobs in current query 
	click(clicker)
	click(clicker)
	click(clicker)
	copy = CopyClip()
	jobsRB = copy.split('\n') #split on new line, seperating each job from one another
	sleep(1)
	for seg in jobsRB : #get only the job code without the job reps initials
		if(seg.find("-") > 0):  #find point where first - is, which is after the rep, also no empty strings
			i = seg.find("-")   #+1 is to get to first character of jobcode, +11 gets to the last character
			  					#save all jobs to an array, use array later for each job 
			if("groups" in seg.lower()):
				jobCodes.append(seg[(i+1):(i+11)]+"-groups") #finds groups in notes, adds extra to codes for groups
			else:
				jobCodes.append(seg[(i+1):(i+11)])		   #if no groups, default
	return jobCodes
def JobLocation(): #works good, not used too often
	jobLoc = ""
	wait("FileBrowserBar.png")
	click("FileBrowserBar.png")
	sleep(0.2)
	jobLoc = CopyClip()
	return jobLoc
def jobFinder(code): #works good
	reg = "" #checks in edge entry for job type of current job
	clickLoc = ""
	jobbs = Location(find("JobListEE.png").getTarget())
	reg = Region(jobbs.getX()-39, jobbs.getY()+21, 50, 100)
	if(code == "E231"):
		wait(Pattern("E231.png").exact())
		clickLoc = Location(reg.find(Pattern("E231.png").exact()).getTarget())
	elif(code == "H231"):
		wait(Pattern("H231.png").exact())
		clickLoc = Location(reg.find(Pattern("H231.png").exact()).getTarget()) 
	elif(code == "E232"):
		wait(Pattern("E232.png").exact())
		clickLoc = Location(reg.find(Pattern("E232.png").exact()).getTarget()) 
		
	return clickLoc
def PrintPopUp():
	reg = Region(220,115,1480,850)
	while True:
		if(reg.exists(Pattern("SavePDF-FileAs.png").exact())):
			break
		else:
			if(Screen(0).exists(Pattern("popUpSaveAs.png").similar(0.69))):
				Screen(0).click(Pattern("popUpSaveAs.png").similar(0.69))
			elif(Screen(0).exists(Pattern("BSave.png").similar(0.69))):
				Screen(0).click(Pattern("BSave.png").similar(0.69))

def FreshReporting(jobCodes):
	def PrintReport(magReg):
		locPrint = ""
		if(magReg.exists("PrintFRB1.png")):
			locPrint = magReg.find("PrintFRB1.png")
		elif(magReg.exists("PrintFRB2.png")):
			locPrint = magReg.find("PrintFRB2.png")
		return locPrint
	def MagReport(magReg):
		locMag = ""
		if(magReg.exists(Pattern("MagGlass1.png").similar(0.72))):
			locMag = magReg.find(Pattern("MagGlass1.png").similar(0.72))
		elif(magReg.exists(Pattern("MagGlass2.png").similar(0.60))):
			locMag = magReg.find(Pattern("MagGlass2.png").similar(0.60))
		return locMag
	def GetMagReg(): #used to find magnifying glass more easily, and printer icon
		wait("FRB_Bar.png")
		mag = Location(find("FRB_Bar.png").getTarget())
		magReg = Region(mag.getX()-88, mag.getY()+17, 98,18)
		return magReg
	def FRBLaunch(): #gets FRB to main page
		doubleClick("FreshRepo.png")
		wait("FieldTicket(2018).png") 
		click("FieldTicket(2018).png")
		click("LaunchButton.png")
		doubleClick("FieldTicket(2018)2.png")
		sleep(4)
		wait("PreviewFRB.png")
		click("PreviewFRB.png")
	def FrbFirstHalf(job, frbApp, locMag, frbReg): #starts loading job in FRB
		frbApp.focus()
		setAutoWaitTimeout(50)
		sleep(2)
		click(locMag)
		while True:
			if(frbReg.exists(Pattern("FRBmagniGlass.png").exact())):
				break
			else:
				click(locMag)
		sleep(1)
		paste(job[0:10])
		sleep(3)
		while True:
			if(exists(Pattern("Main.png").exact())):
				break
			else:
				pass
		sleep(3)
		type(Key.ENTER)
		while True:
			if(frbReg.exists(Pattern("FRBmagniGlass.png").similar(0.86))):
				type(Key.ENTER)
			else:
				break
	def FrbSecondHalf(job, frbApp, first, locPrint, frbReg): #starts printing process
		frbApp.focus()
		setAutoWaitTimeout(50)
		wait("frbMain.png")
		sleep(4)
		click(locPrint)
		sleep(0.2)
		while True:
			if(frbReg.exists("AdobePrinterFRB.png")):
				break
			else:
				click(locPrint)
				sleep(0.4)
		sleep(1)
		type('n')
		sleep(0.2)
		type('a')      #set printer to Adobe to PDF, and save copy of it to harddrive
		frbReg.click("FRB_OK.png")
		PrintPopUp()
		sleep(1)
		wait(Pattern("FileBrowserCheck.png").targetOffset(306,-13))
		if(first):
			frbReg.click(Pattern("FileBrowserBarLeft.png").targetOffset(526,0)) #place where field tickets are saved on the first file, after first it defaults
			paste(reportSaveLoc)
			type(Key.ENTER)
			sleep(0.2)
			frbReg.click(Pattern("FileBrowserCheck.png").targetOffset(306,-13))
		sleep(1)
		paste(job[0:10]+" Field Ticket.pdf")
		frbReg.click("FRBSavePDF.png")
		sleep(2.5)
		click(locPrint) #Print button press
		sleep(0.5)
		while True:
			if(frbReg.exists("AdobePrinterFRB.png")):
				break
			else:
				click(locPrint)
				sleep(1)
		sleep(0.5)
		frbReg.click(Pattern("xxProperties.png").similar(0.71).targetOffset(-51,-4))
		printer = 0
		if(printer == 0):
			frbReg.click("HPPageWide.png")
		elif(printer == 1):
			frbReg.click("HPC0printer.png")
		frbReg.click(Pattern("Printallpage.png").targetOffset(-9,21))
		sleep(2)
	def FreshReportMulti(jobCodes): #to print multiple reports at the same time
		frbApp = []
		first = True
		frbReg = Region(220,115,1480,850) #region of the fresh report builder Window
		locMag = ""
		locPrint = ""
		if(len(jobCodes) > 2): #launches 3 or less FRB apps
			for i in range(3):
				FRBLaunch()
		else:
			for i in range(len(jobCodes)):
				FRBLaunch()
		apps = App.getApps()
		for app in apps: #find the apps for frb and lets us use them specifically later
			if(app.name == "FreshReportBuilder.exe"):
				frbApp.append(app)
		magReg = GetMagReg() #area around where magnifying glass and print should be
		locMag = MagReport(magReg) #location of magnifying glass so we dont have to find it everytime
		locPrint = PrintReport(magReg)
		for i in range(0, len(jobCodes), 3):
			FrbFirstHalf(jobCodes[i], frbApp[0], locMag, frbReg)
			try:
				FrbFirstHalf(jobCodes[i+1], frbApp[1], locMag, frbReg)
			except:
				try:
					frbApp[1].close()
				except:
					pass
			try:
				FrbFirstHalf(jobCodes[i+2], frbApp[2], locMag, frbReg)
			except:
				try:
					frbApp[2].close()
				except:
					pass
			
			FrbSecondHalf(jobCodes[i], frbApp[0], first, locPrint, frbReg)
			first = False
			try:
				FrbSecondHalf(jobCodes[i+1], frbApp[1], first, locPrint, frbReg)
			except:
				pass
			try:
				FrbSecondHalf(jobCodes[i+2], frbApp[2], first, locPrint, frbReg)
			except:
				pass
		frbApp[0].close()
		try:	
			frbApp[1].close()
			frbApp[2].close()
		except:
			pass
		popup("FRB has completed.")
	FreshReportMulti(jobCodes)

def Retaking(jobCodes):
	def CreateJobRetake(codes, eeApp, eeReg): #open job
		setAutoWaitTimeout(180)
		eeApp.focus()
		clickLoc = ""
		sleep(1)
		eeReg.wait("JobsEE.png")
		sleep(1)
		eeReg.click("JobsEE.png")
		sleep(1)
		eeReg.click(Pattern("JobSelectEE.png").targetOffset(76,-14))
		for i in range(3):
			type(Key.BACKSPACE)
		sleep(0.2)
		paste(codes[0])
		sleep(0.2)
		type(Key.ENTER)
		sleep(1)
		eeReg.wait("ViewAssociation.png")
		eeReg.click("ViewAssociation.png")
		sleep(0.25)
		clickLoc = jobFinder(codes[1])
		doubleClick(clickLoc)
	def MakeExe(codes, eeApp): #makes exe
		eeApp.focus()
		jobLoc = "Q:\\Jobs23\\"+codes[0]+"\\"+codes[1]
		sleep(0.5)
		regLoc = Location(find("File-Edit-EE.png").getTarget())
		regExe = Region(regLoc.getX()+25,regLoc.getY()+5, 150,100)
		eeApp.focus()
		keyDown(Key.ALT)
		type('j')
		while True:
			if(regExe.exists(Pattern("EXECheck.png").similar(0.76))):
				break
			else:
				eeApp.focus()
				keyDown(Key.ALT)
				type('j')
		sleep(0.15)
		type('e')
		sleep(0.15)
		type('e')
		sleep(0.15)
		type('r')
		sleep(0.15)
		keyUp()
		
		sleep(0.5)
		type(codes[2])
		sleep(0.2)
		type(Key.ENTER)
	def SaveCardsRetake(codes, eeApp, first, eeReg, sortType): #after exe made, make subject not photographed and save to jobs folder
		jobLoc = "Q:\\Jobs23\\"+codes[0]+"\\"+codes[1]
		eeApp.focus()
		sleep(0.5)
		setAutoWaitTimeout(30)
		eeReg.wait(Pattern("EXE-FirstCheck.png").targetOffset(2,51))
		eeReg.click(Pattern("EXE-FirstCheck.png").targetOffset(2,51))#click ok
		eeReg.wait("EXE-SecondCheck.png")
		sleep(1)
		eeReg.click(Pattern("EXE-SecondCheck.png").targetOffset(22,68))#clicks ok
		sleep(0.5)
		eeReg.click("FindSubjectEE.png")
		sleep(0.1)
		eeReg.click(Pattern("ImageLoadedEE.png").targetOffset(24,6))
		sleep(0.1)
		eeReg.click("FindSubjectButton.png")
		sleep(0.5)
		eeReg.click("SortButtonEE.png")         #sort job before exe making
		eeReg.wait("SortingSquare.png")
		sleep(0.1)
		if ("h" in sortType):
			eeReg.click("SortingSquare.png")
		elif ("g" in sortType):
			eeReg.click(Pattern("SortingSquare.png").targetOffset(0,-31))
		elif ("a" in sortType):
			eeReg.click(Pattern("SortingSquare.png").targetOffset(0,31))
		else:
			if(codes[1]=="E231"):
				eeReg.click("SortingSquare.png")
			elif(codes[1]=="H231"):
				eeReg.click(Pattern("SortingSquare.png").targetOffset(0,-32))
			elif(codes[1]=="E232"):
				eeReg.click("SortingSquare.png")
		sleep(0.5)
		eeReg.click("ReportsPage1.png")
		sleep(0.25)
		eeReg.click(Pattern("ReportsName.png").targetOffset(154,39))
		sleep(0.2)
		paste(r"Q:\Edge\Lab\Reports\Camera Cards\School\Subjects Not Photographed - Alpha.rtm") #sets to reshoot
		sleep(0.2)
		eeReg.click(Pattern("PrintCardType.png").targetOffset(53,-3)) #clicks cameracards
		sleep(0.25)
		type('v', KeyModifier.ALT)
		sleep(0.25)
		eeReg.wait("PrintPreviewCards.png")
		sleep(1)
		eeReg.click(Pattern("PrintPreviewCards.png").targetOffset(-37,27))
		while True:
			if(exists("OKButtonEE.png")):
				break
			else:
				eeReg.click(Pattern("PrintPreviewCards.png").targetOffset(-37,27))
				sleep(0.2)
		sleep(0.2)
		if(first):
			eeReg.wait("AdobePrinterFRB.png")
			eeReg.click("AdobeDropdownFRB.png")
			type('a')	
			eeReg.click("SelectAdobePDF.png")
			sleep(0.2)
		eeReg.click("OKButtonEE.png")
		sleep(0.4)
		PrintPopUp()
		sleep(1)
		paste(jobLoc)
		sleep(0.2)
		type(Key.ENTER)
		sleep(0.5)
		type('a', KeyModifier.CTRL)
		sleep(0.5)
		paste(codes[0] + "-" + codes[1] + "-" + codes[2] + " Subjects Not Photographed - Alpha.pdf")
		sleep(0.5)
		type(Key.ENTER)
		sleep(1)
		regon = Region(0,0,150,150)
		setAutoWaitTimeout(10)
		try:
			regon.wait("ADOBEprintCCards.png")#Wait for the camera cards to start printing
			while regon.exists("ADOBEprintCCards.png"): #while printing exists, stay printing
				sleep(1)
		except:
			sleep(1)
		eeApp.focus()
		setAutoWaitTimeout(15)  
		sleep(1)
		eeReg.click(Pattern("PrintPreviewCards.png").targetOffset(459,-1))
		sleep(2)
	def Retaker(jobCodes):
		#Retakes work by doing 3 exes at the same time, because they take a long time
		#To make it auto, we launch 3 Edge Entrys, and run 3 jobs at the same time to start, 
		#we run through the exe maker 3 times first after that, 
		#go to the first job started and wait for the confirmation window either do cards for job that finished exe, 
		#or wait for other 2 to finish so no popups mess with the run
		
		eeApp = [] #array for Edge Entry Apps
		codes = [] #array for split job codes
		apps = ""
		sorts = ""
		for i in range(len(jobCodes)): #gets info from table into managable split entries
			jobCodes[i].upper()
			codes.append(jobCodes[i].split("-"))
		#opens edge entries
		if(len(jobCodes) > 2):
			for i in range(3):
				doubleClick("edgeIcon.png")
				wait("edgeOpener.png")
				click(Pattern("edgeOpener.png").targetOffset(1,33))
				sleep(0.5)
		else:
			for i in range(len(jobCodes)):
				doubleClick("edgeIcon.png")
				wait("edgeOpener.png")
				click(Pattern("edgeOpener.png").targetOffset(1,33))
				sleep(0.5)
		apps = App.getApps()
		for app in apps:
			if(app.name == "Edge Entry.exe"):
				eeApp.append(app)
		#all 3 edge entries are in an array that can be accessed

		eeReg = Region(390,115,1140,844) #region of the Edge Entry Window default size
		for i in range(0, len(jobCodes), 3): #goes through intervals of 3, and does jobs if there are 3 entries left in the array
			exeMake = ""
			exeGood = ""
			try:
				exeMake = popAsk("Make exes? " + str(jobCodes[i]) + ", " + str(jobCodes[i+1]) + ", " + str(jobCodes[i+2]))
				sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n" + str(jobCodes[i]) + ", " + str(jobCodes[i+1]) + ", " + str(jobCodes[i+2]))
			except:
				try:
					exeMake = popAsk("Make exes? " + str(jobCodes[i]) + ", " + str(jobCodes[i+1]))
					sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n" + str(jobCodes[i]) + ", " + str(jobCodes[i+1]))
				except:
					try:
						exeMake = popAsk("Make exes? " + str(jobCodes[i]))
						sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n" + str(jobCodes[i]))
					except:
						exeMake = popAsk("Make exes?")
						sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n")
			sorts = sorts.split(",") #h for homeroom, g for grade, a for alpha
			if(exeMake):
				CreateJobRetake(codes[i], eeApp[0], eeReg)
				MakeExe(codes[i], eeApp[0])
				try: #tries to create and make exe, if not, close window
					CreateJobRetake(codes[i+1], eeApp[1], eeReg) 
					MakeExe(codes[i+1], eeApp[1])
				except:
					try:
						eeApp[1].close()
					except:
						pass
				try:
					CreateJobRetake(codes[i+2], eeApp[2], eeReg)
					MakeExe(codes[i+2], eeApp[2])
				except:
					try:
						eeApp[2].close()
					except:
						pass
			#make exe and switch to next job to make exe, after all 3 exes are started, 
			#goto job 1 and wait for confirmation window
			exeGood = popAsk("Exe made?")
			if(exeGood):
				SaveCardsRetake(codes[i], eeApp[0], True, eeReg, sorts[0])
				try:
					SaveCardsRetake(codes[i+1], eeApp[1], False, eeReg, sorts[1])
				except:
					try:
						SaveCardsRetake(codes[i+1], eeApp[1], False, eeReg, "")
					except:
						pass
				try:
					SaveCardsRetake(codes[i+2], eeApp[2], False, eeReg, sorts[2])
				except:
					try:
						SaveCardsRetake(codes[i+2], eeApp[2], False, eeReg, "")
					except:
						pass
			try:
				if(codes[i][3] == "groups"):
					eeApp[0].focus()
					popup(jobCodes[i] + " has groups")
			except:
				pass
			try:
				if(codes[i+1][3] == "groups"):
					eeApp[1].focus()
					popup(jobCodes[i+1] + " has groups")
			except:
				pass
			try:
				if(codes[i+2][3] == "groups"):
					eeApp[2].focus()
					popup(jobCodes[i+2] + " has groups")
			except:
				pass


		popup("retakes all done :^)")
		eeApp[0].close()
		try:
			eeApp[1].close()
			eeApp[2].close()
		except:
			pass
	Retaker(jobCodes)

def Originaling(jobCodes):
	def CreateJobOriginal(codes, eeApp, eeReg): #will create job if not already, and open email
		eeApp.focus()
		clickLoc = ""
		sleep(1)
		eeReg.click("JobsEE.png")
		eeReg.click(Pattern("JobSelectEE.png").targetOffset(76,-14))
		for i in range(3):
			type(Key.BACKSPACE)
		sleep(0.2)
		paste(codes[0])
		sleep(0.2)
		type(Key.ENTER)
		sleep(1)
		eeReg.wait("ViewAssociation.png")
		eeReg.click("ViewAssociation.png")
		sleep(0.5)
		clickLoc = jobFinder(codes[1])
		doubleClick(clickLoc)
		setAutoWaitTimeout(5)
		if(eeReg.exists("CreateJobEE.png")):
			eeReg.click("CreateJobEE.png")
			sleep(2)
		
		try:
			outApp = App(r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE")
			outApp.focus()
			wait(Pattern("OutlookSearchBar.png").similar(0.62))
			click(Pattern("OutlookSearchBar.png").similar(0.66).targetOffset(221,0))
			for i in range(4):
				type(Key.BACKSPACE)
			sleep(0.1)
			paste(codes[0])
			sleep(0.1)
			type(Key.ENTER)
			sleep(1)		
		except:
			sleep(1)
		eeApp.focus()
		type('e', KeyModifier.CTRL)
		wait("FileBrowserBarLeft.png")
	def DatabaseTime(eeApp):
		#Imports asciiclean into database onto subjects table of current job
		ascii = ""
		dataBase = ""
		jobLoc = JobLocation()
		sleep(0.1)
		click("asciicleanCheck.png")
		sleep(0.1)
		type(Key.F2)
		ascii = CopyClip()
		sleep(0.2)
		dataBase = jobLoc+"\\"+ascii+".xlsx"
		doubleClick("DataFolderCheck.png")
		wait("databaseEONE.png")
		click("databaseEONE.png") #creates copy and renames copy to todays date
		sleep(0.1)
		rightClick("databaseEONE.png")
		click(Pattern("databaseCopy.png").targetOffset(0,13))
		sleep(0.25)
		rightClick()
		click(Pattern("databasePaste.png").targetOffset(-33,-10))
		sleep(0.5)
		type(Key.F2)
		sleep(0.2)
		today = date.today() #str is to string, zfill is to have int as always 2 characters, ex 05
		paste("eone HRK " + str(today.month).zfill(2)+str(today.day).zfill(2))
		sleep(0.2)
		type(Key.ENTER)
		sleep(0.3)
		doubleClick("databaseEONE.png") #open database
		sleep(0.5)
		type(Key.LEFT)
		sleep(0.5)
		type(Key.ENTER)
		sleep(0.2)
		click("AccessExternalDataCheck.png")
		sleep(0.2)
		while True:
			if(exists("AccessNewDataSource.png")):
				break
			else:
				click("AccessExternalDataCheck.png") #start loading data segment
		sleep(0.1)
		click("AccessNewDataSource.png")
		while True:
			if(exists("databaseDataClick.png")):
				break
			else:
				click("AccessNewDataSource.png") #start loading data segment
		sleep(0.1)
		type('f')
		sleep(0.1)
		type('x')
		sleep(0.1)
		type('a',KeyModifier.CTRL)
		sleep(0.1)
		paste(dataBase)  #location of asciiclean
		sleep(0.1)
		type(Key.TAB)
		sleep(0.1)
		type(Key.TAB)
		sleep(0.1)
		type(Key.DOWN)
		sleep(0.1)
		type(Key.TAB)
		sleep(0.1) #maybe instead, type('v'), click on Subjects
		type('s')
		sleep(0.1)
		for i in range(6):
			type(Key.DOWN)
			sleep(0.1)
		sleep(0.4)
		type(Key.ENTER)
		sleep(0.1)
		type(Key.TAB)
		sleep(0.1)
		type(Key.ENTER)
		sleep(0.1)
		setAutoWaitTimeout(20)
		wait("ImportSpreadsheetWizard.png")
		click("ImportSpreadsheetWizard.png")
		for i in range(3):
			type(Key.ENTER)
			sleep(0.2)
		sleep(1.5)
		type(Key.ESC)
		sleep(0.5)
		type(Key.F4, KeyModifier.ALT) 
		sleep(0.5)
		click(Pattern("FileBrowserTopLeftCheck.png").targetOffset(720,-17))
		sleep(0.5)
	def SaveCardsOriginal(codes, eeApp, eeReg):
		eeApp.focus()
		sortType = input("what is sort type, gr, hr, al?")
		sortType.lower()
		eeReg.click("ViewAssociation.png")
		sleep(0.2) #make sure 2023 job is selected
		clickLoc = jobFinder(codes[1])
		doubleClick(clickLoc)
		sleep(0.5)
		type('e', KeyModifier.CTRL)
		jobLoc = JobLocation()
		click(Pattern("FileBrowserTopLeftCheck.png").targetOffset(720,-17))
		sleep(0.2) 
		eeReg.click("SubjectsEE.png")
		sleep(1.5)
		
		sleep(0.5)
		regLoc = Location(find("File-Edit-EE.png").getTarget())
		regExe = Region(regLoc.getX()+25,regLoc.getY()+5, 150,100)
		keyDown(Key.ALT)
		type('j')  
		while True:
			if(regExe.exists(Pattern("EXECheck.png").similar(0.76))):
				break
			else:
				 keyDown(Key.ALT)
				 type('j')     
		sleep(0.15)
		type('e')
		sleep(0.15)
		type('e')
		sleep(0.15)
		type('o')
		sleep(0.15)
		keyUp()
		eeApp.focus()
		setAutoWaitTimeout(600)  
		if(codes[2]=="1"):
			type(Key.ENTER)
		while True:
			if(eeReg.exists("EXE-FirstCheck.png")):
				break
			else:
				sleep(1)
		sleep(2)
		setAutoWaitTimeout(30)
		eeReg.click(Pattern("EXE-FirstCheck.png").targetOffset(2,51))#click ok
		eeReg.wait("EXE-SecondCheck.png") 
		sleep(2)
		eeReg.click(Pattern("EXE-SecondCheck.png").targetOffset(22,68))#clicks ok
		sleep(1)	
		eeReg.click("SortButtonEE.png")         #sort job before exe making
		sleep(0.5)
		while True:
			if(eeReg.exists("quickSort.png")):
				break
			else:
				eeReg.click("SortButtonEE.png")  
				sleep(0.2)
		if ("h" in sortType):
			eeReg.click("quickSort.png")
		elif ("g" in sortType):
			eeReg.click(Pattern("quickSort.png").targetOffset(0,-30))
		elif ("a" in sortType):
			eeReg.click(Pattern("quickSort.png").targetOffset(0,30))
		else:
			if(codes[1]=="E231"):
				eeReg.click("quickSort.png")
			elif(codes[1]=="H231"):
				eeReg.click(Pattern("quickSort.png").targetOffset(0,-30))
		sleep(0.5)
		eeReg.click("ReportsPage1.png")
		sleep(0.5)
		eeReg.click(Pattern("ReportsName.png").targetOffset(154,39))
		sleep(0.2)
		paste("Q:\\Edge\\Lab\\Reports\\Camera Cards\\School\\ccard SAP (Standard).rtm") 
		sleep(0.2)		#resets ccard SAP incase of ID last job
		eeReg.click(Pattern("PrintCardType.png").targetOffset(53,-3))
		sleep(0.1)
		eeReg.click("StackOrderButton.png")       #Stack job and wait to preview
		sleep(1)
		type('v', KeyModifier.ALT)
		sleep(1)
		eeReg.wait("PrintPreviewCards.png")
		sleep(1)
		eeReg.click(Pattern("PrintPreviewCards.png").targetOffset(-37,27))
		while True:
			if(exists("OKButtonEE.png")):
				break
			else:
				eeReg.click(Pattern("PrintPreviewCards-2.png").targetOffset(-37,27))	
				sleep(0.2)
		sleep(1)
		eeReg.click("OKButtonEE.png")
		sleep(1)
		paste(jobLoc)
		sleep(0.2)
		type(Key.ENTER)
		sleep(0.1)
		type(Key.ENTER)
		sleep(1)
		regPrint = Region(0,0,150,150)
		setAutoWaitTimeout(10)
		try:
			regPrint.wait("ADOBEprintCCards.png")#Wait for the camera cards to start printing
			while regPrint.exists("ADOBEprintCCards.png"): #while printing exists, stay printing
				sleep(1)
		except:
			sleep(1)
		eeApp.focus()
		setAutoWaitTimeout(5)  
		sleep(1)
		eeReg.click(Pattern("PrintPreviewCards.png").targetOffset(459,-1))
		sleep(2)           
		type('e', KeyModifier.CTRL)
		sleep(2)
	def PrintCards(codes):
		Settings.MoveMouseDelay = 0.25
		dragDrop(find("ccardPDF.png"),find(Pattern("CamerCardWhite.png").similar(0.80)))
		Settings.MoveMouseDelay = 0
		sleep(0.25)
		click(Pattern("FileBrowserBar.png").targetOffset(-2,-1))
		paste("C:\edge\jobs")
		sleep(0.1)
		type(Key.ENTER)
		wait("DateMod-Type.png")
		doubleClick(Pattern("DateMod-Type.png").targetOffset(-88,27)) #clicks most recently made exe and opens folder with it
		doubleClick(Pattern("EXEDataFolder.png").targetOffset(-7,11))
		sleep(0.2)
		try:
			Settings.MoveMouseDelay = 0.1
			king = Location(find(Pattern("Kingston.png").similar(0.78)).getTarget())
			dragDrop(find(Pattern("exeLogo.png").similar(0.84)),king)
			Settings.MoveMouseDelay = 0
			sleep(0.1)
			click(king)
			sleep(2) 
		except:
			popup("missing USB")
		popup("Job done :)") #does PrintCards of current job
	def OriginalJobs(jobCodes):
		eeApp = App(r"Q:\Edge\Software\Edge Entry.exe")
		eeReg = Region(390,115,1140,844) #region for Edge Entry Window
		for job in jobCodes:
			job.upper()
			codes = job.split("-")
			createOK = popAsk("Create Job? " + job) #does job need creating?
			if(createOK):
				CreateJobOriginal(codes, eeApp, eeReg)
			popat(1500,100)
			dataOK = popAsk("Is the ascii cleaned?") #does job need database filled?
			if(dataOK):
				DatabaseTime(eeApp)
			popat() 
			baseOK = popAsk("Database loaded?") #does job need cards and exe made?
			if(baseOK):
				SaveCardsOriginal(codes, eeApp, eeReg)
			ccardOK = popAsk("Camera Cards OK? USB plugged in?") #does job need cards printed and exe to usb?
			if(ccardOK):
				PrintCards(codes)
			popup("originals all done :^)")
	OriginalJobs(jobCodes)

jobCodes = CopyJobCodes()

while not choice == "4":
	choice = input("Enter Job Type: \n1 for Reports\n2 for Retakes\n3 for 0 Jobs\n4 to exit\n5 to get new jobcodes")
	if(choice == "1"):
		FreshReporting(jobCodes)
	elif(choice == "2"):
		Retaking(jobCodes)
	elif(choice == "3"):
		Originaling(jobCodes)
	elif(choice == "5"):
		jobCodes = CopyJobCodes()
