from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Folder, Photo
from .forms import FolderForm, PhotoForm
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

@login_required
def album_list(request):
    # Кореневі папки та фото (folder=None) для поточного користувача
    root_folders = Folder.objects.filter(owner=request.user, parent=None).order_by('name')
    root_photos = Photo.objects.filter(owner=request.user, folder=None).order_by('-uploaded_at')

    context = {
        'root_folders': root_folders,
        'root_photos': root_photos,
    }
    return render(request, 'albums/album_list.html', context)


@login_required
def album_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    subfolders = folder.subfolders.all().order_by('name')
    photos_list = folder.photos.all().order_by('-uploaded_at')

    # Пагінація для фото: по 6 фото на сторінку, наприклад
    paginator = Paginator(photos_list, 6)
    page_number = request.GET.get('page')
    photos = paginator.get_page(page_number)

    context = {
        'folder': folder,
        'subfolders': subfolders,
        'photos': photos,
    }
    return render(request, 'albums/album_detail.html', context)


@login_required
def create_folder(request, parent_id=None):
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)
    else:
        parent_folder = None

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            new_folder = form.save(commit=False)
            new_folder.owner = request.user
            new_folder.parent = parent_folder
            new_folder.save()
            if parent_folder:
                return redirect('album_detail', folder_id=parent_folder.id)
            else:
                return redirect('album_list')
    else:
        form = FolderForm()

    context = {
        'form': form,
        'parent_folder': parent_folder
    }
    return render(request, 'albums/folder_form.html', context)


@login_required
def edit_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        form = FolderForm(request.POST, instance=folder)
        if form.is_valid():
            form.save()
            if folder.parent:
                return redirect('album_detail', folder_id=folder.parent.id)
            else:
                return redirect('album_list')
    else:
        form = FolderForm(instance=folder)

    context = {
        'form': form,
        'folder': folder
    }
    return render(request, 'albums/folder_edit_form.html', context)


@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        parent_folder = folder.parent
        folder.delete()
        if parent_folder:
            return redirect('album_detail', folder_id=parent_folder.id)
        else:
            return redirect('album_list')

    context = {
        'folder': folder
    }
    return render(request, 'albums/folder_delete_confirm.html', context)


@login_required
def upload_photo(request, folder_id=None):
    if folder_id:
        folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    else:
        folder = None

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.folder = folder
            photo.save()
            if folder:
                return redirect('album_detail', folder_id=folder.id)
            else:
                return redirect('album_list')
    else:
        form = PhotoForm()

    context = {
        'form': form,
        'folder': folder
    }
    return render(request, 'albums/upload_photo.html', context)

@login_required
def photo_delete_confirm(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, owner=request.user)
    if request.method == 'POST':
        folder = photo.folder
        photo.delete()
        if folder:
            return redirect('album_detail', folder_id=folder.id)
        else:
            return redirect('album_list')
    return render(request, 'albums/photo_delete_confirm.html', {'photo': photo})