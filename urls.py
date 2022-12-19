from savraska.urls import Url
from views import IndexPage, Math, ContactPage, SchedulesPage, CoursePage, CourseAddCategoryPage


urlpatterns = [
    Url('^/$', IndexPage),
    Url('^/math.*$', Math),
    Url('^/contact/$', ContactPage),
    Url('^/schedules/$', SchedulesPage),
    Url('^/courses/$', CoursePage),
    Url('^/courses-category/$', CoursePage),
    Url('^/add-course-category/$', CourseAddCategoryPage),
]