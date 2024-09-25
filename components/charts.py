import base64
import io
from copy import deepcopy
import matplotlib.pyplot as plt

import dash_mantine_components as dmc

import pandas as pd
from pythermalcomfort.models import pmv, set_tmp, two_nodes, adaptive_ashrae, pmv_ppd
from pythermalcomfort.utilities import v_relative, clo_dynamic 

from pythermalcomfort.psychrometrics import psy_ta_rh

from scipy import optimize

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import ElementsIDs, Models
from utils.website_text import TextHome

#import plotly.graph_objects as go

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg', depending on your environment
import tkinter as tk

def chart_selector(selected_model: str):
    list_charts = deepcopy(Models[selected_model].value.charts)
    list_charts = [chart.name for chart in list_charts]
    drop_down_chart_dict = {
        "id": ElementsIDs.chart_selected.value,
        "question": TextHome.chart_selection.value,
        "options": list_charts,
        "multi": False,
        "default": list_charts[0],
    }

    return generate_dropdown_inline(
        drop_down_chart_dict, value=drop_down_chart_dict["default"], clearable=False
    )


# fig example
def t_rh_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    for pmv_limit in pmv_limits:
        for rh in np.arange(0, 110, 10):

            def function(x):
                return (
                    pmv(
                        x,
                        tr=inputs[ElementsIDs.t_r_input.value],
                        vr=vr,
                        rh=rh,
                        met=inputs[ElementsIDs.met_input.value],
                        clo=clo_d,
                        wme=0,
                        standard=model,
                        limit_inputs=False,
                    )
                    - pmv_limit
                )

            temp = optimize.brentq(function, 10, 40)
            results.append(
                {
                    "rh": rh,
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )

    df = pd.DataFrame(results)

    f, axs = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
    t1 = df[df["pmv_limit"] == pmv_limits[0]]
    t2 = df[df["pmv_limit"] == pmv_limits[1]]
    axs.fill_betweenx(
        t1["rh"], t1["temp"], t2["temp"], alpha=0.5, label=model, color="#7BD0F2"
    )
    axs.scatter(
        inputs[ElementsIDs.t_db_input.value],
        inputs[ElementsIDs.rh_input.value],
        color="red",
    )
    axs.set(
        ylabel="RH (%)",
        xlabel="Temperature (°C)",
        ylim=(0, 100),
        xlim=(10, 40),
    )
    axs.legend(frameon=False).remove()
    axs.grid(True, which="both", linestyle="--", linewidth=0.5)
    axs.spines["top"].set_visible(False)
    axs.spines["right"].set_visible(False)
    plt.tight_layout()

    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")
    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Heat stress chart",
        py=0,
    )


def t_hr_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    for pmv_limit in pmv_limits:
        for rh in np.arange(0, 110, 10):

            def function(x):
                return (
                    pmv(
                        x,
                        tr=inputs[ElementsIDs.t_r_input.value],
                        vr=vr,
                        rh=rh,
                        met=inputs[ElementsIDs.met_input.value],
                        clo=clo_d,
                        wme=0,
                        standard=model,
                        limit_inputs=False,
                    )
                    - pmv_limit
                )

            temp = optimize.brentq(function, 10, 40)
            results.append(
                {
                    "rh": rh,
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )

    df = pd.DataFrame(results)

    f, axs = plt.subplots(1, 1, figsize=(6, 4), sharex=True)
    t1 = df[df["pmv_limit"] == pmv_limits[0]]
    t2 = df[df["pmv_limit"] == pmv_limits[1]]
    axs.fill_betweenx(
        t1["rh"], t1["temp"], t2["temp"], alpha=0.5, label=model, color="#7BD0F2"
    )
    axs.scatter(
        inputs[ElementsIDs.t_db_input.value],
        inputs[ElementsIDs.rh_input.value],
        color="red",
    )
    axs.set(
        ylabel="RH (%)",
        xlabel="Temperature (°C)",
        ylim=(0, 100),
        xlim=(10, 40),
    )
    axs.legend(frameon=False).remove()
    axs.grid(True, which="both", linestyle="--", linewidth=0.5)
    axs.spines["top"].set_visible(False)
    axs.spines["right"].set_visible(False)
    plt.tight_layout()

    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")
    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Heat stress chart",
        py=0,
    )


def SET_outputs_chart(
    inputs: dict = None, calculate_ce: bool = False, p_atmospheric: int = 101325
):
    # Dry-bulb air temperature (x-axis)
    tdb_values = np.arange(10, 40, 0.5, dtype=float).tolist()

    # Prepare arrays for the outputs we want to plot
    set_temp = []  # set_tmp()
    skin_temp = []  # t_skin
    core_temp = []  # t_core
    clothing_temp = []  # t_cl
    mean_body_temp = []  # t_body
    total_skin_evaporative_heat_loss = []  # e_skin
    sweat_evaporation_skin_heat_loss = []  # e_rsw
    vapour_diffusion_skin_heat_loss = []  # e_diff
    total_skin_senesible_heat_loss = []  # q_sensible
    total_skin_heat_loss = []  # q_skin
    heat_loss_respiration = []  # q_res
    skin_wettedness = []  # w

    # Extract common input values
    tr = float(inputs[ElementsIDs.t_r_input.value])
    vr = float(
        v_relative(  # Ensure vr is scalar
            v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
        )
    )
    rh = float(inputs[ElementsIDs.rh_input.value])  # Ensure rh is scalar
    met = float(inputs[ElementsIDs.met_input.value])  # Ensure met is scalar
    clo = float(
        clo_dynamic(  # Ensure clo is scalar
            clo=inputs[ElementsIDs.clo_input.value], met=met
        )
    )

    # Iterate through each temperature value and call set_tmp
    for tdb in tdb_values:
        set = set_tmp(
            tdb=tdb,
            tr=tr,
            v=vr,
            rh=rh,
            met=met,
            clo=clo,
            wme=0,
            limit_inputs=False,
        )
        set_temp.append(float(set))  # Convert np.float64 to float

    # Iterate through each temperature value and call `two_nodes`
    for tdb in tdb_values:
        results = two_nodes(
            tdb=tdb,
            tr=tr,
            v=vr,
            rh=rh,
            met=met,
            clo=clo,
            wme=0,
        )
        # Collect relevant data for each variable, converting to float
        skin_temp.append(float(results["t_skin"]))  # Convert np.float64 to float
        core_temp.append(float(results["t_core"]))  # Convert np.float64 to float
        total_skin_evaporative_heat_loss.append(
            float(results["e_skin"])
        )  # Convert np.float64 to float
        sweat_evaporation_skin_heat_loss.append(
            float(results["e_rsw"])
        )  # Convert np.float64 to float
        vapour_diffusion_skin_heat_loss.append(
            float(results["e_skin"] - results["e_rsw"])
        )  # Convert np.float64 to float
        total_skin_senesible_heat_loss.append(
            float(results["q_sensible"])
        )  # Convert np.float64 to float
        total_skin_heat_loss.append(
            float(results["q_skin"])
        )  # Convert np.float64 to float
        heat_loss_respiration.append(
            float(results["q_res"])
        )  # Convert np.float64 to float
        skin_wettedness.append(
            float(results["w"]) * 100
        )  # Convert to percentage and float

        # calculate clothing temperature t_cl
        pressure_in_atmospheres = float(p_atmospheric / 101325)
        r_clo = 0.155 * clo
        f_a_cl = 1.0 + 0.15 * clo
        h_cc = 3.0 * pow(pressure_in_atmospheres, 0.53)
        h_fc = 8.600001 * pow((vr * pressure_in_atmospheres), 0.53)
        h_cc = max(h_cc, h_fc)
        if not calculate_ce and met > 0.85:
            h_c_met = 5.66 * (met - 0.85) ** 0.39
            h_cc = max(h_cc, h_c_met)
        h_r = 4.7
        h_t = h_r + h_cc
        r_a = 1.0 / (f_a_cl * h_t)
        t_op = (h_r * tr + h_cc * tdb) / h_t
        clothing_temp.append(
            float((r_a * results["t_skin"] + r_clo * t_op) / (r_a + r_clo))
        )
        # calculate mean body temperature t_body
        alfa = 0.1
        mean_body_temp.append(
            float(alfa * results["t_skin"] + (1 - alfa) * results["t_core"])
        )

    # Create the figure and axis
    fig, ax1 = plt.subplots(figsize=(8, 6))

    # Plot temperature-related variables on the left y-axis
    ax1.plot(tdb_values, set_temp, label="SET temperature", color="blue")
    ax1.plot(tdb_values, skin_temp, label="Skin temperature", color="cyan")
    ax1.plot(tdb_values, core_temp, label="Core temperature", color="green")
    ax1.plot(tdb_values, clothing_temp, label="Clothing temperature", color="magenta")
    ax1.plot(tdb_values, mean_body_temp, label="Mean body temperature", color="brown")

    # Set labels for the left y-axis
    ax1.set_xlabel("Dry-bulb air temperature [°C]")
    ax1.set_ylabel("Dry-bulb air temperature [°C]")
    ax1.set_ylim(22, 38)

    # Create a secondary y-axis
    ax2 = ax1.twinx()

    # Plot heat loss-related variables on the right y-axis
    ax2.plot(
        tdb_values,
        total_skin_evaporative_heat_loss,
        label="Total skin evaporative heat loss",
        color="black",
    )
    ax2.plot(
        tdb_values,
        sweat_evaporation_skin_heat_loss,
        label="Sweat evaporation skin heat loss",
        color="red",
    )
    ax2.plot(
        tdb_values,
        vapour_diffusion_skin_heat_loss,
        label="Vapour diffusion skin heat loss",
        color="yellow",
    )
    ax2.plot(
        tdb_values,
        total_skin_senesible_heat_loss,
        label="Total skin senesible heat loss",
        color="purple",
    )
    ax2.plot(
        tdb_values, total_skin_heat_loss, label="Total skin heat loss", color="pink"
    )
    ax2.plot(
        tdb_values, heat_loss_respiration, label="Heat loss respiration", color="grey"
    )
    ax2.plot(tdb_values, skin_wettedness, label="Skin wettedness [%]", color="orange")

    # Set labels for the right y-axis
    ax2.set_ylabel("Heat Loss [W/m²] / Skin wettedness [%]")
    ax2.set_ylim(0, 100)

    # Combine legends from both axes and place them below the plot
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines_1 + lines_2,
        labels_1 + labels_2,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        fancybox=True,
        shadow=False,
        ncol=3,  # Set ncol to 3 to arrange in 3 columns
    )

    # Apply a tight layout
    plt.tight_layout()

    # Save the plot as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", dpi=300)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    plt.close()

    return dmc.Image(
        src=f"data:image/png;base64,{img_base64}", alt="SET Outputs Chart", py=0
    )


def pmot_ot_adaptive_ashrae(inputs: dict = None, model: str = "ashrae"):
    results = []
    air_temperature = inputs[ElementsIDs.t_db_input.value]  # Air Temperature
    mean_radiant_temp = inputs[ElementsIDs.t_r_input.value]  # Mean Radiant Temperature
    prevailing_mean_outdoor_temp = inputs[
        ElementsIDs.t_rm_input.value
    ]  # Prevailing Mean Outdoor Temperature
    air_speed = inputs[ElementsIDs.v_input.value]  # Air Speed
    units = inputs[ElementsIDs.UNIT_TOGGLE.value]  # unit（IP or SI）
    operative_temperature = (
        air_temperature + mean_radiant_temp
    ) / 2  # I do not know how to calculate 'operative_temperature', and assume it equals (air_temperature + mean_radiant_temp) / 2
    outdoor_temp_range = np.arange(
        10, 36, 1
    )  # the range of outdoor_temp_range is (10, 35)

    # Traverse the temperature range and calculate the corresponding comfort range
    for t_running_mean in outdoor_temp_range:
        adaptive = adaptive_ashrae(
            tdb=air_temperature,
            tr=mean_radiant_temp,
            t_running_mean=t_running_mean,
            v=air_speed,
        )
        results.append(
            {
                "prevailing_mean_outdoor_temp": t_running_mean,
                "tmp_cmf_80_low": round(adaptive.tmp_cmf_80_low, 2),
                "tmp_cmf_80_up": round(adaptive.tmp_cmf_80_up, 2),
                "tmp_cmf_90_low": round(adaptive.tmp_cmf_90_low, 2),
                "tmp_cmf_90_up": round(adaptive.tmp_cmf_90_up, 2),
            }
        )

    df = pd.DataFrame(results)

    # Create image
    fig, ax = plt.subplots(figsize=(6, 4))
     
    print("Create image")
    # Draw blue areas with 80% and 90% acceptance ranges

    ax.fill_between(
        df["prevailing_mean_outdoor_temp"],
        df["tmp_cmf_80_low"],
        df["tmp_cmf_80_up"],
        color="lightblue",
        label="80% Acceptability",
    )
    ax.fill_between(
        df["prevailing_mean_outdoor_temp"],
        df["tmp_cmf_90_low"],
        df["tmp_cmf_90_up"],
        color="blue",
        label="90% Acceptability",
    )

    print("Draw red dots")
    # Draw red dots：Operative Temperature and Prevailing Mean Outdoor Temperature
    ax.scatter(
        prevailing_mean_outdoor_temp,
        operative_temperature,
        color="red",
        label="Current Condition",
    )

    # Set the axis label and range
    ax.set_xlabel("Prevailing Mean Outdoor Temperature (°C)")
    ax.set_ylabel("Operative Temperature (°C)")
    ax.set_xlim(10, 35)
    ax.set_ylim(df["tmp_cmf_80_low"].min(), df["tmp_cmf_80_up"].max())

    # Displays legends and grids
    ax.legend()
    ax.grid(True)

    plt.tight_layout()

    # Save the image as base64 encoding
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="png", dpi=300, bbox_inches="tight")
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

    # Close the currently drawn image to prevent memory leaks
    plt.close(fig)

    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Adaptive chart",
        py=0,
    )



def t_ra_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]  # PMV upper and lower limits
 
    met_d = float(inputs[ElementsIDs.met_input.value])

    clo_d = clo_dynamic(
        clo = float(inputs[ElementsIDs.clo_input.value]), met = met_d
    )

    vr_d = v_relative(
        v = float(inputs[ElementsIDs.v_input.value]), met = met_d
    )

    current_tr = float(inputs[ElementsIDs.t_r_input.value])
    current_tdb = float(inputs[ElementsIDs.t_db_input.value])
    current_rh = float(inputs[ElementsIDs.rh_input.value])
    
    
    

    psy_data = psy_ta_rh(tdb=current_tdb, rh=current_rh, p_atm=101325)["hr"] * 1000  
    psy_data_rh = psy_data
    print(f"current_tdb: {current_tdb}")
    print(f"current_tr: {current_tr}")
    print(f"vr_d: {vr_d}")
    print(f"current_rh: {current_rh}")
    print(f"met_d: {met_d}")
    print(f"clo_d: {clo_d}")

    
    # Traverse the upper and lower limits of PMV and calculate different rh
    for pmv_limit in pmv_limits:
        for rh in np.arange(10, 110, 10):  # rh increases by 10% each time
            
            # Use optimize.brentq to calculate the temperature at a given rh
            def function(x):
                print(f"Inputs to pmv_ppd -> tdb: {current_tdb}, tr: {current_tr}, vr: {vr_d}, rh: {current_rh}, met: {met_d}, clo: {clo_d}")
    
                # 创建一个字典来存储返回值
                intermediate_values = {
                    "tdb": current_tdb,
                    "tr": current_tr,
                    "vr": vr_d,
                    "rh": current_rh,
                    "met": met_d,
                    "clo": clo_d,
                    "valid": True  # 初始假设所有值有效
                }

                # 将 vr 和 clo 转换为标量值
                intermediate_values["vr"] = intermediate_values["vr"].item() if hasattr(intermediate_values["vr"], 'item') else intermediate_values["vr"]
                intermediate_values["clo"] = intermediate_values["clo"].item() if hasattr(intermediate_values["clo"], 'item') else intermediate_values["clo"]

                # check out whether the input is in the effective area.
                if not (10 < intermediate_values["tdb"] < 40):
                    print(f"tdb {intermediate_values['tdb']} is out of range for ASHRAE limits.")
                    intermediate_values["tdb"] = 11  
                    intermediate_values["valid"] = True
                    
                if not (10 < intermediate_values["tr"] < 40):
                    print(f"tr {intermediate_values['tr']} is out of range for ASHRAE limits.")
                    intermediate_values["tr"] = 11  
                    intermediate_values["valid"] = True

                if not (0 < intermediate_values["vr"] < 2):
                    print(f"vr {intermediate_values['vr']} is out of range for ASHRAE limits.")
                    intermediate_values["vr"] = 0.1  
                    intermediate_values["valid"] = True

                if not (1 < intermediate_values["met"] < 4):
                    print(f"met {intermediate_values['met']} is out of range for ASHRAE limits.")
                    intermediate_values["met"] = 1.1  
                    intermediate_values["valid"] = True

                if not (0 < intermediate_values["clo"] < 1.5):
                    print(f"clo {intermediate_values['clo']} is out of range for ASHRAE limits.")
                    intermediate_values["clo"] = 0.1  
                    intermediate_values["valid"] = True
   
                print("5 if ok")
                print(f"Inputs to pmv_ppd -> {intermediate_values}")

               
                
                
                result = pmv_ppd(
                    tdb=intermediate_values["tdb"],
                    tr=intermediate_values["tr"],
                    vr=intermediate_values["vr"],
                    rh=intermediate_values["rh"],
                    met=intermediate_values["met"],
                    clo=intermediate_values["clo"]
                )
                
                
               
                pmv_value = result.get("pmv", None)
                ppd_value = result.get("ppd", None)
                

                print(f"tdb: {intermediate_values['tdb']}, pmv_value: {pmv_value}, ppd_value: {ppd_value}, pmv_limit:{pmv_limit}")
                
               
                
                return pmv_value, ppd_value

            
            pmv_value, ppd_value = function(x=25)
            
            # print final result
            print(f"Final results -> pmv: {pmv_value}, ppd: {ppd_value}")

            # store the outcomes into result lists
            
            
            results.append({
                    
                    "pmv": pmv_value, 
                    "ppd": ppd_value,
                    "category": "",
            })

            

  
            # calculation part end    
     
    # Initialize figure and axis

    p_tdb = current_tdb
    p_rh = current_rh

    air_speed = vr_d
    met = met_d
    clo = clo_d

    fig, ax = plt.subplots(figsize=(6, 4))

    print("Create psychrometric chart")

    # Define adjustments
    air_speed_adjustment = 0.1  # Increment/decrement for air speed
    met_adjustment = 0.1  # Increment/decrement for metabolic rate
    clo_adjustment = 0.3  # Increment/decrement for clothing value

    # Category III
    offset = (air_speed + air_speed_adjustment) * 1 - (met + met_adjustment) * 2 - (clo + clo_adjustment) * 2
    category_3_up = np.linspace(20.5 + offset, 27.1 + offset, 100)
    category_3_low = np.array([33.3 + offset, 24.2 + offset])
    category_3_x = np.concatenate((category_3_up, category_3_low))
    category_3_y = np.concatenate(
        (
            [psy_ta_rh(tdb=t, rh=100, p_atm=101325)["hr"] * 1000 for t in category_3_up],
            [0, 0],
        )
    )
    ax.fill_between(category_3_x, category_3_y, color="lightgreen", label="Category III")
    
    # Category II
    offset = (air_speed - air_speed_adjustment) * 1 - (met - met_adjustment) * 2 - (clo - clo_adjustment) * 2
    category_2_up = np.linspace(21.4 + offset, 26.2 + offset, 100)
    category_2_low = np.array([32 + offset, 25.5 + offset])
    category_2_x = np.concatenate((category_2_up, category_2_low))
    category_2_y = np.concatenate(
        (
            [psy_ta_rh(tdb=t, rh=100, p_atm=101325)["hr"] * 1000 for t in category_2_up],
            [0, 0],
        )
    )
    ax.fill_between(category_2_x, category_2_y, color="green", label="Category II")
    
    # Category I
    offset = (air_speed + air_speed_adjustment) * 1 - (met + met_adjustment) * 2 - (clo + clo_adjustment) * 2
    category_1_up = np.linspace(22.7 + offset, 24.7 + offset, 100)
    category_1_low = np.array([30 + offset, 27.4 + offset])
    category_1_x = np.concatenate((category_1_up, category_1_low))
    category_1_y = np.concatenate(
        (
            [psy_ta_rh(tdb=t, rh=100, p_atm=101325)["hr"] * 1000 for t in category_1_up],
            [0, 0],
        )
    )
    ax.fill_between(category_1_x, category_1_y, color="darkgreen", label="Category I")

    # 更新红点位置
    red_point = [p_tdb, psy_ta_rh(p_tdb, p_rh, p_atm=101325)["hr"] * 1000]
    ax.scatter(red_point[0], red_point[1], color="red", label="Current Condition")

    # 绘制红点周围的虚线圆圈
    theta = np.linspace(0, 2 * np.pi, 100)
    circle_x = red_point[0] + 0.6 * np.cos(theta)
    circle_y = red_point[1] + 1.2 * np.sin(theta)
    ax.plot(circle_x, circle_y, color="red", linestyle="--")

    print("Plot humidity ratio lines")
    
    # 绘制湿度比曲线
    rh_list = np.arange(0, 101, 10)
    tdb = np.linspace(10, 36, 500)
    for rh in rh_list:
        hr_list = np.array(
            [psy_ta_rh(tdb=t, rh=rh, p_atm=101325)["hr"] * 1000 for t in tdb]
        )
        ax.plot(tdb, hr_list, color="black", linewidth=1, label=f"{rh}% RH")

    # 设置坐标轴和标题
    ax.set_xlabel("Dry-bulb Temperature (°C)")
    ax.set_ylabel("Humidity Ratio (g_w/kg_da)")
    ax.set_title("Psychrometric (air temperature)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    # 保存为 base64
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="png", dpi=300, bbox_inches="tight")
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close(fig)
    
    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Psychrometric chart",
        py=0,
    )



#1. graph moving for each part
#