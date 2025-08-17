import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

def fetch_news(api_key, query):
    """
    Fetches news articles from NewsAPI based on a query.
    """
    # URL for everything endpoint, searching for the query, sorted by relevancy
    url = (f'https://newsapi.org/v2/everything?'
           f'q={query}&'
           f'sortBy=relevancy&'  # You can also use 'popularity' or 'publishedAt'
           f'language=en&'
           f'apiKey={api_key}')
    
    print(f"Fetching news for '{query}'...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to fetch news. Please check your API key and network connection.")
        # Print error details from the API
        print(f"Error details: {response.json().get('message', 'No details provided')}")
        return []
        
    data = response.json()
    articles = data.get('articles', [])
    print(f"Found {len(articles)} articles.")
    return articles

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text and returns scores.
    """
    # VADER sentiment analyzer is great for news and social media text
    analyzer = SentimentIntensityAnalyzer()
    # The 'compound' score is a single metric for the sentiment
    # Positive: compound > 0.05
    # Neutral: -0.05 <= compound <= 0.05
    # Negative: compound < -0.05
    sentiment_dict = analyzer.polarity_scores(text)
    
    if sentiment_dict['compound'] >= 0.05:
        return "Positive", sentiment_dict
    elif sentiment_dict['compound'] <= -0.05:
        return "Negative", sentiment_dict
    else:
        return "Neutral", sentiment_dict

def run_analysis():
    """
    Main function to run the sentiment analysis process.
    """
    # IMPORTANT: Replace with your actual NewsAPI key
    API_KEY = 'd156668f55a846ed884aa6a2fb9f7f18' 
    
    # Keywords to search for. Using "OR" broadens the search.
    KEYWORDS = '"IIT Mandi" OR "Mandi Himachal Pradesh"'
    
    articles = fetch_news(API_KEY, KEYWORDS)
    
    if not articles:
        print("No articles found to analyze. Exiting.")
        return

    positive_news = []
    negative_news = []
    neutral_news = []

    for article in articles:
        # We analyze the title and description for a comprehensive sentiment
        content_to_analyze = f"{article.get('title', '')}. {article.get('description', '')}"
        
        if not content_to_analyze or content_to_analyze == ". ":
            continue # Skip articles with no content

        sentiment_label, scores = analyze_sentiment(content_to_analyze)
        
        article_details = {
            "title": article.get('title'),
            "url": article.get('url'),
            "scores": scores
        }

        if sentiment_label == "Positive":
            positive_news.append(article_details)
        elif sentiment_label == "Negative":
            negative_news.append(article_details)
        else:
            neutral_news.append(article_details)

    total_analyzed = len(positive_news) + len(negative_news) + len(neutral_news)
    
    if total_analyzed == 0:
        print("\nCould not analyze any articles.")
        return

    # --- Displaying the results ---
    print("\n" + "="*50)
    print("      SENTIMENT ANALYSIS REPORT FOR IIT MANDI")
    print("="*50 + "\n")

    # Calculate exact positive sentiment percentage
    positive_percentage = (len(positive_news) / total_analyzed) * 100
    
    print(f"📊 Overall Summary:")
    print(f"   Total Articles Analyzed: {total_analyzed}")
    print(f"   📈 Positive Sentiment: {positive_percentage:.2f}% ({len(positive_news)} articles)")
    print(f"   📉 Negative Sentiment: {(len(negative_news) / total_analyzed) * 100:.2f}% ({len(negative_news)} articles)")
    print(f"   ⚖️ Neutral Sentiment: {(len(neutral_news) / total_analyzed) * 100:.2f}% ({len(neutral_news)} articles)")
    
    print("\n" + "-"*50)
    print(f"\n👍 POSITIVE NEWS ({len(positive_news)} articles):\n")
    if positive_news:
        for item in positive_news:
            print(f"   - {item['title']}")
            print(f"     URL: {item['url']}\n")
    else:
        print("   No positive news found.")

    print("\n" + "-"*50)
    print(f"\n👎 NEGATIVE NEWS ({len(negative_news)} articles):\n")
    if negative_news:
        for item in negative_news:
            print(f"   - {item['title']}")
            print(f"     URL: {item['url']}\n")
    else:
        print("   No negative news found.")
        
    print("\n" + "-"*50)
    print(f"\n😐 NEUTRAL NEWS ({len(neutral_news)} articles):\n")
    if neutral_news:
        for item in neutral_news:
            print(f"   - {item['title']}")
            print(f"     URL: {item['url']}\n")
    else:
        print("   No neutral news found.")

# Run the main function
if __name__ == "__main__":
    run_analysis()