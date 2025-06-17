#!/usr/bin/env python3
"""
Email Spam and False Advertisement Detector

This script analyzes email content to detect spam and potentially false advertisements
using multiple detection methods including keyword analysis, machine learning, and
pattern recognition.
"""

import re
import string
import pickle
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# For machine learning (install with: pip install scikit-learn)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("Warning: scikit-learn not installed. ML features disabled.")

@dataclass
class DetectionResult:
    """Results from spam/false ad detection"""
    is_spam: bool
    is_false_ad: bool
    confidence_score: float
    detected_patterns: List[str]
    risk_factors: List[str]

class SpamDetector:
    """Main class for detecting spam and false advertisements"""
    
    def __init__(self):
        self.spam_keywords = {
            'urgent': ['urgent', 'act now', 'limited time', 'expires soon', 'hurry'],
            'money': ['free money', 'easy money', 'get rich', 'make money fast', 
                     'guaranteed income', 'work from home', 'no experience needed'],
            'promotional': ['free', 'win', 'winner', 'congratulations', 'selected',
                           'special offer', 'discount', 'save money', 'deal'],
            'suspicious': ['click here', 'verify account', 'confirm identity',
                          'suspended', 'temporary hold', 'immediate action'],
            'medical': ['lose weight fast', 'miracle cure', 'doctor approved',
                       'fda approved', 'clinical trial', 'guaranteed results']
        }
        
        self.false_ad_patterns = {
            'exaggerated_claims': [
                r'\b(100%|completely|totally|absolutely)\s+(free|guaranteed|safe)',
                r'\bmiracle\s+(cure|solution|product)',
                r'\binstant(ly)?\s+(results?|cure|fix)',
                r'\bno\s+(risk|side\s+effects?|questions?\s+asked)',
                r'\bdoctors?\s+hate\s+(this|him|her)'
            ],
            'urgency_scams': [
                r'\bact\s+now\b',
                r'\blimited\s+time\s+offer',
                r'\btoday\s+only\b',
                r'\bexpires?\s+(today|soon|in\s+\d+\s+hours?)',
                r'\bhurry\b.*\bwhile\s+supplies?\s+last'
            ],
            'financial_scams': [
                r'\$\d+.*\bper\s+(day|hour|week)\b',
                r'\bmake\s+\$?\d+.*\b(working\s+from\s+home|online)',
                r'\bguaranteed\s+(income|return|profit)',
                r'\bno\s+investment\s+required',
                r'\bearn\s+money\s+(fast|quickly|easily)'
            ]
        }
        
        # Suspicious patterns for phishing/fraud
        self.phishing_patterns = [
            r'verify.*account',
            r'confirm.*identity',
            r'click.*here.*immediately',
            r'suspended.*account',
            r'unusual.*activity',
            r'temporary.*hold'
        ]
        
        # ML model (if available)
        self.ml_model = None
        if ML_AVAILABLE:
            self._initialize_ml_model()
    
    def _initialize_ml_model(self):
        """Initialize machine learning model with sample data"""
        # Sample training data (in real use, you'd have a larger dataset)
        sample_emails = [
            ("Get rich quick! Make $5000 per day working from home!", 1),
            ("Congratulations! You've won $1,000,000! Click here now!", 1),
            ("Urgent: Your account will be suspended. Verify immediately.", 1),
            ("Miracle weight loss pill - lose 50 pounds in 10 days!", 1),
            ("Free money! No investment required! Act now!", 1),
            ("Meeting scheduled for tomorrow at 2 PM in conference room.", 0),
            ("Please review the quarterly report attached.", 0),
            ("Your order has been shipped and will arrive tomorrow.", 0),
            ("Thank you for your purchase. Here's your receipt.", 0),
            ("Reminder: Team lunch on Friday at the usual place.", 0)
        ]
        
        texts, labels = zip(*sample_emails)
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.ml_model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        
        # Train the model
        self.ml_model.fit(texts, labels)
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess email text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove excessive punctuation and special characters
        text = re.sub(r'[^\w\s\.\!\?]', ' ', text)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        return text.strip()
    
    def check_spam_keywords(self, text: str) -> Tuple[List[str], float]:
        """Check for spam keywords and calculate spam score"""
        text_lower = text.lower()
        detected_patterns = []
        total_score = 0
        
        for category, keywords in self.spam_keywords.items():
            category_score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    detected_patterns.append(f"{category}: {keyword}")
                    category_score += 1
            
            # Weight different categories
            weights = {'urgent': 2, 'money': 3, 'promotional': 1, 'suspicious': 4, 'medical': 2}
            total_score += category_score * weights.get(category, 1)
        
        # Normalize score (max possible score estimation)
        max_possible_score = sum(len(keywords) * weights.get(cat, 1) 
                                for cat, keywords in self.spam_keywords.items())
        normalized_score = min(total_score / max_possible_score, 1.0)
        
        return detected_patterns, normalized_score
    
    def check_false_ad_patterns(self, text: str) -> Tuple[List[str], float]:
        """Check for false advertisement patterns"""
        detected_patterns = []
        total_matches = 0
        
        for category, patterns in self.false_ad_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    detected_patterns.append(f"{category}: {pattern}")
                    total_matches += len(matches)
        
        # Calculate confidence based on number and type of matches
        confidence = min(total_matches * 0.15, 1.0)
        return detected_patterns, confidence
    
    def check_phishing_indicators(self, text: str) -> List[str]:
        """Check for phishing/fraud indicators"""
        indicators = []
        for pattern in self.phishing_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                indicators.append(f"Phishing pattern: {pattern}")
        return indicators
    
    def analyze_text_features(self, text: str) -> Dict[str, float]:
        """Analyze various text features that might indicate spam"""
        features = {}
        
        # Excessive capitalization
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        features['caps_ratio'] = caps_ratio
        
        # Excessive punctuation
        punct_ratio = sum(1 for c in text if c in string.punctuation) / max(len(text), 1)
        features['punct_ratio'] = punct_ratio
        
        # Number of exclamation marks
        exclamation_count = text.count('!')
        features['exclamation_count'] = exclamation_count
        
        # Presence of currency symbols
        currency_count = sum(text.count(symbol) for symbol in ['$', '€', '£', '¥'])
        features['currency_count'] = currency_count
        
        # Number of URLs
        url_count = len(re.findall(r'http[s]?://', text))
        features['url_count'] = url_count
        
        return features
    
    def get_ml_prediction(self, text: str) -> Optional[Tuple[bool, float]]:
        """Get prediction from ML model if available"""
        if not self.ml_model:
            return None
        
        try:
            # Get prediction probability
            prob = self.ml_model.predict_proba([text])[0]
            spam_prob = prob[1] if len(prob) > 1 else 0
            prediction = spam_prob > 0.5
            return prediction, spam_prob
        except Exception as e:
            print(f"ML prediction failed: {e}")
            return None
    
    def analyze_email(self, subject: str, body: str) -> DetectionResult:
        """Main method to analyze an email for spam and false advertisements"""
        # Combine subject and body
        full_text = f"{subject} {body}"
        processed_text = self.preprocess_text(full_text)
        
        # Initialize results
        detected_patterns = []
        risk_factors = []
        spam_scores = []
        false_ad_scores = []
        
        # Check spam keywords
        spam_patterns, spam_score = self.check_spam_keywords(processed_text)
        detected_patterns.extend(spam_patterns)
        spam_scores.append(spam_score)
        
        # Check false advertisement patterns
        false_ad_patterns, false_ad_score = self.check_false_ad_patterns(processed_text)
        detected_patterns.extend(false_ad_patterns)
        false_ad_scores.append(false_ad_score)
        
        # Check phishing indicators
        phishing_indicators = self.check_phishing_indicators(processed_text)
        detected_patterns.extend(phishing_indicators)
        if phishing_indicators:
            spam_scores.append(0.8)  # High spam score for phishing
        
        # Analyze text features
        features = self.analyze_text_features(full_text)
        
        # Add risk factors based on features
        if features['caps_ratio'] > 0.3:
            risk_factors.append("Excessive capitalization")
        if features['exclamation_count'] > 3:
            risk_factors.append("Too many exclamation marks")
        if features['punct_ratio'] > 0.1:
            risk_factors.append("Excessive punctuation")
        if features['currency_count'] > 2:
            risk_factors.append("Multiple currency symbols")
        
        # Get ML prediction if available
        ml_result = self.get_ml_prediction(processed_text)
        if ml_result:
            ml_spam, ml_confidence = ml_result
            spam_scores.append(ml_confidence)
            if ml_spam:
                detected_patterns.append(f"ML prediction: spam (confidence: {ml_confidence:.2f})")
        
        # Calculate final scores
        final_spam_score = np.mean(spam_scores) if spam_scores else 0
        final_false_ad_score = np.mean(false_ad_scores) if false_ad_scores else 0
        
        # Determine if spam or false ad
        is_spam = final_spam_score > 0.4 or len(phishing_indicators) > 0
        is_false_ad = final_false_ad_score > 0.3
        
        # Overall confidence is the maximum of the two scores
        confidence = max(final_spam_score, final_false_ad_score)
        
        return DetectionResult(
            is_spam=is_spam,
            is_false_ad=is_false_ad,
            confidence_score=confidence,
            detected_patterns=detected_patterns,
            risk_factors=risk_factors
        )

def main():
    """Example usage of the spam detector"""
    detector = SpamDetector()
    
    # Test emails
    test_emails = [
        {
            "subject": "URGENT: Win $1,000,000 NOW!",
            "body": "Congratulations! You've been selected to win $1,000,000! Click here immediately to claim your prize. This offer expires in 24 hours. Act now!"
        },
        {
            "subject": "Your Account Has Been Suspended",
            "body": "We've detected unusual activity on your account. Please verify your identity immediately by clicking the link below to avoid permanent suspension."
        },
        {
            "subject": "Miracle Weight Loss - Lose 50 Pounds Fast!",
            "body": "Doctor-approved miracle pill helps you lose 50 pounds in just 10 days! 100% guaranteed results with no side effects. Order now!"
        },
        {
            "subject": "Meeting Tomorrow",
            "body": "Hi team, just a reminder that we have our weekly meeting tomorrow at 2 PM in the conference room. Please bring your project updates."
        }
    ]
    
    print("Email Spam and False Advertisement Detection Results")
    print("=" * 60)
    
    for i, email in enumerate(test_emails, 1):
        result = detector.analyze_email(email["subject"], email["body"])
        
        print(f"\nEmail {i}:")
        print(f"Subject: {email['subject']}")
        print(f"Spam: {'YES' if result.is_spam else 'NO'}")
        print(f"False Advertisement: {'YES' if result.is_false_ad else 'NO'}")
        print(f"Confidence Score: {result.confidence_score:.2f}")
        
        if result.detected_patterns:
            print("Detected Patterns:")
            for pattern in result.detected_patterns:
                print(f"  - {pattern}")
        
        if result.risk_factors:
            print("Risk Factors:")
            for factor in result.risk_factors:
                print(f"  - {factor}")
        
        print("-" * 40)

if __name__ == "__main__":
    main()

    