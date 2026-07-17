import re

def insert_after(filepath, search_str, insert_content):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if insert_content in content:
        print(f"Content already in {filepath}")
        return
        
    parts = content.split(search_str)
    if len(parts) == 2:
        new_content = parts[0] + search_str + "\n\n" + insert_content + parts[1]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected functions into {filepath}")
    else:
        print(f"Could not find exact injection point in {filepath}")

teacher_manage = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx'

search_string = '''    const handleVideoUpload = async (lessonId: number, file: File) => {
        setUploadingLessonId(lessonId);
        toast.loading("Uploading to YouTube... This may take a minute.", { id: `upload-${lessonId}` });
        try {
            await CoursesService.uploadVideo(lessonId, file);
            toast.success("Video successfully uploaded and linked!", { id: `upload-${lessonId}` });
            fetchData();
        } catch (error) {
            toast.error("Failed to upload video to YouTube", { id: `upload-${lessonId}` });
        } finally {
            setUploadingLessonId(null);
        }
    };'''

missing_functions = '''    const handleUpdateModuleTitle = async (moduleId: number) => {
        if (!editModuleTitle.trim()) return;
        setSaving(true);
        try {
            await CoursesService.updateModule(moduleId, { title: editModuleTitle });
            toast.success("Module renamed");
            setEditingModuleId(null);
            fetchData();
        } catch (error) {
            toast.error("Failed to rename module");
        } finally {
            setSaving(false);
        }
    };

    const handleDeleteModule = async (moduleId: number) => {
        if (!confirm("Are you sure you want to delete this module and ALL its lessons/materials? This action cannot be undone.")) return;
        setDeletingModuleId(moduleId);
        try {
            await CoursesService.deleteModule(moduleId);
            toast.success("Module deleted");
            fetchData();
        } catch (error) {
            toast.error("Failed to delete module");
        } finally {
            setDeletingModuleId(null);
        }
    };

    const handleUpdateLessonTitle = async (lessonId: number) => {
        if (!editLessonTitle.trim()) return;
        setSaving(true);
        try {
            await CoursesService.updateLessonTitle(lessonId, editLessonTitle);
            toast.success("Lesson renamed");
            setEditingLessonId(null);
            fetchData();
        } catch (error) {
            toast.error("Failed to rename lesson");
        } finally {
            setSaving(false);
        }
    };

    const handleDeleteLesson = async (lessonId: number) => {
        if (!confirm("Are you sure you want to delete this lesson and its materials?")) return;
        setDeletingLessonId(lessonId);
        try {
            await CoursesService.deleteLesson(lessonId);
            toast.success("Lesson deleted");
            fetchData();
        } catch (error) {
            toast.error("Failed to delete lesson");
        } finally {
            setDeletingLessonId(null);
        }
    };

    const handleDeleteVideo = async (lessonId: number) => {
        if (!confirm("Are you sure you want to remove this video?")) return;
        setDeletingVideoId(lessonId);
        try {
            await CoursesService.deleteVideo(lessonId);
            toast.success("Video removed successfully");
            fetchData();
        } catch (error) {
            toast.error("Failed to remove video");
        } finally {
            setDeletingVideoId(null);
        }
    };

    const handleDeleteResource = async (resourceId: number) => {
        if (!confirm("Are you sure you want to delete this file?")) return;
        setDeletingResourceId(resourceId);
        try {
            await CoursesService.deleteResource(resourceId);
            toast.success("File deleted");
            fetchData();
        } catch (error) {
            toast.error("Failed to delete file");
        } finally {
            setDeletingResourceId(null);
        }
    };'''

insert_after(teacher_manage, search_string, missing_functions)
