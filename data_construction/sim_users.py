import numpy as np

# this function assumes we're taking in rows from user_df
# the columns are 'age', 'gender', 'occupation', 'zip'
def compare_vals(row1, row2):
    bool_sum = 0

    # we disregard zip code
    if abs(row1['age'].values - row2['age'].values) <= 10:
        bool_sum += 1
    if row1['gender'].values == row2['gender'].values:
        bool_sum += 1
    if row1['occupation'].values == row2['occupation'].values:
        bool_sum += 1

    return float(bool_sum / (len(row1.columns) - 1)) 

# pass in the user info dataframe
def sim_users_predicate(user_df, setting = 'eval'):
    """
    User similarity predicate
    """
    filename = "../movielens/data/" + setting + "/sim_users_obs.txt"
    handle = open(filename, "w")
    indices = user_df.index
    # pairwise comparison of every user for now
    for x in range(len(indices)):

        after_x_len = len(indices[x+1:])
        x_similarities = []

        for y in range(after_x_len):
            x_similarities += [compare_vals(user_df[user_df.index == indices[x]], user_df[user_df.index == indices[y+x+1]])]

        # sort similarities and pick the block_size highest
        sims = np.argsort(x_similarities)
        for y in range(after_x_len):
            handle.write(str(indices[x]) + "\t" + str(indices[sims[y]+x+1]) + "\t" + str(x_similarities[sims[y]]) + "\n")
            handle.write(str(indices[sims[y]+x+1]) + "\t" + str(indices[x]) + "\t" + str(x_similarities[sims[y]]) + "\n")

