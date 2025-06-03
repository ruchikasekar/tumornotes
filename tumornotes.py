import pandas as pd
import sqlite3
import json

with open('tumor_notes (2).json') as f:
    data = json.load(f)

df = pd.json_normalize(data)

df = df[['person_id', 'deid_service_date', 'note_type', 'note_text']]

df['response_binary'] = df['note_text'].str.contains(
    'shrinking|diminished|decrease|reduction|smaller|improvement',
    case=False,
    na=False
).astype(int)

conn = sqlite3.connect('tumor_analysis.db')
df.to_sql('tumor_
