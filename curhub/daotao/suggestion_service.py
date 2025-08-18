import requests # Import requests for making HTTP calls to Ollama
from django.conf import settings
import json
import os # Import os to get environment variables

OLLAMA_API_BASE_URL = os.environ.get("OLLAMA_API_BASE_URL", "http://172.250.4.30:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

def _call_ollama_chat_api(messages, response_format=None, temperature=0.7, max_tokens=500):
    """
    Internal helper to call the Ollama chat API.
    """
    url = f"{OLLAMA_API_BASE_URL}/api/chat"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
        "stream": False # We want a single response, not a stream
    }

    if response_format and response_format.get("type") == "json_object":
        payload["format"] = "json"

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Ollama API connection timed out."}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to Ollama API. Is the server running?"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Ollama API request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Failed to decode JSON from Ollama API response."}

def get_ai_suggestions(prompt_text):
    """
    This function will call the Ollama API to get suggestions.
    """
    messages = [
        {"role": "system", "content": "You are an educational expert helping to create course syllabi. Provide helpful, specific suggestions based on the course information."},
        {"role": "user", "content": prompt_text}
    ]
    
    ollama_response = _call_ollama_chat_api(messages)
    
    if ollama_response and "message" in ollama_response and "content" in ollama_response["message"]:
        return ollama_response["message"]["content"].strip()
    elif "error" in ollama_response:
        return f"Ollama API error: {ollama_response['error']}"
    else:
        return "Unexpected response from Ollama API."

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

def evaluate_cdr_with_llm(cdr_text):
    """
    Evaluates the given CDR text using an LLM.
    """
    try:
        prompt_text = f"""
        Evaluate the following Learning Outcome (Chuẩn Đầu ra) for clarity, measurability, and alignment with educational best practices.
        Provide your assessment in a JSON format with the following keys:
        - "structural_analysis": {{ "verb": "...", "knowledge": "...", "context": "..." }}
        - "evaluation": {{ "relevance_level": "...", "clarity": "..." }}
        - "improvement_suggestions": ["...", "..."] (an array of strings for general suggestions)
        - "suggested_rewrite": "..." (a single string for an actionable, improved version of the CDR, **in Vietnamese**)

        Learning Outcome: '{cdr_text}'
        """
        
        messages = [
            {"role": "system", "content": "You are an educational expert evaluating learning outcomes. Provide a structured JSON assessment. Ensure 'improvement_suggestions' is an array of strings and 'suggested_rewrite' is a single string, and that 'suggested_rewrite' is always in Vietnamese."},
            {"role": "user", "content": prompt_text}
        ]
        
        ollama_response = _call_ollama_chat_api(messages, response_format={"type": "json_object"})
        
        if ollama_response and "message" in ollama_response and "content" in ollama_response["message"]:
            llm_output = ollama_response["message"]["content"].strip()
            try:
                return json.loads(llm_output)
            except json.JSONDecodeError:
                return {"error": "Failed to parse LLM response as JSON.", "raw_output": llm_output}
        elif "error" in ollama_response:
            return {"error": f"Ollama API error: {ollama_response['error']}"}
        else:
            return {"error": "Unexpected response from Ollama API."}
    except Exception as e:
        return {"error": f"Error evaluating CDR with AI: {str(e)}"}
