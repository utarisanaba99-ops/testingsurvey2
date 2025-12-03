import streamlit as st
import pandas as pd

# Function to load and clean data
def load_data():
    DATABASE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTAxA9VZ8KpyHJndvE7e3qA3U2emxqKEtCIMEHYY0dYeUZL4ky3QJEayCbF7E9l22t7tV82bSBdbjHp/pub?gid=195728822&single=true&output=csv"
    RESPONSE_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTAxA9VZ8KpyHJndvE7e3qA3U2emxqKEtCIMEHYY0dYeUZL4ky3QJEayCbF7E9l22t7tV82bSBdbjHp/pub?gid=725032840&single=true&output=csv"

    # Load both course database and response data
    course_database = pd.read_csv(DATABASE_SHEET_URL)
    response_data = pd.read_csv(RESPONSE_SHEET_URL)

    # Clean up data (strip and lowercase for consistency)
    course_database['Matakuliah'] = course_database['Matakuliah'].str.strip().str.upper()
    response_data['Mata Kuliah'] = response_data['Mata Kuliah'].str.strip().str.upper()

    # Ensure NIM columns are of the same type for comparison
    course_database['NIM'] = course_database['NIM'].astype(str)
    response_data['NIM'] = response_data['NIM'].astype(str)

    return course_database, response_data

# Streamlit UI
st.title("Cek Kelengkapan Pengisian Survei")
student_id = st.text_input("Masukkan NIM anda:")

if st.button("Show"):
    if student_id:
        # Load and clean data
        course_database, response_data = load_data()

        # Filter for the student's courses
        student_courses = course_database[course_database['NIM'] == student_id]

        # Filter for the student's responses
        response_data_filtered = response_data[response_data['NIM'] == student_id]

        # Debug: Uncomment these lines if you want to check the data during debugging
        # st.write("Debug: Course Database DataFrame", course_database)
        # st.write("Debug: Response DataFrame", response_data)
        # st.write("Debug: Filtered Response DataFrame", response_data_filtered)

        if not student_courses.empty:
            # Check if the courses are filled in response data
            student_courses['IKM Sudah Terisi'] = student_courses['Matakuliah'].apply(
                lambda x: 'Sudah' if x in response_data_filtered['Nama mata kuliah yang diampu sesuai nama dosen yang dipilih sebelumnya'].values else 'Belum'
            )

            # Apply color formatting for the 'IKM Sudah Terisi' column
            def color_label(val):
                return 'color: red' if val == 'Belum' else ''

            styled_data = student_courses[['Matakuliah', 'IKM Sudah Terisi']].style.applymap(color_label, subset=['IKM Sudah Terisi'])

            # Show the result
            st.subheader(f"Berikut Hasil Pengisian Survey oleh NIM: {student_id}")
            st.dataframe(styled_data)
        else:
            st.warning(f"No courses found for Student ID {student_id}")
    else:
        st.warning("Please enter a valid Student ID.")

# Add informational message
st.write("---")
st.info("Apabila anda merasa sudah mengisi namun tidak muncul, maka anda salah menginputkan NIM saat pengisian")
