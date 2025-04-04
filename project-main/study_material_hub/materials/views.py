from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, HttpResponse
import os
from django.conf import settings
from .models import StudyMaterial
from .forms import StudyMaterialForm

# ✅ View to upload study materials (Only for logged-in users)
@login_required
def upload_material(request):
    if request.method == 'POST':
        form = StudyMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user  # Set the current user
            material.save()
            return redirect('material_list')  # Redirect to the materials list page
    else:
        form = StudyMaterialForm()
    return render(request, 'materials/upload.html', {'form': form})

# ✅ View to list all uploaded materials with search & pagination (Only for logged-in users)
@login_required
def material_list(request):
    query = request.GET.get('q', '')  # Get search query from URL
    materials = StudyMaterial.objects.all().order_by('-id')  # Order by latest uploads

    # Apply search filter if query exists
    if query:
        materials = materials.filter(
            Q(title__icontains=query) | Q(description__icontains=query)  # Search in title & description
        )

    # Pagination: Show 5 materials per page
    paginator = Paginator(materials, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'materials/list.html', {'materials': page_obj, 'query': query})

# ✅ View to delete a study material
@login_required
def delete_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    material.delete()
    return redirect('material_list')  # Redirect to materials list after deletion

# ✅ View to download study material
@login_required
def download_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    file_path = material.file.path  # Get the file path
    if os.path.exists(file_path):  
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        return HttpResponse("File not found.", status=404)

# ✅ View for user signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect('material_list')  # Redirect to material list
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# ✅ View for user login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log in user
            return redirect('material_list')  # Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

# ✅ View for user logout
def user_logout(request):
    logout(request)
    return redirect('/login/')  # Redirect to login page

# ✅ View for user profile (show uploaded materials)
@login_required
def user_profile(request):
    user_materials = StudyMaterial.objects.filter(uploaded_by=request.user).order_by('-id')
    return render(request, 'materials/profile.html', {'user_materials': user_materials})
