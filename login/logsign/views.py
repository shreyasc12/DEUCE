from django.shortcuts import render

# Create your views here.

import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import UpdateView, ListView,DetailView,CreateView
from django.db import connection
from django.views.decorators.csrf import csrf_protect ,csrf_exempt
from .models import Event
from django.db import connection
from .forms import EventCreateForm

#from mysite.core.forms import SignUpForm


def home(request):
    return render(request, 'index.html')

def index(request):
	return render(request, 'index.html', {})

def activity(request):
	return render(request, 'list.html', {})

def sport(request):
	return render(request, 'sports.html', {})

def about(request):
	return render(request, 'about.html', {})

def createform(request):
	with connection.cursor() as cursor:
		cursor.execute("select sportname from sports_list")
		list_sport=cursor.fetchall()
		cursor.execute("select complexname from complex_name")
		list_complex=cursor.fetchall()
		#cursor.execute("select sportname from sports_list")
		#list_timeslot=cursor.fetchall()

	return render(request, 'forms.html', {"list_sport":list_sport,"list_complex":list_complex})

def bookformviaevent(request):
	with connection.cursor() as cursor:
		cursor.execute("select sportname from sports_list")
		list_sport=cursor.fetchall()
		cursor.execute("select complexname from complex_name")
		list_complex=cursor.fetchall()
	return render(request, 'bookingformviaevent.html', {"list_sport":list_sport,"list_complex":list_complex})

def bookform(request):
	return render(request, 'bookingform.html', {})

def booked_events(request):
	current_user=request.session['user']	
	
	with connection.cursor() as cursor:
		cursor.execute("select * from booked where bookname='{0}'".format(current_user))
		booked_user = list(cursor.fetchall())
		cursor.execute("SELECT event_name FROM players_event WHERE username ='{0}'".format(current_user))
		abc=cursor.fetchall()
	return render(request,'bookedevents.html',{"booked_user":booked_user})
			
		

@csrf_protect
def signup(request):
	data = request.POST
	name = data.get('name')
	email = data.get('email')
	passw = data.get('password')
	passwd = data.get('cpassword')
	age = data.get('age')
	interest = data.get('interest')
	print(name, email, passw, passwd,age,interest)
	if (email=="" or  name=="" or passw!=passwd):
		return render(request, 'index.html', {})
	else:
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO users(name, email, password, age, interest) values('{0}', '{1}', '{2}','{3}','{4}')".format(name, email, passw, age, interest))
		return render(request, "index.html", {})

@csrf_protect
def login(request):
	data = request.POST
	email = data.get('email')
	passw = data.get('password')
	if(email==""or passw==""):
		return render(request, 'a.html', {})
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM users WHERE email='{0}' and password='{1}'".format(email, passw))
		abc = cursor.fetchone()
		if (abc!=None):	
			request.session['id'] = abc[0]
			request.session['user'] = abc[4]
			return render(request, 'index.html', {})
		else:
			return render(request, 'a.html', {})
						

def logout(request):
	if request.session['user'] != None:
		user = request.session['user']
	else:
		user = " "
	request.session['user']=None
	request.session['id']=None

	return render(request, 'index.html', {"message":"Thank you, we miss you already "+user})						
	
def join_event(request,pk):
    #username = None
    #username = request.user.username
	if (request.session['user']!=None):	
		group = Event.objects.get(pk=pk)
		event=group.event_name
		user=request.session['user']
		with connection.cursor() as cursor:
			cursor.execute("select event_name,username from players_event where event_name='{0}' and username='{1}'".format(event,user))
			check=cursor.fetchone()
	
		if(check == None):
			username=group.username
			if (request.session['user']==username):
				print("You cant Join Event As you have created it")
			else:	
				group.Required_Players = group.Required_Players-1
				group.Available_Players = group.Available_Players+1
				required = group.Required_Players
				current_user=request.session['user']
				current_eventid=group.id
				current_eventname=group.event_name	
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO players_event(eventid, event_name, username) values('{0}', '{1}', '{2}')".format(current_eventid, current_eventname, current_user))
		
				#group.attendees = username
					group.save()
					if(required==0):
						Event.objects.get(pk=pk).delete()
	
		else:
			print("You Have Already Joined This Event")
	else:
		return render(request, 'index.html',{})
        	
	return render(request, 'index.html',{})

def unjoin_button(request):
	user=request.session['user']
	with connection.cursor() as cursor:
		cursor.execute("select event_name from players_event where username='{0}'".format(user))
		status=cursor.fetchone()
		
	return render(request, 'list.html',{"status":status})



class EventList(ListView):
    template_name ="list.html"
    queryset = Event.objects.all()

class EventDetail(DetailView):
    template_name = "detail.html"
    queryset = Event.objects.all()

class MyEvent(ListView):
    template_name = "mylist.html"
    def get_queryset(self):# it gets the query set which we want
        return Event.objects.filter(username=self.request.session['user'])

#def unjoin_button(request):
#        user=request.session['user']
#        with connection.cursor() as cursor:
#            cursor.execute("select event_name from players_event where username='{0}'".format(user))
#            status=cursor.fetchone()
#		
#            return render(request, 'list.html',{"status":status})


#def MyEvent(request):
#    template_name ="sports/mylist.html"
#    queryset = Event.objects.filter(owner=request.user)
#    context = {"object_list" : queryset}
#    return render(request,template_name,context)

#class EventCreate(CreateView):
 #   form_class = EventCreateForm
 #   #login_url = '/login/'                  #after adding login mixins library do this
 #   template_name = "forms.html"
 #   success_url = "/list"

 #   def form_valid(self, form):         #not understood if user is logged in automatically it will get connected to him
 #       instance = form.save(commit=False)
 #       instance.owner = self.request.user
 #       return super(EventCreate,self).form_valid(form)

def EventCreate(request):
	if (request.session['user'] != None):	
		data = request.POST
		eventname = data.get('eventname')
		sport = data.get('sport')
		required_players = data.get('required_players')
		available_players = data.get('available_players')
		sports_complex = data.get('sports_complex')
		in_time=data.get('in_time')
		out_time=data.get('out_time')
		date = data.get('date')
		print(eventname,sport,required_players,available_players,sports_complex,in_time,out_time,date)
		print("************************************************************************")
		current_user=request.session['user']
		if(sport==""or required_players=="" or available_players=="" or eventname=="" or sports_complex=="" or in_time=="" or out_time=="" or date==" " ):
			return render(request, 'a.html', {})
		else:
			with connection.cursor() as cursor:
				cursor.execute("INSERT INTO logsign_event(username, event_name, sport, Required_Players, Available_Players, in_time,out_time,date,sports_complex) values('{0}', '{1}', '{2}','{3}','{4}','{5}','{6}','{7}','{8}')".format(current_user,eventname, sport, required_players, available_players, in_time, out_time, date, sports_complex))
		return render(request,'list.html',{})
		
def book(request):
	data = request.POST
	sport = data.get('sport')
	sports_complex = data.get('sports_complex')
	time_slot=data.get('time_slot')
	date = data.get('date')
	eventname = data.get('eventname')
	current_user = request.session['user']
	print(sport,sports_complex,time_slot,date,eventname)
	if(sport=="" or  sports_complex =="" or time_slot=="" or date==" " or eventname=="" ):
		return render(request, 'a.html', {})
	else:
		with connection.cursor() as cursor:
				cursor.execute("INSERT INTO booked(eventname,bookname, sport, time_slot, date, sports_complex) values('{0}', '{1}', '{2}','{3}','{4}','{5}')".format(eventname,current_user, sport, time_slot, date, sports_complex))
		return render(request,'a.html',{})

def bookcomplex(request):
	data = request.POST
	sport = data.get('sport')
	sports_complex = data.get('sports_complex')
	time_slot=data.get('time_slot')
	date = data.get('date')
	current_user = request.session['user']
	print(sport,sports_complex,time_slot,date)
	if(sport=="" or  sports_complex =="" or time_slot=="" or date==" " ):
		return render(request, 'a.html', {})
	else:
		with connection.cursor() as cursor:
				cursor.execute("INSERT INTO booked(bookname, sport, time_slot, date, sports_complex) values('{0}', '{1}', '{2}','{3}','{4}')".format(current_user, sport, time_slot, date, sports_complex))
		return render(request,'a.html',{})
  			
	
	
def joined_events(request):
	current_user=request.session['user']
	with connection.cursor() as cursor:
		cursor.execute("SELECT event_name,eventid FROM players_event WHERE username ='{0}'".format(current_user))
		abc=cursor.fetchall()
		print(abc)
		print("**********************************************************************")
		#cursor.execute("SELECT event_name FROM players_event WHERE username ='{0}'".format(current_user))
		#temp=cursor.fetchall()
		#print(temp)
		#print(temp.__len__())
		#print("**********************************************************************")
	
		#event=list(temp)
		#print(event)
		#print("**********************************************************************")
		#print(event[])
		#for i in range(event.__len__()):		
	
			#cursor.execute("select bookname from booked where eventname='{0}'".format(event[i]))
			#joined=cursor.fetchone()
		#print(joined)
		#print("**********************************************************************")
	
		#for i in range(abc.__len__()):
		#	event=abc[i]
		#	for i in range(event.__len__()):
		#		cursor.execute("select * from logsign_event where event_name='{0}'".format(event))
		#		joined[i]=cursor.fetchone()
	return render(request,'joined.html',{"abc":abc})
		
	





