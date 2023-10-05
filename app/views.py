from django.shortcuts import render, redirect
from .models import User, Documents, StudentDocument
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import  UserForm, DocumentForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Count



def menu_dashboard(request):
    print(request.user)
    if request.user.is_active and request.user.role == 'p':
        return redirect('professor_dashboard')
    elif request.user.is_active and request.user.role == 'a':
        return redirect('admin_dashboard')
    elif request.user.is_active and request.user.role == 's':
        return redirect('student_dashboard')
    else:
        return redirect('/login')


@login_required
def student_dashboard(request):
    professors = User.objects.filter(role = 't', documents__isnull=False).distinct()
    
    selected_professor = request.GET.get('professor')
    
    if selected_professor:
        filtered_docs = Documents.objects.filter(studentdocument__student=request.user, created_by_id=selected_professor)
    else:
        filtered_docs = Documents.objects.filter(studentdocument__student=request.user)
        
    sort_option = request.GET.get('sort')
    if sort_option == 'name':
        sorted_docs = filtered_docs.order_by('title')
    elif sort_option == 'date':
        sorted_docs = filtered_docs.order_by('-creation_date')
    else:
        sorted_docs = filtered_docs
    
    return render(request, 'student_dashboard.html', {'professors': professors, 'sorted_docs': sorted_docs})

@login_required
def professor_dashboard(request):
    documents = Documents.objects.all() 
    return render(request, 'professor_dashboard.html', {'documents': documents})



@login_required 
def admin_dashboard(request):
    return render (request, 'admin_dashboard.html')


#ADMIN FUNKCIJE
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})



@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            if form.cleaned_data['role'] == 's':
                user.role == 's'
            elif form.cleaned_data['role'] == 'p':
                user.role == 'p'
            user.set_password(form.cleaned_data['password'])  
            user.save()
            return redirect('user_list')  
    else:
        form = UserForm()
    return render(request, 'create_user.html', {'form': form})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'delete_user.html', {'user': user})





#PROFESOR FUNKCIJE
@login_required
def create_document(request):
    if request.method == 'POST':
        print(request.FILES)
        if request.FILES['uploadDocument']:
            uploadDocument = request.FILES['uploadDocument']
            fs = FileSystemStorage()
            file = fs.save(uploadDocument.name, uploadDocument)
            fileurl = fs.url(file)
            title = request.POST.get("doc_title")
            Documents.objects.create(title=title, created_by=request.user, doc_path=fileurl, doc=file)
        return redirect("document_list")

    documents = Documents.objects.all()

    paginator = Paginator(documents, 4)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {"documents": documents, "page_obj": page_obj}
    return render(request, "create_document.html", context)





@login_required
def edit_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id, created_by=request.user)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            # Update document fields
            document.title = form.cleaned_data['title']
            new_document = form.cleaned_data['doc']
            if new_document:
                document.doc = new_document
            document.save()

            return redirect('document_list')
    else:
        initial_data = {'title': document.title}
        form = DocumentForm(instance=document, initial=initial_data)

    return render(request, 'edit_document.html', {'form': form, 'document': document})




@login_required
def document_list(request):
    documents = Documents.objects.filter(created_by=request.user).order_by('-creation_date')
    return render(request, 'document_list.html', {'documents': documents})



@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id, created_by=request.user)
    if request.method == 'POST':
        # Brisanje dokumenta sa servera i iz direktorija media
        if document.doc:
            document.doc.delete() 

        #brisanje dokumenta iz baze podataka
        document.delete()

        return redirect('document_list') 
    return render(request, 'delete_document.html', {'document': document})




#prikaz liste studenata
@login_required
def share_document(request, document_id):
    document = get_object_or_404(Documents, id=document_id, created_by=request.user)
    students = User.objects.filter(role = 's')
    return render(request, 'share_document.html', {'document': document, 'students': students})

#dijeljenje i ponistavanje dijeljenja
@login_required
def perform_share(request, document_id):
    document = get_object_or_404(Documents, id=document_id, created_by=request.user)
    students = User.objects.filter(role = 's')

    if request.method == 'POST':
        for student in students:
            action = request.POST.get(f'action_{student.id}')
            if action == 'share':
                StudentDocument.objects.get_or_create(document=document, student=student)
            elif action == 'unshare':
                StudentDocument.objects.filter(document=document, student=student).delete()

        return redirect('document_list')  

    return render(request, 'share_document.html', {'document': document, 'students': students})





#STUDENT FUNKCIJE
@login_required
def filtered_documents(request):
    professors = User.objects.filter(documents__isnull=False).distinct()       #'''role = 't','''
    #print("Filtered Professors:", professors)  
    
    selected_professor = request.GET.get('professor')
    
    if selected_professor:
        filtered_docs = Documents.objects.filter(studentdocument__student=request.user, created_by_id=selected_professor)
    else:
        filtered_docs = Documents.objects.filter(studentdocument__student=request.user)
        
    #logika za sortiranje
    sort_option = request.GET.get('sort')
    if sort_option == 'name':
        sorted_docs = filtered_docs.order_by('title')
    elif sort_option == 'date':
        sorted_docs = filtered_docs.order_by('-creation_date')
    else:
        sorted_docs = filtered_docs
    
    return render(request, 'student_dashboard.html', {'professors': professors, 'sorted_docs': sorted_docs})



@login_required
def student_shared_documents(request):
    shared_docs = StudentDocument.objects.filter(student=request.user).order_by('-document__creation_date')
    return render(request, 'shared_doc.html', {'shared_docs': shared_docs})

def download_document(doc_id):
    try:
        document = Documents.objects.get(pk=doc_id)
    except Documents.DoesNotExist:
        return HttpResponse("File does not exist.", status=404)

    file_path = os.path.join(settings.MEDIA_ROOT, document.doc.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = FileResponse(file)
            response['Content-Disposition'] = f'attachment; filename="{document.doc.name}"'
            return response


