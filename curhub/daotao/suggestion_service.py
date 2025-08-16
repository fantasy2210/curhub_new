import openai
from django.conf import settings
import json

def get_ai_suggestions(prompt_text):
    """
    This function will call the OpenAI API to get suggestions.
    In a real application, you would want to handle errors and timeouts.
    """
    try:
        # Check if OpenAI API key is set
        if not hasattr(settings, 'OPENAI_API_KEY') or not settings.OPENAI_API_KEY:
            return "AI suggestions are not configured. Please set OPENAI_API_KEY in settings."
        
        # Make the API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an educational expert helping to create course syllabi. Provide helpful, specific suggestions based on the course information."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        return f"OpenAI API error: {str(e)}"
    except Exception as e:
        return f"Error getting AI suggestions: {str(e)}"

def generate_syllabus_suggestions(course_name, course_description=None, clo_category=None):
    """
    Generate specific suggestions for different parts of the syllabus based on the course information.
    """
    if not course_name:
        return "Please provide a course name to generate suggestions."
    
    base_prompt = f"Course: {course_name}"
    if course_description:
        base_prompt += f"\nDescription: {course_description}"
    
    if clo_category:
        if clo_category == "Về kiến thức":
            prompt = f"{base_prompt}\n\nSuggest 3-5 knowledge-based learning outcomes for this course. Use action verbs and make them specific and measurable."
        elif clo_category == "Về kỹ năng":
            prompt = f"{base_prompt}\n\nSuggest 3-5 skill-based learning outcomes for this course. Focus on practical abilities and competencies students should develop."
        elif clo_category == "Về thái độ":
            prompt = f"{base_prompt}\n\nSuggest 2-3 attitude-based learning outcomes for this course. Focus on values, professional behavior, and ethical considerations."
        else:
            prompt = f"{base_prompt}\n\nSuggest appropriate learning outcomes for this course."
    else:
        prompt = f"{base_prompt}\n\nSuggest appropriate reference materials, textbooks, and online resources for this course."
    
    return get_ai_suggestions(prompt)
