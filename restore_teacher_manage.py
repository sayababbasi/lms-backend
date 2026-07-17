import os

admin_file = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\courses\[id]\manage.tsx'
teacher_file = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx'

with open(admin_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change Layout
content = content.replace("import DashboardLayout from '../../../../../components/layout/DashboardLayout';", "import TeacherLayout from '../../../../../components/layout/TeacherLayout';")
content = content.replace("<DashboardLayout", "<TeacherLayout")
content = content.replace("</DashboardLayout>", "</TeacherLayout>")

# 2. Change Component Name
content = content.replace('CourseManage', 'TeacherCourseManage')

# 3. Change Links for back button
content = content.replace("router.push('/dashboard/courses')", "router.push('/teacher/dashboard/courses')")
content = content.replace("href={`/dashboard/assignments/${assignment.id}/submissions`}", "href={`/teacher/dashboard/assignments/${assignment.id}/submissions`}")

# 4. Remove Admin Header Badge (Status) and Enrollment badge?
# Admin has "Admin Mode" badge, change it:
content = content.replace("Admin Mode", "Instructor Mode")

# 5. Remove "Enrollment" from Tab rendering list
content = content.replace("['overview', 'curriculum', 'enrollment', 'attendance', 'assignments', 'exams', 'resources', 'results']", "['overview', 'curriculum', 'attendance', 'assignments', 'exams', 'resources', 'results']")

# 6. Delete the Enrollment Tab JSX and Logic
# The enrollment tab logic:
idx_logic_start = content.find('// --- ENROLLMENT LOGIC ---')
idx_logic_end = content.find('// --- EXAMS LOGIC ---')
if idx_logic_start != -1 and idx_logic_end != -1:
    content = content[:idx_logic_start] + content[idx_logic_end:]

# The enrollment tab JSX:
idx_jsx_start = content.find('{/* 4. ENROLLMENT TAB */}')
idx_jsx_end = content.find('{/* 5. CURRICULUM TAB */}')
if idx_jsx_start != -1 and idx_jsx_end != -1:
    content = content[:idx_jsx_start] + content[idx_jsx_end:]

with open(teacher_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Restored teacher_manage.tsx from admin_manage.tsx!")
