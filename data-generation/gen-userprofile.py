import json
import random
import uuid
import zipfile
import os


# Define a function to decompress a file
def decompress_file(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall('../couchbase-server/')
        return os.path.splitext(file_path)[0]  # return the file path without .zip


# Load the JSON data
projects_file_path = decompress_file('../couchbase-server/sample-projects.json.zip')
# Load the projects data from the JSON file
with open(projects_file_path, 'r') as proj_file:
    projects = json.load(proj_file)

# List of popular first names and last names in the United States
first_names = [
    "Blake", "Brett", "Elliot", "Matt", "Denis", "Charles", "Joseph", "Thomas", "Dima", "David", "James", 
	"John", "Christopher", "Paul", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Scott",
    "Russell", "Oliver", "Adam", "Andrew", "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Dana", "Nancy", "Lisa", "Margaret", "Ashley", "Dorothy", "Kimberly", "Emily", "Donna", "Jane", "Alice", "Ruth", "Sharon", "Laura", "Carol", "Michelle", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Nicole", "Christine", "Catherine", "Samantha", "Kathleen", "Virginia", "Diane", "Julie", "Joyce", "Teresa", "Frances", "Gloria", "Evelyn", "Jean", "Cheryl", "Mildred", "Joan", "Eve"
]

last_names = [
    "Smith", "Johnson", "Williams", "Brown", "Tyagi", "Azad", "Chechetkin", "Kanwar", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Chen", "Shree", "Slysz", "Nair", "Fraser", "Meike", "Rosa", "Kolichala", "Maclean", "Cain", "Hall", "McDonough", "Sauve", "Spillar", "Groves", "Ingenthron", "Malucelli", "Cardilo", "Ashworth", "Westwood", "Pople", "Lawson", "Norbye", "Barmin", "Walker", "Owen", "Stemkovski", "Nuthan", "Horn", "Finaly", "Liang", "Murthy", "Kaur", "Yen", "Suravarjjala", "Butler", "Duddi" , "Henry", "Heras", "Kreisa", "Irish", "Chow", "McDonough", "Harber", "Wu", "Kumari", "Lupu", "Kurth", "Ramsey", "Goel", "Ghosh"  
]

# (at least 50% should be picked from this list)
ethnic_first_names = [
    "Aayush", "Dhiraj","Aaliyah", "Nithish", "Imani", "Pasin", "Pramada", "Priya", "Deja", "Jada", "Tiara", "Malik", "Jamal", "Kareem", "Aisha", "Jamal", "José", "Carlos", "Alejandro", "Juan", "Luis", "Miguel", "Francisco", "Antonio", "Javier", "Ricardo", "María", "Sofía", "Guadalupe", "Carmen", "Isabel", "Valeria", "Rosa", "Ana", "Teresa", "Elena", "Rupak", "Muk"
]

# Job titles
job_titles = ["Accountant I", "Accountant II", "Sr Accountant"]

# Function to generate user profiles for each project
def generate_user_profiles(projects):
    user_profiles = []
    email_counter = 1

    for project in projects:
        teams = project['teams']

        for _ in range(2):  # Generate 2 users per project
            # Decide the ethnic group for the first name
            rand_val = random.random()
            if rand_val < 0.5:
                first_name = random.choice(ethnic_first_names)
            else:
                first_name = random.choice(first_names)
            
            last_name = random.choice(last_names)
            job_title = random.choice(job_titles)
            email = f"demo{email_counter}@example.com"
            email_counter += 1

            user_profile = {
                "docId": "user::" + email,
                "surname": last_name,
                "givenName": first_name,
                "jobTitle": job_title,
                "department": "Accounting",
                "teams": teams,
                "email": email,
                "isActive": True
            }

            user_profiles.append(user_profile)

    return user_profiles

# Generate user profiles
user_profiles = generate_user_profiles(projects)

# Save the user profiles to a new JSON file
with open('../couchbase-server/sample-userProfiles.json', 'w') as user_file:
    json.dump(user_profiles, user_file, indent=4)

print("User profiles have been generated and saved to sample-userProfiles.json")