import dataiku
import pandas as pd

# 1. Initialize the client and project
client = dataiku.api_client()
# It's best practice to use the current project key dynamically
project_key = dataiku.default_project_key()
project = client.get_project(project_key)

recipes = project.list_recipes()

# List to store our results for a final table
data_summary = []

# 2. Loop through recipes and extract metadata
for r_summary in recipes:
    recipe_name = r_summary['name']
    recipe_type = r_summary['type']
    
    # Get recipe settings
    recipe = project.get_recipe(recipe_name)
    settings = recipe.get_settings()
    raw_data = settings.data
    
    # Extract metadata from the 'recipe' nested dictionary
    recipe_meta = raw_data.get('recipe', {})
    creation_info = recipe_meta.get('creationTag', {})
    creator = creation_info.get('lastModifiedBy', {}).get('login', 'Unknown')
    
    # --- ASSIGNMENT LOGIC ---
    if recipe_type == 'python':
        assigned_group = "Data scientist group"
    elif recipe_type == 'sql_query':
        assigned_group = "Data analyst group"
    else:
        assigned_group = "Other / Visual Analyst"
    
    data_summary.append({
        "recipe_name": recipe_name,
        "recipe_type": recipe_type,
        "user_login": creator,
        "assigned_bucket": assigned_group
    })

# 3. Create the DataFrame
recipe_usage_df = pd.DataFrame(data_summary)

# 4. Write the results to the output dataset 'recipe_usage'
recipe_usage_dataset = dataiku.Dataset("recipe_usage")
recipe_usage_dataset.write_with_schema(recipe_usage_df)

print("Successfully audited {} recipes.".format(len(data_summary)))