import pandas as pd
import numpy as np
import os
from sklearn.decomposition import PCA
import plotly.express as px
from src.assign_global_variables import Blank_identifier, path

def plot_PCA(df: pd.DataFrame, Bio_groups: list, Media_groups: list):

    #Label groups and prep matrix into format ready for PCA

    #get sample groups into a list
    groups = Bio_groups + Media_groups
    groups.append("QC")

    #remove any columns with blank data as we're not interested in this data
    df.drop(df.columns[df.columns.str.contains(Blank_identifier)], axis=1, inplace=True)

    #transpose the df
    df_trans = df.T

    #add a column for which sample group each sample belongs too
    groups_col = list()

    for i in df_trans.index:

        for g in groups:

            if g in i:

                groups_col.append(g)

                break

    df_trans.insert(0, "group", groups_col)

    #get a list of the variables(features/peaks)
    peaks = df_trans.columns[1:]

    # all PCAs done following the tutorial at the following link below
    #https://plotly.com/python/pca-visualization/

    #
    if(os.path.exists(path + "/PCA") == False):

        os.mkdir(path + "/PCA")

    pca = PCA()
    components = pca.fit_transform(df_trans[peaks])
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig = px.scatter_matrix(
        components,
        labels=labels,
        dimensions=range(4),
        color=df_trans["group"]
    )
    fig.update_traces(diagonal_visible=False)
    fig.show()
    fig.write_html(path + "PCA/Multiple_PCAs.html")

    #2D PCA plot
    pca = PCA(n_components=2)
    components = pca.fit_transform(df_trans[peaks])

    fig = px.scatter(components, x=0, y=1, color=df_trans['group'])
    fig.show()
    fig.write_html(path + "PCA/2D_PCA.html")

    #3D PCA plot
    pca = PCA(n_components=3)
    components = pca.fit_transform(df_trans[peaks])

    total_var = pca.explained_variance_ratio_.sum() * 100

    fig = px.scatter_3d(
        components, x=0, y=1, z=2, color=df_trans['group'],
        title=f'Total Explained Variance: {total_var:.2f}%',
        labels={'0': 'PC 1', '1': 'PC 2', '2': 'PC 3'}
    )
    fig.show()
    fig.write_html(path + "PCA/3D_PCA.html")

    #see how much variance is explained
    pca = PCA()
    pca.fit(df_trans[peaks])
    exp_var_cumul = np.cumsum(pca.explained_variance_ratio_)

    px.area(
        x=range(1, exp_var_cumul.shape[0] + 1),
        y=exp_var_cumul,
        labels={"x": "# Components", "y": "Explained Variance"}
    )

    #
    pca = PCA(n_components=2)
    components = pca.fit_transform(df_trans[peaks])

    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    fig = px.scatter(components, x=0, y=1, color=df_trans['group'])
    fig.show()

    print("WHY IS THIS NOT WORKING")

    for i, feature in enumerate(df_trans[peaks]):
        fig.add_annotation(
            ax=0, ay=0,
            axref="x", ayref="y",
            x=loadings[i, 0],
            y=loadings[i, 1],
            showarrow=True,
            arrowsize=2,
            arrowhead=2,
            xanchor="right",
            yanchor="top"
        )
        fig.add_annotation(
            x=loadings[i, 0],
            y=loadings[i, 1],
            ax=0, ay=0,
            xanchor="center",
            yanchor="bottom",
            yshift=5,
        )

    print("THIS SHOULD HAVE WORKED")
    fig.show()


