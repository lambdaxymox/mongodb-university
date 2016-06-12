import pymongo
import json
import collections
import os

from pprint import pprint

class Orderable:

    def __init__(self):
        pass


    def equals(self, obj):
        return NotImplemented


    def less_than(self, obj):
        return NotImplemented


    def less_than_equal(self, obj):
        return self.less_than(obj) or self.equals(obj)


    def greater_than(self, obj):
        return not self.less_than_equal(obj)


    def greater_than_equal(self, obj):
        return not self.less_than(obj)


    def not_equals(self, obj):
        return not self.equals(obj)


    def object_is(self, obj):
        return NotImplemented


    def not_object_is(self, obj):
        return not self.object_is(obj)

   
    def __eq__(self, obj):
        return self.equals(obj)


    def __lt__(self, obj):
        return self.less_than(obj)


    def __le__(self, obj):
        return self.less_than_equal(obj)


    def __gt__(self, obj):
        return self.greater_than(obj)


    def __ge__(self, obj):
        return self.greater_than_equal(obj)


"""
A Score is a dictionary(-like) of the form

{ 'score' : Number, 'type' : String, **kwargs }

where a Score has at minimum:
    'type' is a string
    'score' is a number
"""
class Score(Orderable):

    enc = json.JSONEncoder()

    def __init__(self, score, score_type, data={}):
        self._score = score
        self._score_type = score_type
        self._data = data

    @property
    def score(self):
        return self._score
    
    @property
    def score_type(self):
        return self._score_type
    

    def by_type(score_type):
        return \
            lambda score: score.score_type == score_type


    def equal_by_type(self, other_score):
        return self.score_type == other_score.score_type


    def less_than(self, other_score):
        return self.score < other_score.score


    def equals(self, other_score):
        return self.score == other_score.score


    def as_dict(self):
        dic = self._data
        dic['score'] = self.score
        dic['type'] = self.score_type
        
        return dic


    def to_json(self):
        return enc.encode(self.as_dict())


    def __repr__(self):
        return "Score({{\'score\': {}, \'type\': \'{}\'}})".format(self.score, self.score_type)


    def __str__(self):
        return repr(self)


def to_score_list(scores):
    score_list = collections.deque()
    for item in scores:
        try:
            score = Score(item['score'], item['type'], item)
        except:
            continue
        
        score_list.append(score)

    return score_list


def min_homework_score(score_list):
    return min(filter(Score.by_type('homework'), score_list))


def remove_homework_score(students, student, score):
    student['scores'].remove(score.as_dict())
    scores = student['scores']
    students.update_one(
        filter={'_id': student['_id']},
        update={ '$set': {'scores': scores} }
    )

                    
def remove_lowest_homework_scores(student_list):

    count = 0
    students = student_list.find()
    for student in students:
        min_score = min_homework_score(to_score_list(student['scores']))
        remove_homework_score(student_list, student, min_score)
        count += 1

    return count


def main(command_string):
    # Initialize Database here
    print("Clearling \'school\' database.")
    client = pymongo.MongoClient('localhost', 27017)
    client.drop_database('school')

    print("Initializing \'school\' database")  
    os.system(command_string)
    db = client.school

    student = db.students.find_one()
    print("Example student: {}")
    pprint(student)
    
    print("Removing lowest score for each student")
    remove_lowest_homework_scores(db.students)

    student = db.students.find_one({'_id': student['_id']})
    print("Example student: {}")
    pprint(student)


if __name__ == "__main__":
    command_string = 'mongoimport -d school -c students < students.json'
    main(command_string)
