import requests

from test2 import user_questions

# Replace this URL with your actual server URL
BASE_URL = "http://127.0.0.1:5000"

# Test data
valid_user_email = "David@fluidintellect.com"
invalid_user_email = "nonexistent@domain.com"


def test_login_endpoint():
    # Test successful login
    data = {'user_email': valid_user_email}
    response = requests.post(f"{BASE_URL}/login", json=data)

    print("------------------------------------------")
    print(response)

    assert response.status_code == 200
    assert response.json()['message'] == 'Login successful'

    # Test login with missing user email
    response = requests.post(f"{BASE_URL}/login", json={})
    assert response.status_code == 400
    assert response.json()['error'] == 'User email is required'

    # Test login with invalid user email
    data = {'user_email': invalid_user_email}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 404
    assert response.json()['error'] == 'User not found'


def test_submit_user_input():
    # Test submitting user input
    data = {'userInput': 'Hello, Llama!'}
    response = requests.post(f"{BASE_URL}/submitUserInput", json=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'User input submitted successfully'


def test_get_llama_response():
    # Test getting Llama response
    for test_case in user_questions:
        data = {'userInput': test_case['input']}
        response = requests.post(f"{BASE_URL}/getLlamaResponse", json=data)
        assert response.status_code == 200
        assert 'message' in response.json()
        assert response.json()['message'] == test_case['expected_answer']


def test_get_conversation_history():
    # Test getting conversation history
    response = requests.get(f"{BASE_URL}/getConversationHistory")
    assert response.status_code == 200
    assert 'history' in response.json()
    assert isinstance(response.json()['history'], list)


# Run the test cases in the desired order
if __name__ == '__main__':
    test_login_endpoint()
    test_submit_user_input()
    test_get_llama_response()
    test_get_conversation_history()
