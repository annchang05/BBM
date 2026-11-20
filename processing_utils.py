import os
from opensim import Model
from linecache import getline
from decimal import Decimal
import pandas as pd
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

def generate_dict(path):
    """Generating a dict for each given weight condition"""
    path_str = str(path)
    def sto_Getline(p):
        return getline(p, judge_line_number(p)).strip('\n').split()
    header = sto_Getline(path_str)
    col_dict = dict(zip(header, range(len(header))))
    for each, idx in col_dict.items():
        print(each, ':', idx)
    return col_dict

def judge_line_number(path):
    """Helper function for generate_dict"""
    count = 1
    f = open(path,"r")
    line = f.readline()
    while line!="":
        s=line[:4]
        if s.upper()=="time".upper():
          return count
        else:
          count = count + 1
          line = f.readline()

def load_file(file_name: str | Path) -> pd.DataFrame:
    """Load OpenSim kinematics (.mot/.sto) into a float DataFrame."""
    header_row_idx = judge_line_number(file_name) - 1  
    df = pd.read_csv(file_name, sep=r"\s+", skiprows=header_row_idx)
    return df

def extract_participant_data(
        subject_path: str,
        squat_condition: str,
        output_dir: str = None,
        start_time: float = None,
        end_time: float = None
        
    ):

    """Extracts a participant's data from the given subject path and squat condition
    - unweighted, weighted_10p, weighted_25p

    compute min/max joint angles, save to a .txt file, and save individual
    angle plots as .png files
    

   Args: 
       subject_path (str): The path to the subject's data directory.
       squat_condition (str): The squat condition to extract data for.
       output_dir (str): directory to save output files, if none, will save to default path
       start_time (float): start time for squat mot
       end_time (float): end time for squat mot

"""
    subject_dir = Path(subject_path)
    mot_filename = squat_condition if squat_condition.endswith(".mot") else f"{squat_condition}.mot"
    full_mot_path = subject_dir / 'OpenSimData' / 'Kinematics' / mot_filename
    model_path = subject_dir / 'OpenSimData'/ 'Model' / 'LaiUhlrich2022_scaled.osim'

    if output_dir is None:
        output_folder = Path("Data") / subject_dir.name / Path(squat_condition).stem
    else:
        output_folder = Path(output_dir)
        output_folder.mkdir(parents=True, exist_ok=True)

     
    model = Model(str(model_path))
    state = model.initSystem()
    muscle_count = 0
    for d in model.getMuscleList():
        muscle_count = muscle_count + 1
    generate_dict(full_mot_path)

    df_ik = load_file(full_mot_path)

    # start of plotting/max and mins
    df_ik = df_ik[df_ik["time"] > 0.5].copy()
    if start_time is not None and end_time is not None:
        df_ik = df_ik[(df_ik["time"] >= start_time) & (df_ik["time"] <= end_time)].copy()
        x_ik = np.linspace(0, 100, len(df_ik))
        x_label = "Squat Repetition (%)"
    else:
        x_ik = df_ik["time"]
        x_label = "Time (s)"

    style_r = dict(color="#1f77b4", width=2)               
    style_l = dict(color="#ff7f0e", width=2, dash="dash")  
    style_t = dict(color="#961fb4", width=2)      

    # joint angles that we want 
    angle_groups = [
        (
            "Hip Flexion Angle",
            "hip_flexion_angle",
            [("hip_flexion_r", "Right", style_r), ("hip_flexion_l", "Left", style_l)],
        ),
        (
            "Hip Adduction Angle",
            "hip_adduction_angle",
            [("hip_adduction_r", "Right", style_r), ("hip_adduction_l", "Left", style_l)],
        ),
        (
            "Hip Rotation Angle",
            "hip_rotation_angle",
            [("hip_rotation_r", "Right", style_r), ("hip_rotation_l", "Left", style_l)],
        ),
        (
            "Knee Angle",
            "knee_angle",
            [("knee_angle_r", "Right", style_r), ("knee_angle_l", "Left", style_l)],
        ),
        (
            "Ankle Angle",
            "ankle_angle",
            [("ankle_angle_r", "Right", style_r), ("ankle_angle_l", "Left", style_l)],
        ),
        (
            "Trunk Extension Angle",
            "trunk_extension_angle",
            [("lumbar_extension", "Trunk", style_t)],
        ),
    ]

    min_max_stats: dict[str, dict[str, float]] = {}
    condition_label = Path(squat_condition).stem
    subject_label = subject_dir.name
    os.makedirs(output_folder, exist_ok=True)

    # compute min/max and generate + save plot per angle
    for title, slug, channels in angle_groups:
        fig = go.Figure()
        has_data = False

        for col_name, trace_label, line_style in channels:
            if col_name not in df_ik.columns:
                continue

            has_data = True
            series = df_ik[col_name]
            max_val = float(series.max())
            min_val = float(series.min())
            min_max_stats[col_name] = {"max": max_val, "min": min_val}

            print(f"max_{col_name} = {max_val:.4f} degrees")
            print(f"min_{col_name} = {min_val:.4f} degrees")

            fig.add_trace(
                go.Scatter(
                    x=x_ik,
                    y=series,
                    name=trace_label,
                    line=line_style,
                )
            )

        if has_data:
            descriptive_title = f"{subject_label} ({condition_label}) - {title}"
            fig.update_layout(
                title=descriptive_title,
                xaxis_title=x_label,
                yaxis_title="Angle (degrees)",
                template="plotly_white",
                width=900,
                height=500,
            )
            fig.write_image(f"{output_folder}/{condition_label}_{slug}.png")

    # save max and min values to a .txt file in the same output folder
    txt_path = output_folder / f"{condition_label}_angle_min_max.txt"
    with open(txt_path, "w") as f:
        f.write(f"Subject: {subject_label}\n")
        f.write(f"Condition: {condition_label}\n")
        f.write(f"Source File: {full_mot_path}\n")
        f.write("-" * 50 + "\n")
        for col_name, stats in min_max_stats.items():
            f.write(
                f"{col_name}: max = {stats['max']:.4f} deg, min = {stats['min']:.4f} deg\n"
            )

    print(f"Saved min/max summary to: {txt_path}")
    return min_max_stats

