import os
import urllib.parse
password = urllib.parse.quote_plus('2478152Qwd.')
os.environ['DATABASE_URL'] = f'postgresql://postgres.zfwgxqomsikktyovfktn:{password}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require'

from app import create_app
print('Creating app...')
try:
    app = create_app()
    print('App created successfully!')
except Exception as e:
    print('Error in create_app:', e)
