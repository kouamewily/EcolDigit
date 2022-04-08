from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Cours, Session_year,CustomerUser,Student,Staff,Subject,Notif_Staff,Staff_Leave,Staff_Feedback,Notif_Stud,Stud_Feedback,Attendance,Attendance_report
from django.contrib import messages
from django.http import HttpResponse
import datetime
import csv



@login_required(login_url='/')
def Home(request):
	stu = Student.objects.all().count()
	staff = Staff.objects.all().count()
	cours = Cours.objects.all().count()
	sub = Subject.objects.all().count()

	sut_gend_male = Student.objects.filter(genre='Femme').count()
	sut_gend_fem = Student.objects.filter(genre='Homme').count()

	print(sut_gend_fem,'femmes')
	print(sut_gend_male,'hommes')


	context = {
	'student':stu,
	'staff':staff,
	'cours':cours,
	'subject':sub,
	'total_homme':sut_gend_male,
	'total_femme':sut_gend_fem
	}
	return render(request,'Hod/home.html',context)


@login_required(login_url='/')
def Add_student(request):
	cours = Cours.objects.all()
	session = Session_year.objects.all()
	if request.method == "POST":
		profile_img = request.FILES.get('profile_img')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		address = request.POST.get('address')
		genre = request.POST.get('genre')
		cours_id = request.POST.get('cours_id')
		session_id = request.POST.get('session_id')


		if CustomerUser.objects.filter(email=email).exists():
			messages.warning(request,'Email existe dejà')
			return redirect('add_student')
		if CustomerUser.objects.filter(username=username).exists():
			messages.warning(request,'username deja pris')
			return redirect('add_student')

		else:
			user = CustomerUser(
				first_name = first_name,
				last_name = last_name,
				username = username,
				email = email,
				profile_pic = profile_img,
				user_type = 3
				)
			user.set_password(password)
			user.save()

			cours = Cours.objects.get(id=cours_id)
			session = Session_year.objects.get(id=session_id)

			student = Student(
				adm = user,
				address = address,
				session_year_id = session,
				cours_id = cours,
				genre = genre,
				)
			student.save()
			messages.success(request,'Eleve ajouter')
			return redirect('add_student')



	context = {
	'cours':cours,
	'session':session
	}

	return render(request, 'Hod/add_student.html',context)


@login_required(login_url='/')
def Liste_eleve(request):
	student = Student.objects.all()


	context = {
	'student':student,
	}
	return render(request,'Hod/view_student.html',context)

def Edit_eleve(request,id):

	student = Student.objects.filter(id=id)
	cours = Cours.objects.all()
	session = Session_year.objects.all()

	context = {
	'student':student,
	'cours':cours,
	'session':session
	}
	return render(request,'Hod/edit_student.html',context)


def Update_eleve(request):
	if request.method == "POST":

		student_id = request.POST.get('student_id')
		print(student_id)
		
		profile_img = request.FILES.get('profile_img')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		address = request.POST.get('address')
		genre = request.POST.get('genre')
		cours_id = request.POST.get('cours_id')
		session_id = request.POST.get('session_id')

		user = CustomerUser.objects.get(id=student_id)
		user.first_name = first_name
		user.last_name = last_name
		user.email = email
		user.username = username

		if password != None and password !="":
			user.set_password(password)
		if profile_img != None and profile_img !="":
			user.profile_pic = profile_img
		user.save()

		student = Student.objects.get(adm=student_id)
		student.address = address
		student.genre = genre

		cours = Cours.objects.get(id=cours_id)
		student.cours_id = cours

		session = Session_year.objects.get(id=session_id)
		student.session_year_id = session

		student.save()
		
		return redirect('view_student')

	return render(request,'Hod/edit_student.html')


def Delete_eleve(request,adm):
	student = CustomerUser.objects.get(id=adm)
	student.delete()
	messages.success(request, "est supprimer avec succes")
	return redirect('view_student')

def Ajout_classe(request):
	if request.method == "POST":
		course = request.POST.get('course_name')

		course = Cours(
			name=course 
			)
		course.save()
		messages.success(request,'classe ajouter')
		return redirect('add_classe')
	return render(request,'Hod/add_course.html')



def export_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition']='attachment; filename=ListeEleve'+str(datetime.datetime.now())+'.csv'

	writer = csv.writer(response)
	writer.writerow(['Nom','Email','Classe','Genre','Adresse'])
	eleves = Student.objects.all()
	for i in eleves:
		writer.writerow([i.adm.first_name,i.adm.email,i.cours_id.name,i.genre,i.address])

	return response




def Liste_classe(request):
	course = Cours.objects.all()

	context = {
	'course':course
	}
	return render(request,'Hod/view_course.html',context)

def Edit_classe(request,id):

	course = Cours.objects.get(id=id)

	context = {
	'course':course
	}
	return render(request,'Hod/edit_course.html',context)

def Update_classe(request):
	if request.method == "POST":
		name = request.POST.get('name')
		course_id = request.POST.get('course_id')

		course = Cours.objects.get(id=course_id)
		course.name = name
		course.save()
		messages.success(request,'classe modifier')
		return redirect('view_course')

	return render(request,'Hod/edit_course.html')

def Delete_classe(request,id):
	course = Cours.objects.get(id=id)
	course.delete()
	return redirect('view_course')

def Ajout_staff(request):
	if request.method == "POST":
		profile_img = request.FILES.get('profile_img')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		address = request.POST.get('address')
		genre = request.POST.get('genre')

		if CustomerUser.objects.filter(email=email).exists():
			messages.warning(request,'email existe déja')
			return redirect('add_staff')
		if CustomerUser.objects.filter(username=username).exists():
			messages.warning(request,'username existe deja')
			return redirect('add_staff')
		else:
			user = CustomerUser(
				first_name=first_name,
				last_name=last_name,
				email=email,
				username=username,
				profile_pic=profile_img,
				user_type=2

				)
			user.set_password(password)
			user.save()

			staff = Staff(
				adm =user,
				address=address,
				genre=genre
				)
			staff.save()
			messages.success(request,'succes')
			return redirect('add_staff')		
	return render(request,'Hod/add_staff.html')

def Liste_staff(request):

	staff = Staff.objects.all()
	context = {
	'staff':staff
	}
	return render(request,'Hod/view_staff.html',context)


def Edit_staff(request,id):

	staff = Staff.objects.get(id=id)

	context = {
	'staff':staff,
	}

	return render(request,'Hod/edit_staff.html',context)

def Update_staff(request):
	if request.method == "POST":
		staff_id = request.POST.get('staff_id')
		profile_img = request.FILES.get('profile_img')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		address = request.POST.get('address')
		genre = request.POST.get('genre')

		user = CustomerUser.objects.get(id=staff_id)
		user.username = username
		user.first_name = first_name
		user.last_name = last_name
		user.email = email

		if password != None and password !="":
			user.set_password(password)
		if profile_img != None and profile_img !="":
			user.profile_pic = profile_img
		user.save()

		staff = Staff.objects.get(adm=staff_id)
		staff.genre = genre
		staff.address = address
		staff.save()
		messages.success(request,'modifier ')
		return redirect('view_staff')


	return render(request,'Hod/edit_staff.html')

def Delete_staff(request,adm):
	staff = Staff.objects.get(id=adm)
	staff.delete()
	messages.success(request,'supprimer')
	return redirect('view_staff')

def Ajout_matiere(request):
	cours = Cours.objects.all()
	staff = Staff.objects.all()

	if request.method == "POST":
		matiere = request.POST.get('matiere')
		staff_id = request.POST.get('staff_id')
		cours_id = request.POST.get('cours_id')

		course = Cours.objects.get(id=cours_id)
		staff = Staff.objects.get(id=staff_id)

		matiere = Subject(
			name=matiere,
			course=course,
			staff=staff
			)
		matiere.save()
		messages.success(request,'ajouter')
		return redirect('add_subject')




	context = {
	'cours':cours,
	'staff':staff
	}
	return render(request,'Hod/add_subject.html',context)

def Liste_Subject(request):
	subject = Subject.objects.all()

	context ={
	'matiere':subject
	}
	return render(request,'Hod/list_subject.html',context)


def Edit_subject(request,id):
	subject = Subject.objects.get(id=id)
	course = Cours.objects.all()
	staff 	= Staff.objects.all()

	context = {
	'matiere':subject,
	'course':course,
	'staff':staff
	}
	return render(request,'Hod/edit_subject.html',context)


def Update_matiere(request):
	if request.method == "POST":
		matiere_id = request.POST.get('matiere_id')
		matiere = request.POST.get('matiere')
		course_id = request.POST.get('cours_id')
		staff_id = request.POST.get('staff_id')

		course = Cours.objects.get(id=course_id)
		staff = Staff.objects.get(id=staff_id)

		subject = Subject(
			id=matiere_id,
			name=matiere,
			course=course,
			staff=staff
			)
		subject.save()
		messages.success(request,'modifier')
	return redirect('view_matiere')

def Delete_subject(request,id):
	subject = Subject.objects.get(id=id)
	subject.delete()
	messages.success(request,'supprimer')
	return redirect('view_matiere')

def Ajout_session(request):
	if request.method == "POST":
		debut_date = request.POST.get('start_session')
		date_fin = request.POST.get('end_session')

		session = Session_year(
			session_start=debut_date,
			session_end=date_fin
			)
		session.save()
		messages.success(request,'ajouter')
	return render(request,'Hod/add_session.html')

def List_session(request):

	session = Session_year.objects.all()

	context = {
	'session':session
	}
	return render(request,'Hod/list_session.html', context)

def Edit_session(request,id):
	session = Session_year.objects.filter(id=id)

	context = {
	'sess':session
	}
	return render(request,'Hod/edit_session.html',context)

def Staff_envoi_notif(request):
	staff = Staff.objects.all()
	notif = Notif_Staff.objects.all().order_by('-id')[0:5]
	context = {
	'staff':staff,
	'notif':notif
	}
	return render(request,'Hod/notif_staff.html',context)

def Save_staff_notif(request):
	if request.method == "POST":
		staff_id = request.POST.get('staff_id')
		message = request.POST.get('staff_message')

		staff = Staff.objects.get(adm=staff_id)
		notif = Notif_Staff(
			staff_id=staff,
			message=message
			)
		notif.save()
		return redirect('envoi_notif_staff')


def Voir_depart_conge(request):
	leave_view =Staff_Leave.objects.all()
	context = {
		'leave_view':leave_view,
	}
	return render(request,'Hod/staff_leave.html',context)


def Approuve_conge(request,id):
	leave =Staff_Leave.objects.get(id=id)
	leave.status=1
	leave.save()
	return  redirect('voir_depart_conge')


def Desapprouve_conge(request,id):
	leave = Staff_Leave.objects.get(id=id)
	leave.status =2
	leave.save()
	return  redirect('voir_depart_conge')


def Staff_feedback_reply(request):
	feedback = Staff_Feedback.objects.all()
	context = {
		'feedback':feedback,
	}
	return render(request,'Hod/staff_feedback.html',context)


def Staff_feedback_reply_save(request):
	if request.method == "POST":
		feedback_id = request.POST.get('feedback_id')
		feedback_reply = request.POST.get('feedback_reply')
		feedback = Staff_Feedback.objects.get(id=feedback_id)
		feedback.feedback_reply = feedback_reply
		feedback.save()
		return redirect('staff_feedback')


def  Send_stud_notif(request):
	stud = Student.objects.all()
	notif_stud = Notif_Stud.objects.all()

	context ={
		'stud':stud,
		'notif_stud':notif_stud
	}
	return render(request,'Hod/send_notif_stud.html',context)


def Save_stud_notif(request):
	if request.method == "POST":
		message = request.POST.get('stud_notif')
		stud_id = request.POST.get('stud_id')

		student = Student.objects.get(adm=stud_id)
		stud_notif = Notif_Stud(
			stud_id=student,
			message=message
		)
		stud_notif.save()
		return redirect('send_stud_notif')


def Stud_feedback_reply(request):
	feedback = Stud_Feedback.objects.all()
	context = {
		'feedback':feedback,
	}

	return render(request,'Hod/stud_feedback.html',context)


def Stud_feedback_reply_save(request):
	if request.method == "POST":
		feedback_id = request.POST.get('feedback_id')
		feedback_reply = request.POST.get('feedback_reply')
		feedback = Stud_Feedback.objects.get(id=feedback_id)
		feedback.feedback_reply = feedback_reply
		feedback.save()
		return  redirect('stud_feedback_reply')


def view_attend(request):

	subject = Subject.objects.all()
	session = Session_year.objects.all()
	action = request.GET.get('action')

	get_subject = None
	get_session = None
	attendance_date = None
	attendace_report = None
	if action is not None:
		if request.method == "POST":
			subject_id = request.POST.get('subject_id')
			session_id = request.POST.get('session_id')
			attendance_date = request.POST.get('attendance_date')
			get_subject = Subject.objects.get(id=subject_id)
			get_session = Session_year.objects.get(id=session_id)
			attendace = Attendance.objects.filter(subject_id=get_subject, attendance_data=attendance_date)
			for i in attendace:
				attendace_id = i.id
				attendace_report = Attendance_report.objects.filter(attend_id=attendace_id)

	context = {
		'subject': subject,
		'session': session,
		'action': action,
		'get_subject': get_subject,
		'get_session': get_session,
		'attendance_date': attendance_date,
		'attendace_report': attendace_report
	}
	return render(request,'Hod/view_attend.html',context)