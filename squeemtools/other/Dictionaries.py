import operator

def sort_dict_by_values(dictionary,asc=False):
    '''Takes a dictionary and returns it sorted in descending or ascending order'''
    if asc: return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}
    else: return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1],reverse=True)}

def get_dict_max(dictionary,**kwargs):
    assert 'how' in kwargs, "Need to pass 'how' = 'key' or 'value' so a max can be obtained."
    if kwargs['how'] == 'key':
        return max(test.items(), key=operator.itemgetter(0))[1]
    elif kwargs['how'] == 'value':
        return max(test.items(), key=operator.itemgetter(1))[0]
