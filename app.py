from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from datetime import datetime
import glob

app = Flask(__name__)

def get_states():
    return [
        {'code': 'USA', 'name': 'USA', 'enabled': True},
        {'code': 'CA', 'name': 'California', 'enabled': True},
        {'code': 'TX', 'name': 'Texas', 'enabled': False},
        {'code': 'FL', 'name': 'Florida', 'enabled': False},
        {'code': 'NY', 'name': 'New York', 'enabled': False},
        {'code': 'IL', 'name': 'Illinois', 'enabled': False},
        {'code': 'PA', 'name': 'Pennsylvania', 'enabled': False},
        {'code': 'OH', 'name': 'Ohio', 'enabled': False},
        {'code': 'GA', 'name': 'Georgia', 'enabled': False},
        {'code': 'NC', 'name': 'North Carolina', 'enabled': False},
        {'code': 'MI', 'name': 'Michigan', 'enabled': False},
        {'code': 'NJ', 'name': 'New Jersey', 'enabled': False},
        {'code': 'VA', 'name': 'Virginia', 'enabled': False},
        {'code': 'WA', 'name': 'Washington', 'enabled': False},
        {'code': 'AZ', 'name': 'Arizona', 'enabled': False},
        {'code': 'MA', 'name': 'Massachusetts', 'enabled': False},
        {'code': 'TN', 'name': 'Tennessee', 'enabled': False},
        {'code': 'IN', 'name': 'Indiana', 'enabled': False},
        {'code': 'MO', 'name': 'Missouri', 'enabled': False},
        {'code': 'MD', 'name': 'Maryland', 'enabled': False},
        {'code': 'WI', 'name': 'Wisconsin', 'enabled': False},
        {'code': 'MN', 'name': 'Minnesota', 'enabled': False},
        {'code': 'CO', 'name': 'Colorado', 'enabled': False},
        {'code': 'AL', 'name': 'Alabama', 'enabled': False},
        {'code': 'SC', 'name': 'South Carolina', 'enabled': False},
        {'code': 'LA', 'name': 'Louisiana', 'enabled': False},
        {'code': 'KY', 'name': 'Kentucky', 'enabled': False},
        {'code': 'OR', 'name': 'Oregon', 'enabled': False},
        {'code': 'OK', 'name': 'Oklahoma', 'enabled': False},
        {'code': 'CT', 'name': 'Connecticut', 'enabled': False},
        {'code': 'UT', 'name': 'Utah', 'enabled': False},
        {'code': 'IA', 'name': 'Iowa', 'enabled': False},
        {'code': 'NV', 'name': 'Nevada', 'enabled': False},
        {'code': 'AR', 'name': 'Arkansas', 'enabled': False},
        {'code': 'MS', 'name': 'Mississippi', 'enabled': False},
        {'code': 'KS', 'name': 'Kansas', 'enabled': False},
        {'code': 'NM', 'name': 'New Mexico', 'enabled': False},
        {'code': 'NE', 'name': 'Nebraska', 'enabled': False},
        {'code': 'WV', 'name': 'West Virginia', 'enabled': False},
        {'code': 'ID', 'name': 'Idaho', 'enabled': False},
        {'code': 'HI', 'name': 'Hawaii', 'enabled': False},
        {'code': 'NH', 'name': 'New Hampshire', 'enabled': False},
        {'code': 'ME', 'name': 'Maine', 'enabled': False},
        {'code': 'MT', 'name': 'Montana', 'enabled': False},
        {'code': 'RI', 'name': 'Rhode Island', 'enabled': False},
        {'code': 'DE', 'name': 'Delaware', 'enabled': False},
        {'code': 'SD', 'name': 'South Dakota', 'enabled': False},
        {'code': 'ND', 'name': 'North Dakota', 'enabled': False},
        {'code': 'AK', 'name': 'Alaska', 'enabled': False},
        {'code': 'DC', 'name': 'District of Columbia', 'enabled': False},
        {'code': 'VT', 'name': 'Vermont', 'enabled': False},
        {'code': 'WY', 'name': 'Wyoming', 'enabled': False}
    ]

def get_genders():
    return [
        {'code': 'girls', 'name': 'Girls', 'enabled': True},
        {'code': 'boys', 'name': 'Boys', 'enabled': True}
    ]

def get_seasons():
    return [
        {'code': '24-25', 'name': '2024-2025', 'enabled': True},
        {'code': '23-24', 'name': '2023-2024', 'enabled': True},
        {'code': '22-23', 'name': '2022-2023', 'enabled': True},
        {'code': '21-22', 'name': '2021-2022', 'enabled': True}
    ]

def load_rankings(season, gender, team_filter=None):
    try:
        filename = f'rankings_{season}_{gender}.csv'
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
        df = pd.read_csv(filepath)
        
        if team_filter:
            df = df[df['Team'] == team_filter]
        
        # Get recent results for each team
        games_filename = f'games_ca_soccer_{season}_{gender}.csv'
        games_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', games_filename)
        games_df = pd.read_csv(games_filepath)
        
        # Convert scores to integers
        games_df['Team 1 Score'] = pd.to_numeric(games_df['Team 1 Score'], errors='coerce').fillna(0).astype(int)
        games_df['Team 2 Score'] = pd.to_numeric(games_df['Team 2 Score'], errors='coerce').fillna(0).astype(int)
        
        # Add recent results to each team
        rankings_list = []
        for _, team in df.iterrows():
            team_name = team['Team']
            
            # Get team's recent games
            team_games = games_df[
                (games_df['Team 1'] == team_name) | 
                (games_df['Team 2'] == team_name)
            ].sort_values('Date', ascending=False).head(5)
            
            # Determine result for each game
            recent_results = []
            for _, game in team_games.iterrows():
                if game['Team 1'] == team_name:
                    if game['Team 1 Score'] > game['Team 2 Score']:
                        recent_results.append('win')
                    elif game['Team 1 Score'] < game['Team 2 Score']:
                        recent_results.append('loss')
                    else:
                        recent_results.append('tie')
                else:
                    if game['Team 2 Score'] > game['Team 1 Score']:
                        recent_results.append('win')
                    elif game['Team 2 Score'] < game['Team 1 Score']:
                        recent_results.append('loss')
                    else:
                        recent_results.append('tie')
            
            # Add recent results to team data
            team_dict = team.to_dict()
            team_dict['recent_results'] = recent_results
            rankings_list.append(team_dict)
        
        return rankings_list
    except Exception as e:
        print(f"Error loading rankings: {str(e)}")
        return []

def get_game_results(state, season, gender, page=1, per_page=20, team_filter=None):
    if state == 'USA':
        state = 'CA'  # For now, only California data is available
    
    # Construct the filename based on the parameters
    filename = f'games_{state.lower()}_soccer_{season}_{gender}.csv'
    # Use the absolute path to the data directory
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
    
    print(f"Attempting to read game results from: {filepath}")  # Debug log
    
    try:
        # Read the CSV file
        df = pd.read_csv(filepath)
        print(f"Successfully read {len(df)} rows from {filepath}")  # Debug log
        
        # Convert date to datetime and sort by date
        # First, let's see what the date format looks like
        print(f"Sample date: {df['Date'].iloc[0]}")
        
        # Determine the base year based on the season
        if season == '24-25':
            base_year = 2024
        elif season == '23-24':
            base_year = 2023
        elif season == '22-23':
            base_year = 2022
        elif season == '21-22':
            base_year = 2021
        else:
            base_year = datetime.now().year
        
        # Remove rows with TBA dates
        df = df[~df['Date'].str.contains('TBA', case=False, na=False)]
        
        # Try to parse dates and filter out invalid ones
        valid_dates = []
        for date_str in df['Date']:
            try:
                # Parse the month from the date string
                month = int(date_str.split('/')[0])
                # If month is June or later, use base_year, otherwise use base_year + 1
                year = base_year if month >= 6 else base_year + 1
                # Add year to the date string
                date_with_year = f"{date_str}/{year}"
                pd.to_datetime(date_with_year, format='%m/%d/%Y')
                valid_dates.append(True)
            except:
                valid_dates.append(False)
        
        # Filter out invalid dates
        df = df[pd.Series(valid_dates, index=df.index)]
        
        # Parse valid dates with correct year
        def add_correct_year(date_str):
            month = int(date_str.split('/')[0])
            year = base_year if month >= 6 else base_year + 1
            return f"{date_str}/{year}"
        
        df['Date'] = df['Date'].apply(add_correct_year)
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
        
        # Apply team filter if provided
        if team_filter:
            team_filter = team_filter.lower()
            # Only keep games where the team is playing at home
            df = df[df['Team 1'].str.lower().str.contains(team_filter)]
        else:
            # If no team filter, keep all home games
            df = df
        
        df = df.sort_values('Date', ascending=False)
        
        # Format the date for display
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # Convert scores to integers
        df['Team 1 Score'] = pd.to_numeric(df['Team 1 Score'], errors='coerce').fillna(0).astype(int)
        df['Team 2 Score'] = pd.to_numeric(df['Team 2 Score'], errors='coerce').fillna(0).astype(int)
        
        # Select and rename columns for display
        df = df[['Date', 'Team 1', 'Team 2', 'Team 1 Score', 'Team 2 Score', 'Game Type']]
        df.columns = ['Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Game Type']
        
        # Calculate pagination
        total_results = len(df)
        total_pages = (total_results + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        # Get the paginated results
        paginated_df = df.iloc[start_idx:end_idx]
        
        # Convert to list of dictionaries for the template
        results = paginated_df.to_dict('records')
        print(f"Converted {len(results)} records for display")  # Debug log
        
        return {
            'results': results,
            'total_results': total_results,
            'total_pages': total_pages,
            'current_page': page,
            'per_page': per_page
        }
    except FileNotFoundError:
        print(f"File not found: {filepath}")  # Debug log
        return {
            'results': [],
            'total_results': 0,
            'total_pages': 0,
            'current_page': page,
            'per_page': per_page
        }
    except Exception as e:
        print(f"Error reading game results: {str(e)}")  # Debug log
        return {
            'results': [],
            'total_results': 0,
            'total_pages': 0,
            'current_page': page,
            'per_page': per_page
        }

def get_teams(season, gender):
    try:
        filename = f'rankings_{season}_{gender}.csv'
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
        df = pd.read_csv(filepath)
        return sorted(df['Team'].tolist())
    except Exception as e:
        print(f"Error getting teams: {str(e)}")
        return []

def get_team_info(team_name, season, gender):
    try:
        # Read the games CSV file
        filename = f'games_ca_soccer_{season}_{gender}.csv'
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
        df = pd.read_csv(filepath)
        
        # Get team's home games (Team 1 is home team)
        team_games = df[df['Team 1'] == team_name]
        
        if len(team_games) > 0:
            # Get the first home game which should have the team's info
            team_info = team_games.iloc[0]
            # Convert zip code to integer, keeping only first 5 digits
            try:
                zip_str = str(team_info['Team 1 Zipcode'])
                # Remove any non-digits and take first 5 digits
                zip_digits = ''.join(filter(str.isdigit, zip_str))[:5]
                zip_code = int(zip_digits) if len(zip_digits) == 5 else 0
            except (ValueError, KeyError):
                zip_code = 0
                
            return {
                'city': team_info['Team 1 City'],
                'state': team_info['Team 1 State'],
                'address': team_info['Team 1 Address'],
                'zip_code': zip_code
            }
        else:
            # If no home games found, try away games
            team_games = df[df['Team 2'] == team_name]
            if len(team_games) > 0:
                team_info = team_games.iloc[0]
                # Convert zip code to integer, keeping only first 5 digits
                try:
                    zip_str = str(team_info['Team 2 Zipcode'])
                    # Remove any non-digits and take first 5 digits
                    zip_digits = ''.join(filter(str.isdigit, zip_str))[:5]
                    zip_code = int(zip_digits) if len(zip_digits) == 5 else 0
                except (ValueError, KeyError):
                    zip_code = 0
                    
                return {
                    'city': team_info['Team 2 City'],
                    'state': team_info['Team 2 State'],
                    'address': team_info['Team 2 Address'],
                    'zip_code': zip_code
                }
            
        # If no games found at all
        return {
            'city': 'N/A',
            'state': 'N/A',
            'address': 'N/A',
            'zip_code': 0
        }
        
    except Exception as e:
        print(f"Error getting team info: {str(e)}")
        return {
            'city': 'N/A',
            'state': 'N/A',
            'address': 'N/A',
            'zip_code': 0
        }

def get_historical_rankings(team_name, season, gender):
    try:
        # Read all historical rankings files for the season
        rankings_history = []
        dates = []
        
        # Get list of ranking files sorted by date
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        pattern = f'rankings_{season}_{gender}_*.csv'
        ranking_files = sorted(glob.glob(os.path.join(data_dir, pattern)))
        
        for file_path in ranking_files:
            # Extract date from filename
            date_str = file_path.split('_')[-1].replace('.csv', '')
            date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
            
            # Read rankings
            df = pd.read_csv(file_path)
            team_rank = df[df['Team'] == team_name]['Rank'].iloc[0] if len(df[df['Team'] == team_name]) > 0 else None
            
            if team_rank is not None:
                rankings_history.append(team_rank)
                dates.append(date)
        
        return dates, rankings_history
    except Exception as e:
        print(f"Error getting historical rankings: {str(e)}")
        return [], []

@app.route('/')
def index():
    selected_state = request.args.get('state', 'USA')
    selected_gender = request.args.get('gender', 'girls')
    selected_season = request.args.get('season', '24-25')
    selected_team = request.args.get('team', '')
    
    states = get_states()
    genders = get_genders()
    seasons = get_seasons()
    teams = get_teams(selected_season, selected_gender)
    
    # Get rankings based on selected filters
    rankings = load_rankings(selected_season, selected_gender, selected_team)
    
    return render_template('index.html',
                         states=states,
                         selected_state=selected_state,
                         genders=genders,
                         selected_gender=selected_gender,
                         seasons=seasons,
                         selected_season=selected_season,
                         teams=teams,
                         selected_team=selected_team,
                         rankings=rankings)

@app.route('/get_teams')
def get_teams_endpoint():
    state = request.args.get('state', 'USA')
    season = request.args.get('season', '24-25')
    gender = request.args.get('gender', 'girls')
    search_term = request.args.get('q', '').lower()
    
    teams = get_teams(season, gender)
    filtered_teams = [team for team in teams if search_term in team.lower()]
    
    return jsonify({'teams': filtered_teams})

@app.route('/team/<team_name>')
def team_results(team_name):
    selected_state = request.args.get('state', 'USA')
    selected_gender = request.args.get('gender', 'girls')
    selected_season = request.args.get('season', '24-25')
    
    # Get team's games
    games = get_game_results(selected_state, selected_season, selected_gender, team_filter=team_name)
    
    return render_template('team_results.html',
                         team_name=team_name,
                         games=games['results'],
                         state=selected_state,
                         gender=selected_gender,
                         season=selected_season)

@app.route('/team-details/<team_name>')
def team_details(team_name):
    selected_state = request.args.get('state', 'USA')
    selected_gender = request.args.get('gender', 'girls')
    selected_season = request.args.get('season', '24-25')
    
    # Get team information
    team_info = get_team_info(team_name, selected_season, selected_gender)
    
    # Get historical rankings
    dates, rankings_history = get_historical_rankings(team_name, selected_season, selected_gender)
    
    return render_template('team_details.html',
                         team_name=team_name,
                         team_info=team_info,
                         dates=dates,
                         rankings_history=rankings_history)

if __name__ == '__main__':
    app.run(debug=False) 