import json
import os
import copy
import numpy as np


class Data:
    omscentral_datatype = None

    def __init__(self):
        self.data = self.read_omscentral_json()

    def read_omscentral_json(self):
        path = os.path.join('data', f'omscentral_{self.omscentral_datatype}.json')
        with open(path) as f:
            data = json.load(f)
        return data


class Reviews(Data):
    omscentral_datatype = 'reviews'

    def __init__(self):
        super().__init__()
        self.reviews = self.data

    def filter_by_class(self, course_id):
        filtered_reviews = []
        for review in self.reviews:
            if review['course_id'] == course_id:
                filtered_reviews.append(copy.deepcopy(review))

        self.reviews = filtered_reviews

    def filter_by_semester(self, semester_id):
        filtered_reviews = []
        for review in self.data:
            if review['semester_id'] == semester_id:
                filtered_reviews.append(copy.deepcopy(review))

        self.reviews = filtered_reviews

    def mean_and_std(self, metric_blacklist=None):
        ratings = Metric('rating')
        difficulties = Metric('difficulty')
        workloads = Metric('workload')
        for review in self.reviews:
            if review['rating']:
                ratings.values.append(int(review['rating']))
            if review['difficulty']:
                difficulties.values.append(int(review['difficulty']))
            if review['workload']:
                workloads.values.append(float(review['workload']))
        if 'rating' not in metric_blacklist:
            ratings.print_statistics()
        if 'difficulty' not in metric_blacklist:
            difficulties.print_statistics()
        if 'workload' not in metric_blacklist:
            workloads.print_statistics()


class Metric:
    descriptions = {
        'rating': '1-5, 5 is most liked',
        'difficulty': '1-5, 5 is most difficult',
        'workload': 'hours per week',
    }

    def __init__(self, metric_type):
        self.metric_type = metric_type
        self.values = []

    def print_statistics(self):
        mean = np.mean(self.values)
        std = np.std(self.values)
        points = len(self.values)
        print(f'{self.metric_type} ({self.descriptions[self.metric_type]})')
        print(f' - mean: {mean}')
        print(f' - standard deviation: {std}')
        print(f' - points: {points}')
        # print()


class Courses(Data):
    omscentral_datatype = 'courses'


class Programs(Data):
    omscentral_datatype = 'programs'


class Semesters(Data):
    omscentral_datatype = 'semesters'


class Specializations(Data):
    omscentral_datatype = 'specializations'


if __name__ == '__main__':
    reviews = Reviews()
    courses = Courses()
    # programs = Programs()
    semesters = Semesters()
    # breakpoint()
    # specializations = Specializations()
    # reviews.filter_by_semester('2022-2')
    # semesters = '2021-1', '2021-2', '2021-3', '2022-1', '2022-2'
    omscs_class = 'CS-6601'
    metric_blacklist = [
        'rating',
        'difficulty',
        # 'workload'
        ]
    for semester_object in semesters.data:
        print(semester_object['name'])
        reviews.filter_by_class(omscs_class)
        reviews.filter_by_semester(semester_object['id'])
        reviews.mean_and_std(metric_blacklist=metric_blacklist)
    breakpoint()
