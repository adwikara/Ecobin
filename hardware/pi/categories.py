
#metal_can
#plastic
#bottle
#paper
#glass
#spoon
#fork
#cup
#orange
#apple
#banana
#leafy_greens


def categorize(object):

    #object = 'banana'
    #percentage = 80

    object_array = []

    Recylable_list = ['metal_can', 'plastic', 'bottle', 'paper', 'glass', 'spoon', 'fork', 'cup']
    Trash_list = ['orange', 'apple', 'banana', 'leafy_greens']

    if object in Recylable_list:
        '''
        print ('Recyclable')
        object_array.append('Recyclable')
        object_array.append(percentage)
        object_array.append(object)
        print (percentage + '%')
        '''
        return "Recyclable"

    else:
        '''
        print('Trash')
        print (percentage + '%')
        '''
        return "Trash"
