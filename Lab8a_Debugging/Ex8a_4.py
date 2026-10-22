# Retrieving elements from a list
def get_element(list, index):
    try:
        return list[index]
    except IndexError:
        return f"No element at index {index}"


my_list = [1, 2, 3, 4, 5]
print(get_element(my_list, 2))  
print(get_element(my_list, 5)) 
