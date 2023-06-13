import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import ExtraTreesRegressor
from src.assign_global_variables import Blank_identifier

#peak_matrix = Mods_QC_filt[6]

def random_forest_MVI(peak_matrix: pd.DataFrame, iterations: int, tree_num: int):

    # remove any columns with blank data as we're not interested in this data
    peak_matrix.drop(peak_matrix.columns[peak_matrix.columns.str.contains(Blank_identifier)], axis=1, inplace=True)

    # transpose the df
    peak_matrixT = peak_matrix.T

    estimator_rf = ExtraTreesRegressor(n_estimators=tree_num, max_features="log2", n_jobs=-1, bootstrap=True, verbose=1)

    print("\nBeginning random forest imputation with " + str(iterations) + " iterations implemented. This step may take " +
          "a long time dependent on peak matrix size and number of iterations selected")

    x_rf = IterativeImputer(estimator=estimator_rf, max_iter=iterations).fit_transform(peak_matrixT)
    peak_matrixT_imputed = pd.DataFrame(x_rf)

    peak_matrixT_imputed.index = peak_matrixT.index
    peak_matrixT_imputed.columns = peak_matrixT.columns

    peak_matrix_imputed = peak_matrixT_imputed.T
    print("\nRandom forest imputation complete")

    return peak_matrix_imputed





