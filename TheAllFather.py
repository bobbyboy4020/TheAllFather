#The All Together
from datetime import date
setAutoWaitTimeout(20)    #give program time to wait for the slow report program
Settings.MoveMouseDelay = 0.0   #mouse instant movement
reportSaveLoc = r"C:\Users\hkarn\Documents\PDF\FreshReports\Nov 1 - Nov 18"
jobCodes = []
choice = ""
sortArray = []
frbDone = False


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

		Screen(1).doubleClick(Pattern("HomeroomSpot.png").similar(0.65).targetOffset(0,-15))
		sort = CopyClip()
		sortArray.append(sort[0])
		
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
		while True:
			if(eeReg.exists("ImageLoadedEE.png")):
				break
			else:
				eeReg.click("FindSubjectEE.png")
		sleep(0.1)
		eeReg.click(Pattern("ImageLoadedEE.png").targetOffset(24,6))
		sleep(0.1)
		eeReg.click("FindSubjectButton.png")
		sleep(0.5)
		eeReg.click("SortButtonEE.png")
		while True:
			if(eeReg.exists("quickSort.png")):
				break
			else:
				eeReg.click("SortButtonEE.png")
				sleep(0.2)
		sleep(0.2)
		if not (sortType == ""):
			sortType = sortType[0]
			sortType.lower()
		if ('h' in sortType):
			eeReg.click("quickSort.png")
		elif ('g' in sortType):
			eeReg.click(Pattern("quickSort.png").targetOffset(0,-27))
		elif ('a' in sortType):
			eeReg.click(Pattern("quickSort.png").targetOffset(0,35))
		else:
			if(codes[1] == "E231"):
				eeReg.click("quickSort.png")
			elif(codes[1] == "H231"):
				eeReg.click(Pattern("quickSort.png").targetOffset(0,-27))
			elif(codes[1] == "E232"):
				eeReg.click("quickSort.png")
			elif(codes[1] == "H232"):
				eeReg.click(Pattern("quickSort.png").targetOffset(0,-27))
		sleep(0.5)
		eeReg.click("ReportsPage1.png")
		while True:
			if(eeReg.exists("ReportsName.png")):
				break
			else:
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
			regon.wait("ADOBEprintCCards.png")			#Wait for the camera cards to start printing
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
				if not frbDone:		
					sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n" + str(jobCodes[i]) + ", " + str(jobCodes[i+1]) + ", " + str(jobCodes[i+2]))
					sorts = sorts.split(",") #h for homeroom, g for grade, a for alpha
			except:
				try:
					exeMake = popAsk("Make exes? " + str(jobCodes[i]) + ", " + str(jobCodes[i+1]))
					if not frbDone:
						sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n" + str(jobCodes[i]) + ", " + str(jobCodes[i+1]))
						sorts = sorts.split(",") #h for homeroom, g for grade, a for alpha
				except:
					try:
						exeMake = popAsk("Make exes? " + str(jobCodes[i]))
						if not frbDone:
							sorts = input("sorts for jobs? split by comma, enter nothing if all are default\nh for homeroom, g for grade, a for alpha\n" + str(jobCodes[i]))
							sorts = sorts.split(",") #h for homeroom, g for grade, a for alpha
					except:
						exeMake = popAsk("Make exes?")
						if not frbDone:
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
				if(frbDone): #if reports have been built, will have sort, wont have to ask user
					SaveCardsRetake(codes[i], eeApp[0], True, eeReg, sortArray[i])
				else:
					SaveCardsRetake(codes[i], eeApp[0], True, eeReg, sorts[0])
				try:
					if(frbDone):
						SaveCardsRetake(codes[i+1], eeApp[1], False, eeReg, sortArray[i+1])
					else:
						SaveCardsRetake(codes[i+1], eeApp[1], False, eeReg, sorts[1])
				except:
					try: #if prompt is left empty, sorts[1] and 2 won't work, defaults to blank
						SaveCardsRetake(codes[i+1], eeApp[1], False, eeReg, "")
					except:
						pass
				try:
					if(frbDone):
						SaveCardsRetake(codes[i+2], eeApp[2], False, eeReg, sortArray[i+2])
					else:
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

jobCodes = CopyJobCodes()

while not (choice == "4"):
	choice = input("Enter Job Type: \n1 for Reports\n2 for Retakes\n3 for 0 Jobs\n4 to exit")
	if(choice == "1"):
		FreshReporting(jobCodes)
		frbDone = True
	elif(choice == "2"):
		Retaking(jobCodes)
#	elif(choice == "3"):
#		Originaling(jobCodes)