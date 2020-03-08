
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Any, Dict
from plot_functions.load_palette import load_palette
import plot_functions.format_axis as fmt
import progressbar as pb

def continuous_discrete_time_plot(
    data: pd.DataFrame,
    ax,
    cont_var: str,
    disc_var: str,
    time_var: str,
    cont_c: Any,
    disc_c: Any,
    cont_min_max: Dict = None,
    x_rotation: float = 0,
    ):
    sns.lineplot(
        x=time_var,
        y=cont_var,
        data=data,
        ax=ax,
        color=cont_c,
    )
    if cont_min_max:
        sns.lineplot(
            x=time_var,
            y=cont_min_max['max'],
            data=data,
            ax=ax,
            color=cont_c,
            alpha=0.5
        )
        sns.lineplot(
            x=time_var,
            y=cont_min_max['min'],
            data=data,
            ax=ax,
            color=cont_c,
            alpha=0.5
        )

    ax.set_ylabel(cont_var)
    ax2 = ax.twinx()
    disc_data = data[[time_var, disc_var]].dropna()
    ax.tick_params(axis='x', labelrotation=x_rotation)
    if disc_data.shape[0]:
        if 'mbrep' in disc_var:
            plot_migraine_as_duration(
                data,
                disc_var,
                ax2,
            )
        else:
            ax2.scatter(
                disc_data[time_var],
                disc_data[disc_var],
                c=disc_c,
            )
        ax2.set_ylabel(disc_var)
    return ax, ax2

def plot_cont_disc_all_subjects(
    all_data: pd.DataFrame,
    cont_var: str,
    disc_var: str,
    cont_min_max: Dict = None,
):
    palette = load_palette()
    fig, axes = plt.subplots(ncols=5, nrows=7, figsize=(30,25))
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    i = 0

    for subject_id, data in pb.progressbar(all_data.groupby('subject_id')):
        data = data[data['Date'].astype(str).str[:4] != '2016'] # filter out 2016
        ax = axes.flatten()[i] 
        if (disc_var in data.columns) and (cont_var in data.columns):
            ax1, ax2 = continuous_discrete_time_plot(
                data,
                ax,
                cont_var,
                disc_var,
                'Date',
                palette[cont_var],
                palette[disc_var],
                cont_min_max,
                20
            )
        swtype = 'None'
        if 'swtype' in data.columns:
            swtype = data.swtype.unique()[0]
        ax.set_title(str(subject_id) + ' ' + str(swtype))
        ax.set_xlabel('')
        i += 1

def discrete_discrete_time_plot(
    data: pd.DataFrame,
    ax,
    var_1: str,
    var_2: str,
    time_var: str,
    c_1: str,
    c_2: str,
    x_rotation: float = 0,
    ):

    ax2 = ax.twinx()
    var2_data = data[[time_var, var_2]].dropna()
    var1_data = data[[time_var, var_1]].dropna()
    if var1_data.shape[0]:
        if 'mbrep' in var_1:
            plot_migraine_as_duration(
                data,
                var_1,
                ax,
            )
        else:
            ax.scatter(
                var1_data[time_var],
                var1_data[var_1],
                c=c_1,
            )
        ax.set_ylabel(var_1)
    if var2_data.shape[0]:
        if 'mbrep' in var_2:
            plot_migraine_as_duration(
                data,
                var_2,
                ax2,
            )
        else:
            ax2.scatter(
                var2_data[time_var],
                var2_data[var_2],
                c=c_2,
            )
        ax2.set_ylabel(var_2)

    ax.tick_params(axis='x', labelrotation=x_rotation)
    return ax, ax2

def plot_disc_disc_all_subjects(
    all_data: pd.DataFrame,
    var_1: str,
    var_2: str,
):
    palette = load_palette()
    fig, axes = plt.subplots(ncols=5, nrows=7, figsize=(30,25))
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    i = 0

    for subject_id, data in pb.progressbar(all_data.groupby('subject_id')):
        data = data[data['Date'].astype(str).str[:4] != '2016'] # filter out 2016
        ax = axes.flatten()[i] 
        if (var_1 in data.columns) and (var_2 in data.columns):
            ax1, ax2 = discrete_discrete_time_plot(
                data,
                ax,
                var_1,
                var_2,
                'Date',
                palette[var_1],
                palette[var_2],
                20
            )
        swtype = 'None'
        if 'swtype' in data.columns:
            swtype = data.swtype.unique()[0]
        ax.set_title(str(subject_id) + ' ' + str(swtype))
        ax.set_xlabel('')
        i += 1

def plot_migraine_as_duration(
        data: pd.DataFrame,
        value_col: str,
        ax = None,
        plot_kwargs: Dict = None,
    ):
    time_data = data[['mbrep_duration_1', 'mbrep_start_date_1', value_col]].dropna()
    time_data['mbrep_start_date_1'] = pd.to_datetime(time_data['mbrep_start_date_1'])
    time_data['mbrep_duration_str_1'] = time_data['mbrep_duration_1'].astype(str) + ' hours'
    time_data['mbrep_end_date_1'] = time_data['mbrep_start_date_1'] + time_data['mbrep_duration_str_1'].apply(pd.Timedelta)
    if plot_kwargs is None:
        palette = load_palette()
        plot_kwargs = {
            'color': palette['mbrep_pain_level_1'],
            'lw': 3,
            #'marker': 'o',
            #'ms': 5,
            #'mew': 1,
            #'mec': palette['mbrep_pain_level_1'],
            #'mfc': 'white'

        }
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 8))
        fmt.despine_thicken_axes(
            ax=ax,
            lw=4,
            fontsize=30,
            rotate_x=0,
        )
        sns.despine()
    for _, row in time_data.iterrows():
        t1 = row.mbrep_start_date_1
        t2 = row.mbrep_end_date_1
        val = row[value_col]
        ax.plot([t1, t2], [val, val], **plot_kwargs)

    return ax
