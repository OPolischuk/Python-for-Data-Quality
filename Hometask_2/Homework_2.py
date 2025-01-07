# Creating 4 dictionaries with a random key, values
dict_1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 95, 'f': 55}
dict_2 = {'a': 82, 'b': 13, 'c': 14, 'd': 75, 'e': 16, 'g': 55}
dict_3 = {'a': 23, 'b': 24, 'c': 75, 'd': 26, 'e': 27, 'h': 55}
dict_4 = {'a': 64, 'b': 17, 'c': 35, 'd': 5, 'e': 20, 'j': 55}

# Creating a list of the dictionaries mentioned above
list_dict = [dict_1, dict_2, dict_3, dict_4]
# Checking the displaying of what values of the list_dict list are returned
# print(list_dict)

# Creating the one common dictionary
merged_dict = {}
key_count = {}

# each element of the list_dict list is selected and writing to the merged_dict dictionary
# for dict in list_dict:
#     merged_dict.update(dict)
# print(merged_dict)

# Iteration for each dictionary
for dict in list_dict:
    for key, value in dict.items():
        # If key exists in merged_dict
        if key in merged_dict:
            # Choosing the max value of the key
            merged_dict[key] = max(merged_dict[key], value)

            # Checking of need to rename the key
            count = key_count.get(key, 1)
            # Rename the key
            new_key = f"{key}_{count}"
            while new_key in merged_dict:
                count += 1
                new_key = f"{key}_{count}"

            # Adding new key to the merged_dict
            merged_dict[new_key] = value

            key_count[key] = count + 1
        else:
            # If key doesn't exist
            merged_dict[key] = value


# Filtering only renamed keys and its values
renamed_keys = {key: value for key, value in merged_dict.items() if '_' in key}

print(renamed_keys)

