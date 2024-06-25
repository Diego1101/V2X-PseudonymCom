import pandas as pd
import math

# canfile = 'can_messages.csv'
# can_file = 'camRandTime.csv'
# can_file = 'camRandDistance.csv'
# can_file = 'camDistance.csv'
# can_file = 'camNoChange.csv'
can_file = 'camPeriodical.csv'

data = pd.read_csv(can_file)
# data = data.drop(data.index[724:])
pseudonym_data = data.drop(columns={'ServiceID','Width','Length','Heading'})

#Change Variable Value here
starting_idx = 0
threshold = 60
serviceID = data.ServiceID[starting_idx]

# Initialize variables
vehicle_idx = [starting_idx]
last_idx = starting_idx
all_dist =[]

# Function to calculate the distance between two points
def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lon1 - lon2) ** 2 + (lat1 - lat2) ** 2)

def calculate_distance_formula(spd1,spd2,t1,t2):
    return ((spd2+spd1)*(t2-t1))/(2*1000)

def remove_duplicates(numbers):
    seen = set()
    unique_numbers = []
    for number in numbers:
        if number not in seen:
            unique_numbers.append(number)
            seen.add(number)
    return unique_numbers

def compile_pseudonym_changes(pseudonym_data,indexs):
    pseudonyms = [pseudonym_data.Pseudonym[starting_idx]]
    for i in indexs:
        pseudonyms.append(pseudonym_data.Pseudonym[i])
        
    pseudonyms_no_dup = remove_duplicates(pseudonyms)

    # Prepare the data for the DataFrame
    old_pseudonyms = pseudonyms_no_dup[:-1]
    new_pseudonyms = pseudonyms_no_dup[1:]

    # Create the DataFrame
    pseudonyms_df = pd.DataFrame({
        'Old Pseudonym': old_pseudonyms,
        'New Pseudonym': new_pseudonyms
    })
    return pseudonyms_df

# Iterate through the data to track pseudonym changes
for i in range(last_idx + 1, len(pseudonym_data)):
    if pseudonym_data.Pseudonym[last_idx] == pseudonym_data.Pseudonym[i]:
        vehicle_idx.append(i)
        last_idx = i
        continue
    else:    
        # Calculate the distance from the previous point to the current point
        # using euclidean distance
        dist = calculate_distance(
            pseudonym_data.Latitude[last_idx],
            pseudonym_data.Longitude[last_idx],
            pseudonym_data.Latitude[i],
            pseudonym_data.Longitude[i]
        )
        # Calculate the distance from the previous point to the current point
        # using staight line motion formula
        dist_formula = calculate_distance_formula(
            pseudonym_data.Speed[last_idx], 
            pseudonym_data.Speed[i], 
            pseudonym_data.Timestamp[last_idx], 
            pseudonym_data.Timestamp[i]
        )
        all_dist.append(abs(dist - dist_formula))
        
        # Check if the pseudonym has changed and the distance is reasonable
        if abs(dist - dist_formula) <= threshold:
            vehicle_idx.append(i)
            last_idx = i

actual_idx = [starting_idx]
for i in range(starting_idx + 1,len(data)):
    if data.ServiceID[i] == serviceID  :
        actual_idx.append(i)


vehicle_pseudonym_changes_df = compile_pseudonym_changes(pseudonym_data,vehicle_idx)
actual_pseudonym_changes_df= compile_pseudonym_changes(pseudonym_data,actual_idx)

match_pseudonym_changes = pd.merge(vehicle_pseudonym_changes_df, actual_pseudonym_changes_df)
count_match_pseudonym_changes = match_pseudonym_changes.shape[0]

# pseudonym_change_check = 0
# pseudonym_change_wrong  = 0
# for i in vehicle_pseudonym_changes_df:
#     if i in actual_pseudonym_changes_df:
#         pseudonym_change_check += 1
#     else:
#         pseudonym_change_wrong += 1

# pseudonym_change_check = sum(item in vehicle_pseudonym_changes_df for item in actual_pseudonym_changes_df)
# pseudonym_change_wrong = sum(item not in actual_pseudonym_changes_df for item in vehicle_pseudonym_changes_df)

count = sum(item in vehicle_idx for item in actual_idx)
diff_count = sum(item not in actual_idx for item in vehicle_idx )

# accuracy = (TP + TN) / (TP + TN + FP + FN)
# accuracy = (count + diff_count) / len(vehicle_idx)

print(f'                    ServiceID = {serviceID}')
print('-----------------------------------------------------------------')
print(f'Total Vehicle record found is {len(vehicle_idx)}')
print(f'Total Actual Record is {len(actual_idx)}')
print(f'Matched Record: {count}/{len(actual_idx)}')
print(f'There are {diff_count} records found that is wrong')
print()
print(f'Total Pseudonym changes found is {len(vehicle_pseudonym_changes_df)}')
print(f'Total Actual Pseudonym Cahnges is {len(actual_pseudonym_changes_df)}')
print(f'Matched Pseudonym Changes: {count_match_pseudonym_changes}/{len(actual_pseudonym_changes_df)}')
print(f'There are {len(vehicle_pseudonym_changes_df)-count_match_pseudonym_changes} peudonym changes found that is wrong')
print()
# print(f'The Accuracy of the result is {accuracy}')
         
        
        
        
        
        
        
        
        