from django.conf.urls import url
from . import views
from logsign.views import(
    home,
    EventList,
    EventDetail,
    MyEvent,
    EventCreate,
    join_event,
)


urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^index$', views.index, name='index'),
	url(r'^home$', views.index, name='home'),
	url(r'^activity$', views.activity, name='activity'),
	url(r'^sports$', views.sport, name='sports_complexes'),
	url(r'^about$', views.about, name='about'),
	url(r'^createpage$', views.createform, name='createpage'),
	url(r'^signup$', views.signup, name='signup'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^list$',EventList.as_view()),
	url(r'^createevent$',views.EventCreate,name="createevent"),
	url(r'^e/(?P<pk>[\w-]+)/$',join_event),
	url(r'^mylist/$',MyEvent.as_view()),
	url(r'^list/(?P<pk>[\w-]+)/$',EventDetail.as_view()),
	url(r'^booked_events$', views.booked_events, name='booked_events'),
	url(r'^joined$', views.joined_events, name='joined'),
	url(r'^bookviaevent$', views.bookformviaevent, name='book'),
	url(r'^book$', views.book, name='book'),
	
	
	
	
]
