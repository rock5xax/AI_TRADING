import os

# Base directory for the project
base_dir = "/workspaces/AI_TRADING"  # Update this to your writable directory

# Directory structure
dir_structure = {
    ".": ["README.md", "requirements.txt", ".gitignore", ".env"],
    "config": ["__init__.py", "config.py", "credentials.json"],
    "services": [],
    "services/data_service": ["__init__.py"],
    "services/data_service/src": ["__init__.py", "breeze_connector.py", "data_fetcher.py", "data_processor.py"],
    "services/strategy_service": ["__init__.py"],
    "services/strategy_service/src": ["__init__.py", "strategy.py", "indicators.py"],
    "services/execution_service": ["__init__.py"],
    "services/execution_service/src": ["__init__.py", "order_manager.py", "position_manager.py"],
    "models": ["__init__.py", "predictive_model.py", "risk_model.py"],
    "utils": ["__init__.py", "logger.py", "helpers.py"],
    "tests": ["__init__.py", "test_data_service.py", "test_strategy.py", "test_execution.py"],
    "notebooks": ["data_analysis.ipynb", "strategy_backtest.ipynb"],
    "scripts": ["setup_env.py", "run_trading.py"],
}

# Create directories and files
for folder, files in dir_structure.items():
    try:
        dir_path = os.path.join(base_dir, folder)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print(f"Created directory: {dir_path}")
        for file in files:
            file_path = os.path.join(dir_path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")
                print(f"Created file: {file_path}")
            else:
                print(f"File already exists: {file_path}")
    except PermissionError as e:
        print(f"PermissionError: Cannot create {dir_path}. Please check permissions.")
    except Exception as e:
        print(f"Error: {e}")

print("Directory structure update completed.")

