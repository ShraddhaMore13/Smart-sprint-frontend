import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os
from datetime import datetime

class TrainingModule:
    def __init__(self):
        self.dev_recommendation_model = None
        self.timeline_estimation_model = None
        self.dev_recommendation_preprocessor = None
        self.timeline_estimation_preprocessor = None
        self.is_trained = False
        
    def prepare_training_data(self, tickets, developers, performance_data):
        """Prepare training data from historical tickets and developer performance"""
        training_data = []
        
        for ticket in tickets:
            if ticket.get('status') == 'completed' and 'assigned_to' in ticket:
                dev_id = ticket['assigned_to']
                dev = next((d for d in developers if d['id'] == dev_id), None)
                
                if dev:
                    # Extract features
                    features = {
                        'ticket_id': ticket['id'],
                        'complexity': ticket['complexity'],
                        'estimated_hours': ticket['estimated_hours'],
                        'dev_id': dev_id,
                        'dev_skill_count': len(dev['skills']),
                        'dev_availability': dev['availability'],
                        'dev_current_workload': dev['current_workload'],
                    }
                    
                    # Add developer performance metrics
                    dev_perf = performance_data.get(dev_id, {})
                    features.update({
                        'dev_velocity': dev_perf.get('velocity', 0),
                        'dev_accuracy': dev_perf.get('accuracy', 0),
                        'dev_sentiment': dev_perf.get('sentiment', 0),
                        'dev_tickets_completed': dev_perf.get('tickets_completed', 0)
                    })
                    
                    # Calculate skill match
                    ticket_skills = self._extract_skills_from_ticket(ticket)
                    dev_skills = dev['skills']
                    features['skill_match_score'] = self._calculate_skill_match(ticket_skills, dev_skills)
                    
                    # Target variables
                    features['actual_time'] = ticket.get('completion_time', ticket['estimated_hours'])
                    features['on_time'] = 1 if features['actual_time'] <= features['estimated_hours'] * 1.2 else 0
                    features['high_quality'] = 1 if ticket.get('sentiment_score', 0) > 0.7 else 0
                    
                    training_data.append(features)
        
        return pd.DataFrame(training_data)
    
    def _extract_skills_from_ticket(self, ticket):
        """Extract required skills from ticket title and description"""
        text = f"{ticket['title']} {ticket['description']}".lower()
        skills = []
        
        if 'auth' in text or 'login' in text:
            skills.append('auth')
        if 'database' in text or 'sql' in text:
            skills.append('database')
        if 'api' in text or 'endpoint' in text:
            skills.append('api')
        if 'frontend' in text or 'ui' in text or 'react' in text:
            skills.append('frontend')
        if 'backend' in text or 'server' in text:
            skills.append('backend')
        
        return skills
    
    def _calculate_skill_match(self, ticket_skills, dev_skills):
        """Calculate skill match score between ticket and developer"""
        if not ticket_skills:
            return 0.5
        
        exact_matches = sum(1 for skill in ticket_skills if skill in dev_skills)
        related_matches = 0
        for skill in ticket_skills:
            if skill not in dev_skills:
                for dev_skill in dev_skills:
                    if skill in dev_skill or dev_skill in skill:
                        related_matches += 1
                        break
        
        total_matches = exact_matches + related_matches * 0.7
        return min(1.0, total_matches / len(ticket_skills))
    
    def train_developer_recommendation_model(self, training_data):
        """Train a model to recommend developers for tickets"""
        # Prepare features and target
        X = training_data.drop(['ticket_id', 'actual_time', 'on_time', 'high_quality'], axis=1)
        y = training_data['on_time']  # Target: whether ticket was completed on time
        
        # Preprocessing
        numeric_features = ['complexity', 'estimated_hours', 'dev_skill_count', 
                           'dev_availability', 'dev_current_workload', 'dev_velocity', 
                           'dev_accuracy', 'dev_sentiment', 'dev_tickets_completed', 'skill_match_score']
        
        categorical_features = ['dev_id']
        
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])
        
        # Create model pipeline
        model = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Developer Recommendation Model Accuracy: {accuracy:.2f}")
        
        self.dev_recommendation_model = model
        self.dev_recommendation_preprocessor = preprocessor
        return accuracy
    
    def train_timeline_estimation_model(self, training_data):
        """Train a model to estimate ticket completion time"""
        # Prepare features and target
        X = training_data.drop(['ticket_id', 'actual_time', 'on_time', 'high_quality'], axis=1)
        y = training_data['actual_time']  # Target: actual completion time
        
        # Preprocessing
        numeric_features = ['complexity', 'estimated_hours', 'dev_skill_count', 
                           'dev_availability', 'dev_current_workload', 'dev_velocity', 
                           'dev_accuracy', 'dev_sentiment', 'dev_tickets_completed', 'skill_match_score']
        
        categorical_features = ['dev_id']
        
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])
        
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features)])
        
        # Create model pipeline
        model = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        print(f"Timeline Estimation Model RMSE: {rmse:.2f} hours")
        
        self.timeline_estimation_model = model
        self.timeline_estimation_preprocessor = preprocessor
        return rmse
    
    def train_models(self, tickets, developers, performance_data):
        """Train all models"""
        print("Preparing training data...")
        training_data = self.prepare_training_data(tickets, developers, performance_data)
        
        if len(training_data) < 10:
            print("Not enough training data. Need at least 10 completed tickets.")
            return False
        
        print(f"Training with {len(training_data)} historical records...")
        
        # Train developer recommendation model
        print("\nTraining Developer Recommendation Model...")
        dev_rec_accuracy = self.train_developer_recommendation_model(training_data)
        
        # Train timeline estimation model
        print("\nTraining Timeline Estimation Model...")
        timeline_rmse = self.train_timeline_estimation_model(training_data)
        
        self.is_trained = True
        print("\nModels trained successfully!")
        print(f"Developer Recommendation Accuracy: {dev_rec_accuracy:.2f}")
        print(f"Timeline Estimation RMSE: {timeline_rmse:.2f} hours")
        
        return True
    
    def save_models(self, path='models/'):
        """Save trained models to disk"""
        if not os.path.exists(path):
            os.makedirs(path)
            
        if self.dev_recommendation_model:
            joblib.dump(self.dev_recommendation_model, os.path.join(path, 'dev_recommendation_model.pkl'))
            print(f"Developer recommendation model saved to {path}")
        
        if self.timeline_estimation_model:
            joblib.dump(self.timeline_estimation_model, os.path.join(path, 'timeline_estimation_model.pkl'))
            print(f"Timeline estimation model saved to {path}")
    
    def load_models(self, path='models/'):
        """Load trained models from disk"""
        try:
            if os.path.exists(os.path.join(path, 'dev_recommendation_model.pkl')):
                self.dev_recommendation_model = joblib.load(os.path.join(path, 'dev_recommendation_model.pkl'))
                print("Developer recommendation model loaded.")
            
            if os.path.exists(os.path.join(path, 'timeline_estimation_model.pkl')):
                self.timeline_estimation_model = joblib.load(os.path.join(path, 'timeline_estimation_model.pkl'))
                print("Timeline estimation model loaded.")
            
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def recommend_developers(self, ticket, developers, performance_data, top_n=3):
        """Recommend developers for a ticket using trained model"""
        if not self.is_trained or not self.dev_recommendation_model:
            return None
        
        recommendations = []
        
        for dev in developers:
            # Check if developer has enough availability
            if dev['current_workload'] + ticket['estimated_hours'] > dev['availability']:
                continue  # Skip developers who don't have enough availability
            
            # Prepare features for this developer-ticket pair
            features = {
                'complexity': ticket['complexity'],
                'estimated_hours': ticket['estimated_hours'],
                'dev_id': dev['id'],
                'dev_skill_count': len(dev['skills']),
                'dev_availability': dev['availability'],
                'dev_current_workload': dev['current_workload'],
            }
            
            # Add developer performance metrics
            dev_perf = performance_data.get(dev['id'], {})
            features.update({
                'dev_velocity': dev_perf.get('velocity', 0),
                'dev_accuracy': dev_perf.get('accuracy', 0),
                'dev_sentiment': dev_perf.get('sentiment', 0),
                'dev_tickets_completed': dev_perf.get('tickets_completed', 0)
            })
            
            # Calculate skill match
            ticket_skills = self._extract_skills_from_ticket(ticket)
            dev_skills = dev['skills']
            features['skill_match_score'] = self._calculate_skill_match(ticket_skills, dev_skills)
            
            # Convert to DataFrame
            df = pd.DataFrame([features])
            
            # Predict success probability
            success_prob = self.dev_recommendation_model.predict_proba(df)[0][1]
            
            recommendations.append({
                'developer_id': dev['id'],
                'developer_name': dev['name'],
                'match_score': success_prob,
                'skills_match': dev_perf
            })
        
        # Sort by match score and return top N
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:top_n]
    
    def estimate_timeline(self, ticket, developer, performance_data):
        """Estimate ticket completion time using trained model"""
        if not self.is_trained or not self.timeline_estimation_model:
            return None
        
        # Prepare features
        features = {
            'complexity': ticket['complexity'],
            'estimated_hours': ticket['estimated_hours'],
            'dev_id': developer['id'],
            'dev_skill_count': len(developer['skills']),
            'dev_availability': developer['availability'],
            'dev_current_workload': developer['current_workload'],
        }
        
        # Add developer performance metrics
        dev_perf = performance_data.get(developer['id'], {})
        features.update({
            'dev_velocity': dev_perf.get('velocity', 0),
            'dev_accuracy': dev_perf.get('accuracy', 0),
            'dev_sentiment': dev_perf.get('sentiment', 0),
            'dev_tickets_completed': dev_perf.get('tickets_completed', 0)
        })
        
        # Calculate skill match
        ticket_skills = self._extract_skills_from_ticket(ticket)
        dev_skills = developer['skills']
        features['skill_match_score'] = self._calculate_skill_match(ticket_skills, dev_skills)
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Predict completion time
        predicted_time = self.timeline_estimation_model.predict(df)[0]
        
        # Calculate confidence interval and risk level
        std_dev = predicted_time * 0.2  # Assume 20% standard deviation
        confidence_interval = (predicted_time - 1.96 * std_dev, predicted_time + 1.96 * std_dev)
        p80 = predicted_time + 0.84 * std_dev  # 80th percentile
        
        risk_level = 'low'
        if p80 > ticket['estimated_hours'] * 1.5:
            risk_level = 'high'
        elif p80 > ticket['estimated_hours'] * 1.2:
            risk_level = 'medium'
        
        return {
            'estimated_hours': ticket['estimated_hours'],
            'complexity': ticket['complexity'],
            'mean_duration': predicted_time,
            'std_duration': std_dev,
            'p80_duration': p80,
            'confidence_interval': confidence_interval,
            'risk_level': risk_level
        }