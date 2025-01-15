from functools import reduce

# Step 1: Define helper functions
def merge_dicts(dict1, dict2, key_count):
    """Merge two dictionaries, resolving key conflicts by taking the maximum value and counting occurrences."""
    merged = dict1.copy()  # Start with a copy of the first dictionary
    for key, value in dict2.items():
        if key in merged:
            merged[key] = max(merged[key], value)
            key_count[key] = key_count.get(key, 0) + 1  # Increment count for key
        else:
            merged[key] = value
            key_count[key] = 1  # First occurrence of this key
    return merged

def rename_conflicting_keys(merged_dict, key_count):
    """Rename keys in merged_dict that have been encountered more than once."""
    updated_dict = {}
    for key, value in merged_dict.items():
        if key_count[key] > 1:  # If the key appears more than once
            count = key_count.get(key, 1)
            new_key = f"{key}_{count}"
            while new_key in updated_dict:  # Ensure no conflict with renamed keys
                count += 1
                new_key = f"{key}_{count}"
            updated_dict[new_key] = value
        else:
            updated_dict[key] = value
    return updated_dict

def extract_renamed_keys(merged_dict):
    """Extract keys from merged_dict that have been renamed (i.e., contain underscores)."""
    return {key: value for key, value in merged_dict.items() if '_' in key}

# Step 2: Define the main logic
def process_dictionaries(list_dict):
    """Process a list of dictionaries, merging them and renaming conflicts."""
    key_count = {}
    merged_dict = reduce(lambda x, y: merge_dicts(x, y, key_count), list_dict, {})  # Merge all dictionaries
    print("Merged Dictionary:", merged_dict)  # Debugging output
    merged_dict = rename_conflicting_keys(merged_dict, key_count)  # Rename conflicting keys
    print("After Renaming Conflicts:", merged_dict)  # Debugging output
    return extract_renamed_keys(merged_dict)  # Extract renamed keys

# Input dictionaries
dict_1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 95, 'f': 55}
dict_2 = {'a': 82, 'b': 13, 'c': 14, 'd': 75, 'e': 16, 'g': 55}
dict_3 = {'a': 23, 'b': 24, 'c': 75, 'd': 26, 'e': 27, 'h': 55}
dict_4 = {'a': 64, 'b': 17, 'c': 35, 'd': 5, 'e': 20, 'j': 55}

list_dict = [dict_1, dict_2, dict_3, dict_4]

# Process and display renamed keys
renamed_keys = process_dictionaries(list_dict)
print("Renamed Keys:", renamed_keys)