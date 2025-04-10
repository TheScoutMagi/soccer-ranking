import os
import pandas as pd
import choix
import numpy as np

def calculate_bradley_terry_rankings(games_df):
    # Create a mapping of team names to indices
    teams = sorted(set(games_df['Team 1'].unique()) | set(games_df['Team 2'].unique()))
    team_to_idx = {team: idx for idx, team in enumerate(teams)}
    
    # Create pairwise comparison data
    comparisons = []
    for _, row in games_df.iterrows():
        if row['Team 1 Score'] > row['Team 2 Score']:
            comparisons.append((team_to_idx[row['Team 1']], team_to_idx[row['Team 2']]))
        elif row['Team 1 Score'] < row['Team 2 Score']:
            comparisons.append((team_to_idx[row['Team 2']], team_to_idx[row['Team 1']]))
    
    # Calculate Bradley-Terry rankings
    if comparisons:
        params = choix.ilsr_pairwise(len(teams), comparisons, alpha=0.01)
        # Convert to win probabilities
        win_probs = np.exp(params)
        win_probs = win_probs / win_probs.sum()
        
        # Create rankings DataFrame
        rankings = pd.DataFrame({
            'Team': teams,
            'Rating': params,
            'Win Probability': win_probs
        })
        
        # Sort by rating
        rankings = rankings.sort_values('Rating', ascending=False)
        rankings['Rank'] = range(1, len(rankings) + 1)
        
        return rankings
    return None

def generate_rankings_for_season(season, gender):
    # Construct the filename based on the parameters
    filename = f'games_ca_soccer_{season}_{gender}.csv'
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
    
    try:
        # Read the CSV file
        df = pd.read_csv(filepath)
        
        # Remove rows with TBA dates
        df = df[~df['Date'].str.contains('TBA', case=False, na=False)]
        
        # Convert scores to integers
        df['Team 1 Score'] = pd.to_numeric(df['Team 1 Score'], errors='coerce').fillna(0).astype(int)
        df['Team 2 Score'] = pd.to_numeric(df['Team 2 Score'], errors='coerce').fillna(0).astype(int)
        
        # Calculate rankings
        rankings = calculate_bradley_terry_rankings(df)
        
        if rankings is not None:
            # Save to CSV
            output_filename = f'rankings_{season}_{gender}.csv'
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
            rankings.to_csv(output_path, index=False)
            print(f"Saved rankings to {output_path}")
            return True
    except Exception as e:
        print(f"Error generating rankings for {season} {gender}: {str(e)}")
    return False

def generate_all_rankings():
    seasons = ['24-25', '23-24', '22-23', '21-22']
    genders = ['girls', 'boys']
    
    for season in seasons:
        for gender in genders:
            print(f"Generating rankings for {season} {gender}...")
            generate_rankings_for_season(season, gender)

if __name__ == '__main__':
    generate_all_rankings() 