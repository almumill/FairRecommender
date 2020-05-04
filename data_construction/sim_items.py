import numpy as np

# this function assumes we're taking in rows from user_df
# the columns are "movieId", "movie title", "release date", "video release date", "IMDb URL ", "unknown", "Action",
# "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
# "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"

def compare_vals(row1, row2):
    intersection_count = 0
    union_count = 0

    # column 6 is the first category, "Action"
    categories_start_idx = 6
    col_count = len(row1.columns)
    col_names = row1.columns

    row1_values = row1.values[0]
    row2_values = row2.values[0]

    # count the number of categories they have in common
    for x in range(categories_start_idx, col_count):
        
        if row1_values[x] == 1 and row2_values[x] == 1:
            intersection_count += 1
        if row1_values[x] == 1 or row2_values[x] == 1:
            union_count += 1

    # avoid division by 0 if neither movie has a category for some reason
    if union_count == 0:
        union_count = 1

    return float(intersection_count / union_count)

# pass in the user info dataframe
def sim_items_predicate(movies_df, setting = 'eval'):
    """
    User similarity predicate
    """
    filename = "../movielens/data/" + setting + "/sim_items_obs.txt"
    handle = open(filename, "w")
    indices = movies_df.index
    # pairwise comparison of every user for now
    for x in range(len(indices)):

        after_x_len = len(indices[x+1:])
        x_similarities = []

        for y in range(after_x_len):
            x_similarities += [compare_vals(movies_df[movies_df.index == indices[x]], movies_df[movies_df.index == indices[y+x+1]])]

        # sort similarities and pick the block_size highest
        sims = np.argsort(x_similarities)
        for y in range(after_x_len):
            handle.write(str(indices[x]) + "\t" + str(indices[sims[y]+x+1]) + "\t" + str(x_similarities[sims[y]]) + "\n")
            handle.write(str(indices[sims[y]+x+1]) + "\t" + str(indices[x]) + "\t" + str(x_similarities[sims[y]]) + "\n")

