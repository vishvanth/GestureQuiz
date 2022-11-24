
from tkinter import *
from tkinter import messagebox as mb
import json
import cv2
import time
import handTrackingVishModule as htm

class Quiz:
	totalFingers = 0
    
	def __init__(self):
		self.q_no=0
		self.display_title()
		self.display_question()
		self.opt_selected=IntVar()
		self.opts=self.radio_buttons()
		self.display_options()
		self.buttons()
		self.data_size=len(question)
		self.correct=0
		#self.openCam()
	
	def openCam(self):
		wCam, hCam = 640, 480
		cap = cv2.VideoCapture(0)
		cap.set(3, wCam)
		cap.set(4, hCam)	
		pTime = 0
		detector = htm.handDetector(detectionCon=0.75)

		#used to locate finger tips
		tipIds = [4, 8, 12, 16, 20]
		openTime = time.time()
		while cap.isOpened():
			success, img = cap.read()
			if success:

				img = detector.findHands(img)
				lmList = detector.findPosition(img, draw=False)
				# print(lmList)

				if len(lmList) != 0:
					fingers = []
					for id in range(1, 5):
						if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
							fingers.append(1)
						else:
							fingers.append(0)

					# print(fingers)
					totalFingers = fingers.count(1)
					print(totalFingers)

					#cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
					cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
								10, (255, 0, 0), 25)

				
				cTime = time.time()
				fps = 1 / (cTime - pTime)
				pTime = cTime

				timeLeft = 5 - (cTime-openTime)

				cv2.putText(img, f'Time : {int(timeLeft)}s', (400, 70), cv2.FONT_HERSHEY_PLAIN,
							3, (255, 0, 0), 3)

				cv2.imshow("Result", img)
				if cv2.waitKey(1) &  (cTime > openTime + 5)  :
					return totalFingers
					self.buttons()
					break

        		
	def display_result(self):
		wrong_count = self.data_size - self.correct
		correct = f"Correct: {self.correct}"
		wrong = f"Wrong: {wrong_count}"
		score = int(self.correct / self.data_size * 100)
		result = f"Score: {score}%"
		mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")


	def check_ans(self, q_no):
		if self.opt_selected.get() == answer[q_no]:
			return True


	def next_btn(self):
		
		self.opt_selected.set(self.openCam())
		

		if self.check_ans(self.q_no):
			self.correct += 1
		self.q_no += 1
		if self.q_no==self.data_size:
			self.display_result()
			gui.destroy()
		else:
			
			self.display_question()
			self.display_options()
			#self.invoke()
		


	def buttons(self):
		next_button = Button(gui, text="Start Answering",command=self.next_btn,
		width=10,bg="blue",fg="grey",font=("ariel",16,"bold"))
		next_button.place(x=350,y=380)
		quit_button = Button(gui, text="Quit", command=gui.destroy,
		width=5,bg="black", fg="grey",font=("ariel",16," bold"))
		quit_button.place(x=700,y=50)
		#self.opt_selected.set(self.openCam())

		#next_button.invoke()
		#self.openCam()


	def display_options(self):
		val=0
		self.opt_selected.set(0)
		for option in options[self.q_no]:
			self.opts[val]['text']=option
			val+=1


	def display_question(self):
		q_no = Label(gui, text=question[self.q_no], width=60,
		font=( 'ariel' ,16, 'bold' ), anchor= 'w' )
		q_no.place(x=70, y=100)


	def display_title(self):
		title = Label(gui, text="Gesture QUIZ",
		width=50, bg="blue",fg="white", font=("ariel", 20, "bold"))
		title.place(x=0, y=2)


	def radio_buttons(self):
		q_list = []
		y_pos = 150
	
		while len(q_list) < 4:
			radio_btn = Radiobutton(gui,text=" ",variable=self.opt_selected,
			value = len(q_list)+1,font = ("ariel",14))
			q_list.append(radio_btn)
			radio_btn.place(x = 100, y = y_pos)
			y_pos += 40
		return q_list

    


        



#main porgram
gui = Tk()
gui.geometry("800x450")
gui.title("Gesture Quiz")

with open('data.json') as f:
	data = json.load(f)
question = (data['question'])
options = (data['options'])
answer = (data[ 'answer'])

quiz = Quiz()
gui.mainloop()
#quiz.openCam()

