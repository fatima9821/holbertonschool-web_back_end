#!/usr/bin/env python3
'''
Return the list of schools with a specific topic
'''


def schools_by_topic(mongo_collection, topic):
    '''
    Return the list of schools with a specific topic
    '''
    return mongo_collection.find({'topics': topic})
