







####
import firebase_admin
from firebase_admin import credentials, firestore, storage

def initialize_firebase():
    cred = credentials.Certificate('...')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'aoiwhatsappbot.appspot.com'
    })

def make_image_public_and_save_url(doc_id, file_name):
    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.make_public()  # Make the image publicly accessible
    url = blob.public_url
    # Save the URL in Firestore
    db = firestore.client()
    doc_ref = db.collection('animal_images').document(doc_id)
    doc_ref.set({'url': url})

# Main code
def main():
    initialize_firebase()

    # List of image file names stored in Firebase Storage
    image_names = [
        "Animals+4.jpg",
        "Cute+animals+check-in.jpg",
        "animal.jpg",
        "cute+animals+3.jpg"
    ]

    # Loop through and make each image public, then save URLs to Firestore
    for image_name in image_names:
        # Use image name without extension as document ID
        doc_id = image_name.replace('+', ' ').split('.')[0]  # Removing '+' to match Firestore document naming
        make_image_public_and_save_url(doc_id, image_name)

# Run the main function
if __name__ == '__main__':
    main()
