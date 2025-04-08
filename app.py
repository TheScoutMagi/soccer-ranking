from flask import Flask, render_template, request
import pandas as pd
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

def get_states():
    return [
        {'code': 'USA', 'name': 'United States', 'enabled': True},
        {'code': 'CA', 'name': 'California', 'enabled': True},
        {'code': 'AL', 'name': 'Alabama', 'enabled': False},
        {'code': 'AK', 'name': 'Alaska', 'enabled': False},
        {'code': 'AZ', 'name': 'Arizona', 'enabled': False},
        {'code': 'AR', 'name': 'Arkansas', 'enabled': False},
        {'code': 'CO', 'name': 'Colorado', 'enabled': False},
        {'code': 'CT', 'name': 'Connecticut', 'enabled': False},
        {'code': 'DE', 'name': 'Delaware', 'enabled': False},
        {'code': 'FL', 'name': 'Florida', 'enabled': False},
        {'code': 'GA', 'name': 'Georgia', 'enabled': False},
        {'code': 'HI', 'name': 'Hawaii', 'enabled': False},
        {'code': 'ID', 'name': 'Idaho', 'enabled': False},
        {'code': 'IL', 'name': 'Illinois', 'enabled': False},
        {'code': 'IN', 'name': 'Indiana', 'enabled': False},
        {'code': 'IA', 'name': 'Iowa', 'enabled': False},
        {'code': 'KS', 'name': 'Kansas', 'enabled': False},
        {'code': 'KY', 'name': 'Kentucky', 'enabled': False},
        {'code': 'LA', 'name': 'Louisiana', 'enabled': False},
        {'code': 'ME', 'name': 'Maine', 'enabled': False},
        {'code': 'MD', 'name': 'Maryland', 'enabled': False},
        {'code': 'MA', 'name': 'Massachusetts', 'enabled': False},
        {'code': 'MI', 'name': 'Michigan', 'enabled': False},
        {'code': 'MN', 'name': 'Minnesota', 'enabled': False},
        {'code': 'MS', 'name': 'Mississippi', 'enabled': False},
        {'code': 'MO', 'name': 'Missouri', 'enabled': False},
        {'code': 'MT', 'name': 'Montana', 'enabled': False},
        {'code': 'NE', 'name': 'Nebraska', 'enabled': False},
        {'code': 'NV', 'name': 'Nevada', 'enabled': False},
        {'code': 'NH', 'name': 'New Hampshire', 'enabled': False},
        {'code': 'NJ', 'name': 'New Jersey', 'enabled': False},
        {'code': 'NM', 'name': 'New Mexico', 'enabled': False},
        {'code': 'NY', 'name': 'New York', 'enabled': False},
        {'code': 'NC', 'name': 'North Carolina', 'enabled': False},
        {'code': 'ND', 'name': 'North Dakota', 'enabled': False},
        {'code': 'OH', 'name': 'Ohio', 'enabled': False},
        {'code': 'OK', 'name': 'Oklahoma', 'enabled': False},
        {'code': 'OR', 'name': 'Oregon', 'enabled': False},
        {'code': 'PA', 'name': 'Pennsylvania', 'enabled': False},
        {'code': 'RI', 'name': 'Rhode Island', 'enabled': False},
        {'code': 'SC', 'name': 'South Carolina', 'enabled': False},
        {'code': 'SD', 'name': 'South Dakota', 'enabled': False},
        {'code': 'TN', 'name': 'Tennessee', 'enabled': False},
        {'code': 'TX', 'name': 'Texas', 'enabled': False},
        {'code': 'UT', 'name': 'Utah', 'enabled': False},
        {'code': 'VT', 'name': 'Vermont', 'enabled': False},
        {'code': 'VA', 'name': 'Virginia', 'enabled': False},
        {'code': 'WA', 'name': 'Washington', 'enabled': False},
        {'code': 'WV', 'name': 'West Virginia', 'enabled': False},
        {'code': 'WI', 'name': 'Wisconsin', 'enabled': False},
        {'code': 'WY', 'name': 'Wyoming', 'enabled': False}
    ]

def get_genders():
    return [
        {'code': 'girls', 'name': 'Girls', 'enabled': True},
        {'code': 'boys', 'name': 'Boys', 'enabled': False}
    ]

def get_seasons():
    return [
        {'code': 'all_time', 'name': 'All Time', 'enabled': True},
        {'code': '2024-2025', 'name': '2024-2025', 'enabled': True},
        {'code': '2023-2024', 'name': '2023-2024', 'enabled': True},
        {'code': '2022-2023', 'name': '2022-2023', 'enabled': True},
        {'code': '2021-2022', 'name': '2021-2022', 'enabled': False},
        {'code': '2020-2021', 'name': '2020-2021', 'enabled': False}
    ]

def load_rankings():
    df = pd.read_csv('rankings_2425_03122025.csv')
    # Sort by Total Points and PPG (Points Per Game) in descending order
    df = df.sort_values(['Total Points', 'PPG'], ascending=[False, False])
    return df

def load_game_results():
    df = pd.read_csv('scores_2425_03122025.csv')
    # Convert date to datetime and sort by date in descending order
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date', ascending=False)
    return df

def get_all_teams():
    rankings_df = load_rankings()
    return sorted(rankings_df['Team'].tolist())

@app.route('/')
def index():
    # Get filter parameters
    rankings_filter = request.args.get('rankings_filter', '').strip()
    results_filter = request.args.get('results_filter', '').strip()
    active_tab = request.args.get('active_tab', 'rankings')
    selected_state = request.args.get('state', 'USA')
    selected_gender = request.args.get('gender', 'girls')
    selected_season = request.args.get('season', '2024-2025')  # Default to 2024-2025 season
    
    # Load data
    rankings_df = load_rankings()
    game_results_df = load_game_results()
    
    # Apply filters if provided
    if rankings_filter:
        rankings_df = rankings_df[rankings_df['Team'].str.contains(rankings_filter, case=False)]
    
    if results_filter:
        game_results_df = game_results_df[
            (game_results_df['Home Team'].str.contains(results_filter, case=False)) | 
            (game_results_df['Away Team'].str.contains(results_filter, case=False))
        ]
    
    # Get all teams for the dropdown
    all_teams = get_all_teams()
    
    # Get states, genders, and seasons lists
    states = get_states()
    genders = get_genders()
    seasons = get_seasons()
    
    return render_template('index.html', 
                         rankings=rankings_df.to_dict('records'),
                         game_results=game_results_df.to_dict('records'),
                         all_teams=all_teams,
                         rankings_filter=rankings_filter,
                         results_filter=results_filter,
                         active_tab=active_tab,
                         states=states,
                         selected_state=selected_state,
                         genders=genders,
                         selected_gender=selected_gender,
                         seasons=seasons,
                         selected_season=selected_season)

if __name__ == '__main__':
    app.run(debug=False) 