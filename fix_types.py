import os, re
teacher_file = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx'
with open(teacher_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Tab type: remove 'enrollment'
content = content.replace(" | 'enrollment'", "")

# Fix Icons: remove enrollment
content = re.sub(r"\s+enrollment: <UserPlus className=\"w-5 h-5\" />,", "", content)

with open(teacher_file, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed Types in teacher_manage.tsx')
