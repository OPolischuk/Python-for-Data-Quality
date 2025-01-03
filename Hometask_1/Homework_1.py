import random

# Creating a list of 100 unique random sample numbers from 0 to 1000
random_list = random.sample(range(0, 1001), 100)
# Displaying the random_list
print("Not sorted list:", random_list)

# Finding the length of the random_list
n = len(random_list)

# Passage all the elements of the random_list
for i in range(n):
    # Assigning a value to a variable swapped for each iteration
    swapped = False

    # Traverse the unsorted part of the random_list
    for j in range(0, n - i - 1):
        # Comparing neighboring elements of the random_list
        if random_list[j] > random_list[j + 1]:
            random_list[j], random_list[j + 1] = random_list[j + 1], random_list[j]
            # Assigning a value to a variable swapped for each internal iteration
            swapped = True

    # Checking if no changes the random_list has been already sorted
    if not swapped:
        break

# Displaying sorted random_list
print("\nSorted list:", random_list)


# Creating function avarage_even_odd_number for calculating avarage values
def avarage_even_odd_number(numbers):
    # Creating lists of even and odd numbers
    even_numbers = []
    odd_numbers = []

    # Find even and odd numbers
    for number in numbers:
        # Find the even number by division without remainder
        if number % 2 == 0:
            # Adding appropriate number to the even_numbers list
            even_numbers.append(number)
            # Otherwise 
        else:
            # Adding appropriate number to the odd_numbers list
            odd_numbers.append(number)

    
    # Calculating avarage values for the even_numbers list and odd_numbers list
    if even_numbers:
        even_avarage = sum(even_numbers)/len(even_numbers)
    # If in even_avarage even number is absent
    else:
        even_avarage = None
    
    if odd_numbers:
        odd_avarage = sum(odd_numbers)/len(odd_numbers)
    # If in even_avarage even number is absent
    else:
        odd_avarage = None

    
    return even_avarage, odd_avarage

# Asigning variables even_avg, odd_avg values and calling the avarage_even_odd_number function
even_avg, odd_avg = avarage_even_odd_number(random_list)

print(f"\nAvarage value for even numbers is: {even_avg}")
print(f"Avarage value for odd numbers is: {odd_avg}")