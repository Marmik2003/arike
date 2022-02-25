from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class NurseRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'pri_nurse' or self.request.user.role == 'sec_nurse'


class PrimaryNurseRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'pri_nurse'


class SecondaryNurseRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'sec_nurse'
