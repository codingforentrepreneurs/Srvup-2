from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator

class MemberRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        print("requiring..?")
        obj = self.get_object()
        user = request.user
        if request.user.is_staff:
            return super(MemberRequiredMixin, self).dispatch(request, *args, **kwargs)
        try:
            if obj.free:
                return super(MemberRequiredMixin, self).dispatch(request, *args, **kwargs)
        except:
            pass
        return HttpResponse("Oops not free")


class StaffMemberRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffMemberRequiredMixin, self).dispatch(request, *args, **kwargs)
