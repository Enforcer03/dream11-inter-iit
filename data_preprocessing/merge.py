import json
from tqdm import tqdm

def merge_json_files(till_training_file, after_training_file, output_file):
    """
    Merge two JSON files containing player data from before and after training dates.
    
    Args:
        till_training_file (str): Path to the JSON file with data till training date
        after_training_file (str): Path to the JSON file with data after training date
        output_file (str): Path where the merged JSON file will be saved
    """
    try:
        # Read data from till training file
        with open(till_training_file, 'r', encoding='utf-8') as f:
            till_training_data = json.load(f)
        
        # Read data from after training file
        with open(after_training_file, 'r', encoding='utf-8') as f:
            after_training_data = json.load(f)
        
        # Merge data
        merged_data = {}
        
        # Add all players from till training data
        for player, matches in tqdm(till_training_data.items()):
            if player not in merged_data:
                merged_data[player] = {}
            merged_data[player].update(matches)
        
        # Add all players from after training data
        for player, matches in tqdm(after_training_data.items()):
            if player not in merged_data:
                merged_data[player] = {}
            merged_data[player].update(matches)
        
        # Write merged data to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4)
        
        print(f"Successfully merged data and saved to {output_file}")
        print(f"Total players in merged data: {len(merged_data)}")
        
    except Exception as e:
        print(f"Error merging files: {str(e)}")

def main():
    # Merge T20 data
    print("\nMerging T20 data...")
    merge_json_files(
        'T20_till_training_date_player_match_data.json',
        'T20_after_training_date_player_match_data.json',
        'T20_combined_player_match_data.json'
    )
    
    # Merge ODI/ODM data
    print("\nMerging ODI/ODM data...")
    merge_json_files(
        'ODI_ODM_till_training_date_player_match_data.json',
        'ODI_ODM_after_training_date_player_match_data.json',
        'ODI_ODM_combined_player_match_data.json'
    )
    
    # Merge MDM Test data
    print("\nMerging MDM Test data...")
    merge_json_files(
        'MDM_Test_till_training_date_player_match_data.json',
        'MDM_Test_after_training_date_player_match_data.json',
        'MDM_Test_combined_player_match_data.json'
    )

if __name__ == "__main__":
    main()