#!/usr/bin/env python3

"""
Lahman Baseball Database Analysis Project

This project analyzes real MLB hitting data from the Lahman Baseball Database:
1. Load and process Batting, People, and Teams tables
2. Calculate advanced hitting metrics and sabermetrics
3. Analyze historical trends and era effects
4. Perform statistical analysis on player performance
5. Identify Hall of Fame caliber players using machine learning
6. Create comprehensive visualizations and reports

Required Lahman DB Tables:
- Batting.csv (or batting table)
- People.csv (or people/master table) 
- Teams.csv (or teams table)

Author: Baseball Analytics Team
Date: 2025-08-26
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings

warnings.filterwarnings('ignore')
plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')

# ------------------------------------------------------------------
# 1️⃣ Data Loading and Preprocessing
# ------------------------------------------------------------------

def load_lahman_data(data_path='./'):

    """
    Load Lahman Baseball Database tables.
    
    Expected file structure:
    - Batting.csv: Player batting statistics by year
    - People.csv: Player biographical information  
    - Teams.csv: Team information
    """
    
    print("Loading Lahman Baseball Database...")
    
    try:
        # Load main tables
        batting = pd.read_csv(f'{data_path}Batting.csv')
        people = pd.read_csv(f'{data_path}People.csv')
        teams = pd.read_csv(f'{data_path}Teams.csv')
        
        print(f"✓ Batting data: {len(batting)} records")
        print(f"✓ People data: {len(people)} players") 
        print(f"✓ Teams data: {len(teams)} team-seasons")
        
        # Basic data info
        print(f"Years covered: {batting['yearID'].min()} - {batting['yearID'].max()}")
        print(f"Total unique players: {batting['playerID'].nunique()}")
        
        return batting, people, teams
        
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        print("Please ensure Lahman CSV files are in the specified directory")
        return None, None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None

def preprocess_batting_data(batting, people, teams, min_year=1950, min_ab=100):
    
    """Clean and preprocess batting data with advanced metrics."""
    
    print(f"\nPreprocessing batting data (>= {min_year}, >= {min_ab} AB)...")
    
    # Filter modern era and minimum at-bats
    batting_clean = batting[
        (batting['yearID'] >= min_year) & 
        (batting['AB'] >= min_ab)
    ].copy()
    
    print(f"Records after filtering: {len(batting_clean)}")
    
    # Fill missing values
    numeric_cols = ['H', 'AB', 'BB', 'SO', 'HBP', 'SF', 'SH', 'GIDP']
    for col in numeric_cols:
        if col in batting_clean.columns:
            batting_clean[col] = batting_clean[col].fillna(0)
    
    # Calculate basic metrics
    batting_clean['AVG'] = batting_clean['H'] / batting_clean['AB']
    batting_clean['OBP'] = (batting_clean['H'] + batting_clean['BB'] + batting_clean['HBP']) / (
        batting_clean['AB'] + batting_clean['BB'] + batting_clean['HBP'] + batting_clean['SF']
    )
    batting_clean['SLG'] = (
        batting_clean['H'] + batting_clean['2B'] + 2*batting_clean['3B'] + 3*batting_clean['HR']
    ) / batting_clean['AB']
    
    # Advanced metrics
    batting_clean['OPS'] = batting_clean['OBP'] + batting_clean['SLG']
    batting_clean['ISO'] = batting_clean['SLG'] - batting_clean['AVG']
    
    # Rate stats
    batting_clean['BB_rate'] = batting_clean['BB'] / (batting_clean['AB'] + batting_clean['BB'])
    batting_clean['K_rate'] = batting_clean['SO'] / (batting_clean['AB'] + batting_clean['BB'])
    batting_clean['HR_rate'] = batting_clean['HR'] / batting_clean['AB']
    
    # Calculate singles
    batting_clean['1B'] = batting_clean['H'] - batting_clean['2B'] - batting_clean['3B'] - batting_clean['HR']
    
    # wOBA calculation (using modern weights)
    woba_weights = {
        'BB': 0.692, 'HBP': 0.722, '1B': 0.883,
        '2B': 1.238, '3B': 1.558, 'HR': 1.979
    }
    
    plate_appearances = (batting_clean['AB'] + batting_clean['BB'] + 
                        batting_clean['HBP'] + batting_clean['SF'] + batting_clean['SH'])
    
    batting_clean['wOBA'] = (
        woba_weights['BB'] * batting_clean['BB'] +
        woba_weights['HBP'] * batting_clean['HBP'] +
        woba_weights['1B'] * batting_clean['1B'] +
        woba_weights['2B'] * batting_clean['2B'] +
        woba_weights['3B'] * batting_clean['3B'] +
        woba_weights['HR'] * batting_clean['HR']
    ) / plate_appearances
    
    # Merge with player info
    if people is not None:
        people_subset = people[['playerID', 'nameFirst', 'nameLast', 'birthYear', 'debut', 'finalGame']].copy()
        batting_enhanced = batting_clean.merge(people_subset, on='playerID', how='left')
        batting_enhanced['fullName'] = batting_enhanced['nameFirst'] + ' ' + batting_enhanced['nameLast']
        batting_enhanced['age'] = batting_enhanced['yearID'] - batting_enhanced['birthYear']
    else:
        batting_enhanced = batting_clean.copy()
        batting_enhanced['fullName'] = batting_enhanced['playerID']
        batting_enhanced['age'] = np.nan
    
    print(f"Final dataset: {len(batting_enhanced)} player-seasons")
    return batting_enhanced

# ------------------------------------------------------------------
# 2️⃣ Historical Trend Analysis
# ------------------------------------------------------------------

def analyze_historical_trends(df):
    
    """Analyze how hitting metrics have changed over time."""
    
    print(f"\n{'='*60}")
    print("HISTORICAL TRENDS ANALYSIS")
    print('='*60)
    
    # Calculate yearly league averages
    yearly_stats = df.groupby('yearID').agg({
        'AVG': 'mean',
        'OBP': 'mean', 
        'SLG': 'mean',
        'OPS': 'mean',
        'HR': 'sum',
        'SO': 'sum',
        'AB': 'sum',
        'playerID': 'count'
    }).round(3)
    
    yearly_stats['HR_per_game'] = yearly_stats['HR'] / (yearly_stats['playerID'] * 162 / 30)  # Approximate
    yearly_stats['K_rate_league'] = yearly_stats['SO'] / yearly_stats['AB']
    
    print("Key Historical Trends:")
    print("-" * 30)
    
    # Define eras
    eras = {
        'Dead Ball Era': (1950, 1963),
        'Expansion Era': (1964, 1976), 
        'Free Agency Era': (1977, 1992),
        'Steroid Era': (1993, 2006),
        'Modern Era': (2007, 2024)
    }
    
    for era_name, (start, end) in eras.items():
        era_data = yearly_stats[(yearly_stats.index >= start) & (yearly_stats.index <= end)]
        if len(era_data) > 0:
            print(f"\n{era_name} ({start}-{end}):")
            print(f"  Average BA:  {era_data['AVG'].mean():.3f}")
            print(f"  Average OBP: {era_data['OBP'].mean():.3f}")
            print(f"  Average SLG: {era_data['SLG'].mean():.3f}")
            print(f"  Average OPS: {era_data['OPS'].mean():.3f}")
            print(f"  K Rate:      {era_data['K_rate_league'].mean():.3f}")
    
    # Find significant trend changes using scipy
    years = yearly_stats.index.values
    ops_values = yearly_stats['OPS'].values
    
    # Fit polynomial trends
    coeffs = np.polyfit(years, ops_values, 2)
    polynomial = np.poly1d(coeffs)
    
    print(f"\nOPS Trend Analysis:")
    print(f"Quadratic fit: OPS = {coeffs[0]:.6f}*year² + {coeffs[1]:.4f}*year + {coeffs[2]:.2f}")
    
    # Find turning point
    turning_point = -coeffs[1] / (2 * coeffs[0])
    print(f"Trend turning point: {turning_point:.1f}")
    
    return yearly_stats

# ------------------------------------------------------------------
# 3️⃣ Player Career Analysis
# ------------------------------------------------------------------

def analyze_player_careers(df):
    """Analyze individual player career trajectories."""
    
    print(f"\n{'='*60}")
    print("PLAYER CAREER ANALYSIS")
    print('='*60)
    
    # Calculate career totals and averages
    career_stats = df.groupby('playerID').agg({
        'yearID': ['min', 'max', 'count'],
        'G': 'sum',
        'AB': 'sum', 
        'H': 'sum',
        'HR': 'sum',
        'RBI': 'sum',
        'BB': 'sum',
        'SO': 'sum',
        'OPS': 'mean',
        'wOBA': 'mean',
        'fullName': 'first',
        'age': 'mean'
    }).round(3)
    
    # Flatten column names
    career_stats.columns = ['_'.join(col).strip('_') for col in career_stats.columns]
    career_stats = career_stats.rename(columns={
        'yearID_min': 'debut_year',
        'yearID_max': 'final_year', 
        'yearID_count': 'seasons',
        'fullName_first': 'name',
        'age_mean': 'avg_age'
    })
    
    # Calculate career length and rate stats
    career_stats['career_length'] = career_stats['final_year'] - career_stats['debut_year'] + 1
    career_stats['career_AVG'] = career_stats['H_sum'] / career_stats['AB_sum']
    career_stats['career_HR_rate'] = career_stats['HR_sum'] / career_stats['AB_sum']
    career_stats['career_BB_rate'] = career_stats['BB_sum'] / (career_stats['AB_sum'] + career_stats['BB_sum'])
    
    # Filter for significant careers (min 3000 AB)
    significant_careers = career_stats[career_stats['AB_sum'] >= 3000].copy()
    
    print(f"Players with 3000+ career AB: {len(significant_careers)}")
    
    # Identify different player types using clustering
    features = ['career_AVG', 'career_HR_rate', 'career_BB_rate', 'OPS_mean']
    X = significant_careers[features].dropna()
    
    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Hierarchical clustering
    linkage_matrix = linkage(X_scaled, method='ward')
    clusters = fcluster(linkage_matrix, 4, criterion='maxclust')
    
    significant_careers.loc[X.index, 'player_type'] = clusters
    
    # Define player types
    cluster_names = {1: 'Contact Hitters', 2: 'Power Hitters', 3: 'Balanced', 4: 'Patient Hitters'}
    
    print("\nPlayer Type Analysis (Career 3000+ AB):")
    print("-" * 45)
    for cluster_id in sorted(significant_careers['player_type'].unique()):
        if pd.isna(cluster_id):
            continue
        cluster_players = significant_careers[significant_careers['player_type'] == cluster_id]
        
        print(f"\n{cluster_names.get(cluster_id, f'Cluster {cluster_id}')} ({len(cluster_players)} players):")
        print(f"  Avg BA:      {cluster_players['career_AVG'].mean():.3f}")
        print(f"  Avg OPS:     {cluster_players['OPS_mean'].mean():.3f}")
        print(f"  Avg HR Rate: {cluster_players['career_HR_rate'].mean():.4f}")
        print(f"  Avg BB Rate: {cluster_players['career_BB_rate'].mean():.3f}")
        
        # Top players in cluster
        top_players = cluster_players.nlargest(3, 'OPS_mean')
        print(f"  Top players: {', '.join(top_players['name'].values)}")
    
    return significant_careers

# ------------------------------------------------------------------
# 4️⃣ Era-Adjusted Performance Analysis
# ------------------------------------------------------------------

def calculate_era_adjustments(df):
    """Calculate era-adjusted statistics to compare players across different periods."""
    
    print(f"\n{'='*60}")
    print("ERA-ADJUSTED PERFORMANCE ANALYSIS")
    print('='*60)
    
    # Calculate league averages by year
    league_avg = df.groupby('yearID').agg({
        'AVG': 'mean',
        'OBP': 'mean',
        'SLG': 'mean', 
        'OPS': 'mean'
    }).add_suffix('_lg')
    
    # Merge league averages
    df_era = df.merge(league_avg, left_on='yearID', right_index=True, how='left')
    
    # Calculate era-adjusted stats (player stat / league average * 100)
    df_era['AVG_plus'] = (df_era['AVG'] / df_era['AVG_lg'] * 100).round(1)
    df_era['OBP_plus'] = (df_era['OBP'] / df_era['OBP_lg'] * 100).round(1)
    df_era['SLG_plus'] = (df_era['SLG'] / df_era['SLG_lg'] * 100).round(1)
    df_era['OPS_plus'] = (df_era['OPS'] / df_era['OPS_lg'] * 100).round(1)
    
    # Identify extreme performances
    print("Most Dominant Single Seasons (OPS+):")
    print("-" * 40)
    
    # Filter for minimum plate appearances
    qualified = df_era[df_era['AB'] >= 400].copy()
    top_seasons = qualified.nlargest(10, 'OPS_plus')
    
    for idx, season in top_seasons.iterrows():
        print(f"{season.get('fullName', season['playerID']):25s} {season['yearID']} - "
              f"OPS+: {season['OPS_plus']:5.1f} (OPS: {season['OPS']:.3f})")
    
    return df_era

# ------------------------------------------------------------------
# 5️⃣ Statistical Analysis Functions
# ------------------------------------------------------------------

def perform_statistical_tests(df):
    """Perform various statistical tests on baseball data."""
    
    print(f"\n{'='*60}")
    print("STATISTICAL HYPOTHESIS TESTING")
    print('='*60)
    
    # Test 1: Has offensive performance changed significantly over time?
    modern_data = df[df['yearID'] >= 2000].copy()
    
    if len(modern_data) > 0:
        # Correlation between year and OPS
        year_ops_corr, p_val = stats.pearsonr(modern_data['yearID'], modern_data['OPS'].dropna())
        print(f"Test 1: Year vs OPS Correlation (2000+)")
        print(f"Correlation: {year_ops_corr:.4f}, p-value: {p_val:.6f}")
        print(f"Significant trend: {'Yes' if p_val < 0.05 else 'No'}")
    
    # Test 2: Do left-handed batters perform differently?
    if 'bats' in df.columns:
        left_handed = df[df['bats'] == 'L']['OPS'].dropna()
        right_handed = df[df['bats'] == 'R']['OPS'].dropna()
        
        if len(left_handed) > 0 and len(right_handed) > 0:
            t_stat, p_val = stats.ttest_ind(left_handed, right_handed)
            print(f"\nTest 2: Left vs Right-Handed Batters (OPS)")
            print(f"Left-handed OPS:  {left_handed.mean():.3f}")
            print(f"Right-handed OPS: {right_handed.mean():.3f}")
            print(f"T-statistic: {t_stat:.3f}, p-value: {p_val:.6f}")
            print(f"Significant difference: {'Yes' if p_val < 0.05 else 'No'}")
    
    # Test 3: Is there a home field advantage in offensive stats?
    if 'lgID' in df.columns:
        # Compare AL vs NL (proxy for different rules/parks)
        al_data = df[df['lgID'] == 'AL']['OPS'].dropna()
        nl_data = df[df['lgID'] == 'NL']['OPS'].dropna()
        
        if len(al_data) > 0 and len(nl_data) > 0:
            u_stat, p_val = stats.mannwhitneyu(al_data, nl_data, alternative='two-sided')
            print(f"\nTest 3: American League vs National League (OPS)")
            print(f"AL OPS: {al_data.mean():.3f}")
            print(f"NL OPS: {nl_data.mean():.3f}")
            print(f"Mann-Whitney U: {u_stat:.1f}, p-value: {p_val:.6f}")
            print(f"Significant difference: {'Yes' if p_val < 0.05 else 'No'}")
    
    # Test 4: Distribution analysis of home runs
    hr_data = df['HR'].dropna()
    
    # Fit Poisson distribution (common for count data)
    lambda_param = hr_data.mean()
    ks_stat, ks_p = stats.kstest(hr_data, lambda x: stats.poisson.cdf(x, lambda_param))
    
    print(f"\nTest 4: Home Run Distribution Analysis")
    print(f"Mean HR per season: {lambda_param:.2f}")
    print(f"Poisson fit - KS statistic: {ks_stat:.4f}, p-value: {ks_p:.6f}")
    print(f"Follows Poisson distribution: {'Yes' if ks_p > 0.05 else 'No'}")

# ------------------------------------------------------------------
# 6️⃣ Performance Prediction and Classification
# ------------------------------------------------------------------

def predict_hall_of_fame_candidates(df):
    """Use machine learning to identify potential Hall of Fame players."""
    
    print(f"\n{'='*60}")
    print("HALL OF FAME PREDICTION MODEL")
    print('='*60)
    
    # Calculate career statistics for each player
    career_totals = df.groupby('playerID').agg({
        'G': 'sum',
        'AB': 'sum',
        'H': 'sum', 
        'HR': 'sum',
        'RBI': 'sum',
        'R': 'sum',
        'BB': 'sum',
        'OPS': 'mean',
        'wOBA': 'mean',
        'yearID': ['min', 'max', 'count'],
        'fullName': 'first'
    })
    
    # Flatten columns
    career_totals.columns = ['_'.join(col).strip('_') for col in career_totals.columns]
    career_totals = career_totals.rename(columns={'fullName_first': 'name'})
    
    # Calculate additional metrics
    career_totals['career_length'] = (career_totals['yearID_max'] - career_totals['yearID_min'] + 1)
    career_totals['career_avg'] = career_totals['H_sum'] / career_totals['AB_sum']
    career_totals['hr_per_season'] = career_totals['HR_sum'] / career_totals['yearID_count']
    
    # Create Hall of Fame likelihood score based on traditional benchmarks
    hof_score = 0
    
    # Traditional milestones (simplified scoring)
    conditions = [
        (career_totals['H_sum'] >= 3000, 40),      # 3000 hits
        (career_totals['HR_sum'] >= 500, 35),       # 500 home runs
        (career_totals['HR_sum'] >= 400, 20),       # 400 home runs
        (career_totals['RBI_sum'] >= 1500, 15),     # 1500 RBIs
        (career_totals['R_sum'] >= 1500, 15),       # 1500 runs
        (career_totals['OPS_mean'] >= 0.900, 25),   # .900 OPS
        (career_totals['career_avg'] >= 0.320, 15), # .320 average
        (career_totals['career_length'] >= 15, 10), # Longevity
        (career_totals['yearID_count'] >= 12, 10)   # Seasons played
    ]
    
    for condition, points in conditions:
        hof_score += np.where(condition, points, 0)
    
    career_totals['hof_score'] = hof_score
    
    # Create binary HOF probability (simplified)
    career_totals['hof_likely'] = (career_totals['hof_score'] >= 60).astype(int)
    
    # Show HOF candidates
    hof_candidates = career_totals[
        (career_totals['hof_score'] >= 40) & 
        (career_totals['AB_sum'] >= 3000)
    ].sort_values('hof_score', ascending=False)
    
    print(f"Hall of Fame Candidates (Score >= 40):")
    print("-" * 50)
    print(f"{'Player':25s} {'Score':>5s} {'HR':>4s} {'H':>5s} {'OPS':>5s} {'Years':>5s}")
    print("-" * 50)
    
    for _, player in hof_candidates.head(15).iterrows():
        print(f"{player.get('name', 'Unknown'):25s} "
              f"{player['hof_score']:5.0f} "
              f"{player['HR_sum']:4.0f} "
              f"{player['H_sum']:5.0f} "
              f"{player['OPS_mean']:5.3f} "
              f"{player['yearID_count']:5.0f}")
    
    return career_totals

# ------------------------------------------------------------------
# 7️⃣ Advanced Analytics: Age Curves and Peak Performance
# ------------------------------------------------------------------

def analyze_age_curves(df):
    """Analyze how player performance changes with age."""
    
    print(f"\n{'='*60}")
    print("AGE CURVE ANALYSIS")
    print('='*60)
    
    if 'age' not in df.columns or df['age'].isna().all():
        print("Age data not available for age curve analysis")
        return None
    
    # Filter for players with sufficient playing time
    qualified = df[df['AB'] >= 200].copy()
    
    # Calculate age-based performance
    age_performance = qualified.groupby('age').agg({
        'OPS': ['mean', 'count', 'std'],
        'HR_rate': 'mean',
        'BB_rate': 'mean',
        'K_rate': 'mean'
    }).round(4)
    
    # Flatten columns
    age_performance.columns = ['_'.join(col) for col in age_performance.columns]
    
    # Filter for ages with sufficient sample size
    age_performance = age_performance[age_performance['OPS_count'] >= 20]
    
    # Find peak performance age
    peak_age = age_performance['OPS_mean'].idxmax()
    peak_ops = age_performance['OPS_mean'].max()
    
    print(f"Peak Performance Analysis:")
    print(f"Peak age for OPS: {peak_age} years old")
    print(f"Peak OPS: {peak_ops:.3f}")
    
    # Fit polynomial curve to age vs OPS
    ages = age_performance.index.values
    ops_values = age_performance['OPS_mean'].values
    
    if len(ages) >= 3:
        # Quadratic fit
        coeffs = np.polyfit(ages, ops_values, 2)
        polynomial = np.poly1d(coeffs)
        
        # Find theoretical peak
        theoretical_peak = -coeffs[1] / (2 * coeffs[0])
        
        print(f"Polynomial fit peak: {theoretical_peak:.1f} years old")
        print(f"Performance decline after 30: {((age_performance.loc[30, 'OPS_mean'] - age_performance.loc[35, 'OPS_mean']) / age_performance.loc[30, 'OPS_mean'] * 100):.1f}% per 5 years" if 30 in age_performance.index and 35 in age_performance.index else "Insufficient data")
    
    return age_performance

# ------------------------------------------------------------------
# 8️⃣ Visualization Functions
# ------------------------------------------------------------------

def create_comprehensive_visualizations(df, yearly_stats, career_stats, age_performance):
    """Create a comprehensive dashboard of baseball analytics."""
    
    fig, axes = plt.subplots(3, 3, figsize=(20, 15))
    fig.suptitle('Lahman Baseball Database Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Historical OPS Trends
    axes[0,0].plot(yearly_stats.index, yearly_stats['OPS'], 'b-', linewidth=2, marker='o', markersize=3)
    axes[0,0].set_xlabel('Year')
    axes[0,0].set_ylabel('League Average OPS')
    axes[0,0].set_title('Historical Offensive Trends')
    axes[0,0].grid(True, alpha=0.3)
    
    # Add era shading
    eras = [(1993, 2006, 'Steroid Era'), (2007, 2024, 'Modern Era')]
    for start, end, label in eras:
        if start in yearly_stats.index and end >= yearly_stats.index.min():
            axes[0,0].axvspan(start, min(end, yearly_stats.index.max()), alpha=0.2, label=label)
    axes[0,0].legend()
    
    # 2. Home Run Distribution
    hr_data = df['HR'][df['AB'] >= 200]
    axes[0,1].hist(hr_data, bins=30, alpha=0.7, color='red', edgecolor='black')
    axes[0,1].axvline(hr_data.mean(), color='orange', linestyle='--', 
                     label=f'Mean: {hr_data.mean():.1f}')
    axes[0,1].set_xlabel('Home Runs per Season')
    axes[0,1].set_ylabel('Frequency') 
    axes[0,1].set_title('Distribution of Home Runs (200+ AB)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Power vs Contact
    qualified_recent = df[df['AB'] >= 300]
    axes[0,2].scatter(qualified_recent['K_rate'], qualified_recent['HR_rate'], 
                     alpha=0.5, color='purple')
    axes[0,2].set_xlabel('Strikeout Rate')
    axes[0,2].set_ylabel('Home Run Rate')
    axes[0,2].set_title('Power vs Contact Trade-off')
    axes[0,2].grid(True, alpha=0.3)
    
    # 4. Career Length vs Performance
    if career_stats is not None:
        long_careers = career_stats[career_stats['AB_sum'] >= 2000]
        axes[1,0].scatter(long_careers['career_length'], long_careers['OPS_mean'], alpha=0.6)
        axes[1,0].set_xlabel('Career Length (Years)')
        axes[1,0].set_ylabel('Average OPS')
        axes[1,0].set_title('Career Length vs Performance')
        axes[1,0].grid(True, alpha=0.3)
    
    # 5. Strikeout Rate Over Time
    so_trend = yearly_stats['K_rate_league'].dropna()
    axes[1,1].plot(so_trend.index, so_trend.values, 'g-', linewidth=2, marker='s', markersize=4)
    axes[1,1].set_xlabel('Year')
    axes[1,1].set_ylabel('League Strikeout Rate')
    axes[1,1].set_title('Rise of Strikeouts')
    axes[1,1].grid(True, alpha=0.3)
    
    # 6. Age vs Performance
    if age_performance is not None and len(age_performance) > 0:
        ages = age_performance.index
        ops_by_age = age_performance['OPS_mean']
        axes[1,2].plot(ages, ops_by_age, 'ro-', linewidth=2)
        axes[1,2].set_xlabel('Age')
        axes[1,2].set_ylabel('Average OPS')
        axes[1,2].set_title('Age Curve (Performance vs Age)')
        axes[1,2].grid(True, alpha=0.3)
        
        # Highlight peak performance age
        peak_age = ops_by_age.idxmax()
        axes[1,2].axvline(peak_age, color='gold', linestyle='--', 
                         label=f'Peak: {peak_age}')
        axes[1,2].legend()
    
    # 7. Team Performance Heatmap (recent years)
    recent_years = df[df['yearID'] >= df['yearID'].max() - 5]
    if 'teamID' in recent_years.columns:
        team_year_ops = recent_years.groupby(['teamID', 'yearID'])['OPS'].mean().unstack(fill_value=np.nan)
        
        if not team_year_ops.empty:
            sns.heatmap(team_year_ops, annot=True, fmt='.3f', cmap='RdYlBu_r', 
                       ax=axes[2,0], cbar_kws={'label': 'Team OPS'})
            axes[2,0].set_title('Team OPS by Year (Heatmap)')
            axes[2,0].set_xlabel('Year')
            axes[2,0].set_ylabel('Team')
    
    # 8. Performance Distribution by Position
    if 'position' in df.columns or any(col.startswith('pos') for col in df.columns):
        # Try to find position data
        pos_col = None
        for col in df.columns:
            if 'pos' in col.lower() and df[col].notna().any():
                pos_col = col
                break
        
        if pos_col:
            pos_ops = df.groupby(pos_col)['OPS'].mean().sort_values(ascending=True)
            axes[2,1].barh(range(len(pos_ops)), pos_ops.values, color='lightcoral')
            axes[2,1].set_yticks(range(len(pos_ops)))
            axes[2,1].set_yticklabels(pos_ops.index)
            axes[2,1].set_xlabel('Average OPS')
            axes[2,1].set_title('Offensive Production by Position')
            axes[2,1].grid(True, alpha=0.3)
    
    # 9. Correlation Heatmap
    metrics = ['AVG', 'OBP', 'SLG', 'OPS', 'HR_rate', 'BB_rate', 'K_rate']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if len(available_metrics) >= 3:
        corr_matrix = df[available_metrics].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                   fmt='.2f', ax=axes[2,2])
        axes[2,2].set_title('Hitting Metrics Correlation')
    
    plt.tight_layout()
    plt.show()

# ------------------------------------------------------------------
# 9️⃣ Advanced Sabermetric Analysis
# ------------------------------------------------------------------

def calculate_advanced_sabermetrics(df):
    """Calculate advanced sabermetric statistics."""
    
    print(f"\n{'='*60}")
    print("ADVANCED SABERMETRICS")
    print('='*60)
    
    # Calculate park factors (simplified approach)
    if 'teamID' in df.columns:
        # Home vs road performance proxy
        team_stats = df.groupby(['teamID', 'yearID']).agg({
            'HR': 'sum',
            'AB': 'sum',
            'H': 'sum'
        })
        
        team_stats['HR_rate'] = team_stats['HR'] / team_stats['AB']
        team_stats['AVG'] = team_stats['H'] / team_stats['AB']
        
        # Calculate relative team performance
        yearly_league_avg = df.groupby('yearID')[['HR_rate', 'AVG']].mean()
        
        # This is a simplified park factor calculation
        print("Team Environment Analysis (Top 10 HR-friendly):")
        print("-" * 45)
        
        recent_teams = team_stats[team_stats.index.get_level_values(1) >= df['yearID'].max() - 3]
        hr_friendly = recent_teams.groupby('teamID')['HR_rate'].mean().sort_values(ascending=False)
        
        for i, (team, hr_rate) in enumerate(hr_friendly.head(10).items(), 1):
            print(f"{i:2d}. {team}: {hr_rate:.4f} HR rate")
    
    # Calculate BABIP luck analysis
    df['expected_BABIP'] = 0.300  # League average approximation
    df['BABIP'] = (df['H'] - df['HR']) / (df['AB'] - df['SO'] - df['HR'])
    df['BABIP_luck'] = df['BABIP'] - df['expected_BABIP']
    
    # Players with extreme BABIP (potential regression candidates)
    recent_qualified = df[(df['yearID'] >= df['yearID'].max() - 2) & (df['AB'] >= 300)]
    
    print(f"\nBABIP Analysis (Potential Regression Candidates):")
    print("-" * 50)
    
    unlucky_players = recent_qualified[recent_qualified['BABIP_luck'] < -0.050].nlargest(5, 'BABIP_luck')
    lucky_players = recent_qualified[recent_qualified['BABIP_luck'] > 0.050].nsmallest(5, 'BABIP_luck')
    
    print("Most Unlucky (Low BABIP):")
    for _, player in unlucky_players.iterrows():
        name = player.get('fullName', player['playerID'])
        print(f"  {name:25s} BABIP: {player['BABIP']:.3f} (luck: {player['BABIP_luck']:+.3f})")
    
    print("\nMost Lucky (High BABIP):")
    for _, player in lucky_players.iterrows():
        name = player.get('fullName', player['playerID'])
        print(f"  {name:25s} BABIP: {player['BABIP']:.3f} (luck: {player['BABIP_luck']:+.3f})")

# ------------------------------------------------------------------
# 🔟 Performance Optimization Analysis
# ------------------------------------------------------------------

def optimize_lineup_production(df):
    """Use optimization to find the best lineup construction."""
    
    print(f"\n{'='*60}")
    print("LINEUP OPTIMIZATION ANALYSIS")
    print('='*60)
    
    # Get recent qualified players
    recent_year = df['yearID'].max()
    qualified_players = df[
        (df['yearID'] == recent_year) & 
        (df['AB'] >= 400)  # Regular players
    ].copy()
    
    if len(qualified_players) < 9:
        print("Insufficient qualified players for lineup analysis")
        return None
    
    # Define lineup positions and their typical characteristics
    lineup_positions = {
        1: "Leadoff (Speed/OBP)",
        2: "Contact Hitter", 
        3: "Best Overall Hitter",
        4: "Power (RBI)",
        5: "Power (RBI)", 
        6: "Gap Power",
        7: "Contact/Speed",
        8: "Utility/Defense",
        9: "Pitcher/Weak Hitter"
    }
    
    # Calculate composite scores for different lineup roles
    qualified_players['leadoff_score'] = (
        qualified_players['OBP'] * 0.5 + 
        qualified_players['SB'].fillna(0) * 0.01 +
        (1 - qualified_players['K_rate']) * 0.3
    )
    
    qualified_players['power_score'] = (
        qualified_players['SLG'] * 0.4 +
        qualified_players['HR'] * 0.01 +
        qualified_players['RBI'] * 0.002
    )
    
    qualified_players['contact_score'] = (
        qualified_players['AVG'] * 0.5 +
        (1 - qualified_players['K_rate']) * 0.5
    )
    
    qualified_players['overall_score'] = (
        qualified_players['OPS'] * 0.6 +
        qualified_players['wOBA'] * 0.4
    )
    
    print("Optimal Lineup Construction:")
    print("-" * 40)
    
    # Build optimal lineup
    used_players = set()
    optimal_lineup = {}
    
    # 1. Leadoff - best OBP/speed combination
    leadoff = qualified_players.loc[~qualified_players['playerID'].isin(used_players)].nlargest(1, 'leadoff_score')
    if not leadoff.empty:
        player = leadoff.iloc[0]
        optimal_lineup[1] = player
        used_players.add(player['playerID'])
        print(f"1. {player.get('fullName', player['playerID']):25s} OBP: {player['OBP']:.3f}")
    
    # 3. Best overall hitter
    best_overall = qualified_players.loc[~qualified_players['playerID'].isin(used_players)].nlargest(1, 'overall_score')
    if not best_overall.empty:
        player = best_overall.iloc[0]
        optimal_lineup[3] = player
        used_players.add(player['playerID'])
        print(f"3. {player.get('fullName', player['playerID']):25s} OPS: {player['OPS']:.3f}")
    
    # 4-5. Power hitters
    for pos in [4, 5]:
        power_hitter = qualified_players.loc[~qualified_players['playerID'].isin(used_players)].nlargest(1, 'power_score')
        if not power_hitter.empty:
            player = power_hitter.iloc[0]
            optimal_lineup[pos] = player
            used_players.add(player['playerID'])
            print(f"{pos}. {player.get('fullName', player['playerID']):25s} SLG: {player['SLG']:.3f}, HR: {player['HR']}")
    
    # 2. Contact hitter
    contact_hitter = qualified_players.loc[~qualified_players['playerID'].isin(used_players)].nlargest(1, 'contact_score')
    if not contact_hitter.empty:
        player = contact_hitter.iloc[0]
        optimal_lineup[2] = player
        used_players.add(player['playerID'])
        print(f"2. {player.get('fullName', player['playerID']):25s} AVG: {player['AVG']:.3f}")
    
    return optimal_lineup

# ------------------------------------------------------------------
# 1️⃣1️⃣ Main Execution Pipeline
# ------------------------------------------------------------------

def main():
    """Execute the complete Lahman baseball analysis pipeline."""
    
    print("⚾ LAHMAN BASEBALL DATABASE ANALYSIS PROJECT ⚾")
    print("=" * 60)
    
    # Load data
    batting, people, teams = load_lahman_data()
    
    if batting is None:
        print("Could not load data. Exiting...")
        return
    
    # Preprocess data
    df = preprocess_batting_data(batting, people, teams, min_year=1980, min_ab=50)
    
    # Historical trends
    yearly_stats = analyze_historical_trends(df)
    
    # Statistical analysis
    perform_statistical_tests(df)
    
    # Career analysis
    career_stats = analyze_player_careers(df)
    
    # Age curves
    age_performance = analyze_age_curves(df)
    
    # Era adjustments
    df_era_adjusted = calculate_era_adjustments(df)
    
    # Advanced sabermetrics
    calculate_advanced_sabermetrics(df)
    
    # Hall of Fame analysis
    hof_analysis = predict_hall_of_fame_candidates(df)
    
    # Lineup optimization
    optimal_lineup = optimize_lineup_production(df)
    
    # Create visualizations
    create_comprehensive_visualizations(df, yearly_stats, career_stats, age_performance)
    
    # Final summary report
    print(f"\n{'='*80}")
    print("ANALYSIS SUMMARY REPORT")
    print('='*80)
    
    print(f"Database Coverage:")
    print(f"  Years analyzed: {df['yearID'].min()} - {df['yearID'].max()}")
    print(f"  Total player-seasons: {len(df):,}")
    print(f"  Unique players: {df['playerID'].nunique():,}")
    print(f"  Teams represented: {df['teamID'].nunique() if 'teamID' in df.columns else 'N/A'}")
    
    print(f"\nKey Findings:")
    recent_data = df[df['yearID'] >= df['yearID'].max() - 5]
    print(f"  Modern era OPS average: {recent_data['OPS'].mean():.3f}")
    print(f"  Home run rate trend: {recent_data['HR_rate'].mean():.4f}")
    print(f"  Strikeout rate trend: {recent_data['K_rate'].mean():.3f}")
    
    if age_performance is not None and not age_performance.empty:
        peak_age = age_performance['OPS_mean'].idxmax()
        print(f"  Peak performance age: {peak_age} years old")
    
    # Export top performers
    print(f"\nTop 10 Single-Season OPS Performances:")
    print("-" * 45)
    top_seasons = df.nlargest(10, 'OPS')[['fullName', 'yearID', 'teamID', 'OPS', 'HR', 'AVG']]
    for i, (_, season) in enumerate(top_seasons.iterrows(), 1):
        name = season.get('fullName', season.get('playerID', 'Unknown'))
        team = season.get('teamID', 'UNK')
        print(f"{i:2d}. {name:20s} {season['yearID']} {team} - "
              f"OPS: {season['OPS']:.3f} ({season['HR']:2.0f} HR, {season['AVG']:.3f} AVG)")
    
    print(f"\n🎯 Analysis Complete! Check the generated visualizations above.")
    return df, career_stats, yearly_stats

# ------------------------------------------------------------------
# 1️⃣2️⃣ Additional Analysis Functions
# ------------------------------------------------------------------

def find_statistical_outliers(df):
    """Identify statistical outliers and anomalies in the data."""
    
    print(f"\n{'='*60}")
    print("STATISTICAL OUTLIERS ANALYSIS")
    print('='*60)
    
    # Define metrics to check for outliers
    metrics = ['OPS', 'HR', 'RBI', 'BB_rate', 'K_rate']
    
    for metric in metrics:
        if metric not in df.columns:
            continue
            
        data = df[df['AB'] >= 200][metric].dropna()  # Qualified players only
        
        # Calculate z-scores
        z_scores = np.abs(stats.zscore(data))
        outlier_threshold = 3  # 3 standard deviations
        
        outliers = df.loc[data.index[z_scores > outlier_threshold]]
        
        if len(outliers) > 0:
            print(f"\n{metric} Outliers (|z-score| > {outlier_threshold}):")
            print("-" * 40)
            
            for _, outlier in outliers.head(5).iterrows():
                name = outlier.get('fullName', outlier['playerID'])
                z_score = (outlier[metric] - data.mean()) / data.std()
                print(f"  {name:25s} {outlier['yearID']} - "
                      f"{metric}: {outlier[metric]:.3f} (z-score: {z_score:+.2f})")

def regression_to_mean_analysis(df):
    """Analyze regression to the mean in player performance."""
    
    print(f"\n{'='*60}")
    print("REGRESSION TO THE MEAN ANALYSIS")
    print('='*60)
    
    # Find players with consecutive qualified seasons
    qualified = df[df['AB'] >= 300].copy()
    qualified = qualified.sort_values(['playerID', 'yearID'])
    
    # Calculate year-over-year changes
    qualified['next_year'] = qualified.groupby('playerID')['yearID'].shift(-1)
    qualified['next_ops'] = qualified.groupby('playerID')['OPS'].shift(-1)
    
    # Filter for consecutive seasons
    consecutive = qualified[
        (qualified['next_year'] == qualified['yearID'] + 1) &
        qualified['next_ops'].notna()
    ].copy()
    
    if len(consecutive) > 50:
        # Analyze extreme performers in year 1
        high_performers = consecutive[consecutive['OPS'] >= consecutive['OPS'].quantile(0.9)]
        low_performers = consecutive[consecutive['OPS'] <= consecutive['OPS'].quantile(0.1)]
        
        print("Regression to Mean Analysis:")
        print("-" * 30)
        
        if len(high_performers) > 0:
            avg_decline = high_performers['OPS'].mean() - high_performers['next_ops'].mean()
            print(f"Top 10% performers: Average decline = {avg_decline:.3f} OPS")
        
        if len(low_performers) > 0:
            avg_improvement = low_performers['next_ops'].mean() - low_performers['OPS'].mean()
            print(f"Bottom 10% performers: Average improvement = {avg_improvement:.3f} OPS")
        
        # Correlation between extreme performance and next year
        corr, p_val = stats.pearsonr(consecutive['OPS'], consecutive['next_ops'])
        print(f"Year-to-year OPS correlation: {corr:.3f} (p-value: {p_val:.6f})")

# ------------------------------------------------------------------
# 1️⃣3️⃣ Execute Analysis
# ------------------------------------------------------------------

if __name__ == "__main__":
    # Run main analysis
    results = main()
    
    if results and results[0] is not None:
        df, career_stats, yearly_stats = results
        
        # Additional analyses
        find_statistical_outliers(df)
        regression_to_mean_analysis(df)
        
        print(f"\n{'='*60}")
        print("🏆 ANALYSIS COMPLETE!")
        print("📊 Check the visualizations above for insights")
        print("📈 All statistical tests and trends have been calculated")
        print('='*60)
    else:
        print("\n❌ Analysis could not complete due to data loading issues.")
        print("Please ensure you have the Lahman database CSV files:")
        print("  - Batting.csv")
        print("  - People.csv (or Master.csv)")  
        print("  - Teams.csv")
        print("\nDownload lahman dataset")

# ------------------------------------------------------------------
# 1️⃣4️⃣ Utility Functions for Custom Analysis
# ------------------------------------------------------------------

def custom_player_lookup(df, player_name_partial):
    """Look up specific player statistics."""
    
    if 'fullName' not in df.columns:
        print("Player names not available in dataset")
        return None
    
    matches = df[df['fullName'].str.contains(player_name_partial, case=False, na=False)]
    
    if len(matches) == 0:
        print(f"No players found matching: {player_name_partial}")
        return None
    
    print(f"\nPlayer Lookup Results for '{player_name_partial}':")
    print("-" * 50)
    
    for player_id in matches['playerID'].unique():
        player_seasons = matches[matches['playerID'] == player_id].sort_values('yearID')
        player_name = player_seasons['fullName'].iloc[0]
        
        print(f"\n{player_name}:")
        print(f"  Career: {player_seasons['yearID'].min()} - {player_seasons['yearID'].max()}")
        print(f"  Seasons: {len(player_seasons)}")
        print(f"  Career Totals: {player_seasons['H'].sum()} H, {player_seasons['HR'].sum()} HR, {player_seasons['RBI'].sum()} RBI")
        print(f"  Career Rates: {player_seasons['AVG'].mean():.3f} AVG, {player_seasons['OPS'].mean():.3f} OPS")
        
        # Best season
        best_season = player_seasons.loc[player_seasons['OPS'].idxmax()]
        print(f"  Best Season: {best_season['yearID']} - {best_season['OPS']:.3f} OPS")
    
    return matches

def team_analysis(df, team_id, start_year=None, end_year=None):
    """Analyze a specific team's offensive performance over time."""
    
    if 'teamID' not in df.columns:
        print("Team information not available in dataset")
        return None
    
    team_data = df[df['teamID'] == team_id].copy()
    
    if start_year:
        team_data = team_data[team_data['yearID'] >= start_year]
    if end_year:
        team_data = team_data[team_data['yearID'] <= end_year]
    
    if len(team_data) == 0:
        print(f"No data found for team: {team_id}")
        return None
    
    # Calculate team yearly stats
    team_yearly = team_data.groupby('yearID').agg({
        'AVG': 'mean',
        'OBP': 'mean',
        'SLG': 'mean', 
        'OPS': 'mean',
        'HR': 'sum',
        'RBI': 'sum',
        'playerID': 'count'
    }).round(3)
    
    print(f"\n{team_id} Team Analysis:")
    print("-" * 30)
    print(f"Years covered: {team_yearly.index.min()} - {team_yearly.index.max()}")
    print(f"Average team OPS: {team_yearly['OPS'].mean():.3f}")
    print(f"Best offensive year: {team_yearly['OPS'].idxmax()} (OPS: {team_yearly['OPS'].max():.3f})")
    print(f"Total home runs: {team_yearly['HR'].sum():,}")
    
    return team_yearly

# Example usage functions for demonstration
def run_example_analyses(df):
    """Run some example analyses to demonstrate functionality."""
    
    print(f"\n{'='*60}")
    print("EXAMPLE CUSTOM ANALYSES")
    print('='*60)
    
    # Example 1: Look up a famous player (if data exists)
    famous_players = ['Babe Ruth', 'Ted Williams', 'Barry Bonds', 'Willie Mays']
    for player in famous_players:
        result = custom_player_lookup(df, player)
        if result is not None:
            break  # Found one, that's enough for demo
    
    # Example 2: Analyze a specific team
    if 'teamID' in df.columns:
        example_teams = ['NYY', 'BOS', 'LAD', 'STL']
        for team in example_teams:
            if team in df['teamID'].values:
                team_analysis(df, team, start_year=2000)
                break

    print(f"\n💡 You can now run custom analyses:")
    print(f"   - custom_player_lookup(df, 'Player Name')")
    print(f"   - team_analysis(df, 'TEAM_ID', start_year, end_year)")
    print(f"   - Access the processed dataframe as 'df' for your own analysis")

# ---------------------------------
# Note: Data from Lahman database files
# ---------------------------------