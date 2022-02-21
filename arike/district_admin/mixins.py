from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DistrictAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'dist_admin'
