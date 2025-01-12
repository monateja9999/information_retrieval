import json
import pandas as pd
from scipy.stats import spearmanr

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def compute_overlap_and_spearman(bing_data, google_data):
    """Compute number of overlaps, percentage of overlap, and Spearman correlation coefficient."""
    results = []
    rank_checker = []
    
    query_count = 1
    
    for query, bing_urls in bing_data.items():
        if query in google_data:
            google_urls = google_data[query]
            
            # Find overlap
            bing_set = set(bing_urls)
            google_set = set(google_urls)
            common_urls = bing_set.intersection(google_set)
            num_overlaps = len(common_urls)
            percent_overlap = (num_overlaps / len(google_urls)) * 100
            percent_overlap_str = f"{percent_overlap:.1f}"  # Format to 1 decimal place

            # Rank lists for Spearman correlation calculation
            common_urls = list(common_urls)
            bing_ranks = [bing_urls.index(url) + 1 for url in common_urls]
            google_ranks = [google_urls.index(url) + 1 for url in common_urls]
            
            # Add to rank_checker for only overlapping URLs
            for url in common_urls:
                google_rank = google_urls.index(url) + 1
                bing_rank = bing_urls.index(url) + 1
                rank_checker.append({
                    'Queries': f'Query {query_count}',
                    'Actual Query': query,
                    'Overlapping URL': url,
                    'Google Rank': google_rank,
                    'Bing Rank': bing_rank
                })
            
            # Compute Spearman correlation coefficient
            if len(bing_ranks) > 1 and len(google_ranks) > 1:
                correlation, _ = spearmanr(bing_ranks, google_ranks)
            else:
                correlation = None  # Not enough data to compute correlation

            results.append({
                'Queries': f'Query {query_count}',
                'Number of Overlapping Results': num_overlaps,
                'Percent Overlap': percent_overlap_str,
                'Spearman Coefficient': correlation if correlation is not None else 'N/A'
            })
            
            query_count += 1
    
    return results, rank_checker

def compute_averages(results):
    """Compute averages for the numeric columns."""
    num_overlaps = [result['Number of Overlapping Results'] for result in results]
    percent_overlap = [float(result['Percent Overlap']) for result in results]
    
    # Filter out 'N/A' values for Spearman Coefficient
    spearman_coefficients = [result['Spearman Coefficient'] for result in results if result['Spearman Coefficient'] != 'N/A']
    
    avg_num_overlaps = sum(num_overlaps) / len(num_overlaps) if num_overlaps else 0
    avg_percent_overlap = sum(percent_overlap) / len(percent_overlap) if percent_overlap else 0
    avg_spearman_coefficient = sum(spearman_coefficients) / len(spearman_coefficients) if spearman_coefficients else 'N/A'
    
    # Return averages with one decimal place formatting
    avg_percent_overlap_str = f"{avg_percent_overlap:.1f}"  # Format to 1 decimal place
    
    return avg_num_overlaps, avg_percent_overlap_str, avg_spearman_coefficient

def save_to_csv(results, file_path):
    """Save results to a CSV file with averages as the last row."""    
    df = pd.DataFrame(results)
    
    # Compute averages
    avg_num_overlaps, avg_percent_overlap, avg_spearman_coefficient = compute_averages(results)
    
    # Add averages row
    averages_row = {
        'Queries': 'Averages',
        'Number of Overlapping Results': avg_num_overlaps,
        'Percent Overlap': avg_percent_overlap,
        'Spearman Coefficient': avg_spearman_coefficient
    }
    
    # Convert averages row to a DataFrame and concatenate
    averages_df = pd.DataFrame([averages_row])
    df = pd.concat([df, averages_df], ignore_index=True)
    
    df.to_csv(file_path, index=False)

def save_rank_checker_csv(rank_checker, file_path):
    """Save rank checker results to a CSV file with both query identifiers and actual queries."""
    df = pd.DataFrame(rank_checker)
    df.to_csv(file_path, index=False)

# File paths
bing_file_path = 'hw1.json'
google_file_path = 'Google_Result1.json'
output_csv_path = 'hw1.csv'
rank_checker_csv_path = 'Rank Checker.csv'

# Load JSON data
bing_data = load_json(bing_file_path)
google_data = load_json(google_file_path)

# Compute overlap and correlation
results, rank_checker = compute_overlap_and_spearman(bing_data, google_data)

# Save results to CSV with averages
save_to_csv(results, output_csv_path)

# Save rank checker results to CSV with both query identifiers and actual queries
save_rank_checker_csv(rank_checker, rank_checker_csv_path)

print(f"Results saved to {output_csv_path}")
print(f"Rank checker data saved to {rank_checker_csv_path}")