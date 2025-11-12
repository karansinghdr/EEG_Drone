# Blink-Controlled Virtual Drone

Control a virtual drone using your blinks! This project uses a Muse EEG headband to detect blinks and control a drone visualization.

## Setup

### 1. Activate the Virtual Environment
```powershell
conda activate eeg
```

### 2. Packages Installed
- `python-osc` - For receiving OSC messages from Muse
- `pygame` - For the drone visualization

## Running the Application

### Step 1: Start muse-io
First, make sure your Muse headband is connected and start the muse-io server:
```bash
muse-io --device Muse-0FED --osc osc.udp://localhost:12000
```
(Replace `Muse-0FED` with your Muse device name if different)

### Step 2: Run the Drone Script
```powershell
conda activate eeg
python blink_drone.py
```

## How to Play

- **BLINK** to make the drone go UP!
- **SPACEBAR** to test without the Muse (simulates a blink)
- Try to keep the drone in the green target zone in the middle of the screen
- **ESC** to quit

## Controls
- Your blinks are detected by the Muse headband and sent via OSC
- Each blink gives the drone an upward boost
- Gravity pulls the drone down constantly
- The goal is to maintain altitude by timing your blinks

## Troubleshooting

- Make sure muse-io is running before starting the Python script
- Ensure the Muse headband has good contact with your forehead
- The OSC server listens on port 12000 - make sure nothing else is using this port
- Use SPACEBAR to test the game mechanics without the Muse headband

Enjoy flying! 🚁👁️
