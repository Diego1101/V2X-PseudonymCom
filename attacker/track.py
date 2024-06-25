import pandas as pd
import math

# -------------------- ATTACKER --------------------
# This code input cam messages  track a vehicle by 
# location and speed of the vehicle. At the end, the 
# result is compared to the actual record of the 
# vehicle and compure the accuracy of the attacker to 
# evaluate how good the pseudonym change strategies are

# Comment unwanted cam message file and uncomment wanted cam message file here
# can_file = 'camRandTime.csv'
can_file = 'camRandDistance.csv'
# can_file = 'camDistance.csv'
# can_file = 'camPeriodical.csv'

data = pd.read_csv(can_file)
# data = data.drop(data.index[724:])
pseudonym_data = data.drop(columns={'ServiceID','Width','Length','Heading'})

# Change Variable Value here
starting_idx = 0 # Change the starting index (refer below) and run
threshold = 60

# ServiceID : Starting Index
# 85    : 0
# 155   : 2
# 225   : 12
# 295   : 13
# 365   : 53
# 415   : 100
# 505   : 117
# 575   : 134

# Initialize variables
serviceID = data.ServiceID[starting_idx]
vehicle_idx = [starting_idx]
last_idx = starting_idx
all_dist =[]
check = []

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
        # using coordinates
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
            check.append(abs(dist - dist_formula))

# Compute the actual record indexes
actual_idx = [starting_idx]
for i in range(starting_idx + 1,len(data)):
    if data.ServiceID[i] == serviceID  :
        actual_idx.append(i)


vehicle_record = pseudonym_data.loc[vehicle_idx]

vehicle_pseudonym_changes_df = compile_pseudonym_changes(pseudonym_data,vehicle_idx)
actual_pseudonym_changes_df= compile_pseudonym_changes(pseudonym_data,actual_idx)

match_pseudonym_changes = pd.merge(vehicle_pseudonym_changes_df, actual_pseudonym_changes_df)
count_match_pseudonym_changes = match_pseudonym_changes.shape[0]

count = sum(item in vehicle_idx for item in actual_idx)
diff_count = sum(item not in actual_idx for item in vehicle_idx )

accuracy = 100 * (count / (count+(len(vehicle_idx)-len(actual_idx))+(len(actual_idx)-count)))
pseu_accuracy = 100 * (count_match_pseudonym_changes / (count_match_pseudonym_changes+(len(vehicle_pseudonym_changes_df)-len(actual_pseudonym_changes_df))+(len(actual_pseudonym_changes_df)-count_match_pseudonym_changes)))

print(f'                    ServiceID = {serviceID}')
print('-----------------------------------------------------------------')
print(f'Total Vehicle record found is {len(vehicle_idx)}')
print(f'Total Actual Record is {len(actual_idx)}')
print(f'Matched Record: {count}/{len(actual_idx)}')
print(f'There are {diff_count} predicted records found is wrong')
print('The accuracy of the predicted result is %.2f %%' % accuracy)
print()
print(f'Total Pseudonym changes found is {len(vehicle_pseudonym_changes_df)}')
print(f'Total Actual Pseudonym Cahnges is {len(actual_pseudonym_changes_df)}')
print(f'Matched Pseudonym Changes: {count_match_pseudonym_changes}/{len(actual_pseudonym_changes_df)}')
print(f'There are {len(vehicle_pseudonym_changes_df)-count_match_pseudonym_changes} predicted peudonym changes found is wrong')
print('The accuracy of the predicted result is %.2f %%' % pseu_accuracy)

        
        
        
        
        
        
        
        