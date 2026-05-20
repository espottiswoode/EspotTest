import dataiku
import pandas as pd

# Initialize
client = dataiku.api_client()
project = client.get_project(dataiku.default_project_key())

# Define the mapping for buckets
# Any type not in this list will default to 'Other / Visual Analyst'
ROLE_MAP = {
    'python': 'Data scientist group',
    'sql_query': 'Data analyst group'
}

data_summary = []

for r in project.list_recipes():
    # .get_info() returns basic metadata including the creator (owner)
    recipe_handle = project.get_recipe(r['name'])
    info = recipe_handle.get_info()
    
    # Extract details
    rtype = r['type']
    creator = info.get('owner', 'Unknown')
    
    data_summary.append({
        "recipe_name": r['name'],
        "recipe_type": rtype,
        "user_login": creator,
        "assigned_bucket": ROLE_MAP.get(rtype, 'Other / Visual Analyst')
    })

# Write output
df = pd.DataFrame(data_summary)
dataiku.Dataset("recipe_usage").write_with_schema(df)