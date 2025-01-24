import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel('data/Cropped B03 NCV Data.xlsx', sheet_name='Organized Wrist Data')
df2 = pd.read_excel('data/Cropped B03 NCV Data.xlsx', sheet_name='Organized Elbow Data')
#CH1 = EMG
#CH2 = Voltage

df = df.rename(columns={'Time (s)': 'Time', '40V CH1': 'EMG 40', '40V CH2': 'Stim 40', '45V CH1': 'EMG 45',
                       '45V CH2': 'Stim 45', '50V CH1': 'EMG 50', '50V CH2': 'Stim 50',
                       '55V CH1': 'EMG 55', '55V CH2': 'Stim 55'})
df2 = df2.rename(columns={'Time (s)': 'Time', '35V CH1': 'EMG 35', '35V CH2': 'Stim 35', '40V CH1': 'EMG 40',
                       '40V CH2': 'Stim 40', '45V CH1': 'EMG 45', '45V CH2': 'Stim 45',
                       '50V CH1': 'EMG 50', '50V CH2': 'Stim 50'})

sampling_rate = 2000
num_samples = len(df)
num_samples2 = len(df2)
df['Time'] = [i/sampling_rate for i in range(num_samples)]
df2['Time'] = [i/sampling_rate for i in range(num_samples2)]
# Find stimulation pulse and resultant M-waves at each stimulation intensity
# Plot stimulation and EMG channels on separate Y axes
# M-waves = the M-wave represents the activity generated by individual muscle fibres
## innervated by the stimulated motor axons. The response is measured as the EMG activity
## (M-wave) or force associated with the response. The shape and size of the M-wave
## depends on the number and size of activated muscle fibres as well as temporal dispersion
## of their action potentials. Some M-waves may be preceded by a small potential that
## should be discarded in determining motor latencies.
# STIMULATION PULSE = Voltage
# RESULTANT M-Wave = EMG signal
# NCV (m/s) = nerve segment (m) / conduction time (s)
# NCV (m/s) = (distance between S1 & S2)/(Delta T for S2 - Delta T for S1)
# NCV (upper extremity) = 66.22 + age(-0.09) + height(-0.03)
# age = years, height = cm
# NCV (lower extremity) = 90.15 + age(-0.11) + height(-0.22)

def plot_emg_stim(df, emg_column, stim_column):
    """
    Plots EMG and Stimulation data on separate y-axes with a shared x-axis.

    Parameters:
    - df (pd.DataFrame): The dataframe containing the data.
    - emg_column (str): Column name for EMG data.
    - stim_column (str): Column name for Stimulation data.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot EMG data on the primary y-axis
    ax1.plot(df['Time'], df[emg_column], 'b-', label=emg_column)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel(f'{emg_column} (mV)', color='blue')
    ax1.tick_params(axis='y', colors='blue')

    # Create a second y-axis for Stimulation data
    ax2 = ax1.twinx()
    ax2.plot(df['Time'], df[stim_column], 'r-', label=stim_column)
    ax2.set_ylabel('Voltage (mV)', color='red')
    ax2.tick_params(axis='y', colors='red')

    # Add a title and legend
    plt.title(f'{emg_column} and Voltage with Separate Y-Axes')
    fig.tight_layout()
    plt.show()


plot_emg_stim(df, 'EMG 40', 'Stim 40')
plot_emg_stim(df, 'EMG 45', 'Stim 45')
plot_emg_stim(df, 'EMG 50', 'Stim 50')
plot_emg_stim(df, 'EMG 55', 'Stim 55')

def plot_emg_stim2(df2, emg_column, stim_column):
    """
    Plots EMG and Stimulation data on separate y-axes with a shared x-axis.

    Parameters:
    - df (pd.DataFrame): The dataframe containing the data.
    - emg_column (str): Column name for EMG data.
    - stim_column (str): Column name for Stimulation data.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot EMG data on the primary y-axis
    ax1.plot(df2['Time'], df2[emg_column], 'b-', label=emg_column)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel(f'{emg_column} (mV)', color='blue')
    ax1.tick_params(axis='y', colors='blue')

    # Create a second y-axis for Stimulation data
    ax2 = ax1.twinx()
    ax2.plot(df2['Time'], df2[stim_column], 'r-', label=stim_column)
    ax2.set_ylabel('Voltage (mV)', color='red')
    ax2.tick_params(axis='y', colors='red')

    # Add a title and legend
    plt.title(f'{emg_column} and Voltage with Separate Y-Axes')
    fig.tight_layout()
    plt.show()


plot_emg_stim2(df2, 'EMG 35', 'Stim 35')
plot_emg_stim2(df2, 'EMG 40', 'Stim 40')
plot_emg_stim2(df2, 'EMG 45', 'Stim 45')
plot_emg_stim2(df2, 'EMG 50', 'Stim 50')

# M-wave latency = time difference between onset of stimulus to onset of M-wave

### for wrist

def calculate_m_wave_latency_wrist(df, emg_column, stim_column, threshold=4.7):
    """
    Calculate M-wave latency from the onset of stimulus to the onset of M-wave.

    Parameters:
    - emg_column (str): Column name for the EMG data.
    - stim_column (str): Column name for the stimulation data.
    - threshold (float): Threshold value to define M-wave onset (default is 0.03 mV).

    Returns:
    - latency (float): Latency in seconds.
    """
    # Find the index of the highest stimulation level
    stim_max_index = df[stim_column].idxmax()
    stim_max_time = df.loc[stim_max_index, 'Time']  # Time of maximum stimulation

    # Find the onset of the M-wave (first time EMG exceeds the threshold)
    emg_onset_index = df[df[emg_column] > threshold].index[0]
    emg_onset_time = df.loc[emg_onset_index, 'Time']  # Time of M-wave onset

    # Calculate latency
    latency = abs(emg_onset_time - stim_max_time)

    return latency


latency_40 = calculate_m_wave_latency_wrist(df, 'EMG 40', 'Stim 40')
latency_45 = calculate_m_wave_latency_wrist(df, 'EMG 45', 'Stim 45')
latency_50 = calculate_m_wave_latency_wrist(df, 'EMG 50', 'Stim 50')
latency_55 = calculate_m_wave_latency_wrist(df, 'EMG 55', 'Stim 55')

# Print results (if needed)
### for elbow

def calculate_m_wave_latency_elbow(df2, emg_column, stim_column, threshold=3.0):
    """
    Calculate M-wave latency from the onset of stimulus to the onset of M-wave.

    Parameters:
    - emg_column (str): Column name for the EMG data.
    - stim_column (str): Column name for the stimulation data.
    - threshold (float): Threshold value to define M-wave onset (default is 0.03 mV).

    Returns:
    - latency (float): Latency in seconds.
    """
    # Find the index of the highest stimulation level
    stim_max_index = df2[stim_column].idxmax()
    stim_max_time = df2.loc[stim_max_index, 'Time']  # Time of maximum stimulation

    # Find the onset of the M-wave (first time EMG exceeds the threshold)
    emg_onset_index = df2[df2[emg_column] > threshold].index[0]
    emg_onset_time = df2.loc[emg_onset_index, 'Time']  # Time of M-wave onset

    # Calculate latency
    latency = abs(emg_onset_time - stim_max_time)

    return latency


latency_35 = calculate_m_wave_latency_wrist(df2, 'EMG 35', 'Stim 35')
latency_40 = calculate_m_wave_latency_wrist(df2, 'EMG 40', 'Stim 40')
latency_45 = calculate_m_wave_latency_wrist(df2, 'EMG 45', 'Stim 45')
latency_50 = calculate_m_wave_latency_wrist(df2, 'EMG 50', 'Stim 50')


###

def calculate_m_wave_amplitude(df, emg_column, threshold=0.3, window_start=0, window_end=2.0):
    """
    Calculate the maximum amplitude of the M-wave after the stimulus onset.

    Parameters:
    - threshold (float): Threshold value to define M-wave onset (default is 0.03 mV).
    - window_start (float): Start time (in seconds) to search for the M-wave after the stimulus (default is 0.05s).
    - window_end (float): End time (in seconds) to search for the M-wave (default is 0.2s).

    Returns:
    - max_amplitude (float): Maximum amplitude of the M-wave within the window.
    """

    # Find the onset of the M-wave (first time EMG exceeds the threshold)
    emg_onset_index = df[df[emg_column] > threshold].index[0]
    emg_onset_time = df.loc[emg_onset_index, 'Time']  # Time when M-wave onset exceeds threshold

    # Define the time window after the stimulus to search for the M-wave
    window_start_time = emg_onset_time + window_start
    window_end_time = emg_onset_time + window_end

    # Filter the dataframe to only include rows within the time window
    df_window = df[(df['Time'] >= window_start_time) & (df['Time'] <= window_end_time)]

    # Calculate the maximum amplitude of the EMG signal within this window
    max_amplitude = df_window[emg_column].max()  # Max EMG value within the window

    return max_amplitude


# Example usage:
max_amplitude_40 = calculate_m_wave_amplitude(df, 'EMG 40')
max_amplitude_45 = calculate_m_wave_amplitude(df, 'EMG 45')
max_amplitude_50 = calculate_m_wave_amplitude(df, 'EMG 50')
max_amplitude_55 = calculate_m_wave_amplitude(df, 'EMG 55')

# Print results (if needed)

max_amplitude_35 = calculate_m_wave_amplitude(df2, 'EMG 35')
max_amplitude_40 = calculate_m_wave_amplitude(df2, 'EMG 40')
max_amplitude_45 = calculate_m_wave_amplitude(df2, 'EMG 45')
max_amplitude_50 = calculate_m_wave_amplitude(df2, 'EMG 50')



#Nerve segment
#Proximal nerve segment (S2-Active electrode) (m) = 0.35m
elbow_nerve_segment = 0.35
print(f"Proximal nerve segment = {elbow_nerve_segment} m")
#Distal nerve segment (S1-Active electrode) (m) = 0.045m
wrist_nerve_segment = 0.045
print(f"Distal nerve segment = {wrist_nerve_segment} m")
#S2-S1 nerve segment (m) = 0.297m
s2_s1_segment = 0.297
print(f"S2-S1 nerve segment = {s2_s1_segment} m")

#M-wave Latencies (1 ms = 0.001s)
#Elbow site (proximal)
elbow_m_wave = round((latency_40+latency_45+latency_50+latency_55)/4,4)
print(f"Average elbow to electrode latency is {elbow_m_wave} s")
#Wrist site (distal)
wrist_m_wave = round((latency_35+latency_40+latency_45+latency_50)/4,4)
print(f"Average wrist to electrode latency is {wrist_m_wave} s")
#Conduction time
#mean conduction velocity is 61m/s
#Conduction time = proximal segment - distal segment
conduction_time = round(elbow_m_wave-wrist_m_wave, 4)
print(f"Conduction time using s2_s1_segment & mean conduction velocity "
      f"of 61 m/s is {conduction_time} s")
#Nerve conduction velocity (nerve segment (m) / conduction time (s))
ncv_a = round(s2_s1_segment/conduction_time, 4)
print(f"Experimental NCV of subject A is {ncv_a} m/s")
ncv_a_predicted = 66.22+(23*-0.09)+(166*-0.03)
print(f"Linear regression equation NCV of subject A is {ncv_a_predicted} m/s")
