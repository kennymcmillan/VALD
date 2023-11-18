import streamlit as st
import pandas as pd
from datetime import datetime

# function
def transform_data(df):
    columns_to_drop = ['Tf+Tc', 'PPO / Total mass', 'Tf\\Tc', 'Height', 'Rsi', 'Ppo',
                       'LegStiffness', 'Impulse', 'DeviceCount', 'Total']
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    columns_to_rename = {
        'GivenName': 'Given Name',
        'FamilyName': 'Family Name',
        'JumpIndex': 'Jump index',
        'ContactTime': 'Contact time',
        'FlightTime': 'Flight time'
    }
    df.rename(columns=columns_to_rename, inplace=True)

    df['First Name'] = df['Given Name']
    df['Last Name'] = df['Family Name']

    empty_columns = ['Controller', 'Team', 'Start mode', 'Mass unit', 'Height Unit',
                     'Testing Type', 'External mass', 'Drop height']
    for col in empty_columns:
        df[col] = None

    # Populate specified columns based on non-empty Date column
    date_condition = df['Date'].notna()
    df.loc[date_condition, 'Mass unit'] = "Kilogram"
    df.loc[date_condition, 'Height Unit'] = "Centimetre"
    df.loc[date_condition, 'Testing Type'] = "Testing"

    return df

def main():
    st.title('Aspire Academy - Transform VALD data')

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Original Data")
        st.write(data)


        if st.button('Transform Data'):
            transformed_data = transform_data(data)
            st.write("Transformed Data")
            st.write(transformed_data)

            # Get the current date and time, formatted as 'YYYYMMDD_HHMMSS'
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"VALD_{current_time}.csv"  # Format the file name

            st.download_button(label="Download Transformed Data for Smartabase",
                               data=transformed_data.to_csv(index=False).encode('utf-8'),
                               file_name=file_name,
                               mime='text/csv')

if __name__ == "__main__":
    main()


