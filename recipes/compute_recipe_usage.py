import dataiku
import pandas as pd

client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())

# Mapping for roles
ROLE_MAP = {'python': 'Data scientist group', 'sql_query': 'Data analyst group'}

data_summary = []

for r in project.list_recipes():
    # get_definition() is the most universal way to get the 'creationTag'
    definition = project.get_recipe(r['name']).get_definition()
    
    # Extract creator login from the standard creationTag location
    creator = definition.get('creationTag', {}).get('lastModifiedBy', {}).get('login', 'Unknown')
    
    data_summary.append({
        "recipe_name": r['name'],
        "recipe_type": r['type'],
        "user_login": creator,
        "assigned_bucket": ROLE_MAP.get(r['type'], 'Other / Visual Analyst')
    })

# Write out the results
df = pd.DataFrame(data_summary)
dataiku.Dataset("recipe_usage").write_with_schema(df)