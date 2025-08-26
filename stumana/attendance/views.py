from django.shortcuts import render, redirect
from .models import Student
from .resource import StudentResource
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'attendance/index.html')

def student_list(request):
    students = Student.objects.all()
        # Xử lý Export
    if request.GET.get("export") == "1":
        student_resource = StudentResource()
        dataset = student_resource.export()
        response = HttpResponse(dataset.xlsx, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="students.xlsx"'
        return response

    if request.method == "POST" and request.FILES.get("file"):
        dataset = Dataset()
        file = request.FILES["file"]

        # Xác định định dạng
        filename = file.name.lower()
        if filename.endswith(".xlsx"):
            fmt = "xlsx"
        elif filename.endswith(".xls"):
            fmt = "xls"
        elif filename.endswith(".csv"):
            fmt = "csv"
        else:
            messages.error(request, "Chỉ hỗ trợ file .xls, .xlsx, .csv")
            return redirect("student_list")

        imported_data = dataset.load(file.read(), format=fmt)

        student_resource = StudentResource()
        result = student_resource.import_data(imported_data, dry_run=True)  # kiểm tra trước

        if not result.has_errors():
            student_resource.import_data(imported_data, dry_run=False)  # thực sự import
            messages.success(request, "Import thành công!")
            return redirect("student_list")
        else:
            # Ghi lại chi tiết lỗi
            for row_idx, row in enumerate(result.invalid_rows):
                messages.error(request, f"Lỗi dòng {row.number}: {row.error}")
            for row_idx, row in enumerate(result.invalid_rows):
                print(">> Lỗi:", row.error)

    return render(request, "attendance/student.html", {"students": students})