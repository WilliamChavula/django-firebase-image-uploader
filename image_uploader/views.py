from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages
from django.shortcuts import render

firebase = settings.FIREBASE
storage = firebase.storage()
auth = firebase.auth()


def index(request):
    if request.method == 'POST':
        user = auth.sign_in_anonymous()
        file = request.FILES['file']
        file_save = default_storage.save(file.name, file)
        storage.child(f"files/{file.name}").put(f"media/{file.name}")
        delete = default_storage.delete(file.name)
        image_url = storage.child(f"files/{file.name}").get_url(user["idToken"])
        messages.success(request, "File upload in Firebase Storage successful")
        return render(request, "index.html", {'IMAGE_URL': image_url})
    else:
        return render(request, "index.html", {})
