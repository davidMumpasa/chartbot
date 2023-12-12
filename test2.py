# test_data.py

user_questions = [
    {
        'input': 'what is my id number?',
        'expected_answer': 'Your user ID is 37.'
    },
    {
        'input': 'how many badges do I have?',
        'expected_answer': 'You have 7 badges.'
    },
]

badge_questions = [
    {
        'input': 'tell me about my badges',
        'expected_answer': 'You have the following badges: Badge 1, Badge 2, Badge 3.'
    },
    {
        'input': 'how many badges do I have?',
        'expected_answer': 'You have 5 badges.'
    },
]

course_questions = [
    {
        'input': 'tell me about my courses',
        'expected_answer': 'You are enrolled in the following courses: Course A, Course B.'
    },
    {
        'input': 'what courses am I taking?',
        'expected_answer': 'You are currently taking Course A and Course B.'
    },
]

quiz_questions = [
    {
        'input': 'what quizzes have I taken?',
        'expected_answer': 'You have completed the following quizzes: Quiz 1, Quiz 2.'
    },
    {
        'input': 'tell me about my quiz performance',
        'expected_answer': 'Your quiz performance is excellent.'
    },
]

general_questions = [
    {
        'input': 'tell me something interesting',
        'expected_answer': 'Did you know that llamas are excellent pack animals?'
    },
    {
        'input': 'give me a random fact',
        'expected_answer': 'The Eiffel Tower can be 15 cm taller during the summer.'
    },
]
