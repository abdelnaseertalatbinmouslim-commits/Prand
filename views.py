from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import SignupForm, PhoneLoginForm
from .models import Course, CodeSnippet, Resource, User

def home(request):
    courses = Course.objects.filter(is_published=True)[:6]
    snippets = CodeSnippet.objects.all()[:3]
    resources = Resource.objects.all()[:6]
    return render(request, "core/home.html", {"courses": courses, "snippets": snippets, "resources": resources})

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء طلب التسجيل. انتظر موافقة الإدارة قبل تسجيل الدخول.")
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "core/signup.html", {"form": form})

class PhoneLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = PhoneLoginForm
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_approved and not user.is_superuser:
            form.add_error(None, "حسابك قيد المراجعة. انتظر موافقة الإدارة.")
            return self.form_invalid(form)
        return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    if not request.user.is_approved and not request.user.is_superuser:
        return render(request, "core/pending.html")
    return render(request, "core/dashboard.html", {
        "courses": Course.objects.filter(is_published=True),
        "snippets": CodeSnippet.objects.all()[:5],
        "resources": Resource.objects.all()[:8],
        "pending_users": User.objects.filter(is_approved=False).count() if request.user.role in ("admin", "moderator") or request.user.is_superuser else 0,
    })

def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, "core/courses.html", {"courses": courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    return render(request, "core/course_detail.html", {"course": course})

def snippets(request):
    return render(request, "core/snippets.html", {"snippets": CodeSnippet.objects.all()})

def resources(request):
    return render(request, "core/resources.html", {"resources": Resource.objects.all()})

def cv(request):
    return render(request, "core/cv.html")

def staff_required(user):
    return user.is_authenticated and (user.is_superuser or user.role in ("admin", "moderator"))

@login_required
def staff_panel(request):
    if not staff_required(request.user):
        messages.error(request, "هذه الصفحة مخصصة للإدارة.")
        return redirect("dashboard")
    users = User.objects.order_by("-created_at")
    return render(request, "core/staff.html", {"users": users})

@login_required
@require_POST
def approve_user(request, user_id):
    if not staff_required(request.user):
        messages.error(request, "ليس لديك صلاحية تنفيذ هذا الإجراء.")
        return redirect("dashboard")
    target = get_object_or_404(User, pk=user_id)
    target.is_approved = True
    target.save(update_fields=["is_approved"])
    messages.success(request, f"تم قبول حساب {target.display_name}.")
    return redirect("staff")

@login_required
@require_POST
def change_role(request, user_id):
    if not (request.user.is_superuser or request.user.role == "admin"):
        messages.error(request, "تغيير الصلاحيات متاح لمدير المنصة فقط.")
        return redirect("staff")
    target = get_object_or_404(User, pk=user_id)
    role = request.POST.get("role")
    if role in ("student", "moderator", "admin") and not target.is_superuser:
        target.role = role
        target.save(update_fields=["role"])
        messages.success(request, "تم تحديث الصلاحية.")
    return redirect("staff")

@login_required
@require_POST
def delete_user(request, user_id):
    if not (request.user.is_superuser or request.user.role == "admin"):
        messages.error(request, "حذف الأعضاء متاح لمدير المنصة فقط.")
        return redirect("staff")
    target = get_object_or_404(User, pk=user_id)
    if target.pk == request.user.pk or target.is_superuser:
        messages.error(request, "لا يمكن حذف حسابك الحالي أو حساب مدير النظام الأعلى.")
    else:
        target.delete()
        messages.success(request, "تم حذف العضو.")
    return redirect("staff")
