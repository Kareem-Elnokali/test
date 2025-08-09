#!/usr/bin/env python
"""
Script to set up Google OAuth for django-allauth
Run this after getting your Google OAuth credentials
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def setup_google_oauth(client_id, client_secret):
    """Set up Google OAuth application"""
    try:
        # Get the default site
        site = Site.objects.get(pk=1)
        
        # Create or update Google Social App
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            # Update existing app
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            print("UPDATED: Updated existing Google OAuth app")
        else:
            print("CREATED: Created new Google OAuth app")
        
        # Add site to the app
        google_app.sites.add(site)
        
        print(f"SUCCESS: Google OAuth setup complete!")
        print(f"   - Provider: {google_app.provider}")
        print(f"   - Client ID: {client_id[:10]}...")
        print(f"   - Site: {site.domain}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Error setting up Google OAuth: {e}")
        return False

if __name__ == "__main__":
    print("Google OAuth Setup Script")
    print("=" * 40)
    
    if len(sys.argv) != 3:
        print("Usage: python setup_google_oauth.py <client_id> <client_secret>")
        print("\nTo get these credentials:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Google+ API")
        print("4. Create OAuth 2.0 credentials")
        print("5. Add redirect URI: http://127.0.0.1:8000/accounts/google/login/callback/")
        sys.exit(1)
    
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
    
    success = setup_google_oauth(client_id, client_secret)
    
    if success:
        print("\nNext steps:")
        print("1. Restart your Django server")
        print("2. Google login buttons will be automatically enabled")
        print("3. Test Google login at http://127.0.0.1:8000/accounts/login/")
    else:
        print("\nSetup failed. Please check the error above.")
