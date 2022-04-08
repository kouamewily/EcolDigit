from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import Cours, Session_year,CustomerUser,Student,Staff,Subject,Notif_Staff,Staff_Leave,Staff_Feedback,Attendance,Attendance_report
from django.contrib import messages



def Home(request):
	return render(request,'Staff/home.html')


def Notif_recev(request):
	staff = Staff.objects.filter(adm=request.user.id)

	for i in staff:
		staff_id = i.id

		notifs = Notif_Staff.objects.filter(staff_id=staff_id)

		context = {
		'notifs':notifs
		}
	
		return render(request,'Staff/notif_recev.html',context)


def CommeLu(request,status):
	notif = Notif_Staff.objects.get(id=status)
	notif.status = 1
	notif.save()
	return redirect('notif_recev')


def Depart_conge(request):
	prof = Staff.objects.filter(adm=request.user.id)
	for i in prof:
		staff_id = i.id
		historique_conge = Staff_Leave.objects.filter(staff_id=staff_id)
		context = {
			'historique_conge':historique_conge
		}
		return  render(request,'Staff/depart_conge.html',context)

def Conge_save(request):
	if request.method == "POST":
		leave_date = request.POST.get('date_conge')
		leave_message = request.POST.get('message_conge')
		staff = Staff.objects.get(adm=request.user.id)
		leave = Staff_Leave(
			staff_id=staff,
			data=leave_date,
			message=leave_message,

		)
		leave.save()
		return redirect('depart_conge')


def  Staff_feedback(request):
	staff_id = Staff.objects.get(adm=request.user.id)
	historique_feedback = Staff_Feedback.objects.filter(staff_id=staff_id)
	context = {
		'historique_feedback':historique_feedback
	}
	return  render(request,'Staff/feedback.html',context)

def Staff_feedback_save(request):
	if request.method == "POST":
		feedback = request.POST.get('feedback')
		staff = Staff.objects.get(adm=request.user.id)

		feedback = Staff_Feedback(
			staff_id=staff,
			feedback=feedback,
			feedback_reply=""
		)
		feedback.save()
		return redirect('feedback')


def Staff_take_attendance(request):
	staff = Staff.objects.get(adm=request.user.id)
	subject = Subject.objects.filter(staff=staff)
	session = Session_year.objects.all()
	action = request.GET.get('action')

	students = None
	get_session = None
	get_subject = None
	if action is not None:
		if request.method =="POST":
			subject_id = request.POST.get('subject_id')
			session_id = request.POST.get('session_id')
			get_subject = Subject.objects.get(id=subject_id)
			get_session = Session_year.objects.get(id=session_id)

			subject = Subject.objects.filter(id=subject_id)
			for i in subject:
				student_id = i.course.id
				students = Student.objects.filter(cours_id=student_id)
	context = {
		'subject':subject,
		'session':session,
		'get_subject':get_subject,
		'get_session':get_session,
		'action':action,
		'students':students

	}
	return render(request,'Staff/take_attendance.html',context)


def Save_attendance(request):
	if request.method == "POST":
		subject_id = request.POST.get('subject_id')
		session_id = request.POST.get('session_id')
		attend_date = request.POST.get('attend_date')
		student_id	= request.POST.getlist('student_id')

		get_subject = Subject.objects.get(id=subject_id)
		get_session = Session_year.objects.get(id=session_id)

		attendance = Attendance(
			subject_id=get_subject,
			session_id=get_session,
			attendance_data=attend_date
		)
		attendance.save()
		for i in student_id:
			stud_id = i
			int_stud = int(stud_id)

			p_students = Student.objects.get(id=int_stud)
			attendance_report = Attendance_report(
				stud_id=p_students,
				attend_id=attendance
			)
			attendance_report.save()
	return redirect('staff_take_attendance')


def Staff_view_attendance(request):
	staff_id = Staff.objects.get(adm=request.user.id)
	subject = Subject.objects.filter(staff=staff_id)
	session = Session_year.objects.all()
	action = request.GET.get('action')

	get_subject = None
	get_session = None
	attendance_date = None
	attendace_report=None
	if action is not None:
		if request.method == "POST":
			subject_id = request.POST.get('subject_id')
			session_id = request.POST.get('session_id')
			attendance_date = request.POST.get('attendance_date')
			get_subject = Subject.objects.get(id=subject_id)
			get_session = Session_year.objects.get(id=session_id)
			attendace = Attendance.objects.filter(subject_id=get_subject,attendance_data=attendance_date)
			for i in attendace:
				attendace_id = i.id
				attendace_report = Attendance_report.objects.filter(attend_id=attendace_id)

	context = {
		'subject':subject,
		'session':session,
		'action':action,
		'get_subject':get_subject,
		'get_session':get_session,
		'attendance_date':attendance_date,
		'attendace_report':attendace_report
	}
	return render(request,'Staff/view_attendance.html',context)