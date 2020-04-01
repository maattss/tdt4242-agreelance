from django.http import HttpResponseRedirect
from projects.models import TaskFile
from django.contrib.auth.decorators import login_required

@login_required
def delete_file(request, file_id):
    f = TaskFile.objects.get(pk=file_id)
    f.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))