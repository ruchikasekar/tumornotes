import pandas as pd
import sqlite3
import json

with open('tumor_notes (2).json', encoding='utf-8') as f:
    data = json.load(f)

df = pd.json_normalize(data)

df = df[['person_id', 'deid_service_date', 'note_type', 'note_text']]

df['response_binary'] = df['note_text'].str.contains(
    'shrinking|diminished|decrease|reduction|smaller|improvement',
    case=False,
    na=False
).astype(int)

conn = sqlite3.connect('tumor_analysis.db')
df.to_sql('tumor_notes', conn, if_exists='replace', index=False)

query = """
SELECT note_type,
       COUNT(*) AS total_notes,
       SUM(response_binary) AS positive_responses,
       ROUND(AVG(response_binary) * 100.0, 2) AS response_rate_percent
FROM tumor_notes
GROUP BY note_type
ORDER BY positive_responses DESC;
"""

result = pd.read_sql(query, conn)
result
