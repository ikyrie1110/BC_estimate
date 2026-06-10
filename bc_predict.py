import sys
import os
import numpy as np
import pandas as pd
import joblib
import warnings
from tkinter import filedialog, Tk

# Try to import tqdm (optional)
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

warnings.filterwarnings('ignore')


def resource_path(relative_path):
    """Get absolute path for resource files, supports PyInstaller packaging"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# ==================== Configuration ====================
# Note: Feature names will be dynamically loaded from feature_names.pkl
# If your input CSV column names differ from model feature names, modify the mapping below
COLUMN_MAPPING = {
    # Format: 'column_name_in_input' : 'model_feature_name'
    'YEAR': 'YEAR',
    'MONTH': 'MONTH',
    'CO': 'CO',
    'NO2': 'NO2',
    'SO2': 'SO2',
    'T': 'T',       # wind direction
    'SP': 'SP',       # pressure (or SP)
    'TP': 'TP',     # precipitation (or TP)
    'TAP': 'BCTAP',
}
# ========================================================


def load_model():
    """Load XGBoost model and feature names"""
    print("\nLoading model...")
    try:
        model = joblib.load(resource_path('xgb_best_model.pkl'))
        feature_names = joblib.load(resource_path('feature_names.pkl'))
        print("Model loaded successfully!")
        # print(f"Model features ({len(feature_names)}): {feature_names}")
        return model, feature_names
    except Exception as e:
        print(f"Model loading failed: {e}")
        return None, None


def select_input_file():
    """Select input CSV file using file dialog"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Select Input CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path


def select_output_file(default_name="bc_estimation.csv"):
    """Select output CSV file path"""
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.asksaveasfilename(
        title="Save Result as CSV File",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        initialfile=default_name
    )
    root.destroy()
    return file_path


def map_columns(df, target_feature_names):
    """
    Map input dataframe column names to model feature names
    """
    df_mapped = df.copy()
    for src_col, dst_col in COLUMN_MAPPING.items():
        if src_col in df_mapped.columns:
            df_mapped.rename(columns={src_col: dst_col}, inplace=True)
    return df_mapped


def predict_batch_vectorized(df_features, model, feature_names):
    """
    Batch vectorized prediction - process all data at once
    """
    # Ensure all feature columns exist, fill missing with default values
    for col in feature_names:
        if col not in df_features.columns:
            if col in ['year', 'month']:
                df_features[col] = 2013 if col == 'year' else 1
            else:
                df_features[col] = 0.0
            print(f"  Warning: Missing feature column '{col}', filled with default 0")
    
    # Extract feature matrix in the order used during training
    X = df_features[feature_names].values
    X = np.nan_to_num(X, nan=0.0)
    
    # Batch prediction
    predictions = model.predict(X)
    
    # Ensure non-negative (BC concentration cannot be negative)
    predictions = np.maximum(predictions, 0)
    
    return predictions


def predict_batch(input_file_path, output_file_path, model, feature_names):
    """Main batch prediction function"""
    try:
        # Read input file
        print(f"\nReading input file: {input_file_path}")
        df_original = pd.read_csv(input_file_path)
        print(f"Successfully loaded {len(df_original)} records")
        
        # Map column names
        df_mapped = map_columns(df_original, feature_names)
        
        # Check for missing required features
        missing_cols = [col for col in feature_names if col not in df_mapped.columns]
        if missing_cols:
            print(f"Warning: Input file missing the following feature columns: {missing_cols}")
            print("These columns will be filled with default values, which may reduce prediction accuracy.")
            print(f"Full feature list required by model: {feature_names}")
        
        # Batch prediction
        # print("\nEstimating BC concentration (batch mode)...")
        predictions = predict_batch_vectorized(df_mapped, model, feature_names)
        
        # Build output DataFrame
        df_output = df_original.copy()
        df_output['BC_Predicted'] = predictions
        
        # Save result
        df_output.to_csv(output_file_path, index=False, encoding='utf-8-sig')
        
        # Print statistics
        # print("\n" + "=" * 50)
        # print("Estimation Statistics:")
        # print(f"  Total samples: {len(df_output)}")
        # print(f"  BC concentration range: [{predictions.min():.4f}, {predictions.max():.4f}] μg/m³")
        # print(f"  Mean BC concentration: {predictions.mean():.4f} μg/m³")
        # print(f"  Standard deviation: {predictions.std():.4f} μg/m³")
        # print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"Processing failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 60)
    print("Black Carbon (BC) Concentration Estimation Tool")
    # print("Based on XGBoost model")
    print("=" * 60)
    
    # Load model
    model, feature_names = load_model()
    if model is None or feature_names is None:
        input("\nPress Enter to exit...")
        return
    
    # Select input file
    input_file = select_input_file()
    if not input_file:
        print("No input file selected. Exiting...")
        input("\nPress Enter to exit...")
        return
    
    # Generate default output filename
    base_name = os.path.basename(input_file)
    name_without_ext = os.path.splitext(base_name)[0]
    default_output = os.path.join(
        os.path.dirname(input_file),
        f"BC_result_{name_without_ext}.csv"
    )
    
    # Select output file
    output_file = select_output_file(default_output)
    if not output_file:
        print("No output file path selected. Exiting...")
        input("\nPress Enter to exit...")
        return
    
    # Perform prediction
    success = predict_batch(input_file, output_file, model, feature_names)
    
    if success:
        print(f"\n✅ Estimation completed! Results saved to: {output_file}")
        open_folder = input("\nOpen output folder? (y/n): ").strip().lower()
        if open_folder == 'y':
            folder = os.path.dirname(output_file)
            if sys.platform == 'win32':
                os.startfile(folder)
            elif sys.platform == 'darwin':
                os.system(f'open "{folder}"')
            else:
                os.system(f'xdg-open "{folder}"')
    
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
