import csv

# Initialize our 2 transporters
TRANSPORTER_1 = 1100000 - 72400
TRANSPORTER_2 = 1100000 - 85700

""" Convert the data from from the csv file
While we do so, we calculate the "best_value" as well. This value will indicate the valuepoints per gram and will be useful later on
"""
requirements = []
with open('nutzlast.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        requirements.append({
            'name': row['Hardware'],
            'required': int(row['benötigte Anzahl Einheiten in Bonn']),
            'weight': int(row['Gewicht (mit Verpackung und Zubehör) in g'].replace('.', '')),
            'value': int(row['Nutzwert je Hardware-Einheit (hoch=besser)']),
            'best_value': float(row['Nutzwert je Hardware-Einheit (hoch=besser)']) / int(row['Gewicht (mit Verpackung und Zubehör) in g'].replace('.', ''))
        })

# To optimize the search tree, we sort the items with the one with the best value per gram leading the list
requirements = sorted(requirements, key=lambda requirement: requirement['best_value'], reverse=True)

# We start out with a high score of zero to initialize the program
highscore = 0

# This is the highscore if we'd had a single transporter with the capacity of both
single_highscore = 0

# The combination storage is global to avoid many list mutations which cost us an enourmous amount of time
combination = [[0, 0] for x in requirements]


def fill_transporter(remaining_space_1, remaining_space_2, item_index=0, current_score=0):
    '''
    This is our tree function which fills the transporter recursivly for each iteration it knows the remaining space in each transporter,
    the index of the item next to place and the current score that was achieved with previous items
    '''
    global highscore, single_highscore

    # if we're done with all available types of items, it is about to check our new score
    if item_index >= len(requirements):

        '''
        If we achieved a new highscore, print out some information about it
        change current_score > highscore to current_score >= highscore if you want to see more than one solution
        '''
        if current_score > highscore:
            highscore = current_score
            print("="*30)
            print("Total Score: ", highscore)
            print("Remaining Space: ", remaining_space_1 + remaining_space_2)
            print("-"*30)
            for index, item in enumerate(combination):
                print(requirements[index]['name'], "\t", item[0], "\t", item[1])
            print()

            # Check if the score is the final highscore, comment this out if you want more than one solution
            if current_score >= single_highscore:
                return True
        return

    # Check out the current item of the search tree
    current_item = requirements[item_index]

    '''
    At this point check, if it is theoretically possible to get a higher score down the tree.
    We know that the remaining score, that is required equals the highscore minus the score we already have on this branch
    We also know that the value per gram decreases down our search tree. so the maximum achievable score is the total remaining space
    times the value per gram for this item

    If that value is lower than the required score for a new highscore, we can skip this branch
    '''
    if (remaining_space_1 + remaining_space_2) * current_item['best_value'] < highscore - current_score:
        return

    # Now we check the upper boundry of this iteration. We can only fit as much items into the transporter as there is space remaining
    max_items_in_transporter_1 = remaining_space_1 // current_item['weight']
    max_items_in_transporter_2 = remaining_space_2 // current_item['weight']

    # Since there is no need to transport more items than required, we will start at the minimum of items required and maximum weight
    max_items_total = min(max_items_in_transporter_1, current_item['required'])

    # This loop will create every possible amount of items for the current branch
    for items_in_transporter_1 in range(max_items_total, -1, -1):

        # For transporter 2 we do only need the rest of the items, that was not already put into transporter 1 and also not more than there is space available
        max_available_items_in_transporter_2 = min(max_items_in_transporter_2, current_item['required'] - items_in_transporter_1)

        # Create every possible amount of the current item in transporter 2
        for items_in_transporter_2 in range(max_available_items_in_transporter_2, -1, -1):

            # Compute remaining space in transporters
            current_remaining_space_transporter_1 = remaining_space_1 - items_in_transporter_1 * current_item['weight']
            current_remaining_space_transporter_2 = remaining_space_2 - items_in_transporter_2 * current_item['weight']

            # Compute new score
            new_score = current_score + (items_in_transporter_1 + items_in_transporter_2) * current_item['value']

            # Update combination
            combination[item_index][0] = items_in_transporter_1
            combination[item_index][1] = items_in_transporter_2

            # Continue with the next item. If the highest score was found, propagate that back to the root
            if fill_transporter(current_remaining_space_transporter_1, current_remaining_space_transporter_2, item_index + 1, new_score):
                return True


def fill_single_transporter(remaining_space_1, item_index=0, current_score=0):
    '''
    This function will fill a single transporter and store the highest possible score in the global single_highscore
    '''
    global single_highscore

    # Same code as in fill transporter without the print of highscores
    if item_index >= len(requirements):
        if current_score >= single_highscore:
            single_highscore = current_score
        return
    current_item = requirements[item_index]

    '''
    Here we take a shortcut: if at one layer it is technically not possible anymore to achieve a higher score,
    it makes no sense to decrease the number of higher valued items
    '''
    if (remaining_space_1) * current_item['best_value'] < single_highscore - current_score:
        return True

    # Same code as in fill transporter with the code for the second transporter removed
    max_items_in_transporter_1 = remaining_space_1 // current_item['weight']
    max_items_total = min(max_items_in_transporter_1, current_item['required'])
    for items_in_transporter_1 in range(max_items_total, -1, -1):
        current_remaining_space_transporter_1 = remaining_space_1 - items_in_transporter_1 * current_item['weight']
        new_score = current_score + items_in_transporter_1 * current_item['value']

        # Here the shortcut will stop the decrease on the layer and continue one layer above
        if fill_single_transporter(current_remaining_space_transporter_1, item_index + 1, new_score):
            break


# Start the tree search
fill_single_transporter(TRANSPORTER_1 + TRANSPORTER_2)

# Start full search
if fill_transporter(TRANSPORTER_1, TRANSPORTER_2):
    print("Highest possible score was achived.")
else:
    print("Full tree search finished.")
