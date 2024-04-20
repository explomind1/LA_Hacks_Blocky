

from firebase_admin import credentials, firestore, initialize_app

# Initialize Firebase Admin
cred = credentials.Certificate('...')
initialize_app(cred)
db = firestore.client()

# Define the survey questions
# new_survey_questions = [
#     "What is the most pressing issue in your community that you believe should be addressed?",
#     "Can you suggest a practical initiative that would significantly improve your community in the next couple of months?"
# ]

new_survey_questions = [
    "How large is the dataset you need?",
    "What is your budget for acquiring this data?",
    "How long do you need access to the data, and do you need exclusive access to the data, or can it be shared with other parties?",
    "Do you require real-time data updates, or are periodic updates sufficient?",
    "Are there specific security or compliance requirements you need the data to meet?"
]


# Reference the survey document
survey_ref = db.collection('surveys_LAHACKS').document('community_survey_LAHACKS')
survey_doc = survey_ref.get()

if survey_doc.exists:
    # Fetch existing questions to avoid duplicates
    existing_questions = [q['question'] for q in survey_doc.to_dict().get('questions', [])]
    # Add only new questions
    new_questions = [q for q in new_survey_questions if q not in existing_questions]
    if new_questions:
        survey_ref.update({
            'questions': firestore.ArrayUnion([{'question': q} for q in new_questions])
        })
        print("New survey questions added to Firestore.")
    else:
        print("No new questions to add.")
else:
    # Create a survey object
    survey_data = {
        'title': "Community Survey_LAHACKS",
        'questions': [{'question': q} for q in new_survey_questions]
    }
    # Document does not exist, so create it with the new questions
    survey_ref.set(survey_data)
    print("Survey document created with new questions.")
