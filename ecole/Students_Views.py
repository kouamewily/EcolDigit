from django.shortcuts import render, redirect
from app.models import Notif_Stud,Student,Stud_Feedback,Subject,Attendance,Attendance_report

def Stud_home(request):
    return  render(request,'Student/home.html')


def  Notif_recev(request):
    stud = Student.objects.filter(adm=request.user.id)
    for i in stud :
        stud_id = i.id
        stud_notif = Notif_Stud.objects.filter(stud_id=stud_id)
        context = {
            'stud_notif':stud_notif
        }
    return render(request,'Student/notif_recev.html',context)


def CommeLu(request,status):
    notif_stud = Notif_Stud.objects.get(id=status)
    notif_stud.status = 1
    notif_stud.save()
    return redirect('notif_recev')


def Stud_feedback(request):
    return  render(request,'Student/feedback.html')


def Stud_feedback_save(request):
    if request.method == "POST":
        stud_feedback = request.POST.get('stud_feedback')
        stud = Student.objects.get(adm=request.user.id)

        stud_feedback = Stud_Feedback(
            stud_id=stud,
            feedback=stud_feedback,
            feedback_reply=""

        )
        stud_feedback.save()
        return redirect('stud_feedback')


def Stud_view_attend(request):
    stud = Student.objects.get(adm=request.user.id)
    subject = Subject.objects.filter(course=stud.cours_id)
    action = request.GET.get('action')

    get_subject = None
    attend_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)


            attend_report = Attendance_report.objects.filter(stud_id= stud,attend_id__subject_id=subject_id)

    context = {
        'subject':subject,
        'action':action,
        'get_subject':get_subject,
        'attend_report':attend_report
    }
    return render(request,'Student/view_attend.html',context)