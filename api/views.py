import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import concurrent.futures
import time
import google.generativeai as genai

genai.configure(api_key=os.environ['GAPI_KEY'])
openai.api_key = os.getenv('OPENAI_KEY')
DEV_KEY = os.getenv('DEV_KEY')


@csrf_exempt
def user_input(request):
    print("Received a user input request.")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if 'model_role' in data and 'user_message' in data and 'key' in data:
                if data['key'] == DEV_KEY:
                    conversation = [
                        {"role": "system", "content": data['model_role']},
                        {"role": "user", "content":  data['user_message']}
                    ]
                    print(data)
                    # ai_output = get_ai_response(conversation)
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        # Default message if no response is received
                        ai_output = "Timed out please try again"
                        try:
                            ai_output = executor.submit(
                                get_ai_response, conversation).result(timeout=40)
                        except concurrent.futures.TimeoutError:
                            pass
                    response_data = {
                        'answer': ai_output,
                    }
                    print("Response sent.", response_data)
                    return JsonResponse(response_data)
                else:
                    response_data = {
                        'error': 'Wrong key'
                    }
                    print("Invalid Key")
                    return JsonResponse(response_data, status=200)

            else:
                # Handle the case when required JSON data fields are missing.
                response_data = {
                    'error': '"model_role", "user_message" and "key" are required in the JSON data.'
                }
                print("Invalid JSON data: Missing required fields.")
                return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            # Handle JSON decoding error.
            response_data = {
                'error': 'Invalid JSON data'
            }
            print("Invalid JSON data: JSON decoding error.")
            return JsonResponse(response_data, status=200)
        except Exception as e:
            # Handle unexpected errors and provide detailed error message.
            response_data = {
                'error': f'An unexpected error occurred: {str(e)}'
            }
            print(f"Unexpected error: {str(e)}")
            return JsonResponse(response_data, status=200)
    else:
        # Handle the case when the request method is not POST.
        response_data = {
            'error': 'Invalid request method'
        }
        print("Invalid request method: Must be a POST request.")
        return JsonResponse(response_data, status=200)


# def get_ai_response(conversation):
#     print("Received a request to get AI response.")
#     try:
#         # Use the provided conversation in the OpenAI API request.
#         completion = openai.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=conversation
#         )
#         response_text = completion.choices[0].message.content
#         # response_text = "hi how can i help you.."
#         # time.sleep(3)
#         # response_text = "hi how can i help you.."
#         print("AI response received.")
#         return response_text
#     except Exception as e:
#         # Handle OpenAI API errors and provide specific error message.
#         response_data = {
#             'error': f'OpenAI API error: {str(e)}'
#         }
#         print(f"OpenAI API error: {str(e)}")
#         return response_data
    
def get_ai_response(conversation):
    print("Received a request to get AI response.")
    try:
        text=f"{conversation[0]['content']}\n{conversation[1]['content']}"
        print(text)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text)
        response_text = response.text
        # response_text = "hi how can i help you.."
        # time.sleep(3)
        # response_text = "hi how can i help you.."
        print("AI response received.")
        return response_text
    except Exception as e:
        # Handle OpenAI API errors and provide specific error message.
        response_data = {
            'error': f'OpenAI API error: {str(e)}'
        }
        print(f"OpenAI API error: {str(e)}")
        return response_data