import os
teacher_file = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx'
with open(teacher_file, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("from '../../../../../", "from '../../../../../../")

with open(teacher_file, 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed import paths!')
