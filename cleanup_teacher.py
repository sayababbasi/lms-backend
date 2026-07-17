with open(r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the enrollment tab JSX block (from ENROLLMENT TAB to 1. OVERVIEW)
enrollment_start = content.find('{/* ENROLLMENT TAB */')
overview_start = content.find('{/* 1. OVERVIEW */')
if enrollment_start != -1 and overview_start != -1:
    content = content[:enrollment_start] + content[overview_start:]
    print('Removed enrollment tab JSX')
else:
    print(f'Enrollment start: {enrollment_start}, Overview start: {overview_start}')

# Remove settings tab  
settings_start = content.find('{/* 2. SETTINGS')
curriculum_start = content.find('{/* 5. CURRICULUM TAB */')
if settings_start != -1 and curriculum_start != -1:
    content = content[:settings_start] + content[curriculum_start:]
    print('Removed settings tab JSX')
else:
    print(f'Settings start: {settings_start}, Curriculum start: {curriculum_start}')

# Fix timetable check at bottom
old_check = "{(['results', 'timetable'].includes(activeTab))"
new_check = "{(activeTab === 'results')"
content = content.replace(old_check, new_check)
print('Fixed results check')

# Also remove enrollment from useEffect
content = content.replace("""        if (activeTab === 'enrollment') {
            loadEnrollmentData();
        }
        """, "        ")

with open(r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
