from django.views.decorators.http import require_POST,require_GET
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache

from .models import CustomerProfile, ServiceRequest, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# Create your views here.

# # Home view for the application
# def home(request):

#     return render(
#         request,
#         "users/home.html"
#     )

# Register view for users
def register(request):

    if request.method == "POST":

        print("POST REQUEST RECEIVED")

        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        form_data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
        }

        print("Username:", username)
        print("Email:", email)
        # print("Password:", password)
        # print("Confirm Password:", confirm_password)

        if not username or not first_name or not last_name or not email or not phone or not password or not confirm_password:
            return render(
                request,
                "users/register.html",
                {"error_message": "Please fill all required fields.", "form_data": form_data}
            )
        if not phone.isdigit() or len(phone) != 10:
            return render(
                request,"users/register.html",
                {"error_message": "Phone number must be 10 digits.",
                 "form_data": form_data}
            )
        if password != confirm_password:
            return render(
                request,
                "users/register.html",
                {"error_message": "Passwords do not match.",
                 "form_data": form_data
                 }
            )

        if len(password) < 8:
            return render(
                request,
                "users/register.html",
                {"error_message": "Password must contain at least 8 characters.", 
                 "form_data": form_data}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "users/register.html",
                {"error_message": "Username already exists.",
                  "form_data": form_data}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "users/register.html",
                {"error_message": "Email already exists.",
                 "form_data": form_data}
            )

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=make_password(password),
            role=User.Role.CUSTOMER
        )

        user.save()

        print("User created successfully:", user)

        return render(
            request,
            "users/register.html",
            {"success_message": "Registration successful."}
        )

    return render(request, "users/register.html")

# Login view for users
def user_login(request):

    if request.method == "POST":

        print("LOGIN POST REQUEST RECEIVED")

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(
                request,
                "users/login.html",
                {"error_message": "Please enter both username and password."}
            )

        print("Login username:", username)
        
        user = User.objects.filter(username=username).first()

        if user is None:
            return render(
                request,
                "users/login.html",
                {"error_message": "Invalid username or password."}
            )

        if not user.is_active:
            return render(
                request,
                "users/login.html",
                {"error_message": "This account is inactive."}
            )
        
        if not check_password(password, user.password):
            return render(
                request,
                "users/login.html",
                {"error_message": "Invalid username or password."}
            )

        request.session['user_id'] = user.id

        print("Session user_id:", request.session["user_id"])
#       print("User role:", user.role)
        print("PASSWORD VERIFIED")
        print("Logged in user:", user.username)

        return redirect('dashboard')

        # return render(
        #     request,
        #     "users/login.html",
        #     {"success_message": "Login successful."}
        # )
    return render(request, "users/login.html")


# Dashboard view
@never_cache
def dashboard(request):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    # Customer dashboard
    if user.role == User.Role.CUSTOMER:

        service_requests = user.service_requests.all()

        total_requests = service_requests.count()

        active_requests = service_requests.filter(
            status__in=[
                ServiceRequest.Status.NEW,
                ServiceRequest.Status.ASSIGNED,
                ServiceRequest.Status.IN_PROGRESS,
            ]
        ).count()

        completed_requests = service_requests.filter(
            status=ServiceRequest.Status.COMPLETED
        ).count()

        return render(
            request,
            "users/customer_dashboard.html",
            {
                "user": user,
                "total_requests": total_requests,
                "active_requests": active_requests,
                "completed_requests": completed_requests,
            }
        )

    # Technician dashboard
    if user.role == User.Role.TECHNICIAN:
        service_requests = user.assigned_requests.all().order_by("-created_at")

        return render(
            request,
            "users/technician_dashboard.html",
            {
                "user": user,
                "assigned_requests": service_requests,
            }
        )

    
    # Manager dashboard
    if user.role == User.Role.MANAGER:
        return redirect("manager_dashboard")

    return render(
        request,
        "users/login.html",
        {"error_message": "Invalid user role."}
    )


# customer profile view 
@never_cache
def customer_profile(request):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != User.Role.CUSTOMER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )
    # Get the customer profile
    profile = CustomerProfile.objects.filter(user=user).first()
    # Handle form submission
    if request.method == "POST":
        # Handle profile update
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")

        if not address or not city or not state or not zip_code:
            return render(
                request,
                "users/customer_profile.html",
                {
                    "user": user,
                    "profile": profile,
                    "error_message": "Please fill all fields."
                }
            )

        if profile is None:
            profile = CustomerProfile(
                user=user
            )

        profile.address = address
        profile.city = city
        profile.state = state
        profile.zip_code = zip_code

        profile.save()

        return render(
            request,
            "users/customer_profile.html",
            {
                "user": user,
                "profile": profile,
                "success_message": "Profile saved successfully."
            }
        )

    return render(
        request,
        "users/customer_profile.html",
        {
            "user": user,
            "profile": profile
        }
    )

# Create service request view
@never_cache
def create_service_request(request):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)
    # Check if the user is a customer
    if user.role != User.Role.CUSTOMER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )
    # Handle form submission for creating a service request
    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        address = request.POST.get("address")
        priority = request.POST.get("priority")

        if not title or not description or not address or not priority:
            return render(
                request,
                "users/create_service_request.html",
                {
                    "user": user,
                    "error_message": "Please fill all fields.",
                    "title": title,
                    "description": description,
                    "address": address,
                    "priority": priority
                }
            )


        service_request = ServiceRequest(
            customer=user,
            title=title,
            description=description,
            address=address,
            priority=priority
        )

        service_request.save()

        return redirect("my_service_requests")

        # return render(
        #     request,
        #     "users/create_service_request.html",
        #     {
        #         "user": user,
        #         "success_message": "Service request created successfully."
        #     }
        # )

    return render(
        request,
        "users/create_service_request.html",
        {
            "user": user
        }
    )

# View to display the logged-in customer's service requests
@never_cache
def my_service_requests(request):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != User.Role.CUSTOMER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

                    # Assuming you want to order by creation date
    service_requests = user.service_requests.all().order_by('-created_at')
    total_requests = service_requests.count() 

    return render(
        request,
        "users/my_service_requests.html",
        {
            "user": user,
            "service_requests": service_requests,
            "total_requests": total_requests,
        }
    )

# View to display the details of a specific service request
@never_cache
def service_request_detail(request, service_request_id):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != User.Role.CUSTOMER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )
    # Get the service request for the logged-in customer
    service_request = get_object_or_404(
        ServiceRequest,
        id=service_request_id,
        customer=user
    )

    return render(
        request,
        "users/service_request_detail.html",
        {
            "user": user,
            "service_request": service_request
        }
    )


@never_cache
@require_POST
def cancel_service_request(request, service_request_id):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if user.role != User.Role.CUSTOMER:
        messages.error(request, "you are not allowed to cancel service requests.")
        return redirect("dashboard")

    service_request = get_object_or_404(
        ServiceRequest,
        id=service_request_id,
        customer=user
    )

    if service_request.status in [
        ServiceRequest.Status.NEW, 
        ServiceRequest.Status.ASSIGNED
        ]:

        service_request.status = ServiceRequest.Status.CANCELLED
        service_request.save(update_fields=["status", "updated_at"])
        messages.success(request, "service request cancelled successfully.")
    else:
        messages.error(
            request, "This service request can no longer be cancelled."
            )
        # service_request.save()

    return redirect(
        "service_request_detail", 
        service_request_id=service_request_id
        )


# Technician dashboard view 
@never_cache
def technician_dashboard(request):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    print("LOGGED IN TECHNICIAN USER:", user.username)
    print("USER ROLE:", user.role)


    if user.role != User.Role.TECHNICIAN:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    # Get the service requests assigned to the logged-in technician
    assigned_requests = user.assigned_requests.all().order_by('-created_at')

    print("TECHNICIAN DASHBOARD USER:", user.username)
    print("ASSIGNED REQUESTS:", assigned_requests)

    return render(
        request,
        "users/technician_dashboard.html",
        {
            "user": user,
            "assigned_requests": assigned_requests
        }
    )

# View to display the details of a specific service request for a technician
@never_cache
def technician_service_request_detail(request, request_id):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != User.Role.TECHNICIAN:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id,
        technician=user
    )

    return render(
        request,
        "users/technician_service_request_detail.html",
        {
            "user": user,
            "service_request": service_request
        }
    )



# View to update the status of a service request for a technician
@never_cache
def update_service_request_status(request, request_id):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if user.role != User.Role.TECHNICIAN:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id,
        technician=user
    )

    if request.method == "POST":
        current_status = service_request.status
        new_status = request.POST.get("status")

        allowed_transitions = {
            ServiceRequest.Status.ASSIGNED: [
                ServiceRequest.Status.IN_PROGRESS,
            ],
            ServiceRequest.Status.IN_PROGRESS: [
                ServiceRequest.Status.COMPLETED,
            ],
        }

        if new_status in allowed_transitions.get(current_status, []):
            service_request.status = new_status
            service_request.save()

    return redirect(
        "technician_service_request_detail",
        request_id=request_id
    )



# Manager dashboard view
@never_cache
def manager_dashboard(request):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if user.role != User.Role.MANAGER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    service_requests = ServiceRequest.objects.all().order_by("-created_at")

    # Total number of service requests
    total_requests = service_requests.count()

    # Requests without an assigned technician
    unassigned_count = service_requests.filter(
        technician__isnull=True
    ).exclude(
        status__in=[
            ServiceRequest.Status.COMPLETED,
            ServiceRequest.Status.CANCELLED,
        ]
    ).count()

    # Requests currently being worked on
    in_progress_count = service_requests.filter(
        status=ServiceRequest.Status.IN_PROGRESS
    ).count()

    # Technician account statistics
    technicians = User.objects.filter(role=User.Role.TECHNICIAN)
    total_technicians = technicians.count()
    active_technicians = technicians.filter(is_active=True).count()

    return render(
        request,
        "users/manager_dashboard.html",
        {
            "user": user,
            "service_requests": service_requests,
            "total_requests": total_requests,
            "unassigned_count": unassigned_count,
            "in_progress_count": in_progress_count,
            "total_technicians": total_technicians,
            "active_technicians": active_technicians,
        }
    )



# Manager view: display all technicians and their current workload
@never_cache
def manager_technicians(request):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if user.role != User.Role.MANAGER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    technicians = User.objects.filter(
        role=User.Role.TECHNICIAN
    ).order_by("username")

    total_technicians = technicians.count()
    active_technicians = technicians.filter(is_active=True).count()
    inactive_technicians = total_technicians - active_technicians

    for technician in technicians:
        technician.open_request_count = technician.assigned_requests.filter(
            status__in=[
                ServiceRequest.Status.ASSIGNED,
                ServiceRequest.Status.IN_PROGRESS,
            ]
        ).count()

    return render(
        request,
        "users/manager_technicians.html",
        {
            "user": user,
            "technicians": technicians,
            "total_technicians": total_technicians,
            "active_technicians": active_technicians,
            "inactive_technicians": inactive_technicians,
        }
    )


# Manager view: display details and requests for one technician
@never_cache
def manager_technician_detail(request, technician_id):
    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = get_object_or_404(User, id=user_id)

    if user.role != User.Role.MANAGER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    technician = get_object_or_404(
        User,
        id=technician_id,
        role=User.Role.TECHNICIAN
    )

    assigned_requests = technician.assigned_requests.all().order_by(
        "-created_at"
    )

    open_request_count = assigned_requests.filter(
        status__in=[
            ServiceRequest.Status.ASSIGNED,
            ServiceRequest.Status.IN_PROGRESS,
        ]
    ).count()

    return render(
        request,
        "users/manager_technician_detail.html",
        {
            "user": user,
            "technician": technician,
            "assigned_requests": assigned_requests,
            "open_request_count": open_request_count,
        }
    )


# View to display the details of a specific service request for a manager
@never_cache
def manager_service_request_detail(request, request_id):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != User.Role.MANAGER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    return render(
        request,
        "users/manager_service_request_detail.html",
        {
            "user": user,
            "service_request": service_request
        }
    )

# View to assign a service request to a technician for a manager
@never_cache
def assign_service_request(request, request_id):

    user_id = request.session.get("user_id")

    if user_id is None:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if user.role != User.Role.MANAGER:
        return render(
            request,
            "users/login.html",
            {"error_message": "Access denied."}
        )

    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    technicians = User.objects.filter(
        role=User.Role.TECHNICIAN,
        is_active=True
    ).order_by("username")

    # Handle the assignment of the service request to a technician
    if service_request.status not in [
        ServiceRequest.Status.NEW, 
        ServiceRequest.Status.ASSIGNED
    ]:
        return render(
            request,
            "users/assign_service_request.html",
            {
                "user": user,
                "service_request": service_request,
                "technicians": technicians,
                "error_message": "Service request cannot be assigned."
            }
        )

    if request.method == "POST":

        technician_id = request.POST.get("technician")

        technician = get_object_or_404(
            User,
            id=technician_id,
            role=User.Role.TECHNICIAN
        )

        service_request.technician = technician
        service_request.status = ServiceRequest.Status.ASSIGNED
        service_request.save()

        return redirect("manager_dashboard")

    return render(
        request,
        "users/assign_service_request.html",
        {
            "user": user,
            "service_request": service_request,
            "technicians": technicians
        }
    )

# Logout view for users
@never_cache
def user_logout(request):
    request.session.flush()  # Clear the session data to log out the user
    # Clear the session data to log out the user
    return redirect("login")  # Redirect to the login page after logout


