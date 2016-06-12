import pymongo

def delete_min_scores(collection):

    documents = collection.find({'type': 'homework'}).sort([('student_id', pymongo.ASCENDING), ('score', pymongo.ASCENDING)])
    old_student_id = None

    for document in documents:

        try:
            current_student_id = document['student_id']
        except KeyError as e:
            print(e)
            continue

        if (current_student_id != old_student_id):
            old_student_id = current_student_id
            collection.delete_one(document)


"""
if __name__ == 'main':
    client = pymongo.MongClient('localhost', 27017)
    db = client.students
    col = db.grades
"""