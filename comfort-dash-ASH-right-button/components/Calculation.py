


##### stand by

def update_output(selected_model, temp, mrt, speed):
    # if not temp or not mrt or not speed:
    #     return "Please provide all inputs."
     # Debugging print statements

    print("update_output I 'm here")
    print(f"Selected model: {selected_model}, Temp: {temp}, MRT: {mrt}, Speed: {speed}")

    temp = float(temp)
    mrt = float(mrt)
    # 使用正则表达式提取速度中的数值部分
    speed_value = re.findall(r"[-+]?\d*\.\d+|\d+", speed)
    if speed_value:
          speed = float(speed_value[0])
    else:
          raise ValueError("Invalid speed format")
    # 根据选中的模型，调用不同的计算函数
    if selected_model == 'Adaptive - ASHRAE 55':
        # result_80, result_90 = Calculation.calculate_adaptive_ashrae(temp, mrt, 20, speed)
        # return f"The 80% acceptability limits is: {result_80} and the 90% acceptability limits is: {result_90}"
        # 获取计算结果
        tmp_cmf, tmp_cmf_80_low, tmp_cmf_80_up, tmp_cmf_90_low, tmp_cmf_90_up, acceptability_80, acceptability_90 = Calculation.update_output(temp, mrt, 20, speed)
        
        # 生成输出文本
        result_text = (
            f"The comfortable temperature (tmp_cmf) is: {tmp_cmf:.2f}°C.\n"
            f"The 80% acceptability temperature range is: {tmp_cmf_80_low:.2f}°C to {tmp_cmf_80_up:.2f}°C.\n"
            f"The 90% acceptability temperature range is: {tmp_cmf_90_low:.2f}°C to {tmp_cmf_90_up:.2f}°C.\n"
            f"The conditions are acceptable for 80% of the occupants.\n" if acceptability_80 else f"The conditions are not acceptable for 80% of the occupants.\n"
            f"The conditions are acceptable for 90% of the occupants." if acceptability_90 else "The conditions are not acceptable for 90% of the occupants."
        )

        return result_text
    else:
        return "Unknown model selected"

    # return f"The calculation result is: {result}"