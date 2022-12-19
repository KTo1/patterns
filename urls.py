from savraska.urls import Url
from views import (IndexPage, Math, ContactPage, SchedulesPage, CoursePage, CourseAddCategoryPage, CourseCategoryPage,
    CourseAddPage, CourseCopyPage)

urlpatterns = [
    Url('^/$', IndexPage),
    Url('^/math.*$', Math),
    Url('^/contact/$', ContactPage),
    Url('^/schedules/$', SchedulesPage),
    Url('^/courses/$', CoursePage),
    Url('^/courses-category/$', CourseCategoryPage),
    Url('^/add-category/$', CourseAddCategoryPage),
    Url('^/add-course/$', CourseAddPage),
    Url('^/copy-course/$', CourseCopyPage),
]