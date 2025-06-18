# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Mahjong UI application that provides a graphical interface for playing and analyzing Japanese Mahjong (Riichi Mahjong). It integrates with the akochan AI engine for game analysis and uses Eel to bridge Python backend with a web-based frontend.

## Commands

### Running the Application
```bash
# Launch the main GUI application
python main.py

# Convert Tenhou logs to mjai format
python main.py --tenhou_convlog --year 20XX

# Dump features for ML training
python main.py --dump_feature --input_logdir logdir --input_regex log*.json --output_npzdir outdir

# Check supervised model predictions
python main.py --check_model --log_line XX
python main.py --check_model --log_line XX --player_id P
```

### Building Dependencies
```bash
# Build akochan-reviewer (if needed)
cd akochan-reviewer
cargo build --release
cd ..
```

### Required External Files
Before running, copy these from the akochan project (https://github.com/critter-mj/akochan):
- `ai.dll` (Windows) or `libai.so` (Linux)
- `system.exe`
- `setup_mjai.json`
- `params/` directory

## Architecture

### Backend-Frontend Communication
The application uses Eel for bidirectional communication between Python and JavaScript:

**Python → JavaScript functions:**
- `update_game()` - Updates game display
- `reset_button_ui_game()` - Resets UI buttons
- `activate_*_button()` - Enables specific action buttons
- `show_end_kyoku()` - Displays round results

**JavaScript → Python functions:**
- `get_log()` - Retrieves game log
- `get_game_state()` - Gets current game state
- `tehai_clicked()` - Handles tile clicks
- `do_*()` - Executes game actions
- `start_game()` - Initializes new game

### Core Components

1. **Game Server Integration**: `system.exe` handles game rules and returns available actions as JSON
2. **State Management**: `Global_State` class in `main.py` maintains game state
3. **ML Models**: Neural networks in `lib/ml_modules.py` for AI decision making
4. **Log Processing**: Supports mjai format logs and Tenhou log conversion

### Key Modules
- `lib/mjtypes.py` - Type definitions and game constants
- `lib/util.py` - File I/O and JSON utilities
- `lib/data_proc.py` - ML data processing
- `lib/ml_modules.py` - Neural network architectures
- `lib/tenhou_convlog.py` - Log conversion utilities

### Frontend Structure
- `web/main.html` - Main UI entry point
- `web/js/board.js` - Board rendering
- `web/js/game.js` - Game logic
- `web/js/log.js` - Log viewer functionality

## Development Notes

- Python dependencies are in `requirements.txt`
- No linting or test commands are configured
- The project uses a virtual environment (`myenv/`)
- Game logs are stored in JSON format in the `log/` directory
- Pre-trained ML models are in `supervised_model/`