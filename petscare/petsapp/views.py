from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import user,login,caretaker,details,booking,complaint
from .models import feedback,p_details,adpay,PasswordReset
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import razorpay
# Create your views here.
def index(re):
    return render(re,'index1.html')
def about(re):
    return render(re,'about.html')
def services(re):
    return render(re,'services.html')
def contact(re):
    return render(re,'contact.html')

# user registraion
def uregister(re):
    if re.method == 'POST':
        a = re.POST['u1']
        b = re.POST['u2']
        c = int(re.POST['u3'])
        d = re.POST['u4']
        e=re.POST['u5']
        f=re.POST['u6']
        x=user.objects.filter(Username=e)
        y=user.objects.filter(Email=d)
        # if x:
            # return HttpResponse("Already exists")
        if list(x)==[]:
            if list(y)==[]:
                data = user.objects.create(Name=a, Address=b, Phone=c, Email=d, Username=e)
                data.save()
                # return HttpResponse('ok')
                data1 = login.objects.create(Username=e, Password=f, Status=1)
                data1.save()
                # return HttpResponse('Sucecess')
                return render(re, 'login.html')
            else:
                url='reg1'
                msg = '''<script>alert('Email already exists..')
                                                               window.location='%s'</script>''' % (url)
                return HttpResponse(msg)
                return redirect(uregister)

        else:

            url='reg1'
            msg = '''<script>alert('Username already exists..')
                                                               window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
            return redirect(uregister)
    else:
        return render(re, 'uregister.html')

# caretaker registraion
def cregister(re):
    if re.method == 'POST':
        a = re.POST['c1']
        b = re.POST['c2']
        c = re.POST['c3']
        d = int(re.POST['c4'])
        e = re.POST['c5']
        f = re.FILES['c6']
        i = re.FILES['c7']
        g=re.POST['c8']
        h=re.POST['c9']
        x = caretaker.objects.filter(Username=g)
        y = caretaker.objects.filter(Email=e)
        if list(x)==[]:
            if list(y)==[]:
                data = caretaker.objects.create(Name=a, Address=b,Location=c,Phone=d,Email=e,Licence=f,Photo=i,Username=g,Action='pending')
                data.save()
                #return HttpResponse('ok')
                data1=login.objects.create(Username=g,Password=h,Status=2)
                data1.save()
                #return HttpResponse('success')
                return render(re, 'login.html')
            else:
                url='reg2'
                msg = '''<script>alert('Email already exists..')
                                                               window.location='%s'</script>''' % (url)
                return HttpResponse(msg)
                return redirect(cregister)
        else:

            url='reg2'
            msg = '''<script>alert('Username already exists..')
                                                               window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
            return redirect(cregister)
    else:
        return render(re, 'cregister.html')
#user profile
def uprofile(re):
    if 'uid' in re.session:
        x = re.session['uid']
        data = user.objects.filter(Username=x)
        d=caretaker.objects.filter(Action='confirm')
        s=set()
        for i in d:
            s.add(i.Location)
            l=list(s)
        return render(re,'user.html',{'r':data,'r1':l})
    else:
        return render(re, 'login.html')

#caretaker profile
def cprofile(re):
    if 'cid' in re.session:
        x = re.session['cid']
        data1 = caretaker.objects.filter(Username=x)
        return render(re, 'caretaker.html')
    else:
        return render(re, 'login.html')

#admin profile
def aprofile(re):
    if 'aid' in re.session:
        x = re.session['aid']
        data1 = caretaker.objects.filter(Username=x)
        return render(re, 'admin.html')
    else:
        return render(re, 'login.html')

#login
def log(re):
    if re.method == 'POST':
        a=re.POST['n1']
        b=re.POST['n2']
        try:
            d=login.objects.get(Username=a)
            if d.Password==b:
                if d.Status==1:
                    re.session['uid'] = a #session created
                    return redirect(uprofile)

                elif d.Status==2:
                    x=caretaker.objects.get(Username=a)
                    if x.Action=='confirm':
                        re.session['cid'] = a #session created
                        return redirect(cprofile)
                    else:
                        messages.info(re,'Login failed,request is pending.....')
                        return render(re,'login.html')
                else:
                    re.session['aid'] = a  # session created
                    return redirect(aprofile)
            else:
                return HttpResponse("Password incorrect")
        except Exception:
            return HttpResponse("Invalid username")
    else:
        return render(re, 'login.html')
#logout
def logout(re):
    if 'uid' in re.session:
        re.session.flush()
        return render(re,'index1.html')
    elif 'cid' in re.session:
        re.session.flush()
        return render(re, 'index1.html')
    elif 'aid' in re.session:
        re.session.flush()
        return render(re, 'index1.html')
    else:
        return render(re, 'index1.html')

#admin view -requests of ct
def request(re):
    if re.method == 'GET':
        d = caretaker.objects.filter(Action='pending')
        return render(re, 'request.html', {'r': d})
    else:
        return render(re, 'admin.html')

#delete a ct by admin
def delete(re):
    if re.method == 'POST':
        a=re.POST['n1']
        d = caretaker.objects.filter(Name=a)
        d.delete()
        return redirect(request)
    else:
        return render(re, 'request.html')
#approve ct by admin
def update(re):
    if re.method == 'POST':
        a=re.POST['n1']
        d = caretaker.objects.filter(Name=a)
        d.update(Action='confirm')
        return redirect(request)
    else:
        return render(re, 'request.html')
#approved ct
def viewcare(re):
    if re.method == 'GET':
        d = caretaker.objects.filter(Action='confirm')
        return render(re, 'viewcare.html', {'r': d})
    else:
        return render(re, 'admin.html')
#view all users-admin
def viewusers(re):
    if re.method=='GET':
        d=user.objects.all()
        return render(re,'viewuser.html',{'r':d})
    else:
        return render(re,'admin.html')

#view user profile himself
def umyprof(re):
    if re.method == 'GET':
        a = re.session['uid']
        d = user.objects.filter(Username=a)
        return render(re, 'userprofile.html', {'r': d})
    else:
        return render(re, 'user.html')
#change password
def changepswd(re):
        if re.method == 'POST':
            u = re.POST['n1']
            o = re.POST['n2']
            n = re.POST['n3']
            d = login.objects.filter(Username=u)
            d.update(Password=n)
            #return HttpResponse('success')
            return render(re, 'login.html')
        else:
            return render(re, 'changepswd.html')
# edit user details
def uedit(re):
    if re.method=='POST':
        x=re.POST['c1']
        d=user.objects.filter(Username=x)
        return render(re,'uedit.html',{'r':d})
    else:
        return render(re,'userprofile.html')
#updated user details
def userupdate(re):
    if re.method=='POST':
        a = re.POST['u1']
        b = re.POST['u2']
        c = int(re.POST['u3'])
        d = re.POST['u4']
        e = re.POST['u5']
        data = user.objects.filter(Username=e)
        data.update(Name=a,Address=b,Phone=c,Email=d)
        #return HttpResponse('edited')
        # return redirect(umyprof)
        return render(re,'user.html')
    else:
        return render(re,'user.html')
#user search ct by location
def locfil(request):
    if request.method == 'POST':
        x = request.POST['f1']
        d = caretaker.objects.filter(Location=x,Action='confirm')
        return render(request, 'loc_care.html', {'r': d})
    else:
       return render(request, 'login.html')
#view ct view himself
def cmyprof(re):
    if re.method == 'GET':
        a = re.session['cid']
        d = caretaker.objects.filter(Username=a)
        return render(re, 'ctprofile.html', {'r': d})
    else:
        return render(re, 'caretaker.html')

# edit ct details himself
def cedit(re):
    if re.method=='POST':
        x=re.POST['c1']
        d=caretaker.objects.filter(Username=x)
        return render(re,'cedit.html',{'r':d})
    else:
        return render(re,'ctprofile.html')
#update edited ct details
def ctupdate(re):
    if re.method=='POST':
        a = re.POST['c1']
        b = re.POST['c2']
        c = re.POST['c3']
        d = int(re.POST['c4'])
        e = re.POST['c5']
        # f = re.POST['c6']
        f = re.POST.get('c6', 'default_value')
        # g = re.POST['c7']
        g = re.POST.get('c7', 'default_value')
        h=re.POST['c8']
        data = caretaker.objects.filter(Username=h)
        data.update(Name=a,Address=b,Location=c,Phone=d,Email=e,Licence=f,Photo=g)
        #return HttpResponse('edited')
        return render(re,'caretaker.html')
        # return redirect(cmyprof)
    else:
        return render(re,'caretaker.html')

#Each ct views
def care(re,a):
    re.session['sid']=a
    return render(re,'care.html')
def detailsct(re):
    s=re.session['sid']
    d=caretaker.objects.filter(Name=s)
    return render(re,'wait.html',{'r':d})

# add details by ct
def add_details(re):
    if re.method=='POST':
        a = re.POST['n1']
        b= re.POST['n2']
        c = re.POST['n3']
        d = re.POST['n4']
        e = re.POST['n5']
        data=details.objects.create(Username=a,Name=b,Service=c,Description=d,Amount=e)
        data.save()
        return render(re,'caretaker.html')
    else:
        data=caretaker.objects.get(Username=re.session['cid'])
        return render(re,'adddetails.html',{'r':data})

# ct view-details
def view_details(re):
    if re.method=='GET':
        a=re.session['cid']
        data=details.objects.filter(Username=a)
        return render(re,'viewdetails.html',{'r':data})
    else:
        return render(re,'caretaker.html')

# delete services by CT
def deleteserv(re):
    if re.method == 'POST':
        a = re.POST['n1']
        b=re.POST['n2']
        print(a)
        print(b)
        d=details.objects.filter(Username=a,Service=b)
        print(d)
        d.delete()
        return render(re,'viewdetails.html')
    else:
        return render(re, 'viewdetails.html')

# user view-details
# def det(re):
#     if re.method == 'GET':
#         x = re.session['sid']
#         data = details.objects.filter(Username=x)
#         return render(re, 'viewdetailsbyuser.html', {'r': data})
#     else:
#         return render(re, 'user.html')
def det(re):
    a=re.session['sid']
    d=details.objects.filter(Name=a)
    return render(re,'viewdetailsbyuser.html',{'r':d})


# book appointment by user
def book(re):
    if re.method=='POST':
        a = re.POST['n1']
        b=re.POST['n2']
        c = int(re.POST['n3'])
        d = re.POST['n4']
        e = re.POST['n5']
        f = re.POST['n6']
        g = int(re.POST['n7'])
        h=re.POST['n8']
        i=re.POST['n9']
        j=re.POST['n10']
        data = booking.objects.create(Pet_owner=a,Pet_type=b,No_pets=c,Breed=d,Service=e,Date_of_service=f,Phone=g,Email=h,Name=i,Username=j,Action='pending',Pstatus='pending')
        data.save()
        # return HttpResponse('ok')
        return redirect(uprofile)
    else:
        x = re.session['sid']
        y=re.session['uid']
        d=user.objects.get(Username=y)
        data = details.objects.filter(Name=x)
        return render(re, 'booking.html', {'r': data,'r1':d})

# user view-approved bookings
def viewbooking(re):
    if re.method == 'GET':
        x = re.session['uid']
        d=user.objects.get(Username=x)
        data = booking.objects.filter(Username=x)
        # print(data.Breed)
        # print(data.Action)
        return render(re, 'viewbooking.html', {'r': data,'r1':d})
    else:
        return render(re, 'care.html')

# ct view-booking request form users
def viewbookingct(re):
    if re.method == 'GET':
        c = re.session['cid']
        b = caretaker.objects.get(Username=c)
        print(b.Name)
        data = booking.objects.filter(Name=b.Name,Action='pending')
        return render(re, 'viewbookingbyct.html', {'r': data})
    else:
        return render(re, 'caretaker.html')

# admin view booking
def advbook(re):
    # d=booking.objects.filter(Action='confirm')
    d=booking.objects.all()
    return render(re,'adviewbooking.html',{'r':d})

# accept booking by ct
def accept(re):
    if re.method=='POST':
        a = re.POST['a1']
        b=re.POST['a3']
        d=booking.objects.filter(Username=a)
        d.update(Action='confirm')
        send_mail('Confirm Appointment', 'Your Appointment is confirmed', 'settings.EMAIL_HOST_USER', [b],
                  fail_silently=False)
        return redirect(cprofile)
    else:
        return render(re,'viewbookingbyct.html')

# reject booking by ct
def reject(re):
    if re.method=='POST':
        s = re.POST['a2']
        d=booking.objects.filter(Username=s)
        # d.delete()
        d.update(Action='Rejected')
        return redirect(cprofile)
    else:
        return render(re,'viewbookingbyct.html')

#view ct by user
def ctviewbyuser(re):
    s = re.session['sid']
    d = caretaker.objects.filter(Name=s)
    return render(re, 'ctviewbyuser.html', {'r': d})
# payment status
def payment(re,id):
    if re.method=='POST':
        x = re.POST['b1']
        y = re.POST['b2']
        z = re.POST['b3']

        # a = re.POST['b4']
        re.session['cname']=y
        re.session['pname']=x
        print(x)
        print(y)
        d=booking.objects.get(pk=id)
        print(d)
        if (d.Action == 'pending'):
            return HttpResponse("<script>alert('Payment not allowed ,booking request is pending... ');window.location='../viewbooking'</script>")
        elif (d.Action == 'Rejected'):
            return HttpResponse("<script>alert('Payment not allowed,booking request is rejected... ');window.location='../viewbooking'</script>")
        elif(d.Action=='payment completed'):
            return HttpResponse("<script>alert('Payment is already completed... ');window.location='../viewbooking'</script>")
        # if(d.Action!='confirm'):
        #     # return HttpResponse("payment not allowed")
        #     return HttpResponse("<script>alert('payment not allowed');window.location='../viewbooking'</script>")
        else:
            data=details.objects.filter(Service=z,Name=y)
            print(data)
            for i in data:
                k=i.Amount
                print(k)
            return render(re,'payment.html',{'r':d,'r1':k})
    else:
        return render(re,'payment.html')


# paying amount
def pay(re, id):
    # Amount = id*100
    Amount=(id+10)*100
    re.session['Amount']=id
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    # cursor = connection.cursor()
    # cursor.execute("update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(id) + "' ")
    # payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(re, "pay.html",{'r':Amount})

def wait(re):
    return render(re,'wait.html')
# user feedback
def feed(re):
    if re.method=='POST':
        a = re.POST['n1']
        b = re.POST['n2']
        c = re.POST['n3']
        d = re.POST['n4']
        data = feedback.objects.create(Pet_owner=a, Pet_caretaker=b, Msg_type=c, Message=d, Username=re.session['uid'])
        data.save()
        print(data)
        return render(re, 'user.html')
    else:
        return render(re, 'feedback.html')
        # y=re.session['uid']
        # print(y)
        # data1=user.objects.filter(Username=y)
        # print(data1)
        # return render(re,'feedback.html',{'r1':data1})

# user view-feedback
def viewfeed(re):
    if re.method == 'GET':
        x = re.session['uid']
        b = feedback.objects.filter(Username=x)
        print(b)
        return render(re, 'viewfeed.html', {'r': b})
    else:
        return render(re, 'viewfeed.html')

# admin view-feedback
# def advfeed(re):
#     if re.method=='GET':
#         x=feedback.objects.all()
#         return render(re,'viewfeed.html',{'r':x})
#     else:
#         return render(re,'viewfeed.html')
#


def advfeed(re):
    if re.method=='GET':
        x=feedback.objects.all()
        return render(re,'adviewfeed.html',{'r':x})
    else:
        return render(re,'adviewfeed.html')
def comp(re):
    if re.method == 'POST':
        a = re.POST['n1']
        b = re.POST['n2']
        c=re.POST['n6']
        e = re.POST['n3']
        d = int(re.POST['n4'])
        g = re.POST['n5']
        data = complaint.objects.create(Username=a, Name=b, Ct=c,Email=e, Phone=d, Complaint=g)
        data.save()
        return render(re, 'user.html')
    else:
        a1 = re.session['uid']
        return render(re, 'complaint.html', {'r': a1})
def vcompadmin(re):
    b = complaint.objects.all()
    return render(re, 'vcompbyadmin.html', {'r': b})

def vcompuser(re):
    k = re.session['uid']
    b = complaint.objects.filter(Username=k)
    return render(re, 'vcompuser.html', {'r': b})
 #admin warning
def warning(re):
    if re.method=='POST':
        x=re.POST['a1']
        y=re.POST['a2']
        d=caretaker.objects.filter(Name=x,Email=y)
        return render(re, 'adminwarning.html',{'r':d})
    else:
        return render(re, 'adminwarning.html')

def ctwarning(re):
    if re.method == 'POST':
        b = re.POST['a1']
        c = re.POST['a2']
        send_mail('Warning Message',c,'settings.EMAIL_HOST_USER', [b], fail_silently=False)
        return redirect(aprofile)
    else:
        return render(re,'adminwarning.html')

#cancel/block bp
def deletect(request):
    if request.method=='POST':
        a = request.POST['b1']
        c=request.POST['b2']
        d = caretaker.objects.filter(Name=a,Email=c)
        d.delete()
        send_mail('Rejecting Message', 'You are removed', 'settings.EMAIL_HOST_USER', [c], fail_silently=False)
        return redirect(aprofile)
    else:
        return render(request,'viewcare.html')


def success(re):
    a = re.session['pname']
    b = re.session['cname']
    c = re.session['Amount']
    print(a)
    print(b)
    print(c)
    d = booking.objects.get(Pet_owner=a,Name=b)
    x = d.Email
    d1 = p_details.objects.create(Pet_owner=a,Name=b,Amount=c,Email=x)
    d1.save()
    d2 = booking.objects.get(Pet_owner=a,Name=b)
    # d2 = booking.objects.filter(Pet_owner=a)
    y = d2.Username
    d3 = adpay.objects.create(Username=y,Amount=10,Name=b)
    d3.save()
    d4=booking.objects.filter(Pet_owner=a,Name=b)
    d4.update(Action='payment completed')
    return render(re, 'index1.html')


#admin viewing payment
def vadpay(re):
    d=adpay.objects.all()
    return render(re,'adviewpayment.html',{'r':d})

# #admin view total

def  adpaytot(re):
    l=[]
    if re.method=='POST':
        v=re.POST['n1']
        d=adpay.objects.filter(Date=v)
        for i in d:
            a=i.Amount
            l.append(a)
        s=sum(l)
        print(s)
        return render(re,'adviewpayment.html',{'s1':s,'r':d})
    else:
        return render(re, 'adviewpayment.html')
#
# #view payments by caretaker
#
def ctpay(re):
    a = re.session['cid']
    d = caretaker.objects.get(Username=a)
    b = d.Name
    d1 = p_details.objects.filter(Name=b)
    return render(re, 'viewpaymentct.html', {'r': d1})

def ctpaytot(re):
    l=[]
    if re.method == 'POST':
            a = re.session['cid']
            v = re.POST['n1']
            d = caretaker.objects.get(Username=a)
            b = d.Name
            d1 = p_details.objects.filter(Name=b,Date=v)
            print(d1)
            for i in d1:
                a=i.Amount
                l.append(a)
            s=sum(l)
            print(s)
            return render(re, 'viewpaymentct.html',{'s1':s,'r':d1})
    else:
        return render(re,'viewpaymentct.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            u = user.objects.get(Email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=u, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forget.html')

def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            u=password_reset.user.Username
            login.objects.filter(Username=u).update(Password=new_password)
            # password_reset.user.set_password(new_password)
            # password_reset.user.save()
            # password_reset.delete()
            return redirect(log)
    return render(request, 'reset.html',{'token':token})

def can(request):
    if request.method=='POST':
        a = request.POST['b4']
        b = request.POST['b5']
        d = booking.objects.filter(Name=a)
        if (b == 'confirm')or(b == 'pending'):
            d.update(Action ='Appointment Cancelled')
            return redirect(viewbooking)
        elif b == 'Appointment Cancelled':
            url = 'viewbooking'
            msg = '''<script>alert('already cancelled')
                                        window.location='%s'</script>''' % (url)
            return HttpResponse(msg)

        else:
            url = 'viewbooking'
            msg = '''<script>alert('not allowed.. no refund after payment')
                            window.location='%s'</script>''' % (url)
            return HttpResponse(msg)

    else:
        return render(request,'viewbooking.html')

def logout2(re):
    if 'uid' in re.session:
        re.session.flush()
        return redirect(uprofile)
    else:
        return render(re,'login.html')






